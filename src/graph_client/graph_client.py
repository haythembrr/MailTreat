import os
import logging
from typing import Any, Dict, List

from msal import ConfidentialClientApplication
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


logger = logging.getLogger(__name__)


class GraphClient:
    """Small helper client for Microsoft Graph."""

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
        self._session = self._build_session()

    def _build_session(self) -> requests.Session:
        session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def _acquire_token(self) -> str:
        if self.client is None:
            return ""
        result = self.client.acquire_token_silent(self.scope, account=None)
        if not result:
            result = self.client.acquire_token_for_client(scopes=self.scope)
        return result.get("access_token", "")

    def get_unread_messages(self, folder_id: str = "inbox") -> List[Dict[str, Any]]:
        if self.client is None:
            return []
        token = self._acquire_token()
        if not token:
            logger.warning("Token acquisition failed")
            return []
        headers = {"Authorization": f"Bearer {token}"}
        url = (
            f"https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}/messages?"
            "$filter=isRead eq false&$expand=attachments"
        )

        messages: List[Dict[str, Any]] = []
        while url:
            resp = self._session.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            messages.extend(data.get("value", []))
            url = data.get("@odata.nextLink")
        return messages

    def move_message(self, message_id: str, destination_folder_id: str) -> None:
        """Move a message to another folder to avoid reprocessing."""
        if self.client is None:
            return
        token = self._acquire_token()
        if not token:
            logger.warning("Token acquisition failed for move_message")
            return
        url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/move"
        payload = {"destinationId": destination_folder_id}
        headers = {"Authorization": f"Bearer {token}"}
        resp = self._session.post(url, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
