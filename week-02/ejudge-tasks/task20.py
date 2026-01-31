import sys

read = sys.stdin.readline

n_line = read().strip()
if not n_line:
    sys.exit()

n = int(n_line)
storage = {}
out = []

for _ in range(n):
    line = read()
    if not line:
        break
    line = line.strip()
    if not line:
        continue

    parts = line.split(maxsplit=2)
    cmd = parts[0]

    if cmd == "set":
        # на всякий случай: если вдруг value отсутствует
        key = parts[1]
        value = parts[2] if len(parts) > 2 else ""
        storage[key] = value

    elif cmd == "get":
        key = parts[1]
        if key in storage:
            out.append(storage[key])
        else:
            out.append(f"KE: no key {key} found in the document")

sys.stdout.write("\n".join(out))
