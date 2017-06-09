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

from routevo.constraints.hard.limit import CapacityConstraint
from routevo.constraints.restrictions import Restrictions
from routevo.constraints.mixed.availability import Availability
from routevo.utils.checker import check
from routevo.utils.point import Point


class Vehicle(object):
    """
    Describes vehicle properties.
    """

    def __init__(self, vid, location, speed, amortization, salary, availability=None,
                 locked=None, restrictions=None, time=0.0, waiting=0.0):
        """
        Initialization method.

        :param vid: Unique vehicle ID.
        :type vid: int
        :param location: Current geographical location of vehicle.
        :type location: routevo.utils.point.Point
        :param speed: Average speed in km/h.
        :type speed: float
        :param amortization: Amortization cost per kilometer.
        :type amortization: float
        :param salary: Driver salary cost per hour.
        :type salary: float
        :param availability: Time window defining when vehicle is operational.
        :type availability: routevo.constraints.mixed.availability.Availability | None
        :param locked: Number of locked jobs in route.
        :type locked: int | None
        :param restrictions: Restrictions for vehicle.
        :type restrictions: routevo.constraints.restrictions.Restrictions | None
        :param time: Location age.
        :type time: int
        """

        assert isinstance(vid, six.integer_types)
        assert isinstance(location, Point)
        assert check(time, (float, six.integer_types))
        assert check(speed, (float, six.integer_types))
        assert check(waiting, (float, six.integer_types))
        assert check(amortization, (float, six.integer_types))
        assert check(salary, (float, six.integer_types))
        assert check(availability, (Availability, None))
        assert check(locked, (six.integer_types, None))
        assert check(restrictions, (Restrictions, None))

        self.id = vid
        self.location = location
        self.time = float(time)
        self.speed = float(speed)
        self.waiting = float(waiting)
        self.amortization = float(amortization)
        self.salary = float(salary)
        self.availability = availability
        self.locked = 0 if locked is None else int(locked)
        self.restrictions = Restrictions() if restrictions is None else restrictions

    def __repr__(self):
        return 'VEHICLE {0}: {1}'.format(self.id, self.location)

    @property
    def capacity(self):
        """
        Gets capacity limit for vehicle.

        :return: Capacity of vehicle.
        :rtype: float | None
        """
        constraint = [c for c in self.restrictions.hard if isinstance(c, CapacityConstraint)]
        if not constraint:
            return None

        return constraint[0].limit

    def to_dict(self):
        """
        Convert Vehicle to dictionary.

        :return: Dictionary with vehicle properties.
        :rtype: dict[basestring, T]
        """
        return {
            'vid': self.id,
            'location': self.location.to_dict(),
            'speed': self.speed,
            'waiting': self.waiting,
            'amortization': self.amortization,
            'salary': self.salary,
            'availability': None if self.availability is None else self.availability.to_dict(),
            'locked': self.locked,
            'restrictions': self.restrictions.to_dict(),
            'time': self.time
        }

    @classmethod
    def from_dict(cls, data):
        """
        Construct Vehicle from dictionary.

        :param data: Properties of vehicle.
        :type data: dict
        :return: Vehicle object.
        :rtype: Vehicle
        """
        callers = {
            'location': Point.from_dict,
            'availability': Availability.from_dict,
            'restrictions': Restrictions.from_dict
        }

        for key, func in callers.items():
            if data[key] is not None:
                data[key] = func(data[key])

        return cls(**data)
