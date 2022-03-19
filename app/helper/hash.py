import sha3

class Hash:
    def hash_data(self, data):
        k = sha3.keccak_256()
        k.update(data)
        return k.hexdigest()
