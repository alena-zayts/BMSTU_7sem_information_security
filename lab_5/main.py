import rsa
import base64
import hashlib
# sha2 https://www.mytecbits.com/internet/python/sha-2-hash-code

public_key_file_name = 'public.pem'
# private_key_file_name = 'private.pem'
signature_file_name = "signature_real"
another_signature_file_name = 'signature_broken'


class DocumentSigner:
    def __init__(self, hash_func, enc_func, dec_func):
        self.hash_func = hash_func
        self.enc_func = enc_func
        self.dec_func = dec_func
        self.signed = False


    def signData(self, data, enc_key):
        # with open(priv_filename, "rb") as k:
        #     enc_key = k.read()
        # enc_key = rsa.PrivateKey.load_pkcs1(enc_key, format='PEM')

        data = data.encode(ENCODING)
        hashed_data = bytes(self.hash_func(data).encode(ENCODING))
        eSignature = self.enc_func(hashed_data, enc_key)
        self.signed = True

        return eSignature

    def checkSign(self, data, sign_filename, pub_filename):
        if not self.signed:
            raise ValueError("Document was not signed")

        with open(pub_filename, "rb") as k:
            dec_key = k.read()
        dec_key = rsa.PrivateKey.load_pkcs1(dec_key, format='PEM')
        with open(sign_filename, "rb") as f:
            sign = f.read()
        # print(symb)
        # print(dec_key)

        data = data.encode(ENCODING)
        hashed_data = bytes(self.hash_func(data).encode(ENCODING))

        hashed_data_according_to_signature = self.dec_func(sign, dec_key)
        return hashed_data == hashed_data_according_to_signature

        # try:
        #     hashed_data_according_to_signature = self.dec_func(symb, dec_key)
        #     return hashed_data == hashed_data_according_to_signature
        # except:
        #     return False



ENCODING = 'utf8'


data_filename = "text.txt"
data_filename = "img.jpeg"
with open(data_filename, 'rb') as f_in:
    messageBytes = f_in.read()
    message = base64.b64encode(messageBytes)
    message = message.decode(ENCODING)
    print(message)


documentSigner = DocumentSigner(hash_func=lambda data: hashlib.sha256(data).hexdigest(),
                                enc_func=rsa.encrypt, dec_func=rsa.decrypt)

E_secret, D_open = rsa.newkeys(1024)
with open(public_key_file_name, "wb") as pub:
    pub.write(D_open.save_pkcs1('PEM'))


signature = documentSigner.signData(message, E_secret)
# print(signature)
# print(D_open)
with open(signature_file_name, "wb") as f:
    f.write(signature)


correct = documentSigner.checkSign(message, signature_file_name, public_key_file_name)
print('Checking the same data and signature', correct)


another_message = message + 'abc'
correct = documentSigner.checkSign(another_message, signature_file_name, public_key_file_name)
print('Checking different data', correct)


another_signature = documentSigner.signData(another_message, E_secret)
with open(another_signature_file_name, "wb") as f:
    f.write(another_signature)
correct = documentSigner.checkSign(message, another_signature_file_name, public_key_file_name)
print('Checking different signature', correct)


