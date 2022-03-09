from copy import deepcopy
from collections import namedtuple
from itertools import groupby
import json
import os
import numpy as np


EVENT_TYPES = {
    "train": "train_events", "Train": "train_events",
    "test": "test_events", "Test": "test_events",
    "valid": "valid_events", "Valid": "valid_events",
    "dev": "valid_events", "Dev": "valid_events"
}


def safe_get(_object, key, alt):
    val = _object.get(key)
    if val is None or str(val) is None:
        return alt
    return val

class XPRepo:

    def __init__(self):
        super().__init__()

    def get_task_names(self):
        """Get the names of all tasks in the repository

        :return: A list of tasks
        """

    def config2dict(self, task, sha1):
        """Convert a configuration stored in the repository to a string

        :param task: (``str``) The task name
        :param sha1: (``str``) The sha1 of the configuration
        :return: (``dict``) The configuration
        """

    @staticmethod
    def create_repo(**kwargs):
        """Create a MongoDB-backed repository

        :param dbtype: (``str``) The database type
        :param dbhost: (``str``) The host name
        :param dbport: (``str``) The port
        :param user: (``str``) The user
        :param passwd: (``str``)The password
        :return: A MongoDB/Sql-backed repository
        """
        dbhost = kwargs.get('dbhost', kwargs.get('host'))
        dbport = kwargs.get('dbport', kwargs.get('port'))
        user = kwargs.get('dbuser', kwargs.get('user'))
        passwd = kwargs.get('dbpasswd', kwargs.get('passwd'))
        dbtype = kwargs.get('dbtype', kwargs.get('type', 'mongo'))


        if dbtype == 'mongo':
            from backends.mongo.store import MongoRepo
            return MongoRepo(dbhost, int(dbport), user, passwd)
        else:
            from backends.sql.store import SQLRepo
            return SQLRepo(type=dbtype, host=dbhost, port=dbport, user=user, passwd=passwd)

    def get_model_location(self, task, eid):
        """Get the physical location of the model specified by this experiment id

        :param task: (``str``) The task name
        :param eid: The identifier of the experiment
        :return: (``str``) The model location
        """

    def get_experiment_details(self, task, eid, event_type, metric):
        """Get detailed description for an experiment
        :param task: (``str``) The task name
        :param eid: The identifier of the experiment
        :param event_type: (List[``str``]) event types to listen for
        :param metric: (List[``str``]) The metric(s) to use
        :return: xpctl.backend.data.Experiment object
        """

    def get_results(self, task, param_dict, reduction_dim, metric, sort, numexp_reduction_dim, event_type):
        """Get results from the database
        :param task: (``str``) The taskname
        :param param_dict: (``dict``) The dict of parameters for query
        :param reduction_dim: (``str``) The property on which the results will be reduced
        :param metric: (``str``) The metric(s) to use
        :param sort: (``str``) The field to sort on
        :param numexp_reduction_dim: (``str``) number of results to show per group
        :param event_type: (``str``) event types to listen for
        :return: List[xpctl.backend.data.ExperimentAggregate]
        """

    def task_summary(self, task):
        """Summary for a task: What datasets were used? How many times each dataset was used?
        :param task: (``str``) Task name
        :return xpctl.backend.data.TaskSummary
        """

    def summary(self):
        """
        Summary for all tasks in the database
        :return: List[xpctl.backend.data.TaskSummary]
        """

    def find_experiments(self, task, prop, value):
        """
        find experiments by a property, eg: dataset
        :param task: (``str``) task name
        :param prop: (``str``) a property of an experiment, eg: dataset, label
        :param value: (``str``) value for the property
        :return: List[xpctl.backend.data.Experiment]
        """

    def update_prop(self, task, eid, prop, value):
        """
        Update a property(label, username etc) for an experiment
        :param task: (``str``) task name
        :param eid: The identifier for this record
        :param prop: (``str``) property to change
        :param value: (``str``) the value of the property
        :return: Union[xpctl.backend.data.Success, xpctl.backend.data.Error]
        """
        raise NotImplemented("Base ExperimentRepo events are immutable")

    def remove_experiment(self, task, eid):
        """Remove a record specified by this id
        :param task: (``str``) The task name for this record
        :param eid: The identifier for this record
        :return: Union[xpctl.backend.data.Success, xpctl.backend.data.Error]
        """
        raise NotImplemented("Base ExperimentRepo tasks are immutable")

    def put_result(self, task, experiment):
        """Put tan experiment in the database

        :param task: (``str``) The task name
        :param experiment: xpctl.backend.data.Experiment
        :return: Union[xpctl.backend.data.Success, xpctl.backend.data.Error]
        """

    def list_results(self, task, param_dict, user, metric, sort, event_type):
        """Get results from the database
        :param task: (``str``) The taskname
        :param param_dict: (``dict``) The dict of parameters for query
        :param user: List[``str``)] filter by users
        :param metric: (``str``) The metric(s) to use
        :param sort: (``str``) The field to sort on
        :param event_type: (``str``) event types to listen for
        :return: List[xpctl.backend.data.Experiment]
        """

    def dump(self, zipfile, task_eids):
        """
        dump the whole database. creates a zipfile which unzips into the following directory structure
        <xpctldump>
         - <task>
           - <id>
             - <id>-reporting.log
             - <id>-config.yml
             - <id>-meta.yml (any meta info such as label, username etc.)

        :param zipfile: zip file location for the dump. defaults to xpctldump-datetimestamp.zip
        :param task_eids: a dictionary of the form {'task': [eid1, eid2]}, if you want to dump specific files.
        :return: the path to the dumped file
        """

    def restore(self, dump):
        """
        restore a database from the dump. be careful: the experiment ids will change.
        :param dump: dump file location
        :return:
        """

