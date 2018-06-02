keys = {}
with open('ApiKeys.cfg', 'r') as f:
    for line in f:
        (key, value) = line.split(":")
        keys[key] = value
