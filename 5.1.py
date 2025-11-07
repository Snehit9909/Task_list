def traverse(data, path):
    parts = path.split('.')
    for p in parts:
        if isinstance(data, (list, tuple)):
            p = int(p)
        elif isinstance(data, set):
            data = list(data)
            p = int(p)
        data = data[p]
    return data

def set_value(data, path, value):
    parts = path.split('.')
    for p in parts[:-1]:
        if isinstance(data, (list, tuple)):
            p = int(p)
        elif isinstance(data, set):
            data = list(data)
            p = int(p)
        data = data[p]
    last = parts[-1]
    if isinstance(data, (list, tuple)):
        data[int(last)] = value
    elif isinstance(data, dict):
        data[last] = value

def delete_value(data, path):
    parts = path.split('.')
    for p in parts[:-1]:
        if isinstance(data, (list, tuple)):
            p = int(p)
        elif isinstance(data, set):
            data = list(data)
            p = int(p)
        data = data[p]
    last = parts[-1]
    if isinstance(data, (list, tuple)):
        del data[int(last)]
    elif isinstance(data, dict):
        del data[last]

def list_keys(data, path):
    target = traverse(data, path) if path else data
    if isinstance(target, dict):
        return list(target.keys())
    elif isinstance(target, (list, tuple, set)):
        return list(range(len(target)))
    return []


nested = {
    "students": [
        {"name": "John", "scores": {"math": 90}},
        {"name": "Tony", "scores": {"math": 85}},
        {"name": "Sam", "scores": {"math": 92}}
    ]
}

print(traverse(nested, "students.2.scores.math"))     
set_value(nested, "students.2.scores.math", 99)
print(traverse(nested, "students.2.scores.math"))     
delete_value(nested, "students.1.scores.math")
print(list_keys(nested, "students.0.scores"))         
