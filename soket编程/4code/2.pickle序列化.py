import pickle

data = [1, ['a', 'b'], 2]

# with open('a.txt', 'wb') as fp:
#      pickle.dump(data, fp)

with open('a.txt', 'rb') as fp:
    res = pickle.load(fp)
    print(res)

# with open('a.txt', 'wb') as fp:
#     my_data = pickle.dumps(data)
#     fp.write(my_data)

# with open('a.txt', 'rb') as fp:
#     buf = fp.read(1024)
#     print(buf)
#     res = pickle.loads(buf)
#     print(res)
