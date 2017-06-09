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

from six import add_metaclass, integer_types

from routevo.constraints.soft.base import BaseSoftConstraint
from routevo.utils.checker import check
from routevo.utils.penalty import Penalty


@add_metaclass(ABCMeta)
class LimitConstraint(BaseSoftConstraint):
    """
    Base abstract class for soft limit constraints group.
    """

    def __init__(self, penalty, limit, margin=0.0):
        """
        Initialization method.

        :param penalty: Penalty for violating constraint.
        :type penalty: routevo.utils.penalty.Penalty
        :param limit: Constraint limit, eg. distance, time etc.
        :type limit: float
        :param margin: Safety margin. Limit + margin = upper limit.
        :type margin: float
        """
        assert isinstance(penalty, Penalty)
        assert check(limit, (float, integer_types))
        assert check(margin, (float, integer_types))

        self.limit = float(limit)
        self.margin = float(margin)
        self.cf = penalty

    def to_dict(self):
        """
        Convert LimitConstraint to dictionary.

        :return: Dictionary with LimitConstraint properties.
        :rtype: dict[basestring, T]
        """
        return {
            'name': self.__class__.__name__,
            'params': {
                'limit': self.limit,
                'margin': self.margin,
                'penalty': self.cf.to_dict()
            }
        }

    @classmethod
    def from_dict(cls, data):
        """
        Construct LimitConstraint from dictionary.

        :param data: Properties of LimitConstraint.
        :type data: dict
        :return: LimitConstraint object.
        :rtype: LimitConstraint
        """
        data['params']['penalty'] = Penalty.from_dict(data['params']['penalty'])
        return cls(**data['params'])


class DistanceConstraint(LimitConstraint):
    """
    Maximum total transport distance constraint.
    Useful for limiting the reach of certain vehicles such as bicycles.
    """

    def __init__(self, penalty, limit, margin=1000.0):
        """
        Initialization method.

        :param penalty: Penalty for violating constraint.
        :type penalty: routevo.utils.penalty.Penalty
        :param limit: Distance limit in meters.
        :type limit: float
        :param margin: Safety margin in meters. Limit + margin = upper limit.
        :type margin: float
        """

        super(DistanceConstraint, self).__init__(penalty, limit, margin)


class WaitingConstraint(LimitConstraint):
    """
    Maximum possible additional waiting time during cumulation from one pickup location.
    """

    def __init__(self, penalty, limit, margin=5 * 60.0):
        """
        Initialization method.

        :param penalty: Penalty for violating constraint.
        :type penalty: routevo.utils.penalty.Penalty
        :param limit: Waiting time limit in seconds.
        :type limit: float
        :param margin: Safety margin in seconds. Limit + margin = upper limit.
        :type margin: float
        """

        super(WaitingConstraint, self).__init__(penalty, limit, margin)
