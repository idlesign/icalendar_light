from collections import namedtuple, Iterable
from datetime import datetime, timedelta
from functools import partial
from pathlib import Path
from typing import Generator, Union

from dateutil.tz import tzlocal

from .casters import cast_date, cast_default, cast_recurrence


class Calendar:

    _key_map = {
        'UID': ('uid', None),
        'STATUS': ('status', None),  # CONFIRMED, TENTATIVE, CANCELLED
        'DTSTART': ('dt_start', cast_date),
        'DTEND': ('dt_end', cast_date),
        'DESCRIPTION': ('description', None),
        'SUMMARY': ('summary', None),
        'LOCATION': ('location', None),
        'RRULE': ('recurrence', cast_recurrence),
    }

    _event_attrs = [key for key, _ in _key_map.values()]
    Event = namedtuple('Event', _event_attrs)

    @classmethod
    def event_stringify(cls, event: Event) -> str:
        """Create a string representation for an event object.

        :param event:

        """
        location = event.location
        if location:
           location = f' [{location}]'

        status = event.status
        if status:
           status = f' [{status}]'

        out = f"{event.dt_start} - {event.dt_end} | {event.summary}{location or ''}{status or ''}"

        return out

    @classmethod
    def iter_events_from_file(
        cls,
        filepath: Union[Path, str],
        upcoming_days: int = None
    ) -> Generator[Event, None, None]:
        """Yields event objects from a given file.

        :param filepath:
        :param upcoming_days:

        """
        if upcoming_days is None:
            func = cls.iter_events

        else:
            func = partial(cls.iter_events_upcoming, days_forward=upcoming_days)

        with open(f'{filepath}') as f:
            yield from func(f)

    @classmethod
    def iter_events(cls, source: Iterable) -> Generator[Event, None, None]:
        """Yields event objects from a given source.

        .. note:: This won't yield recurrent events automatically, as `.iter_events_upcoming()` does.

        :param source:

        """
        def init_event_data():
            return {}.fromkeys(cls._event_attrs)

        event_data = init_event_data()
        in_event = False
        last_key = ''

        shared_params = {
            'tz': None,
        }

        cls_event = cls.Event
        key_map = cls._key_map

        for line in source:
            line = line.rstrip()

            if line == 'BEGIN:VEVENT':
                last_key = ''
                in_event = True
                event_data = init_event_data()
                continue

            if line == 'END:VEVENT':

                yield cls_event(**event_data)

                last_key = ''
                in_event = False
                continue

            if not in_event:

                if line.startswith('X-WR-TIMEZONE:'):
                    shared_params['tz'] = line.partition(':')[2]

                continue

            if line.startswith(' '):
                key = last_key
                value = line[1:]
                params = ''  # No params support for continuation.

            else:
                key, _, value = line.partition(':')
                key, _, params = key.partition(';')

            last_key = key
            mapped = key_map.get(key)

            if mapped is None:
                continue

            mapped_key, func_cast = mapped
            func_cast = func_cast or cast_default

            value = func_cast(value=value, params=params, shared=shared_params)

            value_seen = event_data[mapped_key]

            if value_seen is None:
                value_seen = value

            else:
                # Continuation (folding) support.
                value_seen = f"{value_seen}{value}"

            event_data[mapped_key] = value_seen

    @classmethod
    def iter_events_recurrent(cls, *, event: Event, date_max: datetime) -> Generator[Event, None, None]:
        """Builds and yields recurrent events for a given event till the date.

        :param event:
        :param date_max:

        """
        start = event.dt_start
        end = event.dt_end

        recurred = []

        for recurrent_start in event.recurrence:

            recurrent_start = recurrent_start.replace(
                hour=start.hour,
                minute=start.minute,
                second=start.second,
                tzinfo=start.tzinfo,
            )

            recurrent_end = recurrent_start.replace(
                hour=end.hour,
                minute=end.minute,
                second=end.second,
            )

            recurred.append((recurrent_start, recurrent_end))

            if recurrent_start >= date_max:
                break

        for recurrent_start, recurrent_end in recurred:
            yield event._replace(dt_start=recurrent_start, dt_end=recurrent_end)

    @classmethod
    def iter_events_upcoming(cls, source: Iterable, *, days_forward=30) -> Generator[Event, None, None]:
        """Yields upcoming event objects from a given source for nex N days.

        .. note:: This will yield recurrent events automatically, in contrast to `.iter_events()`.

        :param source:
        :param days_forward:

        """
        now = datetime.now(tzlocal())
        date_max = now + timedelta(days=days_forward)

        for event in cls.iter_events(source):

            if event.recurrence:
                yield from cls.iter_events_recurrent(event=event, date_max=date_max)

            elif now <= event.dt_start <= date_max:
                yield event
