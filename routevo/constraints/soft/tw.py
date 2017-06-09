#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Routevo
#
# You may use, distribute and modify this code under the
# terms of the MIT license.
#
# You should have received a copy of the MIT license with
# this file. If not, please visit <https://opensource.org/licenses/MIT>
from six import integer_types

from routevo.utils.checker import check
from routevo.utils.penalty import Penalty


class TimeWindow(object):
    """
    Time Window Soft Constraint.
    """

    def __init__(self, lower, expected, upper, penalty):
        """
        Initialization method.

        :param lower: lower time limit in seconds of arrival
        :type lower: float
        :param expected: expected time in seconds of arrival
        :type expected: float | None
        :param upper: upper time limit in seconds of arrival
        :type upper: float | None
        :param penalty: cost function object
        :type penalty: routevo.utils.penalty.Penalty | None
        """

        assert check(lower, (float, integer_types))
        assert check(expected, (float, integer_types, None))
        assert check(upper, (float, integer_types, None))
        assert isinstance(penalty, Penalty)

        self.lower = float(lower)
        self.expected = float(expected)
        self.upper = float(upper)
        self.penalty = penalty

    def __str__(self):
        return '{0} - {1}'.format(
            'N' if self.expected is None else int(self.expected / 60.0),
            'N' if self.upper is None else int(self.upper / 60.0)
        )

    def to_dict(self):
        """
        Convert TimeWindow to dictionary.

        :return: Dictionary with TimeWindow properties.
        :rtype: dict[basestring, T]
        """
        return {
            'lower': self.lower,
            'expected': self.expected,
            'upper': self.upper,
            'penalty': self.penalty.to_dict() if self.penalty else None,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Construct TimeWindow from dictionary.

        :param data: Properties of TimeWindow.
        :type data: dict
        :return: TimeWindow object.
        :rtype: TimeWindow
        """
        if data['penalty'] is not None:
            data['penalty'] = Penalty.from_dict(data['penalty'])

        return cls(**data)
