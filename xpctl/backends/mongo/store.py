import os
import shutil
import pymongo
import datetime
import socket
import getpass
from baseline.utils import listify, unzip_files, read_config_file
from mead.utils import hash_config
from xpctl.backends.core import ExperimentRepo
from xpctl.backends.backend import DatasetSummary, BackendSuccess, BackendError, Experiment, ExperimentSet, Result, \
    EVENT_TYPES, log2json, get_experiment_label, METRICS_SORT_ASCENDING, safe_get, \
    client_experiment_to_put_result_consumable, aggregate_results, write_experiment
from bson.objectid import ObjectId
from baseline.version import __version__
import logging
DEFAULT_TASK = 'dt'


class MongoRepo(ExperimentRepo):

    def __init__(self, dbhost, user, passwd, **kwargs):
        super(MongoRepo, self).__init__()
        self.logger = logging.getLogger('xpctl-mongo')
        self.dbhost = dbhost
        srv_scheme = kwargs.get('srv_scheme', False)
        dbport = kwargs.get('dbport')
        if srv_scheme:  # https://docs.mongodb.com/manual/reference/connection-string/ more about this
            # host, user and passwd must be specified
            uri = "mongodb+srv://{}:{}@{}/test".format(user, passwd, dbhost)
            client = pymongo.MongoClient(uri)
        else:
            if user and passwd:
                uri = "mongodb://{}:{}@{}:{}/test".format(user, passwd, dbhost, dbport)
                client = pymongo.MongoClient(uri)
            else:
                client = pymongo.MongoClient(dbhost, dbport)
        if client is None:
            s = "cannot connect to mongo at host: [{}], port [{}], username: [{}], password: [{}]".format(dbhost,
                                                                                                          dbport,
                                                                                                          user,
                                                                                                          passwd)
            raise Exception(s)
        try:
            dbnames = client.list_database_names()
        except pymongo.errors.ServerSelectionTimeoutError:
            raise Exception("cannot get database from mongo at host: {}, port {}, connection timed out".format(dbhost,
                                                                                                               dbport))

        if "reporting_db" not in dbnames:
            self.logger.warning("Warning: database reporting_db does not exist, do not query before inserting results")

        self.db = client.reporting_db
        self.coll = self.db[DEFAULT_TASK]

    def put_result(self, exp):
        unpacked = client_experiment_to_put_result_consumable(exp)
        return self._put_result(config_obj=unpacked.config_obj, events_obj=unpacked.events_obj,
                                **unpacked.extra_args)

    def _put_result(self, config_obj, events_obj, **kwargs):
        now = safe_get(kwargs, 'date', datetime.datetime.utcnow().isoformat())
        hostname = safe_get(kwargs, 'hostname', socket.gethostname())
        username = safe_get(kwargs, 'username', getpass.getuser())
        config_sha1 = safe_get(kwargs, 'sha1', hash_config(config_obj))
        label = safe_get(kwargs, 'label', get_experiment_label(config_obj, **kwargs))
        checkpoint = kwargs.get('checkpoint')
        version = safe_get(kwargs, 'version', __version__)
        dataset = safe_get(kwargs, 'dataset', config_obj.get('dataset'))
        date = safe_get(kwargs, 'exp_date', now)
        train_events = list(filter(lambda x: x['phase'] == 'Train', events_obj))
        valid_events = list(filter(lambda x: x['phase'] == 'Valid', events_obj))
        test_events = list(filter(lambda x: x['phase'] == 'Test', events_obj))

        post = {
            "dataset": dataset,
            "config": config_obj,
            "train_events": train_events,
            "valid_events": valid_events,
            "test_events": test_events,
            "username": username,
            "hostname": hostname,
            "date": date,
            "label": label,
            "sha1": config_sha1,
            "version": version,
            "checkpoint": checkpoint
        }
        if 'eid' in kwargs:
            post.update({'_id': ObjectId(kwargs['eid'])})

        try:
            result = self.coll.insert_one(post)
            return BackendSuccess(message=str(result.inserted_id))
        except pymongo.errors.PyMongoError as e:
            return BackendError(message='experiment could not be inserted: {}'.format(e.message))

    def get_model_location(self, eid):
        query = {'_id': ObjectId(eid)}
        projection = {'checkpoint': 1}
        results = [x.get('checkpoint') for x in list(self.coll.find(query, projection))]
        results = [x for x in results if x is not None]
        if not results:
            return BackendError(message='no model location for experiment id [{}] in database'.format(eid))
        return BackendSuccess(results[0])

    def update_prop(self, eid, prop, value):
        try:
            r = self.coll.find_one({'_id': ObjectId(eid)}, {prop: 1})
            if r is None:
                return BackendError(message='property {} for experiment {} not found in database'.format(prop, eid))
            prev_value = r[prop]
            self.coll.update({'_id': ObjectId(eid)}, {'$set': {prop: value}}, upsert=False)
            changed_value = self.coll.find_one({'_id': ObjectId(eid)}, {prop: 1})[prop]
            return BackendSuccess(message='for experiment [{}] property [{}] was changed from [{}] to [{}]'
                                  .format(eid, prop, prev_value, changed_value))
        except pymongo.errors.PyMongoError as e:
            return BackendError(message='property update failed: {}'.format(e.message))

    def remove_experiment(self, eid):
        try:
            prev = self.coll.find_one({'_id': ObjectId(eid)})
            if prev is None:
                return BackendError(message='delete operation failed: experiment [{}] not found in database'.
                                    format(eid))
            model_loc_response = self.get_model_location(eid)
            model_loc = model_loc_response.message
            if model_loc is not None and type(model_loc_response) is not BackendError and os.path.exists(model_loc):
                try:
                    os.remove(model_loc)
                except IOError:
                    return BackendError(message='model {} exists on host but could not be removed'.format(model_loc))
            self.coll.remove({'_id': ObjectId(eid)})
            try:
                assert self.coll.find_one({'_id': ObjectId(eid)}) is None
                return BackendSuccess("record [{}] deleted successfully from database".format(eid))
            except AssertionError:
                return BackendError('delete failed: could not delete experiment {} from database'.format(eid))
        except pymongo.errors.PyMongoError as e:
            return BackendError(message='experiment could not be removed: {}'.format(e.message))

    def get_experiment_details(self, eid, event_type, metric):
        metrics = [x for x in listify(metric) if x.strip()]
        if event_type is None or event_type == 'None':
            event_type = 'test_events'
        query = {'_id': ObjectId(eid)}
        all_results = list(self.coll.find(query))
        if not all_results:
            return BackendError(message='no experiment with id [{}]'.format(eid))
        experiments = mongo_to_experiment_set(all_results, event_type=event_type, metrics=metrics)
        if type(experiments) == BackendError:
            return BackendError(experiments.message)
        return experiments[0]

    def get_results(self, param_dict, reduction_dim, metric, sort, numexp_reduction_dim, event_type):
        metrics = [x for x in listify(metric)]
        if event_type is None or event_type == 'None':
            event_type = 'test_events'
        reduction_dim = reduction_dim if reduction_dim is not None else 'sha1'
        if 'dataset' in param_dict.keys():
            value = self.get_related_datasets(param_dict['dataset'])
            param_dict['dataset'] = value
        query = self._update_query({}, **param_dict)
        all_results = list(self.coll.find(query))
        if not all_results:
            return BackendError(message='no information available for {} in database'
                                .format(param_dict))
        resultset = mongo_to_experiment_set(all_results, event_type=event_type, metrics=metrics)
        if type(resultset) is BackendError:
            return resultset
        experiment_aggregate_set = aggregate_results(resultset, reduction_dim, event_type, numexp_reduction_dim,
                                                     param_dict)
        if sort is None or sort == 'None':
            return experiment_aggregate_set
        else:
            if event_type == 'test_events':
                if sort in METRICS_SORT_ASCENDING:
                    return experiment_aggregate_set.sort(sort, reverse=False)
                else:
                    return experiment_aggregate_set.sort(sort)
            else:
                return BackendError(message='experiments can only be sorted when event_type=test_events')

    @staticmethod
    def _update_query(q, **kwargs):
        query = q
        if not kwargs:
            return query
        else:
            if "id" in kwargs and kwargs["id"]:
                if type(kwargs["id"]) is list:
                    query.update({"_id": {"$in": [ObjectId(x) for x in kwargs["id"]]}})
                else:
                    query.update({"_id": ObjectId(kwargs["id"])})
                kwargs.pop("id")
            if "eid" in kwargs and kwargs["eid"]:
                if type(kwargs["eid"]) is list:
                    query.update({"_id": {"$in": [ObjectId(x) for x in kwargs["eid"]]}})
                else:
                    query.update({"_id": ObjectId(kwargs["eid"])})
                kwargs.pop("eid")
            if "dataset" in kwargs:
                if type(kwargs["dataset"]) is list:
                    query.update({"$or": [
                        {"config.dataset": {"$in": kwargs["dataset"]}},
                        {"dataset": {"$in": kwargs["dataset"]}}
                    ]})
                else:
                    query.update({"$or": [{"config.dataset": kwargs["dataset"]}, {"dataset": kwargs["dataset"]}]})
                kwargs.pop("dataset")
            for key, value in kwargs.items():
                if type(value) == list:
                    query.update({key: {"$in": value}})
                else:
                    query.update({key: value})
            return query

    @staticmethod
    def _update_projection(event_type):
        projection = {"_id": 1, "sha1": 1, "label": 1, "username": 1, "config.dataset": 1, "date": 1, "dataset": 1}
        projection.update({event_type: 1})
        return projection

    def list_results(self, param_dict, user, metric, sort, event_type):
        if event_type is None or event_type == 'None':
            event_type = 'test_events'
        metrics = [x for x in listify(metric) if x.strip()]
        users = [x for x in listify(user) if x.strip()]
        if users:
            param_dict.update({'username': users})
        query = self._update_query({}, **param_dict)
        all_results = list(self.coll.find(query))
        if not all_results:
            return BackendError(message='no information available for {} in database'
                                .format(param_dict))
        experiments = mongo_to_experiment_set(all_results, event_type=event_type, metrics=metrics)
        if type(experiments) == BackendError:
            return experiments
        if sort is None or sort == 'None':
            return experiments
        else:
            if event_type == 'test_events':
                if sort in METRICS_SORT_ASCENDING:
                    return experiments.sort(sort, reverse=False)
                else:
                    return experiments.sort(sort)
            else:
                return BackendError(message='experiments can only be sorted when event_type=test_events')

    def find_experiments(self, prop, value):
        d = {prop: value}
        query = self._update_query({}, **d)
        all_results = list(self.coll.find(query))
        if not all_results:
            return BackendError(message='no information available for [{}]: [{}] in database'
                                .format(prop, value))
        return mongo_to_experiment_set(all_results, event_type='test_events', metrics=[])

    def config2json(self, sha1):
        j = self.coll.find_one({"sha1": sha1}, {"config": 1})
        if not j:
            return BackendError('no config [{}] in database'.format(sha1))
        else:
            return j["config"]

    def get_related_datasets(self, dataset):
        """
        for now, lets just get the datasets from all tasks and filter by 'project:name:features'
        We should have a dataset collection in the future.
        :param dataset:
        :return:
        """
        projection = {"dataset": 1, "config.dataset": 1, "_id": 0}
        results = list(self.coll.find({}, projection))
        all_datasets = []
        for result in results:
            all_datasets.append(result.get('dataset'))
            all_datasets.append(result.get('config', {}).get('dataset'))
        all_datasets = set([x for x in all_datasets if x is not None])
        if dataset in all_datasets:
            return [dataset]
        else:
            datasets = []
            for d in all_datasets:
                if d.startswith(dataset):
                    datasets.append(d)
            return datasets

    def get_dataset_names(self):
        q = {}
        p = self._update_projection(event_type='test_events')
        datasets = []
        results = list(self.coll.find(q, p))
        for result in results:
            datasets.append(result.get('dataset'))
            datasets.append(result.get('config', {}).get('dataset'))
        return list(set([dataset for dataset in datasets if dataset is not None]))

    def dataset_summary(self, dataset):
        event_type = 'test_events'
        q = self._update_query({}, dataset=dataset)
        p = self._update_projection(event_type)
        results = list(self.coll.find(q, p))
        experiment_set = mongo_to_experiment_set(results, event_type, metrics=[])
        if type(experiment_set) == BackendError:
            return BackendError('could not get summary for dataset: [{}]'.format(dataset))
        return DatasetSummary(dataset=dataset, experiment_set=experiment_set)

    def summary(self):
        datasets = self.get_dataset_names()
        return [self.dataset_summary(dataset) for dataset in datasets]

    def dump(self, zipfile='xpctldump-{}'.format(datetime.datetime.now().isoformat()), eids=[]):
        """ dump reporting log and config for later consumption"""
        base_dir = '/tmp/xpctldump'
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)

        os.makedirs(base_dir, exist_ok=True)
        query = self._update_query({}, id=listify(eids))
        all_results = list(self.coll.find(query))
        experiments = mongo_to_experiment_set(all_results, event_type=[], metrics=[]).data
        _dir = os.path.join(base_dir)
        os.makedirs(_dir)
        for exp in experiments:
            write_experiment(exp, _dir)
        return shutil.make_archive(base_name=zipfile, format='zip', root_dir='/tmp', base_dir='xpctldump')

    def restore(self, dump):
        """ if dump is in zip format, will unzip it. expects the following dir structure in the unzipped file:
        <root>
         - <task>
           - <id>-reporting.log
           - <id>.yml
        """
        dump_dir = unzip_files(dump)
        task_dir = dump_dir
        for exp in os.listdir(task_dir):
            exp_dir = os.path.join(task_dir, exp)
            meta = [os.path.join(exp_dir, x) for x in os.listdir(exp_dir) if x.endswith('meta.yml')]
            reporting = [os.path.join(exp_dir, x) for x in os.listdir(exp_dir) if x.endswith('reporting.log')]
            config = [os.path.join(exp_dir, x) for x in os.listdir(exp_dir) if x.endswith('config.yml')]
            try:
                assert len(config) == 1
                assert len(reporting) == 1
                assert len(meta) == 1
                config = read_config_file(config[0])
                meta = read_config_file(meta[0])
                reporting = log2json(reporting[0])
            except AssertionError:
                raise RuntimeError('There should be exactly one meta file, one config file and one reporting log '
                                   'in {}'.format(exp_dir))
            self._put_result(config_obj=config, events_obj=reporting, **meta)
        if dump_dir != dump:
            shutil.rmtree(dump_dir)


