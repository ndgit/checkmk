#!/usr/bin/env python3
# Copyright (C) 2023 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from dataclasses import dataclass

from .agent_based_api.v1 import Attributes, contains, register, SNMPTree
from .agent_based_api.v1.type_defs import InventoryResult, StringTable


@dataclass(frozen=True)
class KyoceraPrinter:
    system_firmware: str
    serial_number: str
    device_number: str
    install_date: str
    model: str


def parse_kyocera_printer(string_table: StringTable) -> KyoceraPrinter | None:
    if not string_table:
        return None

    line = string_table[0]
    return KyoceraPrinter(
        system_firmware=line[0],
        serial_number=line[1],
        device_number=line[2],
        install_date=line[3],
        model=line[4],
    )


register.snmp_section(
    name="kyocera_printer",
    parse_function=parse_kyocera_printer,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.1347",
        oids=[
            "43.5.4.1.5.1.1",  # system (firmware)
            "43.5.1.1.28.1",  # serial number
            "43.5.1.1.29.1",  # device number
            "42.2.6.3.0.0",  # install date (not used, as it is currently empty in all our walks)
            "43.5.1.1.1.1",  # product/model
        ],
    ),
    detect=contains(".1.3.6.1.2.1.1.1.0", "KYOCERA"),
)


def inventory_kyocera_printer(section: KyoceraPrinter) -> InventoryResult:
    yield Attributes(
        path=["hardware", "system"],
        inventory_attributes={
            "manufacturer": "Kyocera",
            "model": section.model,
            "device_number": section.device_number,
            "serial": section.serial_number,
        },
    )

    yield Attributes(
        path=["software", "firmware"],
        inventory_attributes={
            "vendor": "Kyocera",
            "version": section.system_firmware,
        },
    )


register.inventory_plugin(
    name="kyocera_printer",
    inventory_function=inventory_kyocera_printer,
)
