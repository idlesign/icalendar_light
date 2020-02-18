from itertools import islice
from pathlib import Path

import pytest
from freezegun import freeze_time

from icalendar_light.toolbox import Calendar


@pytest.fixture
def dir_fixtures(request):
    return Path(request.module.__file__).absolute().parent / 'fixtures'


def test_basic(dir_fixtures):

    def events_to_lines(events):
        events = sorted(islice(events, 10), key=lambda event: event.dt_start)
        lines = list(map(Calendar.event_stringify, events))
        return lines

    with freeze_time('2020-02-18T20:10'):

        lines = events_to_lines(Calendar.iter_events_from_file(dir_fixtures / 'cut.ics'))

        assert lines == [
            '2019-12-10 00:00:00+00:00 - 2019-12-12 00:00:00+00:00 | PyCon Tanzania [Dar Es Salaam, Tanzania] [CONFIRMED]',
            '2020-02-20 00:00:00+00:00 - 2020-02-23 00:00:00+00:00 | Open Source Festival [Lagos, Nigeria] [CONFIRMED]',
            '2020-03-27 00:00:00+00:00 - 2020-03-28 00:00:00+00:00 | MoscowPythonConf++ [Moscow, Russia] [CONFIRMED]',
            '2020-04-18 00:00:00+00:00 - 2020-04-20 00:00:00+00:00 | DragonPy 2020 [Ljubljana, Slovenia] [CONFIRMED]',
            '2020-05-04 00:00:00+00:00 - 2020-05-07 00:00:00+00:00 | PyCon Israel 2020 [Ramat Gan, Israel] [CONFIRMED]',
            '2020-05-09 00:00:00+00:00 - 2020-05-11 00:00:00+00:00 | PyConWeb 2020 [Munich, Germany] [CONFIRMED]',
            '2020-05-25 00:00:00+00:00 - 2020-05-27 00:00:00+00:00 | enterPy [Mannheim, Germany] [CONFIRMED]',
            '2020-06-05 00:00:00+00:00 - 2020-06-08 00:00:00+00:00 | PyLondinium 2020 [London, UK] [CONFIRMED]',
            '2020-08-28 00:00:00+00:00 - 2020-08-30 00:00:00+00:00 | PyCon JP 2020 [Tokyo, Japan] [CONFIRMED]',
            '2020-09-19 00:00:00+00:00 - 2020-09-21 00:00:00+00:00 | PyCon APAC 2020 [Kota Kinabalu, Sabah, Malaysia] [CONFIRMED]',
        ]

        lines = events_to_lines(Calendar.iter_events_from_file(dir_fixtures / 'cut.ics', upcoming_days=5))

        assert lines == [
            '2020-02-19 09:00:00+03:00 - 2020-02-19 12:00:00+03:00 | PiterPy Breakfast [Saint Petersburg, St Petersburg, Russia] [CONFIRMED]',
            '2020-02-20 00:00:00+00:00 - 2020-02-23 00:00:00+00:00 | Open Source Festival [Lagos, Nigeria] [CONFIRMED]',
            '2020-02-21 00:00:00+00:00 - 2020-02-23 00:00:00+00:00 | PyCon Belarus 2020 [Minsk, Belarus] [CONFIRMED]',
            '2020-03-04 09:00:00+03:00 - 2020-03-04 12:00:00+03:00 | PiterPy Breakfast [Saint Petersburg, St Petersburg, Russia] [CONFIRMED]'
        ]

        assert list(Calendar.iter_events_upcoming([], days_forward=5)) == []