from xpclient.utils import write_config_file


TRAIN_EVENT = 'train_events'
VALID_EVENT = 'valid_events'
TEST_EVENT = 'test_events'
EVENT_TYPES = [TRAIN_EVENT, VALID_EVENT, TEST_EVENT]


METRICS_SORT_ASCENDING = ['avg_loss', 'perplexity']


class Result:
    def __init__(self, metric, value, tick_type, tick, phase):
        super(Result, self).__init__()
        self.metric = metric
        self.value = value
        self.tick_type = tick_type
        self.tick = tick
        self.phase = phase

    def get_prop(self, field):
        if field not in self.__dict__:
            raise ValueError('{} does not have a property {}'.format(self.__class__, field))
        return self.__dict__[field]


class AggregateResult:
    def __init__(self, metric, values):
        super(AggregateResult, self).__init__()
        self.metric = metric
        self.values = values

    def get_prop(self, field):
        if field not in self.__dict__:
            raise ValueError('{} does not have a property {}'.format(self.__class__, field))
        return self.__dict__[field]


class Experiment:
    """ an experiment"""
    def __init__(self, train_events, valid_events, test_events, task, eid, username, hostname, config, exp_date, label,
                 dataset, sha1, version):
        super(Experiment, self).__init__()
        self.task = task
        self.train_events = train_events if train_events is not None else []
        self.valid_events = valid_events if valid_events is not None else []
        self.test_events = test_events if test_events is not None else []
        self.eid = eid
        self.username = username
        self.hostname = hostname
        self.config = config
        self.exp_date = exp_date
        self.label = label
        self.dataset = dataset
        self.sha1 = sha1
        self.version = version

    def get_prop(self, field):
        if field not in self.__dict__:
            raise ValueError('{} does not have a property {}'.format(self.__class__, field))
        return self.__dict__[field]

    def add_result(self, result, event_type):
        if event_type == TRAIN_EVENT:
            self.train_events.append(result)
        elif event_type == VALID_EVENT:
            self.valid_events.append(result)
        elif event_type == TEST_EVENT:
            self.test_events.append(result)
        else:
            raise NotImplementedError('no handler for event type: [{}]'.format(event_type))


