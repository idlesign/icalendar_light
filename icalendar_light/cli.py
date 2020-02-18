#!/usr/bin/env python
import sys
import click
from icalendar_light import VERSION_STR
from icalendar_light.toolbox import Calendar


@click.group()
@click.version_option(version=VERSION_STR)
def entry_point():
    """icalendar_light command line utilities."""


@entry_point.command()
@click.argument('filepath', type=click.Path(dir_okay=False))
@click.option('--days', help='Number of days forward to show events', default=60)
def upcoming(filepath, days):
    """Shows upcoming events from a given calendar file."""

    for event in Calendar.iter_events_from_file(filepath, upcoming_days=days):
        click.secho(Calendar.event_stringify(event))


def main():
    entry_point(obj={})


if __name__ == '__main__':
    main()
