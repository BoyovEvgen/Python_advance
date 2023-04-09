import hashlib


def get_hash(file):
    hasher = hashlib.md5()
    while True:
        chunk = file.read(8192)
        if not chunk:
            break
        hasher.update(chunk)
    file.seek(0)
    return hasher.hexdigest()

