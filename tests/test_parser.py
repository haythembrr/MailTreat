import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.email_parser import parser


def test_parse_email_basic():
    message = {
        "id": "1",
        "subject": "Test",
        "body": {"content": "Hello"},
        "from": {"emailAddress": {"address": "sender@example.com"}},
        "toRecipients": [{"emailAddress": {"address": "to@example.com"}}],
        "ccRecipients": [],
        "attachments": [
            {
                "id": "att1",
                "name": "file.txt",
                "contentType": "text/plain",
                "size": 10,
            }
        ],
    }
    parsed = parser.parse_email(message)
    assert parsed["id"] == "1"
    assert parsed["attachments"][0]["name"] == "file.txt"
