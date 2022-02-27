import hashlib


class Hash:
    def hash_data(self, data):
        s = hashlib.sha3_256()
        s.update(data)
        return s.hexdigest()
