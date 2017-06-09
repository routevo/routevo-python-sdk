#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Routevo
#
# You may use, distribute and modify this code under the
# terms of the MIT license.
#
# You should have received a copy of the MIT license with
# this file. If not, please visit <https://opensource.org/licenses/MIT>

from routevo.job import Job
from routevo.vehicle import Vehicle


class Route(object):
    """
    Links the vehicle with route points.
    """

    def __init__(self, vehicle, jobs, distances=None, times=None):
        """
        Initialization method.

        :param vehicle: Vehicle that execute this route.
        :type vehicle: routevo.vehicle.Vehicle
        :param jobs: List of route points.
        :type jobs: list[routevo.job.Job]
        """
        assert isinstance(vehicle, Vehicle)
        assert isinstance(jobs, list) and all(isinstance(j, Job) for j in jobs)

        self.vehicle = vehicle
        self.jobs = jobs
        self.distances = distances
        self.times = times

    def __len__(self):
        return len(self.jobs)

    def __getitem__(self, key):
        return self.jobs[key]

    def __iter__(self):
        return iter(self.jobs)

    def __repr__(self):
        return 'ROUTE V{0} {1}'.format(self.vehicle.id, [j.id for j in self.jobs])

    @staticmethod
    def __fill_up(array, n):
        if len(array) < n:
            array += [float('nan')] * (n - len(array))

        return array

    def __str__(self):
        result = ''
        fmt = '{:<15}{:<15}{:<15}{:<15}{:<15}{:<15}{:<15}\n'

        result += '{:<15}{:<15}\n'.format('Route:', self.vehicle.id)
        result += '{:<15}{:<15}\n'.format('Speed:', self.vehicle.speed)
        result += '{:<15}{:<15}\n'.format('Locked:', self.vehicle.locked)

        result += fmt.format('Request', 'Type', 'Size', 'Distance', 'Arrival', 'Expected', 'Waiting')

        jobs = len(self.jobs)

        distances = self.distances if self.distances else []
        distances = self.__fill_up(distances, jobs)

        times = [t['at'] for t in self.times] if self.times else []
        times = self.__fill_up(times, jobs)

        waitings = [t['end'] - t['at'] for t in self.times] if self.times else []
        waitings = self.__fill_up(waitings, jobs)

        for idx, j in enumerate(self.jobs):
            result += fmt.format(
                j.request.id, j.type, j.size,
                round(distances[idx] / 1000.0, 2),
                round(times[idx] / 60.0, 2),
                '' if j.arrival is None else str(j.arrival),
                round(waitings[idx] / 60.0, 2)
            )

        return result

    @property
    def requests(self):
        """
        Returns all requests delivered by this route.

        :return: Tuple containing requests objects.
        :rtype: tuple[routevo.request.Request]
        """

        return tuple(j.request for j in self.jobs if Job.MULTIPLIER[j.type] < 0)
