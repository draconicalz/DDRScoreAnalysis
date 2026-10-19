import json

with open("data/raw/output.json", encoding = "utf-8") as file:
    data = json.load(file)

print(type(data))

if isinstance(data, dict):
    print(data.keys())
elif isinstance(data, list):
    print(len(data))
    if data:
        print(data[0])