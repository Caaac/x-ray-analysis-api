from datetime import datetime


print(datetime.now().year)
print(datetime.now().month)
print(datetime.now().day)



def test(**kwargs):
    print(kwargs)
    
    
test(key = 234)


import uuid

print(dir(uuid.uuid4()))
print(str(uuid.uuid4()))
print(type(str(uuid.uuid4())))
print(uuid.uuid4())
print(uuid.uuid4().int)
print(uuid.uuid4().time)
print(uuid.uuid4().urn)
print(uuid.uuid4().bytes)
