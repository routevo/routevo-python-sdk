#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Routevo
#
# You may use, distribute and modify this code under the
# terms of the MIT license.
#
# You should have received a copy of the MIT license with
# this file. If not, please visit <https://opensource.org/licenses/MIT>

from abc import ABCMeta

from six import add_metaclass


@add_metaclass(ABCMeta)
class Serializable(object):
    """
    Base class for constraints serialization.
    """

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.__dict__ == other.__dict__

    def to_dict(self):
        """
        Convert Serializable object to dictionary.

        :return: Dictionary with object properties.
        :rtype: dict[basestring, T]
        """
        return {'name': self.__class__.__name__, 'params': {}}

    @classmethod
    def from_dict(cls, data):
        """
        Construct object from dictionary.

        :param data: Properties of object.
        :type data: dict
        :return: Concrete object.
        :rtype: T
        """
        return cls(**data['params'])
