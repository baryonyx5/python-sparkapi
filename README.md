# sparkapi-python
Cisco Spark (Webex Teams) API wrapper for python

==Note: Please see [webexteamssdk](https://webexteamssdk.readthedocs.io/en/latest/index.html] for a more complete and well-tested Webex Teams library.==

## Usage

```python
from sparkapi import SparkAPI
>>> TOKEN = '<OAUTH TOKEN OR DEVELOPER TOKEN'
>>> sp = SparkAPI(access_token=TOKEN)
>>> me = sp.people.me()
>>> me
Person(email=xxx.xxx@xyz.com)
>>> me.displayName
'Jon Joe'
>>> me.lastActivity
datetime.datetime(2019, 3, 22, 18, 59, 52, tzinfo=tzutc())


>>> results = sp.people.get_by_email('fred@gmail.com')
>>> results
[Person(email=fred@gmail.com)]


>>> rooms = sp.rooms.list()
>>> for room in rooms:
...     print(room.title, room.lastActivity)
...

```