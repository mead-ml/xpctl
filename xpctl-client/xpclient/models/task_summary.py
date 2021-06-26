# coding: utf-8

"""
    xpctl

    This is a sample xpctl  server.  You can find out more about xpctl at [baseline](https://github.com/dpressel/baseline/blob/master/docs/xpctl.md).  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: apiteam@swagger.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class TaskSummary(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'task': 'str',
        'summary': 'object'
    }

    attribute_map = {
        'task': 'task',
        'summary': 'summary'
    }

    def __init__(self, task=None, summary=None):  # noqa: E501
        """TaskSummary - a model defined in Swagger"""  # noqa: E501

        self._task = None
        self._summary = None
        self.discriminator = None

        self.task = task
        self.summary = summary

    @property
    def task(self):
        """Gets the task of this TaskSummary.  # noqa: E501


        :return: The task of this TaskSummary.  # noqa: E501
        :rtype: str
        """
        return self._task

    @task.setter
    def task(self, task):
        """Sets the task of this TaskSummary.


        :param task: The task of this TaskSummary.  # noqa: E501
        :type: str
        """
        if task is None:
            raise ValueError("Invalid value for `task`, must not be `None`")  # noqa: E501

        self._task = task

    @property
    def summary(self):
        """Gets the summary of this TaskSummary.  # noqa: E501


        :return: The summary of this TaskSummary.  # noqa: E501
        :rtype: object
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """Sets the summary of this TaskSummary.


        :param summary: The summary of this TaskSummary.  # noqa: E501
        :type: object
        """
        if summary is None:
            raise ValueError("Invalid value for `summary`, must not be `None`")  # noqa: E501

        self._summary = summary

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(TaskSummary, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TaskSummary):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other