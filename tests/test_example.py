#!/usr/bin/env pytest

import pytest


def test_success():
    assert 1 + 1 == 2


def test_error():
    with pytest.raises(ZeroDivisionError):
        assert 1 / 0
