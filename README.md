# sparkapi-python
Cisco Spark (Webex Teams) API wrapper for pythong

### Table of Contents  
* The [service definition docs][docs]   
* The [protobuf][protorepo] for this project  
* How are these docs [created][how]?
* [Change Log](#change-log)
* [Client Usage](#client-usage)
* [Server Usage](#server-usage)
 
#### Change Log
v1.0.0
 - Initial version
 
 
#### Usage
A client class is provided with the following services implemented:
 - GetOrg
 - GetUser
 - CreateNewRepo
 - CheckOrgMembership

An example is shown below. 

```python

>>> from protorepo_gha.gha_client import GHAClient

>>> client = GHAClient(host='localhost', port=50051, secure=False)

>>> resp = client.get_user(name='jon@doe.com', profile_type='GitHub')
>>> print(resp)
user {
  login: "jon@doe.com"
  name: "jon@doe.com"
  company: "Fake Company"
  url: "https://github.com/fakeuri"
}

>>> print(resp.user.name)
jon@doe.com
>>>
```

#### Server Usage
You can run the utils.gha_server module provides a grpc server for testing the client. 

Start the server from a command line:

```bash
python -m protorepo_gha.utils.gha_server --host localhost --port 50051
Starting grpc server localhost:50051
```

[docs]: ./docs.md 
[how]: https://github.com/pseudomuto/protoc-gen-doc
[gha]: https://github.com/cdwlabs/gha
[protorepo]: https://github.com/cdwlabs/protorepo/tree/master/gha
