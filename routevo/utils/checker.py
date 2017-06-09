#!/usr/bin/env python
# -*- coding: utf-8 -*-


def check(variable, types):
    result = False
    for t in types:
        if t is None:
            result |= variable is None
        else:
            result |= isinstance(variable, t)

        if result:
            break

    return result

