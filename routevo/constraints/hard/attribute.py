#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Routevo
#
# You may use, distribute and modify this code under the
# terms of the MIT license.
#
# You should have received a copy of the MIT license with
# this file. If not, please visit <https://opensource.org/licenses/MIT>

from routevo.constraints.hard.base import BaseMatchConstraint


class AttributesOperators(object):
    AND = 'and'
    OR = 'or'
    NOR = 'nor'


class AttributesMatchConstraint(BaseMatchConstraint):
    """
    Forces the matching of requests and vehicles attributes.
    When request requires vehicle to have a special equipment
    or vehicle can serve only special types of requests,
    this constraint will ensure, that this requirements will be fulfilled.
    """

    def __init__(self, requirements):
        """
        Initialization method.

        :param requirements: user defined attribute requirements
            grouped by operator defined in AttributesOperators
        :type requirements: dict[str, dict[T, T]]
        """
        self.requirements = requirements

    def to_dict(self):
        """
        Convert AttributesMatchConstraint to dictionary.

        :return: Dictionary with constraint properties.
        :rtype: dict[basestring, T]
        """
        result = {
            'name': self.__class__.__name__,
            'params': {
                'requirements': {f: req for f, req in self.requirements.items()}
            }
        }

        return result

    @classmethod
    def from_dict(cls, data):
        """
        Construct AttributesMatchConstraint from dictionary.

        :param data: Properties of constraint.
        :type data: dict
        :return: AttributesMatchConstraint object.
        :rtype: AttributesMatchConstraint
        """
        requirements = {k: v for k, v in data['params']['requirements'].items()}
        return cls(requirements)
