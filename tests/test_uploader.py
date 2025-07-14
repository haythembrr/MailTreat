import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.sftp_uploader.uploader import upload_file


def test_upload_signature():
    assert callable(upload_file)
