import os


# print(os.listdir('.'))

mypath = os.walk('.')

for data in mypath:
    print(data)

