from boten_anna_db import boten_anna_db

db = boten_anna_db()
db.insert("http://dev-nu11.de","Nothing","Visit IT!","DAU")
print(db.get_links())
print(db.search_duplicated("http://dev-nu11.de"))
print(db.search_uid(1))
