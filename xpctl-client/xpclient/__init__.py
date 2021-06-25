# coding: utf-8

# flake8: noqa

"""
    xpctl

    This is a sample xpctl  server.  You can find out more about xpctl at [baseline](https://github.com/dpressel/baseline/blob/master/docs/xpctl.md).  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: apiteam@swagger.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import
from xpclient.version import __version__

# import apis into sdk package
from xpclient.api.xpctl_api import XpctlApi

# import ApiClient
from xpclient.api_client import ApiClient
from xpclient.configuration import Configuration
# import models into sdk package
from xpclient.models.aggregate_result import AggregateResult
from xpclient.models.aggregate_result_values import AggregateResultValues
from xpclient.models.experiment import Experiment
from xpclient.models.experiment_aggregate import ExperimentAggregate
from xpclient.models.response import Response
from xpclient.models.result import Result
from xpclient.models.task_summary import TaskSummary
