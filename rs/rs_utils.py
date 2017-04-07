from codecs import open as open
import os
import pickle

def save(path, content):
    with open(path, 'w', 'utf-8') as f:
        f.write(content)

def readfilebylines(path):
    r = []
    with open(path, 'r', 'utf-8') as f:
        r = f.readlines()
    return r

def save_obj(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(path):
    with open(path, 'rb') as f:
        return pickle.load(f)
