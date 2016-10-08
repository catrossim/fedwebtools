dict={}
try:
    dict['a']
except KeyError,arg:
    print arg
