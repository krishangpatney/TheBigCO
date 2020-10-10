import inspect
file_name = __file__
with open(inspect.stack()[0][1],"r") as f:
    lines = f.readlines()
    for i in lines:
        print(i.strip()[::-1])
