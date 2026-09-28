import json
class FileManager:
    def save(self,filename,data):
        with open(filename,'w') as f:
            json.dump(data,f,indent=4)
    
    def load(self,filename):
        try:
            with open(filename,'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []