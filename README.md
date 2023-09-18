# Python FreeDNS Client

This is a Python wrapper for [FreeDNS.afraid.org](https://freedns.afraid.org), which allows for the free registration of subdomains.

## Features:
- Login with existing account
- Send account creation email
- Get domains in the registry
- Get subdomains in an account
- Create a new subdoman record
- Update subdomain records

## Installation:
You can install this library using the following command: 
```
pip3 install git+https://github.com/ading2210/freedns-client
```

## Documentation:

### Using the Client:
The `freedns.Client` object does not take any arguments.

```python
import freedns
client = freedns.Client()
```

### Request a Captcha:
Whenever a captcha is needed, you can request it from the server using `client.get_captcha`. It accepts no arguments, and returns the bytes of a PNG image containing the captcha.

### Logging In:
You can log into an existing account with the `client.login` function. It takes the following arguments:
- `username` - The username/email of the account to log into.
- `password` - The password of the account.

If the login fails, the library will raise a `RuntimeError` with the error message reported by FreeDNS.

### Signing Up (Captcha Required):
You can send an activation email using `client.create_account`, which accepts the following arguments:
- `captcha_code` - The solution for the last captcha requested.
- `firstname` - The first name associated with the account.
- `lastname` - The last name associated with the account.
- `username` - The new account's username.
- `password` - The new account's password. 
- `email` - The email used for login and verification.

After recieving the activation email, you can run `client.activate_account`, which accepts the following arugments:
- `activation_code` - The activation code that you recieved in your email. This should be the random string of letters at the end of the activation URL. For example, `klsEii2txkW7Wa9DgGaaG6s8` would be the activation code for this URL: `http://freedns.afraid.org/signup/activate.php?klsEii2txkW7Wa9DgGaaG6s8` 

### Fetching the Domain Registry:
You can query the public domain registry using `client.get_registry`. It accepts the following optional arguments:
- `page = 1` - Which page of results to start at.
- `sort = 5` - The sort mode to use (details below).

**Sort modes:**
1. Domain Name
2. Status, Age
3. Domain Owner
4. Age
5. Popularity
6. Domain Length, Popularity

Any other value will default to sorting by popularity.

The function returns a list of dictionaries which represent each domain entry.

```python
>> client.get_registry()
[{'domain': 'chickenkiller.com', 'id': 14, 'hosts': 305876, 'status': 'public', 'owner_name': 'josh', 'owner_id': 1, 'age': 8293, 'created': '01/02/2001'}, ...]
```

### List Subdomains in an Account (Auth Needed):
You can list the subdomains registered to your account using `client.get_subdomains`. The function takes no arguments.

```python
>> client.get_subdomains()
[{'subdomain': 'randomdomain.hs.vc', 'id': '34523523', 'type': 'CNAME', 'destination': 'example.com'}, ...]
```

This function returns a list of dictionaries represnting each subdomain.

### Get a Subdomain's Details (Authe Needed):
To get the details for a specific subdomain, use `client.get_subdomain_details`. The function takes the following arguments:
- `subdomain_id` - The ID of the subdomain you are querying. You can find this with `client.get_subdomains`.

The function will return a dict with the subdomain details.

```python
>> client.get_subdomain_details(20123422)
{'type': 'A', 'subdomain': 'subdomain', 'domain': 'example.com', 'domain_id': 435322, 'destination': '1.1.1.1', 'wildcard': False}
```

### Register a New Subdomain (Auth+Captcha Needed):
Use the `client.create_subdomain` function to register a new subdomain. The function accepts the following arguments:
- `captcha_code` - The solution for the last captcha requested.
- `record_type` - The type of record to create (for example `CNAME` or `A`).
- `subdomain` - The subdomain to create (does not include the domain name).
- `domain_id` - The ID of the domain to use. You can get this with `client.get_registry`, as documented earlier.
- `destination` - The destination for the record. 

The function will not return anything on success, but it'll raise a `RuntimeError` if the subdomain creation has failed.

### Update a Subdomain (Auth+Captcha Needed):
Use the `client.update_subdomain` function to update an existing subdomain. The function accepts the following arguments:
- `subdomain_id` - The ID of the subdomain to modify.
- `captcha_code` - The solution for the last captcha requested.
- `record_type = None` - The record type.
- `subdomain = None` - The subdomain to use.
- `domain_id = None` - The ID of the domain to use. 
- `destination = None` - The destination for the record. 

If you don't supply one of the optional arguments, then the value won't change. If the operation fails, a `RuntimeError` will be raised.

## Copyright: 
This program is licensed under the [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.txt). All code has been written by me, [ading2210](https://github.com/ading2210).

### Copyright Notice:
```
ading2210/freedns-client: a Python API wrapper for FreeDNS.afraid.org
Copyright (C) 2023 ading2210

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```