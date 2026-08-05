from app.core.hashing import hash_payload
def test_hash(): assert len(hash_payload({'a':1}))==64
