# Copyright 2012, 2013 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Test server-address-guessing logic."""

from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    )

str = None

__metaclass__ = type
__all__ = []

import random
from socket import gethostname

from maastesting.factory import factory
from maastesting.testcase import MAASTestCase
from metadataserver import address
from testtools.matchers import MatchesRegex


def parse_locale_lines(output):
    """Parse lines of output from /bin/locale into a dict."""
    return {
        key: value.strip('"')
        for key, value in [line.split('=') for line in output]}


class TestAddress(MAASTestCase):

    def test_get_command_output_executes_command(self):
        self.assertEqual(
            ["Hello"], address.get_command_output('echo', 'Hello'))

    def test_get_command_output_does_not_expand_arguments(self):
        self.assertEqual(["$*"], address.get_command_output('echo', '$*'))

    def test_get_command_output_returns_sequence_of_lines(self):
        self.assertEqual(
            ['1', '2'], address.get_command_output('echo', '1\n2'))

    def test_get_command_output_uses_C_locale(self):
        locale = parse_locale_lines(address.get_command_output('locale'))
        self.assertEqual('C', locale['LC_CTYPE'])
        self.assertEqual('C', locale['LC_MESSAGES'])
        self.assertEqual('en_US.UTF-8', locale['LANG'])

    def test_find_default_interface_finds_default_interface(self):
        sample_ip_route = [
            "default via 10.0.0.1 dev eth1  proto static",
            "169.254.0.0/16 dev eth2  scope link  metric 1000",
            "10.0.0.0/24 dev eth0  proto kernel  scope link  src 10.0.0.11  "
            "metric 2",
            "10.1.0.0/24 dev virbr0  proto kernel  scope link  src 10.1.0.1",
            "10.1.1.0/24 dev virbr1  proto kernel  scope link  src 10.1.1.1",
            ]
        self.assertEqual(
            'eth1', address.find_default_interface(sample_ip_route))

    def test_find_default_interface_makes_a_guess_if_no_default(self):
        sample_ip_route = [
            "10.0.0.0/24 dev eth2  proto kernel  scope link  src 10.0.0.11  "
            "metric 2",
            "10.1.0.0/24 dev virbr0  proto kernel  scope link  src 10.1.0.1",
            "10.1.1.0/24 dev virbr1  proto kernel  scope link  src 10.1.1.1",
            ]
        self.assertEqual(
            'eth2', address.find_default_interface(sample_ip_route))

    def test_find_default_interface_returns_None_on_failure(self):
        self.assertIsNone(address.find_default_interface([]))

    def test_get_ip_address_finds_IP_address_of_interface(self):
        self.assertEqual('127.0.0.1', address.get_ip_address(b'lo'))

    def test_get_ip_address_prefers_v4_addresses_to_v6(self):
        addresses = [factory.get_random_ipv6_address() for i in range(3)]
        # We add a deliberately low v6 address to show that the v4
        # address is always preferred.
        ipv6_address = "::1"
        ipv4_address = factory.getRandomIPAddress()
        addresses.append(ipv6_address)
        addresses.append(ipv4_address)
        self.patch(
            address, 'get_all_addresses_for_interface').return_value = (
            addresses)
        self.assertEqual(ipv4_address, address.get_ip_address(b'lo'))

    def test_get_ip_address_returns_v6_address_if_no_v4_available(self):
        ipv6_address = factory.get_random_ipv6_address()
        self.patch(
            address, 'get_all_addresses_for_interface').return_value = (
            [ipv6_address])
        self.assertEqual(ipv6_address, address.get_ip_address(b'lo'))

    def test_get_ip_address_returns_consistent_result_from_address_set(self):
        addresses = [factory.get_random_ipv6_address() for i in range(5)]
        expected_address = sorted(addresses)[0]
        for _ in range(5):
            random.shuffle(addresses)
            self.patch(
                address, 'get_all_addresses_for_interface').return_value = (
                addresses)
            self.assertEqual(
                expected_address, address.get_ip_address(b'lo'))

    def test_get_ip_address_returns_None_on_failure(self):
        self.assertIsNone(address.get_ip_address(b'ethturboveyronsuper9'))

    def test_guess_server_address_finds_IP_address(self):
        self.assertThat(
            address.guess_server_address(),
            MatchesRegex("^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$"))

    def test_guess_server_address_returns_hostname_as_last_ditch_guess(self):
        def return_empty_list(*args):
            return []

        self.patch(address, 'get_command_output', return_empty_list)
        self.assertEqual(gethostname(), address.guess_server_address())
