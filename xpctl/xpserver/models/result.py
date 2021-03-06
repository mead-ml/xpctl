# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from xpctl.xpserver.models.base_model_ import Model
from xpctl.xpserver import util


class Result(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, metric=None, value=None, tick_type=None, tick=None, phase=None):  # noqa: E501
        """Result - a model defined in Swagger

        :param metric: The metric of this Result.  # noqa: E501
        :type metric: str
        :param value: The value of this Result.  # noqa: E501
        :type value: float
        :param tick_type: The tick_type of this Result.  # noqa: E501
        :type tick_type: str
        :param tick: The tick of this Result.  # noqa: E501
        :type tick: int
        :param phase: The phase of this Result.  # noqa: E501
        :type phase: str
        """
        self.swagger_types = {
            'metric': str,
            'value': float,
            'tick_type': str,
            'tick': int,
            'phase': str
        }

        self.attribute_map = {
            'metric': 'metric',
            'value': 'value',
            'tick_type': 'tick_type',
            'tick': 'tick',
            'phase': 'phase'
        }

        self._metric = metric
        self._value = value
        self._tick_type = tick_type
        self._tick = tick
        self._phase = phase

    @classmethod
    def from_dict(cls, dikt):
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Result of this Result.  # noqa: E501
        :rtype: Result
        """
        return util.deserialize_model(dikt, cls)

    @property
    def metric(self):
        """Gets the metric of this Result.


        :return: The metric of this Result.
        :rtype: str
        """
        return self._metric

    @metric.setter
    def metric(self, metric):
        """Sets the metric of this Result.


        :param metric: The metric of this Result.
        :type metric: str
        """
        if metric is None:
            raise ValueError("Invalid value for `metric`, must not be `None`")  # noqa: E501

        self._metric = metric

    @property
    def value(self):
        """Gets the value of this Result.


        :return: The value of this Result.
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this Result.


        :param value: The value of this Result.
        :type value: float
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501

        self._value = value

    @property
    def tick_type(self):
        """Gets the tick_type of this Result.


        :return: The tick_type of this Result.
        :rtype: str
        """
        return self._tick_type

    @tick_type.setter
    def tick_type(self, tick_type):
        """Sets the tick_type of this Result.


        :param tick_type: The tick_type of this Result.
        :type tick_type: str
        """
        if tick_type is None:
            raise ValueError("Invalid value for `tick_type`, must not be `None`")  # noqa: E501

        self._tick_type = tick_type

    @property
    def tick(self):
        """Gets the tick of this Result.


        :return: The tick of this Result.
        :rtype: int
        """
        return self._tick

    @tick.setter
    def tick(self, tick):
        """Sets the tick of this Result.


        :param tick: The tick of this Result.
        :type tick: int
        """
        if tick is None:
            raise ValueError("Invalid value for `tick`, must not be `None`")  # noqa: E501

        self._tick = tick

    @property
    def phase(self):
        """Gets the phase of this Result.


        :return: The phase of this Result.
        :rtype: str
        """
        return self._phase

    @phase.setter
    def phase(self, phase):
        """Sets the phase of this Result.


        :param phase: The phase of this Result.
        :type phase: str
        """
        if phase is None:
            raise ValueError("Invalid value for `phase`, must not be `None`")  # noqa: E501

        self._phase = phase
