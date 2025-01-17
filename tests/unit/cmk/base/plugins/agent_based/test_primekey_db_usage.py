#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.base.plugins.agent_based.agent_based_api.v1 import Metric, Result, Service, State
from cmk.base.plugins.agent_based.primekey_db_usage import _Section, check, discover, parse


def test_parse() -> None:
    assert parse([["85.3"]]) == _Section(85.3)


def test_discover() -> None:
    assert list(discover(section=_Section(85.3))) == [Service()]


def test_check() -> None:
    assert list(check(params={"levels": (80.0, 90.0)}, section=_Section(85.3))) == [
        Result(state=State.WARN, summary="Disk Utilization: 85.30% (warn/crit at 80.00%/90.00%)"),
        Metric("disk_utilization", 85.3, levels=(80.0, 90.0)),
    ]
