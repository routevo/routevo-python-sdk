#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Routevo
#
# You may use, distribute and modify this code under the
# terms of the MIT license.
#
# You should have received a copy of the MIT license with
# this file. If not, please visit <https://opensource.org/licenses/MIT>

from routevo.constraints.hard.attribute import AttributesMatchConstraint
from routevo.constraints.hard.comeback import BanPickupComebackConstraint
from routevo.constraints.hard.cumulate import CumulationConstraint, BanExternalPickupsConstraint, \
    ForceCommonDirectionConstraint
from routevo.constraints.hard.limit import CapacityConstraint, MaximumDeliveriesConstraint
from routevo.constraints.soft.angle import InternalCumulationAngleSC, ExternalCumulationAngleSC, InterruptionAngleSC
from routevo.constraints.soft.limit import DistanceConstraint, WaitingConstraint
from routevo.utils.checker import check


class Restrictions(object):
    """
    Aggregates hard, soft constraints, attributes and filters.

    Hard constraints ensure that restriction needs to be fulfilled in order to accept solution.
    For example, if vehicle has limited capacity, hard constraint will not allow to exceeds it.

    Soft constraints are the type of restrictions that can be violated.
    They are kind of guide for algorithm, that helps to determine the desired solution.
    For example, if bike shouldn't carry distant deliveries, we can limit its range with DistanceConstraint.
    This way distant deliveries will be accepted if there is no other configuration.
    Otherwise, algorithm will always try to minimize the cost function (penalty),
    and find another, more suitable vehicle.


    Attributes are user-defined properties of objects (vehicles, requests).
    Filters helps select only these objects, that has desired attributes.
    For example, if we want to deliver medicines, that should be kept refrigerated,
    we can define AttributesMatchConstraint. In this way, we can ensure that the order will be delivered only
    by the vehicle equipped with a cooled container. If there is no such vehicle, than order will remain unassigned.
    """

    FILTERS = {
        'AttributesMatchConstraint': AttributesMatchConstraint,
    }

    HARD = {
        'BanPickupComebackConstraint': BanPickupComebackConstraint,
        'CumulationConstraint': CumulationConstraint,
        'BanExternalPickupsConstraint': BanExternalPickupsConstraint,
        'ForceCommonDirectionConstraint': ForceCommonDirectionConstraint,
        'CapacityConstraint': CapacityConstraint,
        'MaximumDeliveriesConstraint': MaximumDeliveriesConstraint,
    }

    SOFT = {
        'InternalCumulationAngleSC': InternalCumulationAngleSC,
        'ExternalCumulationAngleSC': ExternalCumulationAngleSC,
        'InterruptionAngleSC': InterruptionAngleSC,
        'DistanceConstraint': DistanceConstraint,
        'WaitingConstraint': WaitingConstraint
    }

    def __init__(self, attributes=None, filters=None, hard=None, soft=None):
        """
        Initialization method.

        :param attributes: User defined attributes held by object.
        :type attributes: dict
        :param filters: Filters constraints.
        :type filters: list[routevo.constraints.hard.base.BaseMatchConstraint]
        :param hard: List of hard constraints.
        :type hard: list[routevo.constraints.hard.base.BaseHardConstraint]
        :param soft: List of soft constraints.
        :type soft: list[routevo.constraints.soft.base.BaseSoftConstraint]
        """
        assert check(attributes, (dict, None))
        self._validate(filters, self.FILTERS.values())
        self._validate(hard, self.HARD.values())
        self._validate(soft, self.SOFT.values())

        self.attributes = {} if attributes is None else attributes
        self.filters = [] if filters is None else filters
        self.hard = [] if hard is None else hard
        self.soft = [] if soft is None else soft

    @staticmethod
    def _validate(variable, allowed):
        assert isinstance(variable, list) or variable is None
        if variable is not None:
            for f in variable:
                assert isinstance(f, tuple(allowed))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.__dict__ == other.__dict__

    def to_dict(self):
        """
        Convert Restrictions to dictionary.

        :return: Dictionary with Restrictions properties.
        :rtype: dict[basestring, T]
        """
        return {
            'attributes': self.attributes,
            'filters': [f.to_dict() for f in self.filters],
            'hard': [c.to_dict() for c in self.hard],
            'soft': [c.to_dict() for c in self.soft]
        }

    @staticmethod
    def _decode(restrictions, mapper):
        result = []
        for restriction in restrictions:
            c = mapper.get(restriction['name'])
            if c is not None:
                result.append(c.from_dict(restriction))

        return None if not result else result

    @classmethod
    def from_dict(cls, data):
        """
        Construct Restrictions from dictionary.

        :param data: Properties of Restrictions.
        :type data: dict
        :return: Restrictions object.
        :rtype: Restrictions
        """
        attributes = data['attributes']
        filters = Restrictions._decode(data['filters'], Restrictions.FILTERS)
        hard = Restrictions._decode(data['hard'], Restrictions.HARD)
        soft = Restrictions._decode(data['soft'], Restrictions.SOFT)

        return Restrictions(attributes, filters, hard, soft)
