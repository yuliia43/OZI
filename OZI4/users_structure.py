import pandas as pd
import numpy as np
from os import path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from Cryptodome.Hash import MD4


class UsersStructure:

    def __init__(self):
        self.filename = "Shcherbakova_lab3_data.csv"
        if not path.exists(self.filename):
            password = encode_password("")
            self._passwords_data = pd.DataFrame(data=[["ADMIN", password, 0, 0]],
                                                columns=["Username", "Password",
                                                         "Is blocked", "Password constraint"])
            self._passwords_data.set_index("Username", inplace=True)
        else:
            self._passwords_data = pd.read_csv(self.filename,
                                               index_col="Username")
            self.set_cipher()
            decryptor = self.cipher.decryptor()
            for login in self._passwords_data.index:
                if login != "ADMIN":
                    password = self._passwords_data.loc[login, "Password"]
                    password = decryptor.update(password.encode('cp855'))
                    self._passwords_data.loc[login, "Password"] = password.decode()

    def get_user_row(self, login):
        if not self._passwords_data.index.isin([login]).any():
            return None
        return self._passwords_data.loc[[login]]

    def add_user(self, login):
        password = encode_password("")
        row = pd.Series([password, 0, 0], index=self._passwords_data.iloc[0].index, name=login)
        self._passwords_data = self._passwords_data.append(row)

    def block_user(self, login):
        self._passwords_data.loc[login, "Is blocked"] = 1

    def constraints_exist(self, login):
        return self._passwords_data.loc[login]["Password constraint"] == 1

    def change_constraint_to_user(self, login):
        if self.constraints_exist(login):
            self.remove_constraint_from_user(login)
        else:
            self.add_constraint_to_user(login)

    def add_constraint_to_user(self, login):
        self._passwords_data.loc[login, "Password constraint"] = 1

    def remove_constraint_from_user(self, login):
        self._passwords_data.loc[login, "Password constraint"] = 0

    def change_password(self, login, new_password):
        password = encode_password(new_password)
        self._passwords_data.loc[login, "Password"] = password

    def save(self):
        self.set_cipher()
        encryptor = self.cipher.encryptor()
        for login in self._passwords_data.index:
            if login != "ADMIN":
                password = self._passwords_data.loc[login, "Password"]
                encoded_password = encryptor.update(password.encode("utf-8"))
                self._passwords_data.loc[login, "Password"] = encoded_password.decode('cp855')
        self._passwords_data.to_csv(self.filename)

    def set_cipher(self):
        admin_password = self._passwords_data.loc["ADMIN", "Password"]
        admin_password += '0' * (len(admin_password) % 16)
        key = admin_password.encode()
        self.cipher = Cipher(algorithms.AES(key), modes.ECB())

    def get_all_users(self):
        data_copy = self._passwords_data.copy()
        data_copy.drop("Password", axis=1, inplace=True)
        data_copy["Is blocked"] = np.where(data_copy["Is blocked"] == 1, "Blocked", "Not blocked")
        data_copy["Password constraint"] = np.where(data_copy["Password constraint"] == 1, "On", "Off")
        return data_copy


def check_password(user_row, password):
    if (user_row["Is blocked"] == 0).any():
        encoded_password = encode_password(password)
        return (user_row["Password"] == encoded_password).any()
    else:
        return None


def encode_password(password):
    return MD4.new(password.encode("utf-8")).hexdigest()