class ExperimentSet:
    """ a list of experiment objects"""
    def __init__(self, data):
        super(ExperimentSet, self).__init__()
        self.data = data if data else []  # this should ideally be a set but the items are not hashable
        self.length = len(self.data)

    def __getitem__(self, i):
        return self.data[i]

    def __iter__(self):
        for i in range(self.length):
            yield self.data[i]

    def __len__(self):
        return self.length

    def add_data(self, datum):
        """
        add a experiment data point
        :param datum:
        :return:
        """
        self.data.append(datum)
        self.length += 1

    def groupby(self, key):
        """ group the data points by key"""
        data_groups = {}
        if len(self.data) == 0:
            raise RuntimeError('Trying to group empty experiment set')
        task = self.data[0].get_prop('task')
        for datum in self.data:
            if datum.get_prop('task') != task:
                raise RuntimeError('Should not be grouping two experiments from different tasks')
            field = datum.get_prop(key)
            if field not in data_groups:
                data_groups[field] = ExperimentSet([datum])
            else:
                data_groups[field].add_data(datum)
        return ExperimentGroup(data_groups, key, task)

    def sort(self, key, reverse=True):
        """
        you can only sort when event_type is test, because there is only one data point
        :param key: metric to sort on
        :param reverse: reverse=True always except when key is avg_loss
        :return:
        """
        if key is None or key == 'None':
            return self
        test_results = [(index, [y for y in x.get_prop(TEST_EVENT) if y.metric == key][0]) for index, x in
                        enumerate(self.data)]
        test_results.sort(key=lambda x: x[1].value, reverse=reverse)
        final_results = []
        for index, _ in test_results:
            final_results.append(self.data[index])
        return ExperimentSet(data=final_results)


class ExperimentGroup:
    """ a group of resultset objects"""
    def __init__(self, grouped_experiments, reduction_dim, task):
        super().__init__()
        self.grouped_experiments = grouped_experiments
        self.reduction_dim = reduction_dim
        self.task = task

    def items(self):
        return self.grouped_experiments.items()

    def keys(self):
        return self.grouped_experiments.keys()

    def values(self):
        return self.grouped_experiments.values()

    def __iter__(self):
        for k, v in self.grouped_experiments.items():
            yield (k, v)

    def get(self, key):
        return self.grouped_experiments.get(key)

    def __len__(self):
        return len(self.grouped_experiments.keys())

    def reduce(self, aggregate_fns, event_type=TEST_EVENT, prop_dict={}):
        """ aggregate results across a result group
        :param aggregate_fns: aggregating functions
        :param event_type: train/valid/test event
        :param prop_dict: Experiments in this group are expected to share some properties (since they are typically a
        query results from the database. This dict stores the shared properties and their values. The
        ExperimentAggregate created by the this reduce function will be labeld by these properties and values.
        """
        data = {}
        num_experiments = {}
        for reduction_dim_value, experiments in self.grouped_experiments.items():
            for dataset, _experiments in groupby(experiments, key=lambda exp: exp.dataset):
                _experiments = list(_experiments)
                num_experiments[reduction_dim_value] = {dataset: len(_experiments)}
                data[reduction_dim_value] = {dataset: {} for dataset in prop_dict['dataset']}
                for experiment in _experiments:
                    results = experiment.get_prop(event_type)
                    for result in results:
                        if result.metric not in data[reduction_dim_value][dataset]:
                            data[reduction_dim_value][dataset][result.metric] = [result.value]
                        else:
                            data[reduction_dim_value][dataset][result.metric].append(result.value)
        # for each reduction_dim_value, only one dataset can have metrics, the others are empty
        _data = {reduction_dim_value: {} for reduction_dim_value in data}
        for reduction_dim_value in data:
            for dataset in data[reduction_dim_value]:
                if data[reduction_dim_value][dataset]:
                    _data[reduction_dim_value][dataset] = data[reduction_dim_value][dataset]
        data = _data
        # for each reduction dim value, (say when sha1 = x), all data[x][metric] lists should have the same length.
        for reduction_dim_value in data:
            for dataset in data[reduction_dim_value]:
                lengths = []
                for metric in data[reduction_dim_value][dataset]:
                    lengths.append(len(data[reduction_dim_value][dataset][metric]))
                try:
                    assert len(set(lengths)) == 1
                except AssertionError:
                    raise AssertionError('when reducing experiments over {}, for {}={}, the number of results are '
                                         'not the same over all metrics'.format(self.reduction_dim,
                                                                                self.reduction_dim,
                                                                                reduction_dim_value))

        aggregate_resultset = ExperimentAggregateSet(data=[])
        del prop_dict['dataset']  # prop_dict must have dataset
        for reduction_dim_value in data:
            for dataset in data[reduction_dim_value]:
                prop_dict.update({'dataset': dataset})
                values = {}
                d = {
                    self.reduction_dim: reduction_dim_value,
                    'num_exps': num_experiments[reduction_dim_value][dataset],
                    **prop_dict
                }
                agr = deepcopy(ExperimentAggregate(task=self.task, **d))
                for metric in data[reduction_dim_value][dataset]:
                    for fn_name, fn in aggregate_fns.items():
                        agg_value = fn(data[reduction_dim_value][dataset][metric])
                        print(metric, dataset, fn_name, data[reduction_dim_value][dataset][metric], agg_value)
                        values[fn_name] = agg_value
                    agr.add_result(deepcopy(AggregateResult(metric=metric, values=values)), event_type=event_type)
                aggregate_resultset.add_data(agr)
        return aggregate_resultset


