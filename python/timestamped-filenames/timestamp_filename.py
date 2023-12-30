import os
from datetime import datetime, timezone
from pathlib import Path


def get_now(fmt: str = "%Y%m%dT%H%M%S") -> str:
    return datetime.now(timezone.utc).strftime(fmt)


def append_timestamp(file: str) -> str:
    # Probably not the best way to do this
    timestamp = get_now()
    if "/" in file:
        path, filename = file.rsplit("/", 1)
        return f"{path}/{timestamp}_{filename}"
    return f"{timestamp}_{file}"


def append_timestamp_os(file: str) -> str:
    # Do it with os
    timestamp = get_now()
    path, filename = os.path.split(file)
    return os.path.join(path, f"{timestamp}_{filename}")


def append_timestamp_pathlib(file: str) -> str:
    # Do it with pathlib
    timestamp = get_now()
    path = Path(file)
    return path.parent / f"{timestamp}_{path.name}"


# Test
print("No lib: ", append_timestamp("some/path/to/test.csv"))
print("Pathlib: ", append_timestamp_pathlib("some/path/to/test.csv"))
print("os: ", append_timestamp_os("some/path/to/test.csv"))
