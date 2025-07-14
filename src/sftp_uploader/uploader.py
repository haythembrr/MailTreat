"""Placeholder SFTP uploader."""
import os
import paramiko


def upload_file(local_path, remote_path=None):
    host = os.getenv("SFTP_HOST", "localhost")
    user = os.getenv("SFTP_USER", "user")
    password = os.getenv("SFTP_PASSWORD", "pass")
    remote_path = remote_path or os.path.basename(local_path)

    transport = paramiko.Transport((host, 22))
    transport.connect(username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        sftp.put(local_path, remote_path)
    finally:
        sftp.close()
        transport.close()
