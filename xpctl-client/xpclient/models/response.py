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


class Response(object):
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
        'code': 'int',
        'message': 'str',
        'response_type': 'str'
    }

    attribute_map = {
        'code': 'code',
        'message': 'message',
        'response_type': 'response_type'
    }

    def __init__(self, code=None, message=None, response_type=None):  # noqa: E501
        """Response - a model defined in Swagger"""  # noqa: E501

        self._code = None
        self._message = None
        self._response_type = None
        self.discriminator = None

        self.code = code
        self.message = message
        self.response_type = response_type

    @property
    def code(self):
        """Gets the code of this Response.  # noqa: E501


        :return: The code of this Response.  # noqa: E501
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this Response.


        :param code: The code of this Response.  # noqa: E501
        :type: int
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501

        self._code = code

    @property
    def message(self):
        """Gets the message of this Response.  # noqa: E501


        :return: The message of this Response.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this Response.


        :param message: The message of this Response.  # noqa: E501
        :type: str
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")  # noqa: E501

        self._message = message

    @property
    def response_type(self):
        """Gets the response_type of this Response.  # noqa: E501


        :return: The response_type of this Response.  # noqa: E501
        :rtype: str
        """
        return self._response_type

    @response_type.setter
    def response_type(self, response_type):
        """Sets the response_type of this Response.


        :param response_type: The response_type of this Response.  # noqa: E501
        :type: str
        """
        if response_type is None:
            raise ValueError("Invalid value for `response_type`, must not be `None`")  # noqa: E501
        allowed_values = ["success", "error"]  # noqa: E501
        if response_type not in allowed_values:
            raise ValueError(
                "Invalid value for `response_type` ({0}), must be one of {1}"  # noqa: E501
                .format(response_type, allowed_values)
            )

        self._response_type = response_type

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
        if issubclass(Response, dict):
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
        if not isinstance(other, Response):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other