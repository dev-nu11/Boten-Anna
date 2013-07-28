Boten Anna
===

This is a simple XMPP MUC Bot especially written for thatsapp.org, but you can of course use it for your own purposes :).

Dependency
---
* SleekXMPP (https://github.com/fritzy/SleekXMPP)

Features
---
* Search URLs in the chat messages, return the page title and save the url, page title, message, user and current timestamp to sqlite database

Commands
---
* !links - Get all saved links
* !link <NUMBER> - Show link with number

Install
---
* Create SQLITE Database
````
sqlite3 boten_anna.db -init create_tables.sql
````
* Install SleekXMPP and start muc.py with the following parameters:
````
python muc.py -j user@jabberid.tld -p secret_password -r room@domain.tld -n nickname
````

License
---
GPL3 license.
Feel free to use it and even contribute bug fixes or enhancements if you want. Enjoy!
