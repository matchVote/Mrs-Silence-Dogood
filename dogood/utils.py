from datetime import datetime, timezone


def normalize_date(date):
    if date:
        current_date = datetime.now(timezone.utc)
        if date > current_date:
            date = current_date
    else:
        date = datetime.now(timezone.utc)
    return date
