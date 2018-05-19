# coding=utf-8
import base64
from random import choice
from string import letters

try:
    from Crypto import Random
    from Crypto.Cipher import AES
except ImportError:
    import crypto
    import sys

    sys.modules['Crypto'] = crypto
    from crypto.Cipher import AES
    from crypto import Random


class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = key

    def encrypt(self, raw):
        _raw = raw
        raw = self._pad(raw)

        print "block size: ", AES.block_size
        print raw, ';'
        print _raw, ';'

        iv = "".join([choice(letters[:26]) for i in xrange(16)])
        print " iv :", iv
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        a = (self.bs - len(s) % self.bs)
        b = chr(self.bs - len(s) % self.bs)
        return s + a * b

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
def encrypt(k, t):
    o = AESCipher(k)
    return o.encrypt(t)


def decrypt(k, t):
    o = AESCipher(k)
    return o.decrypt(t)


def main():
    k = "qwertyuiopasdfghjklzxcvbnmqwerty"
    s1 = "Hello World!"

    d2 = encrypt(k, s1)

    print " Password :", k
    print "Encrypted :", d2
    print "    Plain :", decrypt(k, d2)

if __name__ == '__main__':
    main()