class ExperimentAggregate:
    """ a result data point"""
    def __init__(self, task, train_events=[], valid_events=[], test_events=[], **kwargs):
        super(ExperimentAggregate, self).__init__()
        self.train_events = train_events if train_events is not None else []
        self.valid_events = valid_events if valid_events is not None else []
        self.test_events = test_events if test_events is not None else []
        self.task = task
        self.num_exps = kwargs.get('num_exps')
        self.eid = kwargs.get('eid')
        self.username = kwargs.get('username')
        self.label = kwargs.get('label')
        self.dataset = kwargs.get('dataset')
        self.exp_date = kwargs.get('exp_date')
        self.sha1 = kwargs.get('sha1')

    def get_prop(self, field):
        return self.__dict__[field]

    def add_result(self, aggregate_result, event_type):
        if event_type == TRAIN_EVENT:
            self.train_events.append(aggregate_result)
        elif event_type == VALID_EVENT:
            self.valid_events.append(aggregate_result)
        elif event_type == TEST_EVENT:
            self.test_events.append(aggregate_result)
        else:
            raise NotImplementedError('no handler for event type: [{}]'.format(event_type))


class ExperimentAggregateSet:
    """ a list of aggregate result objects"""
    def __init__(self, data):
        super(ExperimentAggregateSet, self).__init__()
        self.data = data if data else []
        self.length = len(self.data)

    def add_data(self, data_point):
        """
        add a aggregateresult data point
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

    def sort(self, metric, aggregate_fn='avg', reverse=True):
        """
        you can only sort when event_type is test, because there is only one data point
        :param metric: metric to sort on
        :param aggregate_fn: this is an aggregate result, you have values for for different aggregate_fns. choose one
        :param reverse: reverse=True always except when key is avg_loss, perplexity
        :return:
        """
        if metric is None:
            return self
        test_results = [(index, [y for y in x.get_prop(TEST_EVENT) if y.metric == metric][0]) for index, x in
                        enumerate(self.data)]
        test_results.sort(key=lambda x: x[1].values[aggregate_fn], reverse=reverse)
        final_results = []
        for index, _ in test_results:
            final_results.append(self.data[index])
        return ExperimentSet(data=final_results)


class TaskDatasetSummary:
    """ How many users experimented with this dataset in the given task?"""
    def __init__(self, task, dataset, experiment_set, user_num_exps=None):
        super(TaskDatasetSummary, self).__init__()
        self.task = task
        self.dataset = dataset
        if user_num_exps is not None:
            self.user_num_exps = user_num_exps
        else:
            exp_groups = experiment_set.groupby('username')
            self.user_num_exps = {username: len(exp_group)for username, exp_group in exp_groups}


class TaskDatasetSummarySet:
    """ a list of TaskDatasetSummary objects."""
    def __init__(self, task, data):
        self.task = task
        self.data = data

    def groupby(self):
        """ group the TaskDatasetSummary objects. """
        d = {}
        for tdsummary in self.data:
            dataset = tdsummary.dataset
            d[dataset] = []
            for username in tdsummary.user_num_exps:
                d[dataset].append((username, tdsummary.user_num_exps[username]))

        return TaskSummary(self.task, d)


class TaskSummary:
    def __init__(self, task, summary):
        self.task = task
        self.summary = summary

def log2json(log_file):
    s = []
    with open(log_file) as f:
        for line in f:
            x = line.replace("'", '"')
            s.append(json.loads(x))
    return s


def json2log(events, log_file):
    with open(log_file, 'w') as wf:
        for event in events:
            wf.write(json.dumps(event)+'\n')


def get_experiment_label(config_obj, task, **kwargs):
    if kwargs.get('label', None) is not None:
        return kwargs['label']
    if 'description' in config_obj:
        return config_obj['description']
    else:
        model_type = config_obj.get('model_type', 'default')
        backend = config_obj.get('backend', 'tensorflow')
        return "{}-{}-{}".format(task, backend, model_type)



def deserialize_result(result):
    return Result(
        metric=result.metric,
        value=result.value,
        tick_type=result.tick_type,
        tick=result.tick,
        phase=result.phase
    )


def pack_results_in_events(results):
    d = {}
    for result in results:
        if result.tick not in d:
            d[result.tick] = {result.metric: result.value,
                              'tick_type': result.tick_type,
                              'phase': result.phase,
                              'tick': result.tick
                              }
        else:
            d[result.tick].update({result.metric: result.value})
    return list(d.values())


def client_experiment_to_put_result_consumable(exp):
    train_events = pack_results_in_events(exp.train_events)
    valid_events = pack_results_in_events(exp.valid_events)
    test_events = pack_results_in_events(exp.test_events)
    config = exp.config
    task = exp.task
    extra_args = {
        'sha1': exp.sha1,
        'dataset': exp.dataset,
        'username': exp.username,
        'hostname': exp.hostname,
        'exp_date': exp.exp_date,
        'label': exp.label
    }
    put_result_consumable = namedtuple('put_result_consumable', ['task', 'config_obj', 'events_obj', 'extra_args'])
    return put_result_consumable(task=task, config_obj=json.loads(config),
                                 events_obj=train_events+valid_events+test_events,
                                 extra_args=extra_args)


def aggregate_results(resultset, reduction_dim, event_type, num_exps_per_reduction, prop_dict):
    # TODO: implement a trim method for ExperimentGroup
    # The resultset here is a query result from prop_dict as the filtering parameters, so these results should share
    # the parameters in prop_dict
    grouped_result = resultset.groupby(reduction_dim)
    aggregate_fns = {'min': np.min, 'max': np.max, 'avg': np.mean, 'std': np.std}
    return grouped_result.reduce(aggregate_fns=aggregate_fns, event_type=event_type, prop_dict=prop_dict)


def write_experiment(experiment, basedir):
    eid = str(experiment.eid)
    basedir = os.path.join(basedir, eid)
    os.makedirs(basedir)
    train_events = pack_results_in_events(experiment.train_events)
    valid_events = pack_results_in_events(experiment.valid_events)
    test_events = pack_results_in_events(experiment.test_events)
    json2log(train_events + valid_events + test_events, os.path.join(basedir, '{}-reporting.log'.format(eid)))
    config = json.loads(experiment.config) if type(experiment.config) is str else experiment.config
    write_config_file(config, os.path.join(basedir, '{}-config.yml'.format(eid)))
    d = experiment.__dict__
    [d.pop(event_type) for event_type in EVENT_TYPES]
    d.pop('config')
    write_config_file(d, os.path.join(basedir, '{}-meta.yml'.format(eid)))


class BackendResponse:
    def __init__(self, message, response_type, code=550):
        super().__init__()
        self.message = message
        self.response_type = response_type
        self.code = code

class BackendError(BackendResponse):
    def __init__(self, message, response_type="error", code=550):
        super().__init__(message, response_type, code)


class BackendSuccess(BackendResponse):
    def __init__(self, message, response_type="success", code=250):
        super().__init__(message, response_type, code)
