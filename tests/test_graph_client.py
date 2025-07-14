import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.graph_client.graph_client import GraphClient


def test_client_initialization():
    client = GraphClient()
    assert hasattr(client, "get_unread_messages")
    assert hasattr(client, "move_message")
