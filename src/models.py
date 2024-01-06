import json

class User():
    def __init__(self, userID) -> None:
        self.userID = userID
    
    
    def download(self, userID, data) -> None:
        """
        Access JSON and insert new data into existing data stream
        
        """
        with open('data.json') as file:
            array = []
            jsonData = json.load(file)
            
            for i in jsonData:
                array.append(i)
                
            for i in range(len(array)):
                if array[i]["user"] == userID:
                    array[i]['stream'].append(data)
                    
        with open('data.json', 'w') as file:
            json.dump(array, file, indent = 2)
   
    def createUser(self) -> None:
        """
        Create a JSON file holding a user and null data in data stream
        """    
        with open('data.json', 'w') as file:
            data = [{
                "user": self.userID,
                "stream": []
            }]
            
            json.dump(data, file, indent = 2)
            
            
    def deleteUser(self, userID) -> None:
        """
        Delete a JSON file w/ associated user ID
        """
        with open('data.json') as file:
            array = []
            jsonData = json.load(file)
            
            for i in jsonData:
                array.append(i)
                
                
            for i in range(len(array)):
                if array[i]['user'] == userID:
                    array.pop(i)
                    break
        
        with open('data.json', 'w') as file:
            json.dump(array, file, indent = 2)
            
            
def main():
    test = User(1)
    test.createUser()
    test.download(1,1)
    test.download(1,2)
    
    #test = User(2)
    #test.createUser()
    #test.download(2,1)
    #test.download(2,2)
    
    test.deleteUser(1)
    
main()