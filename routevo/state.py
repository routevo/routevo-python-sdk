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

from routevo.request import Request
from routevo.route import Route
from routevo.utils.checker import check
from routevo.vehicle import Vehicle


class State(object):
    """
    Encapsulates routes, vehicles and requests.
    """

    def __init__(self, routes, unassigned=None):
        """
        Initialization method.

        :param routes: Routes.
        :type routes: list[routevo.route.Route]
        :param unassigned: New or unassigned requests to any vehicle.
        :type unassigned: list[routevo.request.Request]
        """
        assert isinstance(routes, list)
        for r in routes:
            assert isinstance(r, Route)

        assert check(unassigned, (list, None))
        if unassigned is not None:
            for r in unassigned:
                assert isinstance(r, Request)

        self.routes = {r.vehicle.id: r for r in routes}
        self.unassigned = [] if unassigned is None else unassigned

    def __iter__(self):
        return self.routes.values()

    def __str__(self):
        result = ''
        for route in self.routes.values():
            result += str(route)
            result += '\n' + '-' * 15 * 7 + '\n'

        return result

    def to_dict(self):
        """
        Convert State to dictionary.

        :return: Dictionary with State properties.
        :rtype: dict[basestring, T]
        """
        vehicles, requests, routes = [], [], {}
        for r in self.routes.values():
            vehicles.append(r.vehicle.to_dict())
            requests.extend([req.to_dict() for req in r.requests])

            routes[r.vehicle.id] = {
                'jobs': [j.id for j in r.jobs],
                'distances': [],
                'times': [],
            }

        requests.extend([req.to_dict() for req in self.unassigned])
        return {'vehicles': vehicles, 'requests': requests, 'routes': routes}

    @staticmethod
    def _unpack(method, objects):
        result = {}
        for o in objects:
            obj = method(o)
            result[obj.id] = obj
        return result

    @classmethod
    def from_dict(cls, data):
        """
        Construct State from dictionary.

        :param data: Properties of vehicle.
        :type data: dict
        :return: Vehicle object.
        :rtype: Vehicle
        """
        requests = cls._unpack(Request.from_dict, data['requests'])
        vehicles = cls._unpack(partial(Vehicle.from_dict), data['vehicles'])

        jobs = {}
        for r in requests.values():
            jobs[r.pickup.id] = r.pickup
            jobs[r.delivery.id] = r.delivery

        routes, old = {}, set()
        for vid, seq in data['routes'].items():
            vid = int(vid)
            route = Route(vehicles[vid], [jobs[jid] for jid in seq['jobs']], seq['distances'], seq['times'])
            routes[vid] = route
            old |= set(route.requests)

        new = set(requests.values()) - old
        return cls(list(routes.values()), list(new))
