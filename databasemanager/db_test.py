from boten_anna_db import boten_anna_db

# Create new database and tables
db = boten_anna_db("testdb.db",'url',['uid integer PRIMARY KEY',
                                      'url text',
                                      'page_title text',
                                      'message text',
                                      'user text',
                                      'timestamp datetime default current_timestamp'])
# Insert data into table
print(db.insert(['url','page_title','message','user'],'url',['http://dev-nu11.de','Nothing','Visit IT!','DAU']))

# Select Test
print('-----Select *-Fetch All-----')
print(db.select(['*'],'url'))
print('\n-----Select url,page_tile-Fetch One--')
print(db.select(['url','page_title'],'url',False))
print('\n-----Search url, page_title,message by uid-----------')
print(db.search(['uid','page_title','message','user'],'url','url=?',['http://dev-nu11.de']))
print(db.search(['url','page_title','message','user'],'url','uid=?',['1']))
