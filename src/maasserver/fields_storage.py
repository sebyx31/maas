# Copyright 2015 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Fields for storage API."""

from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    )

str = None

__metaclass__ = type
__all__ = [
    ]

from math import ceil
import re

from django import forms
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from maasserver.utils.converters import machine_readable_bytes


PRECENTAGE_REGEX = r"\d+(\.\d*)?%"
BYTES_REGEX = r"-?[0-9]+([KkMmGgTtPpEe]{1})?"


def is_precentage(value):
    """Return true if value is percentage."""
    if isinstance(value, (unicode, bytes)):
        return re.match(PRECENTAGE_REGEX, value) is not None
    else:
        return False


def calculate_size_from_precentage(size, precentage):
    """Convert precentage string into precentage of size."""
    multipler = float(precentage.strip("%")) / 100
    return int(ceil(size * multipler))


class BytesOrPrecentageField(forms.RegexField):
    """Validates and converts a byte value or a precentage."""

    def __init__(self, *args, **kwargs):
        self.min_value = kwargs.pop("min_value", None)
        self.max_value = kwargs.pop("max_value", None)
        regex = r"^(%s|%s)$" % (PRECENTAGE_REGEX, BYTES_REGEX)
        super(BytesOrPrecentageField, self).__init__(
            regex, *args, **kwargs)

    def to_python(self, value):
        if value is not None:
            # Make sure the value is a string not an integer.
            value = "%s" % value
        return value

    def clean(self, value):
        value = super(BytesOrPrecentageField, self).clean(value)
        if value is not None:
            # Exit early if this is precentage value.
            if is_precentage(value):
                return value
            else:
                value = machine_readable_bytes(value)

        # Run validation again, but with the min and max validators. This is
        # because the value has now been converted to an integer.
        self.validators = []
        if self.min_value is not None:
            self.validators.append(MinValueValidator(self.min_value))
        if self.max_value is not None:
            self.validators.append(MaxValueValidator(self.max_value))
        self.run_validators(value)
        return value
