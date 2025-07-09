"""Placeholder parser for email messages."""


def parse_email(message):
    """Parse a Graph API message object and return a dict structure."""
    return {
        "id": message.get("id"),
        "subject": message.get("subject"),
        "body": message.get("body", {}).get("content", ""),
    }
