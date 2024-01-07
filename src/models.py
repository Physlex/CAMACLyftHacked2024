import json
import os
from pathlib import Path

class User():
    def __init__(self, userID) -> None:
        self.userID = userID
        self.filename = Path('static/data/user' + str(userID) + '.json')

    def upload(self, data) -> None:
        """
            Access JSON and insert new data into existing data stream
        """
        with open(self.filename) as file:
            # Mutate the data
            array = json.load(file)
            new_data = array["stream"]
            for element in data:
                new_data.append(element)

            # Upload the data to the json
            array["stream"] = new_data
            json_enc = json.dumps(array, indent = 2)
            with open(self.filename, "w+") as file:
                file.write(json_enc)

    def download(self) -> None:
        """
            Access JSON and return stream data
        """
        data = []
        with open(self.filename) as file:
            array = json.load(file)
            data = array["stream"]

        return data

    def createUser(self) -> None:
        """
        Create a JSON file holding a user and null data in data stream
        """    
        data = {
            "user": self.userID,
            "stream": []
        }

        json_enc = json.dumps(data, indent = 2)
        with open(self.filename, "w+") as file:
            file.write(json_enc)

    def deleteUser(self) -> None:
        """
        Delete a JSON file w/ associated user ID
        """
        os.remove(self.filename)
