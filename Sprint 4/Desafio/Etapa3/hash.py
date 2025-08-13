import hashlib

while True:
    texto = input("Digite uma palavra para ser transformada em hash: ")
    hash = hashlib.sha1((texto).encode('utf-8'))
    sha1 = hash.hexdigest()
    print("Hash SHA-1:", sha1)
