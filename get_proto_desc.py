from protocols import get_protocol_descriptions

lst_protos = [91, 186, 95, 40, 178, 100, 55, 153, 25, 54]

dct_protos = get_protocol_descriptions(lst_protos)

# print out the key value pairs
for key, value in dct_protos.items():
    print(key, value)
