"""Utilities to parse Microsoft Graph email messages."""

from __future__ import annotations

from typing import Any, Dict, List


def _extract_addresses(entries: List[Dict[str, Any]]) -> List[str]:
    """Return a list of email addresses from recipient entries."""
    addresses = []
    for entry in entries or []:
        email = entry.get("emailAddress", {}).get("address")
        if email:
            addresses.append(email)
    return addresses


def parse_email(message: Dict[str, Any]) -> Dict[str, Any]:
    """Parse a Graph API message object, including metadata and attachments."""

    attachments = []
    for att in message.get("attachments", []):
        attachments.append(
            {
                "id": att.get("id"),
                "name": att.get("name"),
                "contentType": att.get("contentType"),
                "size": att.get("size"),
                # contentBytes can be large; include if present
                "contentBytes": att.get("contentBytes"),
            }
        )

    parsed = {
        "id": message.get("id"),
        "conversationId": message.get("conversationId"),
        "subject": message.get("subject"),
        "receivedDateTime": message.get("receivedDateTime"),
        "from": message.get("from", {}).get("emailAddress", {}).get("address"),
        "to": _extract_addresses(message.get("toRecipients")),
        "cc": _extract_addresses(message.get("ccRecipients")),
        "body": message.get("body", {}).get("content", ""),
        "attachments": attachments,
        "internetMessageId": message.get("internetMessageId"),
    }

    return parsed
