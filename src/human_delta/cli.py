"""human‑delta – a tiny CLI for human‑readable time diffs.

Author: TopherBot <topherbot@proton.me>
License: MIT
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from typing import Iterable, List

import click
from dateutil import parser as date_parser


def _now_utc() -> datetime:
    """Return the current UTC time with tzinfo attached."""
    return datetime.now(timezone.utc)


def _parse_timestamp(value: str) -> datetime:
    """Parse *value* into a timezone‑aware ``datetime``.

    Accepts:
    - ISO‑8601 strings (e.g. ``2024-01-01T12:00:00Z``)
    - Unix timestamps (seconds since epoch)
    - Anything ``dateutil.parser`` can handle.
    """
    # Try Unix timestamp first (int/float string)
    try:
        ts = float(value)
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    except ValueError:
        pass

    # Fallback to dateutil parser – force UTC if no tz supplied
    dt = date_parser.parse(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


UNITS: List[tuple[int, str, str]] = [
    (60, "second", "seconds"),
    (60, "minute", "minutes"),
    (24, "hour", "hours"),
    (7, "day", "days"),
    (4, "week", "weeks"),
    (12, "month", "months"),
    (float("inf"), "year", "years"),
]


def _humanize_delta(delta_seconds: float) -> str:
    """Convert a raw *delta_seconds* into a friendly phrase.

    Positive values indicate a future date ("in X …"), negative values the past
    ("X … ago").
    """
    past = delta_seconds < 0
    secs = abs(int(delta_seconds))
    for factor, singular, plural in UNITS:
        if secs < factor:
            unit = singular if secs == 1 else plural
            break
        secs //= int(factor)
    else:
        unit = "year"
    phrase = f"{secs} {unit}"
    return f"{phrase} ago" if past else f"in {phrase}"


@click.command()
@click.argument("date1", type=str)
@click.argument("date2", required=False, type=str)
def main(date1: str, date2: str | None = None) -> None:
    """Print a human‑readable difference between *date1* and *date2*.

    If *date2* is omitted, the current time is used.
    """
    try:
        dt1 = _parse_timestamp(date1)
        dt2 = _parse_timestamp(date2) if date2 else _now_utc()
    except Exception as exc:  # pragma: no cover – defensive
        click.echo(f"Error parsing dates: {exc}", err=True)
        sys.exit(1)

    delta = (dt2 - dt1).total_seconds()
    click.echo(_humanize_delta(delta))


if __name__ == "__main__":
    main()
