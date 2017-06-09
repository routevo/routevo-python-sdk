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

from routevo.constraints.hard.base import BaseHardConstraint, BaseMatchConstraint


@add_metaclass(ABCMeta)
class CumulationConstraintBase(BaseHardConstraint):
    """
    Base abstract class for hard cumulation constraints group.
    """
    pass


class CumulationOperators(object):
    OR = 'or'
    NOR = 'nor'


class CumulationConstraint(CumulationConstraintBase, BaseMatchConstraint):
    """
    Forces cumulation of deliveries.
    """

    def __init__(self, requirements):
        """
        Initialization method.

        :param requirements: Cumulation requirements for request.
        :type requirements: dict[str, list[int]]
        """
        self.requirements = requirements

    def to_dict(self):
        """
        Convert CumulationConstraint to dictionary.

        :return: Dictionary with CumulationConstraint properties.
        :rtype: dict[basestring, T]
        """
        result = {
            'name': self.__class__.__name__,
            'requirements': {
                f: [rid for rid in reqs] for f, reqs in self.requirements.items()
                }
        }

        return result

    @classmethod
    def from_dict(cls, data):
        """
        Construct CumulationConstraint from dictionary.

        :param data: Properties of CumulationConstraint.
        :type data: dict
        :return: CumulationConstraint object.
        :rtype: CumulationConstraint
        """
        restrictions = {
            k: [rid for rid in v] for k, v in data['requirements'].items()
            }
        return cls(restrictions)


class BanExternalPickupsConstraint(CumulationConstraintBase):
    """
    Disables cumulation from different pickups locations.
    """
    pass


class ForceCommonDirectionConstraint(CumulationConstraintBase):
    """
    Forces common direction for deliveries from many different pickup locations.
    """
    pass
