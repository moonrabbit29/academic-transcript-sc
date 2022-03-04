import hashlib


class Hash:
    def hash_data(self, data):
        s = hashlib.sha3_256()
        s.update(data)
        return s.hexdigest()

# #if want to use keccak256 instead
# import sha3

# class Hash:
#     def hash_data(self, data):
#         k = sha3.keccak_256()
#         k.update(data)
#         return k.hexdigest()
