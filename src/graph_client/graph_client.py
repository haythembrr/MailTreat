import os
from msal import ConfidentialClientApplication
import requests


class GraphClient:
    """Minimal Graph API client placeholder."""

    def __init__(self):
        tenant_id = os.getenv("TENANT_ID", "placeholder")
        client_id = os.getenv("CLIENT_ID", "placeholder")
        client_secret = os.getenv("CLIENT_SECRET", "placeholder")
        if "placeholder" in (tenant_id, client_id, client_secret):
            # Running in placeholder mode - do not attempt real auth
            self.client = None
        else:
            self.client = ConfidentialClientApplication(
                client_id=client_id,
                client_credential=client_secret,
                authority=f"https://login.microsoftonline.com/{tenant_id}",
            )
        self.scope = ["https://graph.microsoft.com/.default"]

    def _acquire_token(self) -> str:
        if self.client is None:
            return ""
        result = self.client.acquire_token_silent(self.scope, account=None)
        if not result:
            result = self.client.acquire_token_for_client(scopes=self.scope)
        return result.get("access_token", "")

    def get_unread_messages(self):
        if self.client is None:
            return []
        token = self._acquire_token()
        if not token:
            return []
        headers = {"Authorization": f"Bearer {token}"}
        url = (
            "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages?"
            "$filter=isRead eq false"
        )
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json().get("value", [])
