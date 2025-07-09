"""Placeholder config utilities."""


def get_setting(name, default=None):
    import os

    return os.getenv(name, default)
