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

import six
from six import add_metaclass

from routevo.constraints.hard.base import BaseHardConstraint
from routevo.utils.checker import check


@add_metaclass(ABCMeta)
class LimitConstraint(BaseHardConstraint):
    """
    Base abstract class for hard limit constraints group.
    """

    def __init__(self, limit):
        """
        Initialization method.

        :param limit: Constraint limit, eg. vehicle capacity, maximum deliveries etc.
        :type limit: float
        """
        assert check(limit, (float, six.integer_types))
        self.limit = float(limit)

    def to_dict(self):
        """
        Convert LimitConstraint to dictionary.

        :return: Dictionary with LimitConstraint properties.
        :rtype: dict[basestring, T]
        """
        return {'name': self.__class__.__name__, 'params': {'limit': self.limit}}

    @classmethod
    def from_dict(cls, data):
        """
        Construct LimitConstraint from dictionary.

        :param data: Properties of LimitConstraint.
        :type data: dict
        :return: LimitConstraint object.
        :rtype: LimitConstraint
        """
        return cls(**data['params'])


class CapacityConstraint(LimitConstraint):
    """
    Vehicle capacity constraints.
    """
    pass


class MaximumDeliveriesConstraint(LimitConstraint):
    """
    Restricts number of cumulated deliveries.
    """
    pass
