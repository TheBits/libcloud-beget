import functools
import os
from collections import namedtuple
from pathlib import Path
from typing import Tuple

import pytest
import vcr
from libcloud.common.types import InvalidCredsError

from libcloudbeget import BegetDNSDriver


@pytest.fixture()
def credentials() -> Tuple[str, str]:
    Creds = namedtuple("Creds", ("user_id", "key"))

    user_id = os.getenv("DRIVER_USER_ID")
    if user_id is None:
        pytest.exit("set up DRIVER_USER_ID environment variable")

    key = os.getenv("DRIVER_PASSWORD")
    if key is None:
        pytest.exit("set up DRIVER_PASSWORD environment variable")

    creds = Creds(user_id, key)

    return creds


def filter_response(response):
    try:
        del response["headers"]["Set-Cookie"]
    except KeyError:
        pass
    return response


def vcr_record(f):
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        path = Path("./tests/fixtures/") / f"{f.__name__}.yaml"
        kwargs = dict(
            filter_query_parameters=("login", "passwd"),
            decode_compressed_response=True,
            match_on=["method", "path"],
            path=str(path),
        )
        if not path.exists():
            kwargs["before_record_response"] = filter_response
        with vcr.use_cassette(**kwargs):
            return f(*args, **kwds)

    return wrapper


@vcr_record
def test_dns_list_zones(credentials):
    beget = BegetDNSDriver(credentials.user_id, credentials.key)
    zones = beget.iterate_zones()
    assert not zones


@vcr_record
def test_logon_invalid_creds():
    beget = BegetDNSDriver(key="123", user_id="abc")
    with pytest.raises(InvalidCredsError):
        beget.iterate_zones()


@vcr_record
def test_dns_iterate_zones(credentials):
    beget = BegetDNSDriver(credentials.user_id, credentials.key)
    zones = beget.iterate_zones()
    assert not zones
