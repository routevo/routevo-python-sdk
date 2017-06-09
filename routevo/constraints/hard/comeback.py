#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Routevo
#
# You may use, distribute and modify this code under the
# terms of the MIT license.
#
# You should have received a copy of the MIT license with
# this file. If not, please visit <https://opensource.org/licenses/MIT>

from routevo.constraints.hard.base import BaseHardConstraint


class BanPickupComebackConstraint(BaseHardConstraint):
    """
    Disables return to pickup location for another delivery until current delivery from that location will be finished.
    """
    pass
