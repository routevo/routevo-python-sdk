#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Routevo
#
# You may use, distribute and modify this code under the
# terms of the MIT license.
#
# You should have received a copy of the MIT license with
# this file. If not, please visit <https://opensource.org/licenses/MIT>

import random
import sys
import time

from routevo import Job, Request, Route, State, Vehicle
from routevo.constraints import Restrictions
from routevo.constraints.hard.comeback import BanPickupComebackConstraint
from routevo.constraints.hard.cumulate import ForceCommonDirectionConstraint
from routevo.constraints.hard.limit import CapacityConstraint
from routevo.constraints.soft import TimeWindow
from routevo.constraints.soft.angle import InternalCumulationAngleSC, ExternalCumulationAngleSC, InterruptionAngleSC
from routevo.constraints.soft.limit import WaitingConstraint
from routevo.service import Routevo, Algorithm, Distances, ServiceError
from routevo.utils import Point, Penalty, CF

restrictions = Restrictions(
    soft=[InternalCumulationAngleSC(), ExternalCumulationAngleSC(),
          InterruptionAngleSC(), WaitingConstraint(Penalty(CF.QUADRATIC, cost=100), 60 * 10)],
    hard=[CapacityConstraint(8.0), BanPickupComebackConstraint(), ForceCommonDirectionConstraint()]
)

vehicles = []
for idx in range(10):
    v = Vehicle(idx, Point.random(), 15.0, 1.0, 10.0, restrictions=restrictions)
    vehicles.append(v)

sl = TimeWindow(0, 60 * 60, 90 * 60, Penalty(CF.QUADRATIC, cost=100))
carry = TimeWindow(0, 50 * 60, 60 * 60, Penalty(CF.QUADRATIC, cost=10.0 ** 5))

requests = []
for idx in range(30):
    p = Job(idx * 10 + 1, Job.PICKUP, Point.random(), None, 60 * 5, None)
    d = Job(idx * 10 + 2, Job.DELIVERY, Point.random(), sl, 60 * 5, None)
    r = Request(idx, 0, random.randint(1, 4), p, d, carry=carry)
    requests.append(r)

state = State([Route(v, []) for v in vehicles], requests)

API_KEY = '1008d98e6889bbc40124b9ecfd7ad2a0'
service = Routevo(API_KEY)

distances = Distances(Distances.ROUTING, timeout=15)
algorithm = Algorithm(timeout=60)

try:
    job = service.optimize(state, algorithm, distances)
    if job is None:
        print('Ups, something goes wrong...')
        sys.exit(1)

    print('Job ID: {}'.format(job))
    print('Waiting for result....')

    for _ in range(50):
        status, result = service.result(job)
        if result is not None:
            print('Got result!')
            print(result)
            break

        time.sleep(10)

except ServiceError as ex:
    print(ex)
