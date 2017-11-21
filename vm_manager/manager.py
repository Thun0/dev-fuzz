#!/usr/bin/python3

import argparse

import libvirt
import settings
from logger import *


def parse_arguments():
    """Argument parser for console usage

    """
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


def connect_hypervisor(uri=settings.hypervisor_uri):
    """Connects to hypervisor

    :param uri: URI to connect to
    :return: Object representing connection to hypervisor
    """
    conn = libvirt.open(uri)
    if conn is None:
        log_error("Failed to connect")
        exit(1)
    log_info("Libvirt connected to: " + settings.hypervisor_uri)
    return conn


def run_temporary_domain_from_xml_file(connection, filepath):
    """Runs temporary domain from xml file

    :param connection: connection object to hypervisor
    :param filepath: path to xml file with defined domain
    :return: domain object for success, None otherwise.

    """
    log_info("Running temporary domain from file: " + filepath)
    file = open(filepath, "r")
    xml = file.read()
    file.close()
    domain = connection.createXML(xml)
    if domain is None:
        log_error("Unable to create domain")
        return None
    log_info("New domain is running")
    return domain


def print_domains(connection, flags=0):
    """Prints list of virtual domains.

    :param connection: connection object to hypervisor
    :param flags: flag parameter for listing (0 for all domains) more: libvirt listAllDomains

    """
    domains = connection.listAllDomains(flags)
    if domains is None:
        log_fatal("Failed to get a list of domains")
    if len(domains) == 0:
        print("No domains found!")
    else:
        print("Domains:")
    for domain in domains:
        print("\t" + domain.name())


def create_domain_from_xml_file(connection, filepath):
    """Creates domain from xml file

    :param connection: connection object to hypervisor
    :param filepath: path to xml file with defined domain
    :return: domain object for success, None otherwise.

    """
    log_info("Creating new domain from file: " + filepath)
    file = open(filepath, "r")
    xml = file.read()
    file.close()
    domain = connection.defineXML(xml)
    if domain is None:
        log_error("Unable to create domain")
        return None
    log_info("New domain created")
    return domain


def run_domain(domain):
    """Run defined domain.

    :param domain: domain to run (e.g. created by defineXML)
    :return: 1 for success, -1 otherwise.

    """
    if domain.create(domain) < 0:
        log_error("Unable to boot new domain")
        return -1
    else:
        log_info("New domain is up and running!")
        return 1


def main():
    parse_arguments()
    connection = connect_hypervisor()
    test1(connection)
    connection.close()


def test1(connection):
    pools = connection.listAllStoragePools(0)
    if pools is None:
        log_fatal("Failed to locate any StoragePool objects.")
    for pool in pools:
        log_info("Pool: " + pool.name())
    print_domains(connection)
    domain = create_domain_from_xml_file(connection, "/home/thun/inzynierka/src/xml_domains/sample1.xml")
    run_domain(domain)
    print_domains(connection)


if __name__ == "__main__":
    main()
