import pandas as pd
import numpy as np
from os import path


class UsersStructure:

    def __init__(self):
        self.filename = "Shcherbakova_lab1_data.csv"
        if not path.exists(self.filename):
            self._passwords_data = pd.DataFrame(data=[["ADMIN", "", 0, 0]],
                                                columns=["Username", "Password",
                                                         "Is blocked", "Password constraint"])
            self._passwords_data.set_index("Username", inplace=True)
            self.save()
        else:
            self._passwords_data = pd.read_csv(self.filename,
                                               index_col="Username")
            self._passwords_data.replace(np.nan, '', regex=True, inplace=True)

    def get_user_row(self, login):
        if not self._passwords_data.index.isin([login]).any():
            return None
        return self._passwords_data.loc[[login]]

    def add_user(self, login):
        self._passwords_data.loc[login] = pd.Series(["", 0, 0])
        self.save()

    def block_user(self, login):
        self._passwords_data.loc[login, "Is blocked"] = 1
        self.save()

    def constraints_exist(self, login):
        return self._passwords_data.loc[login]["Password constraint"] == 1

    def change_constraint_to_user(self, login):
        if self.constraints_exist(login):
            self.remove_constraint_from_user(login)
        else:
            self.add_constraint_to_user(login)

    def add_constraint_to_user(self, login):
        self._passwords_data.loc[login, "Password constraint"] = 1
        self.save()

    def remove_constraint_from_user(self, login):
        self._passwords_data.loc[login, "Password constraint"] = 0
        self.save()

    def change_password(self, login, new_password):
        self._passwords_data.loc[login, "Password"] = new_password
        self.save()

    def save(self):
        self._passwords_data.to_csv(self.filename)

    def get_all_users(self):
        data_copy = self._passwords_data.copy()
        data_copy.drop("Password", axis=1, inplace=True)
        data_copy["Is blocked"] = np.where(data_copy["Is blocked"] == 1, "Blocked", "Not blocked")
        data_copy["Password constraint"] = np.where(data_copy["Password constraint"] == 1, "On", "Off")
        return data_copy
