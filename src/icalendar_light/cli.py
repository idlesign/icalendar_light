import click
from icalendar_light import VERSION
from icalendar_light.toolbox import Calendar


@click.group()
@click.version_option(version=VERSION)
def entry_point():
    """icalendar_light command line utilities."""


@entry_point.command()
@click.argument('source')
@click.option('--days', help='Number of days forward to show events', default=60)
def upcoming(source, days):
    """Shows upcoming events from a given calendar file or URL."""

    if source.startswith(("http://", "https://")):
        events = Calendar.iter_events_from_url(source, upcoming_days=days)

    else:
        events = Calendar.iter_events_from_file(source, upcoming_days=days)

    for event in events:
        click.secho(Calendar.event_stringify(event))


def main():
    entry_point(obj={})


if __name__ == '__main__':
    main()
