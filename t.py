import data_storage
import uuid
all_ukey = data_storage.u_key()
ids = uuid.uuid1()
ids = str(ids)
print(ids)
token = True
while token:
    if ids in all_ukey:
        ids = uuid.uuid1()
        ids = str(ids)
        print(ids)
    else:
        token = False