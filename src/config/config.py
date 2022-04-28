import json
import os

def load():
    path = os.getcwd()
    yamlPath = os.path.join(path, "env","config","default.json")
    with open(yamlPath, 'r', encoding='utf-8') as f:
        config = f.read()
    d = json.loads(config)
    return d

if __name__=="__main__":
    print(load())