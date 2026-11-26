"""Verify a locally staged wrapper against an independently trusted digest."""
import hashlib
import hmac
import re
from pathlib import Path


def verify_wrapper(path, expected_sha256):
    if not isinstance(expected_sha256, str) or not re.fullmatch(r'[0-9a-fA-F]{64}', expected_sha256):
        raise ValueError('A trusted SHA-256 digest is required')
    path = Path(path)
    if not path.is_file() or path.is_symlink():
        raise ValueError('Regular wrapper file required')
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return hmac.compare_digest(digest.hexdigest(), expected_sha256.lower())
