#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Routevo
#
# You may use, distribute and modify this code under the
# terms of the MIT license.
#
# You should have received a copy of the MIT license with
# this file. If not, please visit <https://opensource.org/licenses/MIT>

from routevo.constraints.soft.base import BaseSoftConstraint


class InternalCumulationAngleSC(BaseSoftConstraint):
    """
    Restricts cumulation from one pickup location when the are in different directions.
    """
    pass


class ExternalCumulationAngleSC(BaseSoftConstraint):
    """
    Restricts cumulation from different pickup locations when the are in different directions.
    """
    pass


class InterruptionAngleSC(BaseSoftConstraint):
    """
    Restricts interruption of currently executed job when new possible job
    is far away from current vehicle location and in opposite direction.
    """
    pass
