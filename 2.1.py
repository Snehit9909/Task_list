inputs = []
print("Do enter the values (type 'ok' to end):")
while True:
    val = input("> ")
    if val.lower() == "ok":
        break
    if val.isdigit():
        converted = int(val)
        dtype = "int"
    elif val.replace('.', '', 1).isdigit() and val.count('.') == 1:
        converted = float(val)
        dtype = "float"
    elif val.lower() in ["true", "false"]:
        converted = val.lower() == "true"
        dtype = "bool"
    else:
        converted = val
        dtype = "str"
    inputs.append((val, dtype, converted))

print("\nSummary:")
print("{:<15} {:<10} {:<15}".format("Original", "Type", "Converted"))
for orignal, dtype, conv in inputs:
    print("{:<15} {:<10} {:<15}".format(orignal, dtype, str(conv)))
