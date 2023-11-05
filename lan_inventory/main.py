"""Main."""
import script_code as code


def main():
    """Entry point."""
    config = code.Config.from_file('config.json')
    hostnames = code.get_local_hostnames()
    local_machines = code.scan_network(config.subnet)

    for machine in local_machines:
        machine.hostname = hostnames.get(machine.ip) or ''

        host = config.known_hosts.get(machine.mac.lower())

        if host:
            machine.is_known = True
            machine.comment = host.comment

    code.print_results(local_machines)


if __name__ == '__main__':
    main()
