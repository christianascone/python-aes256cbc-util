import sys
import base64
from Crypto.Cipher import AES


class AESCipher(object):
    def __init__(self, key):
        self.bs = 32

    def encrypt(self, raw, iv):
        raw = self._pad(raw)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(raw)
        encoded = base64.b64encode(iv.encode() + encrypted)
        return str(encoded, 'utf-8')

    def decrypt(self, raw):
        decoded = base64.b64decode(raw)
        iv = decoded[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(decoded[AES.block_size:])
        return str(self._unpad(decrypted), 'utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]


if __name__ == '__main__':
    key = 'qwertyuiopasdfghjklzxcvbnmqwerty'
    iv = "ksalksaksadksald"
    cipher = AESCipher(key)

    plaintext = '542#1504891440039'
    encrypted = cipher.encrypt(plaintext, iv)
    print('Encrypted: %s' % encrypted)
    ciphertext = 'a3NhbGtzYWtzYWRrc2FsZDaMIPDC+Vev8jlgL0HXHGn6iPSJEkNu+fIgQtC0W2yT'
    assert encrypted == ciphertext

    decrypted = cipher.decrypt(encrypted)
    print('Decrypted: %s' % decrypted)
    assert decrypted == plaintext