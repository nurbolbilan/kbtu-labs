n = int(input())

dorama_episodes = {}

for _ in range(n):
    name, episodes = input().split()
    episodes = int(episodes)

    if name in dorama_episodes:
        dorama_episodes[name] += episodes
    else:
        dorama_episodes[name] = episodes

for name in sorted(dorama_episodes.keys()):
    print(name, dorama_episodes[name])
