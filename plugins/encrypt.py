def run(data):
    # shift each character by +1
    return "".join(chr(ord(c) + 1) for c in data)
