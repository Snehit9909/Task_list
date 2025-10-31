import re

def decode_pattern(pattern):
    decoded = ""
    i = 0
    while i < len(pattern):
        char = pattern[i]
        if not char.isalpha():
            raise ValueError(f"Invalid character '{char}' at position {i}. Expected a letter.")
        i += 1
        
        num_str = ""
        while i < len(pattern) and pattern[i].isdigit():
            num_str += pattern[i]
            i += 1
        
        count = int(num_str) if num_str else 1
        if count < 1:
            raise ValueError(f"Invalid count '{count}' after '{char}'.")
        
        decoded += char * count

    return decoded

def encode_pattern(text):
    encoded = ""
    i = 0
    while i < len(text):
        char = text[i]
        if not char.isalpha():
            raise ValueError(f"Invalid character '{char}' at position {i}. Expected a letter.")
        
        count = 1
        i += 1
        while i < len(text) and text[i] == char:
            count += 1
            i += 1
        
        encoded += f"{char}{count if count > 1 else ''}"
    
    return encoded


def main():
    user_input = input("Enter a string pattern or text: ").strip()
    
    if not user_input:
        print("Please enter a non-empty string.")
        return
    
    try:

        if any(ch.isdigit() for ch in user_input):
            result = decode_pattern(user_input)
            print(f" Decoded result: {result}")
        else:
            result = encode_pattern(user_input)
            print(f" Encoded result: {result}")
    except ValueError as e:
        print(f" Error: {e}")


if __name__ == "__main__":
    main()
