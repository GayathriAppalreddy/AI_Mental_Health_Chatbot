import os
import csv
from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(hash: str, password: str) -> bool:
    return check_password_hash(hash, password)


def append_to_csv(path: str, row: list, header: list = None):
    """Append a row to a csv file; add header if the file is new or empty."""
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    write_header = False
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        write_header = True
    with open(path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header and header:
            writer.writerow(header)
        writer.writerow(row)
