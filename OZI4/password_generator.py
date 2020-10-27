import random
import string
from Cryptodome.Hash import MD4


def generate_password():
    characters = string.printable
    characters = characters[:-5]
    password_length = int(5 + 10 * random.random())
    password = ''.join(random.choice(characters) for _ in range(password_length))
    print("Generated password:", password)
    hashed = MD4.new(password.encode("utf-8")).hexdigest()
    print("Hashed password:", hashed, '\n')
    return hashed


if __name__ == '__main__':
    for _ in range(40):
        generate_password()
