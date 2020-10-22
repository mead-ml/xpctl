import connexion

from xpctl.xpserver.models.experiment import Experiment  # noqa: E501
import flask
from xpctl.backends.backend import serialize_dict, serialize_experiment, \
    serialize_experiment_aggregate, serialize_experiment_list, serialize_response, serialize_dataset_summary_list, \
    serialize_dataset_summary


def config2json(sha1):  # noqa: E501
    """get config for sha1

    config for sha1 # noqa: E501

    :param sha1: sha1
    :type sha1: str

    :rtype: object
    """
    backend = flask.globals.current_app.backend
    return serialize_dict(backend.config2json(sha1))


def dataset_summary(dataset):  # noqa: E501
    """get summary for dataset

    summary for dataset # noqa: E501

    :param dataset: dataset
    :type dataset: str

    :rtype: DatasetSummary
    """
    backend = flask.globals.current_app.backend
    return serialize_dataset_summary(backend.dataset_summary(dataset))


def experiment_details(eid, event_type=None, metric=None):  # noqa: E501
    """Find experiment by id

    Returns a single experiment # noqa: E501

    :param eid: ID of experiment to return
    :type eid: str
    :param event_type:
    :type event_type: str
    :param metric:
    :type metric: List[str]

    :rtype: Experiment
    """
    backend = flask.globals.current_app.backend
    return serialize_experiment(backend.get_experiment_details(eid, event_type, metric))


def get_model_location(eid):  # noqa: E501
    """get model loc for experiment

    get model loc for experiment # noqa: E501

    :param eid: experiment id
    :type eid: str

    :rtype: Response
    """
    backend = flask.globals.current_app.backend
    return serialize_response(backend.get_model_location(eid))


def get_results_by_prop(dataset=None, eid=None, sha1=None, label=None, reduction_dim=None, metric=None, sort=None, numexp_reduction_dim=None, event_type=None):  # noqa: E501
    """Find results by property and value

    Find results by property and value # noqa: E501

    :param dataset: dataset
    :type dataset: str
    :param eid: eid
    :type eid: str
    :param sha1: sha1
    :type sha1: str
    :param label: label
    :type label: str
    :param reduction_dim: which dimension to reduce on, default&#x3D;sha1
    :type reduction_dim: str
    :param metric: metric
    :type metric: List[str]
    :param sort: metric to sort results on
    :type sort: str
    :param numexp_reduction_dim: max number of experiments in an aggregate group
    :type numexp_reduction_dim: int
    :param event_type: train/dev/test
    :type event_type: str

    :rtype: List[ExperimentAggregate]
    """
    backend = flask.globals.current_app.backend
    param_dict = {}
    if eid:
        param_dict['eid'] = eid
    if sha1:
        param_dict['sha1'] = sha1
    if dataset:
        param_dict['dataset'] = dataset
    if label:
        param_dict['label'] = label
    return serialize_experiment_aggregate(backend.get_results(param_dict, reduction_dim, metric, sort,
                                                              numexp_reduction_dim, event_type))


def list_experiments_by_prop(eid=None, sha1=None, dataset=None, label=None, user=None, metric=None, sort=None,
                             event_type=None):  # noqa: E501
    """list all experiments for this property and value

    list all experiments for this property (sha1/ username) and value (1cd21df91770b4dbed64a683558b062e3dee61f0/ dpressel) # noqa: E501

    :param eid: eid
    :type eid: str
    :param sha1: sha1
    :type sha1: str
    :param dataset: dataset, e.g. SST2
    :type dataset: str
    :param label: label
    :type label: str
    :param user:
    :type user: List[str]
    :param metric:
    :type metric: List[str]
    :param sort:
    :type sort: str
    :param event_type:
    :type event_type: str

    :rtype: List[Experiment]
    """
    backend = flask.globals.current_app.backend
    param_dict = {}
    if eid:
        param_dict['eid'] = eid
    if sha1:
        param_dict['sha1'] = sha1
    if dataset:
        param_dict['dataset'] = dataset
    if label:
        param_dict['label'] = label
    return serialize_experiment_list(backend.list_results(param_dict, user, metric, sort, event_type))


def put_result(experiment, user=None, label=None):  # noqa: E501
    """Add a new experiment in database

     # noqa: E501

    :param experiment: 
    :type experiment: dict | bytes
    :param user: 
    :type user: str
    :param label: 
    :type label: str

    :rtype: Response
    """
    if connexion.request.is_json:
        experiment = Experiment.from_dict(connexion.request.get_json())  # noqa: E501
    backend = flask.globals.current_app.backend
    return serialize_response(backend.put_result(experiment))


def remove_experiment(eid):  # noqa: E501
    """delete an experiment from the database

     # noqa: E501

    :param eid: 
    :type eid: str

    :rtype: Response
    """
    backend = flask.globals.current_app.backend
    return serialize_response(backend.remove_experiment(eid))


def summary():  # noqa: E501
    """get summary for database

    summary for database # noqa: E501


    :rtype: List[DatasetSummary]
    """
    backend = flask.globals.current_app.backend
    return serialize_dataset_summary_list(backend.summary())


def update_property(eid, prop, value):  # noqa: E501
    """update property for an experiment

     # noqa: E501

    :param eid: 
    :type eid: str
    :param prop: 
    :type prop: str
    :param value: 
    :type value: str

    :rtype: Response
    """
    backend = flask.globals.current_app.backend
    return serialize_response(backend.update_prop(eid, prop, value))
