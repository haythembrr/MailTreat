from airflow.decorators import dag, task
from datetime import datetime, timedelta

from src.graph_client.graph_client import GraphClient
from src.email_parser.parser import parse_email
from src.transform.to_doaat import to_doaat
from src.sftp_uploader.uploader import upload_file
from src.notification.mailer import send_notification
from src.common.logging import configure_logging

configure_logging()


default_args = {"retries": 1, "retry_delay": timedelta(minutes=1)}


@dag(
    schedule_interval="*/5 * * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
)
def process_mailbox():
    @task
    def fetch_emails():
        client = GraphClient()
        return client.get_unread_messages()

    @task
    def parse_and_transform(messages):
        paths = []
        for message in messages:
            parsed = parse_email(message)
            paths.append(to_doaat(parsed))
        return paths

    @task
    def upload(paths):
        for path in paths:
            upload_file(path)

    @task(trigger_rule="all_done")
    def notify(context=None):
        send_notification(context)

    msgs = fetch_emails()
    files = parse_and_transform(msgs)
    upload(files)
    notify()


dag = process_mailbox()
