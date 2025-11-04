def run(data):
    for v in "AEIOUaeiou":
        data = data.replace(v, "*")
    return data