class MongoResult(object):
    """ a result data point"""
    def __init__(self, metric, value, eid, username, hostname, label, config, dataset, date, sha1, event_type,
                 tick_type, tick, phase, version):
        super(MongoResult, self).__init__()
        self.metric = metric
        self.value = value
        self.eid = eid
        self.username = username
        self.hostname = hostname
        self.label = label
        self.dataset = dataset
        self.date = date
        self.sha1 = sha1
        self.event_type = event_type
        self.config = config
        self.tick_type = tick_type
        self.tick = tick
        self.phase = phase
        self.version = version

    def get_prop(self, field):
        return self.__dict__[field]


class MongoResultSet(object):
    """ a list of result objects"""
    def __init__(self, data):
        super(MongoResultSet, self).__init__()
        self.data = data if data else []
        self.length = len(self.data)

    def add_data(self, data_point):
        """
        add a result data point
        :param data_point:
        :return:
        """
        self.data.append(data_point)
        self.length += 1

    # TODO: add property annotations
    def __getitem__(self, i):
        return self.data[i]

    def __iter__(self):
        for i in range(self.length):
            yield self.data[i]

    def __len__(self):
        return self.length

    def groupby(self, key):
        """ group the data points by key"""
        data_groups = {}
        for datum in self.data:
            field = datum.get_prop(key)
            if field not in data_groups:
                data_groups[field] = [datum]
            else:
                data_groups[field].append(datum)
        return data_groups

    def experiments(self):
        grouped_results = self.groupby('eid')
        experiments = []
        for eid, resultset in grouped_results.items():
            first_result = resultset[0]
            eid = str(first_result.eid)
            username = first_result.username
            hostname = first_result.hostname
            label = first_result.label
            dataset = first_result.dataset
            date = first_result.date
            sha1 = first_result.sha1
            config = first_result.config
            version = first_result.version
            exp = Experiment(
                eid=eid,
                sha1=sha1,
                config=config,
                dataset=dataset,
                username=username,
                hostname=hostname,
                exp_date=date,
                label=label,
                version=version,
                train_events=[],
                valid_events=[],
                test_events=[])
            for _result in resultset:
                r = Result(metric=_result.metric, value=_result.value, tick_type=_result.tick_type, tick=_result.tick,
                           phase=_result.phase)
                exp.add_result(r, _result.event_type)
            experiments.append(exp)
        return ExperimentSet(experiments)


