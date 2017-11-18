#!/usr/bin/python3

import argparse

import libvirt
import settings
from logger import *


def parse_arguments():
    parser = argparse.ArgumentParser(description="Qemu/kvm script")
    parser.add_argument("-u", "--uri", help="hypervisor driver uri, default: qemu:///system")
    parser.add_argument("-v", "--verbose", help="verbose output", action="store_true")
    args = parser.parse_args()
    if settings.debug:
        settings.verbose = True
    if settings.debug is not True and len(sys.argv) == 1:
        parser.print_help()
        exit(1)
    if args.verbose:
        settings.verbose = True
    if args.uri:
        settings.hypervisor_uri = args.uri


def connect_hypervisor():
    conn = libvirt.openReadOnly(settings.hypervisor_uri)
    if conn is None:
        log_error("Failed to connect")
        exit(1)
    log_info("Libvirt connected to: " + settings.hypervisor_uri)
    return conn


def main():
    parse_arguments()
    conn = connect_hypervisor()
    pools = conn.listAllStoragePools(0)
    if pools is None:
        log_fatal('Failed to locate any StoragePool objects.')
    for pool in pools:
        log_info('Pool: ' + pool.name())

    domainIDs = conn.listDomainsID()
    if domainIDs is None:
        log_fatal('Failed to get a list of domain IDs')

    log_info("Active domain IDs:")
    if len(domainIDs) == 0:
        log_info('  None')
    else:
        for domainID in domainIDs:
            log_info('  ' + str(domainID))
    conn.close()


if __name__ == "__main__":
    main()
