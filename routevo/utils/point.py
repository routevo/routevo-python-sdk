#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Routevo
#
# You may use, distribute and modify this code under the
# terms of the MIT license.
#
# You should have received a copy of the MIT license with
# this file. If not, please visit <https://opensource.org/licenses/MIT>

from random import uniform

import six

from routevo.utils.checker import check


class Point(object):
    """
    Represents a geographic location.
    """

    def __init__(self, longitude, latitude):
        """
        Initialization method.

        :param longitude: Longitude in degrees.
        :type longitude: float
        :param latitude: Latitude in degrees
        :type latitude: float
        """
        assert check(longitude, (float, six.integer_types))
        assert check(latitude, (float, six.integer_types))

        self.longitude = float(longitude)
        self.latitude = float(latitude)

    def __repr__(self):
        return 'Point: ' + self.__str__()

    def __str__(self):
        return '[{0:.6f}, {1:.6f}]'.format(self.latitude, self.longitude)

    def to_dict(self):
        """
        Convert Point to dictionary.

        :return: Dictionary with Point properties.
        :rtype: dict[basestring, T]
        """
        return {'type': 'Point', 'coordinates': [self.longitude, self.latitude]}

    @classmethod
    def from_dict(cls, data):
        """
        Construct Point from dictionary.

        :param data: Properties of Point.
        :type data: dict
        :return: Point object.
        :rtype: Point
        """
        return cls(data['coordinates'][0], data['coordinates'][1])

    @classmethod
    def random(cls, longitude=(17.88, 17.98), latitude=(50.6, 50.7)):
        return cls(uniform(*longitude), uniform(*latitude))
