import json

def merge_patch(source, patch):
    word = None
    for key, value in patch.items():
        if key in source and isinstance(source[key], dict) and isinstance(value, dict):
            merge_patch(source[key], value)
            if word is None:
                word = str(key)
            else:
                word = str(word) + "." + str(value)
        else:
            if key in source:
                if value != source[key]:
                    if word is None:
                        word = str(key)
                        a = source[key]
                        b = value
                        source[key] = value
                        return word, a, b
                    else:
                        a = source[key]
                        b = value
                        source[key] = value
                        return word, a, b
            else:
                 return False, False, False

    return source

source = json.loads(input())
patch = json.loads(input())

result, a, b = merge_patch(source, patch)

if result == False:
    print("No differences")
else:
    result = str(result) + " : " + str(a) + " -> " + str(b)
    print(result)
