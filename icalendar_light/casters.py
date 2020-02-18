from datetime import datetime
from typing import Any

from dateutil.parser import parse as parse_datestr
from dateutil.tz import gettz
from dateutil.utils import default_tzinfo
from dateutil.rrule import rrulestr


def cast_date(*, value: str, params: str, shared: dict) -> datetime:
    """Cast date/datetime string into object.

    :param value: Current value.
    :param params: Additional value-related parameters.
    :param shared: Global shared parameters.

    """
    param_key, _, param_val = params.partition('=')

    date = parse_datestr(value)
    tz = param_val if param_key == 'TZID' else shared['tz'] or 'UTC'

    return default_tzinfo(date, gettz(tz))


def cast_recurrence(*, value: str, params: str, shared: dict) -> Any:
    """Parses recurrence rule string.

    :param value: Current value.
    :param params: Additional value-related parameters.
    :param shared: Global shared parameters.

    """
    return rrulestr(value)


def cast_default(*, value: str, params: str, shared: dict) -> str:
    """Default caster, performing basic transformations.

    :param value: Current value.
    :param params: Additional value-related parameters.
    :param shared: Global shared parameters.

    """
    return value.replace(r'\,', ',')
