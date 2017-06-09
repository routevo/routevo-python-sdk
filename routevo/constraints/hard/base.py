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

from routevo.constraints.base import Constraint
from routevo.constraints.serializable import Serializable


@add_metaclass(ABCMeta)
class BaseHardConstraint(Constraint, Serializable):
    """
    Abstract base class for hard constraints.
    """
    pass


@add_metaclass(ABCMeta)
class BaseMatchConstraint(Constraint, Serializable):
    """
    Abstract base class for attribute match constraints.
    """
    pass
