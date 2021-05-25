from cryptography.fernet import Fernet

from app.utils.enum import EnumUtils

class FernetCipher(object):
    def __init__(self, key = EnumUtils.key.value.encode()): 
        self.key = key
        self.obj = Fernet(self.key)

    def encrypt(self, raw):
        cipher = self.obj.encrypt(raw.encode())
        return cipher

    def decrypt(self, enc):
        decrypt = self.obj.decrypt(enc)
        return decrypt