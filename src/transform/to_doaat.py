"""Placeholder transformation to DOAAT format."""
import os
from pathlib import Path


def to_doaat(parsed_email, output_dir="/tmp"):
    """Write parsed email to a text file. Return path to created file."""
    filename = f"{parsed_email['id']}.txt"
    path = Path(output_dir) / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(parsed_email.get("subject", ""))
        f.write("\n")
        f.write(parsed_email.get("body", ""))
    return str(path)
