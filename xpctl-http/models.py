#from pydantic import BaseModel as Model
# This gives us backwards compatible API calls
from fastapi_camelcase import CamelModel as Model
from typing import Optional, List
from datetime import date, datetime


class Result(Model):
    metric: str
    phase: str
    tick: int
    tick_type: str
    value: float


class AggregateResultValue(Model):
    aggregate_fn: str
    score: float


class AggregateResult(Model):
    metric: str
    values: List[AggregateResultValue]

class Experiment(Model):
    task: str
    eid: str
    sha1: str
    config: str
    dataset: str
    username: Optional[str] = None
    hostname: str
    exp_date: Optional[datetime] = None
    label: str
    version: str
    train_events: List[Result]
    valid_events: List[Result]
    test_events: List[Result]


class TaskSummary(Model):
    task: str
    summary: dict


class Response(Model):
    code: int
    message: str
    response_type: str




