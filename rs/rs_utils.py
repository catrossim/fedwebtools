from codecs import open as open

def save(path, content):
    with open(path, 'w', 'utf-8') as f:
        f.write(content)

def readfilebylines(path):
    r = []
    with open(path, 'r', 'utf-8') as f:
        r = f.readlines()
    return r
