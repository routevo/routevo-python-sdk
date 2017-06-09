#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Routevo
#
# You may use, distribute and modify this code under the
# terms of the MIT license.
#
# You should have received a copy of the MIT license with
# this file. If not, please visit <https://opensource.org/licenses/MIT>

import json

import requests
import six
from requests import ConnectionError
from requests import Timeout

from routevo.state import State
from routevo.utils.checker import check


class Distances(object):
    """
    Distance matrix configuration.
    """

    ROUTING = 'routing'
    STRAIGHT = 'straight'

    ALL = (ROUTING, STRAIGHT)

    def __init__(self, kind=None, timeout=None):
        """
        Initialization method.

        :param kind: Type of distances in matrix.
        :type kind: basestring | None
        :param timeout: Maximum time in seconds to wait for a computation of distances matrix.
            None means to wait as much as necessary.
        :type timeout: float | int | None
        """
        assert kind is None or kind in self.ALL
        assert check(timeout, (float, six.integer_types, None))

        self.kind = kind
        self.timeout = float(timeout)

    def to_dict(self):
        """
        Convert Distances to dictionary.

        :return: Dictionary with Distances properties.
        :rtype: dict[basestring, T]
        """
        return {'endpoint': self.kind, 'timeout': self.timeout}


class Algorithm(object):
    """
    Optimization algorithm configuration.
    """

    def __init__(self, timeout=None):
        """
        Initialization method.

        :param timeout: Maximum time in seconds for optimization.
            None means to optimize as long, as there is no improvement.
        :type timeout: float | int | None
        """
        assert check(timeout, (float, six.integer_types, None))
        self.timeout = float(timeout)

    def to_dict(self):
        """
        Convert Algorithm to dictionary.

        :return: Dictionary with Algorithm properties.
        :rtype: dict[basestring, T]
        """
        return {'type': 'genetic', 'params': {'timeout': self.timeout}}


class ServiceError(Exception):
    def __init__(self, reason, code):
        self.reason = reason
        self.code = code

    def __str__(self):
        return 'Routevo Service Error: "{}", code: {}'.format(self.reason, self.code)


class Routevo(object):
    """
    Routevo service communication wrapper.
    """

    URL = 'http://127.0.0.1:7777'

    def __init__(self, key):
        """
        Service initialization.

        :param key: API access key.
        :type key: basestring
        """
        assert isinstance(key, six.string_types)
        self.key = key

        self.__previous_job = None
        self.__current_job = None

    @staticmethod
    def _validate(response):
        if not response.ok:
            raise ServiceError('HTTP error', response.status_code)

        result = json.loads(response.text)
        if 'response' not in result:
            raise ServiceError('Wrong response format.', 2)

        status = result['response']
        if status == 'error':
            raise ServiceError(result.get('explanation', 'Unknown error'), result.get('code', 1))

        return result

    def optimize(self, state, algorithm, distances):
        """
        Sends state to Routevo service for optimization.

        :param state: Set of requests to assign and routes to optimize.
        :type state: routevo.state.State
        :param algorithm: Optimization algorithm configuration
        :type algorithm: Algorithm
        :param distances: Distance matrix calculation parameters
        :type distances: Distances
        :return: Optimization job ID.
        :rtype: basestring
        """

        if self.__current_job is not None:
            raise ServiceError('Optimization in progress. Wait till the end, before submitting next state.', 3)

        assert isinstance(state, State)
        assert isinstance(algorithm, Algorithm)
        assert isinstance(distances, Distances)

        data = {
            'state': json.dumps(state.to_dict()),
            'key': self.key,
            'distances': json.dumps(distances.to_dict()),
            'algorithm': json.dumps(algorithm.to_dict()),
            'previous_task': self.__previous_job
        }

        try:
            response = requests.post('{}/api/v1/solve'.format(self.URL), data=data, timeout=10)
        except (Timeout, ConnectionError):
            raise ServiceError('Service unavailable: timeout.', 4)

        result = self._validate(response)
        self.__current_job = result.get('jid')
        return self.__current_job

    def result(self, job):
        """
        Gets results of the optimization.

        :param job: Optimization job ID.
        :type job: basestring
        :return: status, result
        :rtype: (basestring, T)
        """

        assert isinstance(job, six.string_types)

        try:
            response = requests.get('{}/api/v1/result/{}'.format(self.URL, job))
        except (Timeout, ConnectionError):
            raise ServiceError('Service unavailable: timeout.', 4)

        result = self._validate(response)
        data = result.get('state')
        state = State.from_dict(data) if data else None

        if state is not None:
            self.__previous_job = self.__current_job
            self.__current_job = None

        return result.get('status'), state
