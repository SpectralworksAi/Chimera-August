import hashlib,json
def hash_payload(data):
    return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
