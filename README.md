# icalendar_light

<https://github.com/idlesign/icalendar_light>

[![release](https://img.shields.io/pypi/v/icalendar_light.svg)](https://pypi.python.org/pypi/icalendar_light)
[![lic](https://img.shields.io/pypi/l/icalendar_light.svg)](https://pypi.python.org/pypi/icalendar_light)
[![coverage](https://img.shields.io/coveralls/idlesign/icalendar_light/master.svg)](https://coveralls.io/r/idlesign/icalendar_light)

## Description

*Light and easy iCalendar event reader*

No fancy stuff, just iCalendar (`.ics`) events reading.

* Uses `namedtuple` for event representation;
* Features iterative event reading to be fast and minimize memory usage.

## API

```python
from icalendar_light.toolbox import Calendar

for event in Calendar.iter_events_from_file('my_calendar.ics'):
    print(Calendar.event_stringify(event))

# Or get events upcoming in next 5 days from iCalendar represented as lines:
lines = []  # Let's imagine this one is not empty %)
events = Calendar.iter_events_upcoming(lines, days_forward=5)
```

## CLI

Requires `click` package (can be installed with: `pip install icalendar_light[cli]`).

```shell
# Show upcoming event for next 90 days
$ icalendar_light upcoming my_calendar.ics --days 90
```
