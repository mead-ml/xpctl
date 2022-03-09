import glob
import requests
import time
from shutil import copyfile
import yaml
from shortid import ShortId
from fastapi import FastAPI, Depends, Body, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from jinja2 import Template
from kubernetes import client, config
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
import git
from datetime import datetime
import logging
from eight_mile.utils import read_yaml


from models import Result as ServerResult
from models import AggregateResultValue as ServerAggregateResultValue
from models import AggregateResult as ServerAggregateResult
from models import Experiment as ServerExperiment
from models import TaskSummary as ServerTaskSummary
from models import Response as ServerResponse


from backends.core import *
from eight_mile.utils import read_config_file

XPCTL_CRED = os.getenv('XPCRED', os.path.expanduser('~/xpctlcred.json'))
XPCTL_BACKEND = os.getenv('XPBACKEND', 'mongo')
EVENT_TYPES = {
    "train": "train_events", "Train": "train_events",
    "test": "test_events", "Test": "test_events",
    "valid": "valid_events", "Valid": "valid_events",
    "dev": "valid_events", "Dev": "valid_events"
}
d = read_config_file(XPCTL_CRED)
d.update({'dbtype': XPCTL_BACKEND})
REPO = XPRepo().create_repo(**d)

class VersionedAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.router.prefix = "/v1"


app = VersionedAPI(prefix="/v1")

# FIXME: tighten this up
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['OPTIONS'],
                   allow_headers=['Origin', 'X-Requested-With'])


@app.get("/ping")
def ping():
    return "pong"


def serialize_experiment_list(exps):
    results = []
    for exp in exps:
        if type(exp) == BackendError:
            raise Exception(BackendError.message)
        train_events = [ServerResult(**r.__dict__) for r in exp.train_events]
        valid_events = [ServerResult(**r.__dict__) for r in exp.valid_events]
        test_events = [ServerResult(**r.__dict__) for r in exp.test_events]
        d = exp.__dict__
        d.update({'train_events': train_events})
        d.update({'valid_events': valid_events})
        d.update({'test_events': test_events})
        results.append(ServerExperiment(**d))
    return results

@app.get("/find/{task}")
async def list_experiments_by_prop(
        task: str,
        eid: Optional[str]=None,
        sha1: Optional[str]=None,
        dataset: Optional[str]=None,
        label: Optional[str]=None,
        user: Optional[str]=None,
        metric: Optional[str]=None,
        sort: Optional[str]=None,
        event_type: Optional[str]=None
):
    REPO.list_results(task, param_dict, user, metric, sort, event_type)
    param_dict = {}
    if eid:
        param_dict['eid'] = eid
    if sha1:
        param_dict['sha1'] = sha1
    if dataset:
        param_dict['dataset'] = dataset
    if label:
        param_dict['label'] = label
    return serialize_experiment_list(backend.list_results(task, param_dict, user, metric, sort, event_type))

"""
@app.put("{task}")
async def put_result(pipe_def: PipelineWrapperDefinition, token: str=Depends(oauth2_scheme)) -> PipelineWrapperDefinition:
    user: User = await _get_current_user(token)
    job = _convert_to_path(pipe_def.pipeline.job)
    _update_job_repo()
    if _is_template(job):
        job = _substitute_template(job, pipe_def.context or {})
    pipe_id = await _submit_job(get_ws_url(), job)
    dao.create_job_ref(user, pipe_id)
    p = PipelineDefinition(name=pipe_id, id=pipe_id, job=job)
    return PipelineWrapperDefinition(pipeline=p)
"""
"""
def serialize_experiment_aggregate(agg_exps):

    if is_error(agg_exps):
        return abort(500, agg_exps.message)
    results = []
    for agg_exp in agg_exps:
        train_events = [ServerAggregateResult(metric=r.metric,
                                              values=[AggregateResultValues(k, v) for k, v in r.values.items()])
                        for r in agg_exp.train_events]
        valid_events = [ServerAggregateResult(metric=r.metric,
                                              values=[AggregateResultValues(k, v) for k, v in r.values.items()])
                        for r in agg_exp.valid_events]
        test_events = [ServerAggregateResult(metric=r.metric,
                                             values=[AggregateResultValues(k, v) for k, v in r.values.items()])
                       for r in agg_exp.test_events]

        d = agg_exp.__dict__
        d.update({'train_events': train_events})
        d.update({'valid_events': valid_events})
        d.update({'test_events': test_events})
        results.append(ServerExperimentAggregate(**d))
    return results


def serialize_experiment(exp):
   
    if is_error(exp):
        return Exception(exp.message)
    train_events = [ServerResult(**r.__dict__) for r in exp.train_events]
    valid_events = [ServerResult(**r.__dict__) for r in exp.valid_events]
    test_events = [ServerResult(**r.__dict__) for r in exp.test_events]
    d = exp.__dict__
    d.update({'train_events': train_events})
    d.update({'valid_events': valid_events})
    d.update({'test_events': test_events})
    return ServerExperiment(**d)

def serialize_experiment_list(exps):
    if is_error(exps):
        return abort(500, exps.message)
    results = []
    for exp in exps:
        if type(exp) == BackendError:
            return BackendResponse(**exp.__dict__)
        train_events = [ServerResult(**r.__dict__) for r in exp.train_events]
        valid_events = [ServerResult(**r.__dict__) for r in exp.valid_events]
        test_events = [ServerResult(**r.__dict__) for r in exp.test_events]
        d = exp.__dict__
        d.update({'train_events': train_events})
        d.update({'valid_events': valid_events})
        d.update({'test_events': test_events})
        results.append(ServerExperiment(**d))
    return results

def is_error(_object):
    if hasattr(_object, 'response_type'):
        return True
    return False



def serialize_task_summary(task_summary):
    if is_error(task_summary):
        return abort(500, task_summary.message)
    return ServerTaskSummary(**task_summary.__dict__)


def serialize_task_summary_list(task_summaries):
    _task_summaries = []
    for task_summary in task_summaries:
        if not is_error(task_summary):  # should we abort if we cant get summary for a task in the database?
            _task_summaries.append(ServerTaskSummary(**task_summary.__dict__))
    return _task_summaries


def serialize_dict(config):
    if is_error(config):
        return abort(500, config.message)
    return config


def serialize_response(result):
    return ServerResponse(**result.__dict__)
"""