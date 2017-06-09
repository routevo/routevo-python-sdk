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

from routevo.constraints.soft.tw import TimeWindow
from routevo.utils.checker import check
from routevo.utils.point import Point


class Job(object):
    """
    Basic unit of courier work.
    """

    PICKUP = 'pickup'
    DELIVERY = 'delivery'
    ALL = (PICKUP, DELIVERY)

    MULTIPLIER = {
        PICKUP: 1,
        DELIVERY: -1
    }

    def __init__(self, jid, t, location, arrival, waiting, aid=None, times=None):
        """
        Initialization method.

        :param jid: Job unique ID.
        :type jid: int
        :param t: Type of job: PICKUP or DELIVERY
        :type t: str
        :param location: Job location.
        :type location: routevo.utils.point.Point
        :param arrival: Soft restriction on arrival time.
        :type arrival: routevo.constraints.soft.tw.TimeWindow | None
        :param aid: Location ID. It is used to distinguish, for example,
            different floors of the same building, and to group jobs from the same location.
        :type aid: int | None
        :param times: Realization times of finished phases of job, in seconds from now.
        :type times: dict[str, int|float|None] | None
        """
        assert isinstance(jid, six.integer_types)
        assert isinstance(t, six.string_types) and t in self.ALL
        assert isinstance(location, Point)
        assert check(arrival, (TimeWindow, None))
        assert check(waiting, (float, six.integer_types))
        assert check(aid, (six.integer_types, None))
        assert check(times, (dict, None))

        self.id = jid
        self.type = t
        self.aid = aid
        self.location = location
        self.arrival = arrival
        self.waiting = float(waiting)

        _times = {} if times is None else times
        self.begin = _times.get('begin', None)
        self.at = _times.get('at', None)
        self.end = _times.get('end', None)

        self.request = None
        self._size = None

    def parent(self, request):
        """
        Sets job parent.

        :param request: Parent request.
        :type request: routevo.request.Request
        :return: self
        :rtype: routevo.job.Job
        """
        self.request = request
        return self

    @property
    def size(self):
        """
        Size of delivery package

        :return: Size of package.
        :rtype: float | None
        """
        if self.request is None:
            return None

        if self._size is None:
            self._size = self.request.size * Job.MULTIPLIER[self.type]

        return self._size

    def __repr__(self):
        return '({0}, {1})'.format(self.type, self.request.id)

    def to_dict(self):
        """
        Convert Job to dictionary.

        :return: Dictionary with Job properties.
        :rtype: dict[basestring, T]
        """
        return {
            'jid': self.id,
            'aid': self.aid,
            'location': self.location.to_dict(),
            'arrival': None if self.arrival is None else self.arrival.to_dict(),
            'waiting': self.waiting,
            'times': {
                'begin': self.begin,
                'at': self.at,
                'end': self.end,
            }
        }

    @classmethod
    def from_dict(cls, data, t):
        """
        Construct Job from dictionary.

        :param data: Properties of Job.
        :type data: dict
        :param t: Job type:
        :type t: basestring
        :return: Job object.
        :rtype: Job
        """
        callers = {
            'location': Point.from_dict,
            'arrival': TimeWindow.from_dict,
        }

        for key, func in callers.items():
            if data[key] is not None:
                data[key] = func(data[key])

        data['t'] = t
        return cls(**data)
