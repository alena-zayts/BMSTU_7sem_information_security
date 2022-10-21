import rsa
import hashlib


class DocumentSigner:
    def __init__(self, hash_func, enc_func, dec_func):
        self.hash_func = hash_func
        self.enc_func = enc_func
        self.dec_func = dec_func
        self.signed = False

    def signData(self, data, enc_key):
        data = data.encode(ENCODING)
        hashed_data = self.hash_func(data)
        hashed_data = hashed_data.encode(ENCODING)
        hashed_data = bytes(hashed_data)
        eSignature = self.enc_func(hashed_data, enc_key)
        self.signed = True
        return eSignature

    def checkSign(self, data, sign, dec_key):
        if not self.signed:
            raise ValueError("Document was not signed")
        data = data.encode(ENCODING)
        hashed_data = self.hash_func(data)
        hashed_data = hashed_data.encode(ENCODING)
        hashed_data = bytes(hashed_data)
        hashed_data_according_to_sign = self.dec_func(sign, dec_key)
        return hashed_data == hashed_data_according_to_sign




ENCODING = 'utf8'
message = "hello"
documentSigner = DocumentSigner(hash_func=lambda data: hashlib.sha256(data).hexdigest(),
                                enc_func=rsa.encrypt, dec_func=rsa.decrypt)

E_secret, D_open = rsa.newkeys(1024)
signature = documentSigner.signData(message, E_secret)


correct = documentSigner.checkSign(message, signature, D_open)
print(correct)


another_message = message + 'abc'
correct = documentSigner.checkSign(another_message, signature, D_open)
print(correct)


another_signature = signature[:-1] + b'a'
correct = documentSigner.checkSign(message, another_signature, D_open)
print(correct)


