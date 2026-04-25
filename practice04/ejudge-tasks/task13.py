import json


def resolve_query(obj, query):
    parts = query.replace(']', '').split('[')
    parts = [p for part in parts for p in part.split('.')]
    parts = [p for p in parts if p]

    current = obj
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return None
    return current


obj = json.loads(input())
n = int(input())

for _ in range(n):
    query = input().strip()
    result = resolve_query(obj, query)
    if result is None:
        print("NOT_FOUND")
    else:
        print(json.dumps(result, separators=(',', ':')))