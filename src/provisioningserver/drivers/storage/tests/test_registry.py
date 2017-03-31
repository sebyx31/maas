# Copyright 2017 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Tests for `provisioningserver.drivers.storage.registry`."""

__all__ = []

from unittest.mock import sentinel

from maastesting.testcase import MAASTestCase
from provisioningserver.drivers.storage.registry import StorageDriverRegistry
from provisioningserver.drivers.storage.tests.test_base import (
    make_storage_driver,
)
from provisioningserver.utils.testing import RegistryFixture


class TestStorageDriverRegistry(MAASTestCase):

    def setUp(self):
        super(TestStorageDriverRegistry, self).setUp()
        # Ensure the global registry is empty for each test run.
        self.useFixture(RegistryFixture())

    def test_registry(self):
        self.assertItemsEqual([], StorageDriverRegistry)
        StorageDriverRegistry.register_item("driver", sentinel.driver)
        self.assertIn(
            sentinel.driver,
            (item for name, item in StorageDriverRegistry))

    def test_get_schema(self):
        fake_driver_one = make_storage_driver()
        fake_driver_two = make_storage_driver()
        StorageDriverRegistry.register_item(
            fake_driver_one.name, fake_driver_one)
        StorageDriverRegistry.register_item(
            fake_driver_two.name, fake_driver_two)
        self.assertItemsEqual([
            {
                'name': fake_driver_one.name,
                'description': fake_driver_one.description,
                'fields': [],
                'missing_packages': fake_driver_one.detect_missing_packages(),
            },
            {
                'name': fake_driver_two.name,
                'description': fake_driver_two.description,
                'fields': [],
                'missing_packages': fake_driver_two.detect_missing_packages(),
            }],
            StorageDriverRegistry.get_schema())