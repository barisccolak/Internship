from __future__ import annotations

from pathlib import Path

_encoding = "cp1252"  # default yaskawa file encoding


def _read_file_or_bytes(file_or_bytes: str | Path | bytes, normalize: bool = True):
    """Decode bytes into string contents or read contents from file.

    This function can read YASKAWA files form the following inputs:
    - filepath (as str or Path)
    - full string defined in Python
    - bytes
    """
    if isinstance(file_or_bytes, bytes):
        file_or_bytes = file_or_bytes.decode(_encoding)

    if not (isinstance(file_or_bytes, str) and ("\n" in file_or_bytes)):
        with open(file_or_bytes, encoding=_encoding) as f:
            file_or_bytes = f.read()

    if normalize:
        file_or_bytes = file_or_bytes.replace("\r\n", "\n").replace("\r", "\n")

    return file_or_bytes
