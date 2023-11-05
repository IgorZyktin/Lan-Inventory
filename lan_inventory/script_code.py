"""Code of the script."""
import json
import re
import subprocess
import sys
from dataclasses import dataclass

import colorama
import getmac
from prettytable import PrettyTable


@dataclass
class KnownHost:
    """Known host description."""
    mac: str
    comment: str


@dataclass
class Config:
    """Script config."""
    subnet: str  # poor man's subnet notation
    known_hosts: dict[str, KnownHost]

    @classmethod
    def from_file(cls, filename: str) -> 'Config':
        """Read config from file."""
        with open(filename, mode='r', encoding='utf-8') as file:
            data = json.load(file)

        return cls(
            subnet=data['subnet'],
            known_hosts={
                mac: KnownHost(mac=mac, comment=comment)
                for mac, comment in data['known_hosts'].items()
            }
        )


@dataclass
class Machine:
    """Specific host."""
    ip: str
    mac: str
    hostname: str | None
    comment: str | None
    is_known: bool

    @property
    def numeric_ip(self) -> tuple[int, ...]:
        """Return IPv4 as tuples."""
        return tuple([
            int(x) for x in self.ip.split('.')
        ])


def get_local_hostnames() -> dict[str, str]:
    """Return mapping ip -> hostname."""
    if sys.platform == 'win32':
        path = 'c:\\windows\\system32\\drivers\\etc\\hosts'
    elif sys.platform == 'darwin':
        path = '/private/etc/hosts'
    else:
        path = '/etc/hosts'

    result: dict[str, str] = {}

    with open(path, mode='r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith('#'):
                continue

            line = re.sub(r'\t+', ' ', line)
            line = re.sub(r'\s+', ' ', line)

            ip, hostname, *_ = line.split(' ')
            result[ip] = hostname

    return result


def scan_network(subnet: str) -> list[Machine]:
    """Scann all ips in LAN."""
    machines: list[Machine] = []
    empty = '00:00:00:00:00:00'

    for i in range(0, 256):
        ip = f'{subnet}.{i}'

        res = subprocess.run(
            ['ping', '-c', '2', '-W', '1', ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )

        if res.returncode != 0:
            continue

        if '100% packet loss' in (res.stdout or res.stderr):
            continue

        mac = getmac.get_mac_address(ip=ip)

        if mac is None or mac == empty:
            mac = '???'

        machine = Machine(
            ip=ip,
            mac=mac,
            hostname=None,
            comment=None,
            is_known=False,
        )
        machines.append(machine)

    return machines


def print_results(machines: list[Machine]) -> None:
    """Show human-readable output."""
    machines.sort(key=lambda _machine: _machine.numeric_ip)

    table = PrettyTable()
    table.field_names = [
        'N',
        'MAC',
        'IP',
        'Hostname',
        'Comment',
    ]

    for i, machine in enumerate(machines, start=1):
        if machine.is_known:
            def color(text: str) -> str:
                """Draw known machines in green."""
                return colorama.Fore.GREEN + text + colorama.Fore.RESET
        else:
            def color(text: str) -> str:
                """Draw unknown machines in red."""
                return colorama.Fore.RED + text + colorama.Fore.RESET

        table.add_row(
            [
                str(i),
                color(machine.mac),
                color(machine.ip),
                machine.hostname or '',
                machine.comment or '',
            ]
        )

    print(table.get_string())
