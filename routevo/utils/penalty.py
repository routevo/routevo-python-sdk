#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Routevo
#
# You may use, distribute and modify this code under the
# terms of the MIT license.
#
# You should have received a copy of the MIT license with
# this file. If not, please visit <https://opensource.org/licenses/MIT>
import six

from routevo.utils.checker import check


class CF(object):
    """
    Definitions of available cost functions for Penalty.
    """

    LINEAR = 'linear'
    QUADRATIC = 'quadratic'
    ZERO = 'zero'

    ALL = (LINEAR, QUADRATIC, ZERO)


class Penalty(object):
    """
    Describes how penalty cost are calculated for violating soft constraints.
    """

    def __init__(self, func, cost=100.0, c=0.0):
        """
        Initialization method.

        :param func: Cost function name defined in CF class.
        :type func: basestring
        :param cost: Maximum cost at upper limit of constraint.
        :type cost: float
        :param c: Constant cost parameter of cost function, for linear: y = ax + c.
        :type c: float
        """
        assert isinstance(func, six.string_types) and func in CF.ALL
        assert check(cost, (float, six.integer_types))
        assert check(c, (float, six.integer_types))

        self.func = func
        self.cost = float(cost)
        self.c = float(c)

    def to_dict(self):
        """
        Convert Penalty to dictionary.

        :return: Dictionary with Penalty properties.
        :rtype: dict[basestring, T]
        """
        return {'func': self.func, 'cost': self.cost, 'c': self.c}

    @classmethod
    def from_dict(cls, data):
        """
        Construct Penalty from dictionary.

        :param data: Dictionary with penalty properties.
        :type data: dict
        :return: Penalty object.
        :rtype: Penalty
        """
        return Penalty(**data)