def get_metrics_mongo(xs):
    keys = []
    for x in xs:
        keys += x.keys()
    keys = set(keys)
    if 'tick_type' in keys:
        keys.remove("tick_type")
    if 'tick' in keys:
        keys.remove("tick")
    if 'phase' in keys:
        keys.remove("phase")
    return keys


def mongo_to_experiment_set(all_results, event_type, metrics):
    data = []
    event_types = [event_type] if event_type else EVENT_TYPES
    metrics_from_user = set([x for x in metrics if x.strip()])
    for result in all_results:  # different experiments
        _id = result['_id']
        username = result.get('username', 'root')
        hostname = result.get('hostname', 'localhost')
        label = result.get('label', 'default_label')
        dataset = result.get('dataset', result['config'].get('dataset'))
        date = result['date']
        sha1 = result['sha1']
        config = result['config']
        version = result.get('version', '0.5.0')  # backward compatibility
        for event_type in event_types:
            if not result.get(event_type, []):
                continue
            metrics_from_db = get_metrics_mongo(result[event_type])
            if not metrics_from_user:
                metrics = list(metrics_from_db)
            elif metrics_from_user - metrics_from_db:
                return BackendError(message='Metrics [{}] not found for experiment [{}] in database'.format(','.join(
                    list(metrics_from_user - metrics_from_db)), _id))
            else:
                metrics = list(metrics_from_user)
            # for train_events we can have different metrics than test_events
            for record in result[event_type]:  # train_event epoch 0,
                for metric in metrics:
                    data.append(MongoResult(
                        metric=metric,
                        value=record[metric],
                        eid=str(_id),
                        username=username,
                        hostname=hostname,
                        label=label,
                        config=config,
                        dataset=dataset,
                        date=date,
                        sha1=sha1,
                        event_type=event_type,
                        tick_type=record['tick_type'],
                        tick=record['tick'],
                        phase=record['phase'],
                        version=version
                    ))
    if not data:
        return BackendError(message='No results from the query')
    rs = MongoResultSet(data=data)
    return rs.experiments()
