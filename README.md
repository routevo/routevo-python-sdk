# Routevo Python SDK

Routevo is a cloud-based solution to vehicle routing problem.

---

## Usage

Below is the basic example how to use this SDK.

```
import random
import sys
import time

from routevo import Job, Request, Route, State, Vehicle
from routevo.constraints import Restrictions
from routevo.constraints.hard.limit import CapacityConstraint
from routevo.constraints.soft import TimeWindow
from routevo.service import Routico, Algorithm, Distances, ServiceError
from routevo.utils import Point, Penalty, CF

restrictions = Restrictions(hard=[CapacityConstraint(16.0)])

vehicles = []
for idx in xrange(10):
    loc = (random.uniform(17.88, 17.98), random.uniform(50.6, 50.7))
    vehicles.append(Vehicle(idx, Point(*loc), 15.0, 1.0, 10.0, restrictions=restrictions))

sl = TimeWindow(0, 60 * 60, 90 * 60, Penalty(CF.QUADRATIC, cost=100))

requests = []
for idx in xrange(30):
    p1 = (random.uniform(17.88, 17.98), random.uniform(50.6, 50.7))
    p2 = (random.uniform(17.88, 17.98), random.uniform(50.6, 50.7))

    p = Job(idx * 10 + 1, Job.PICKUP, Point(*p1), None, 60 * 5, None)
    d = Job(idx * 10 + 2, Job.DELIVERY, Point(*p2), sl, 60 * 5, None)
    requests.append(Request(idx, 0, random.randint(1, 4), p, d))

state = State({v.id: Route(v, []) for v in vehicles}, requests)

service = Routico(YOUR_API_KEY)

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

```


---

## Documentation

Detailed documentation is available at [docs.routevo.io](https://docs.routevo.io).

---

## Contact

If you have any questions or suggestions, please send us an email [support@routevo.io](mailto:support@routevo.io).
