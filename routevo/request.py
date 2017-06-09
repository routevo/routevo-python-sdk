#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Routevo
#
# You may use, distribute and modify this code under the
# terms of the MIT license.
#
# You should have received a copy of the MIT license with
# this file. If not, please visit <https://opensource.org/licenses/MIT>

from functools import partial

import six

from routevo.constraints.restrictions import Restrictions
from routevo.constraints.soft.tw import TimeWindow
from routevo.job import Job
from routevo.utils.checker import check


class Request(object):
    """
    Represents a pickup and delivery task.
    """

    def __init__(self, rid, created, size, pickup, delivery, transport=None, carry=None, restrictions=None):
        """
        Initialization method.

        :param rid: Request unique ID.
        :type rid: int
        :param created: Time in seconds from now since the request was created.
        :type created: int
        :param size: Request size.
        :type size: int
        :param pickup: Pickup job.
        :type pickup: routevo.job.Job
        :param delivery: Delivery job.
        :type delivery: routevo.job.Job
        """
        assert isinstance(rid, six.integer_types)
        assert check(created, (float, six.integer_types))
        assert check(size, (float, six.integer_types))
        assert isinstance(pickup, Job)
        assert isinstance(delivery, Job)
        assert check(transport, (TimeWindow, None))
        assert check(carry, (TimeWindow, None))
        assert check(restrictions, (Restrictions, None))

        self.id = rid
        self.created = int(created)
        self.size = float(size)
        self.pickup = pickup.parent(self)
        self.delivery = delivery.parent(self)
        self.transport = transport
        self.carry = carry
        self.restrictions = Restrictions() if restrictions is None else restrictions

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Request({0}, x{1})'.format(self.id, id(self))

    def to_dict(self):
        """
        Convert Request to dictionary.

        :return: Dictionary with Request properties.
        :rtype: dict[basestring, T]
        """
        return {
            'rid': self.id,
            'created': self.created,
            'size': self.size,
            'pickup': self.pickup.to_dict(),
            'delivery': self.delivery.to_dict(),
            'transport': None if self.transport is None else self.transport.to_dict(),
            'carry': None if self.carry is None else self.carry.to_dict(),
            'restrictions': self.restrictions.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        """
        Construct Request from dictionary.

        :param data: Properties of Request.
        :type data: dict
        :return: Request object.
        :rtype: Request
        """
        callers = {
            'pickup': partial(Job.from_dict, t=Job.PICKUP),
            'delivery': partial(Job.from_dict, t=Job.DELIVERY),
            'transport': TimeWindow.from_dict,
            'carry': TimeWindow.from_dict,
            'restrictions': Restrictions.from_dict
        }

        for key, func in callers.items():
            if data[key] is not None:
                data[key] = func(data[key])

        return cls(**data)
