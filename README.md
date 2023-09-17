# Python FreeDNS Client

This is a Python wrapper for [FreeDNS.afraid.org](https://freedns.afraid.org), which allows for the free registration of subdomains.

## Features:
- Login with existing account
- Send account creation email
- Get domains in the registry
- Get subdomains in an account
- Create a new subdoman record

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

### Logging In:
You can log into an existing account with the `client.login` function. It takes the following arguments:
- `username` - The username/email of the account to log into.
- `password` - The password of the account.

If the login fails, the library will raise a `RuntimeError` with the error message reported by FreeDNS.

### Signing Up:
You can send a confirmation email using `client.signup`. This function is unfinished so it will not be documented.

### Request a Captcha (No Auth):
When a captcha is needed, you can request it from the server using `client.get_captcha`. It accepts no arguments, and returns the bytes of a PNG image containing the captcha.

### Fetching the Domain Registry (No Auth):
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
>> client.
[{'subdomain': 'randomdomain.hs.vc', 'id': '34523523', 'type': 'CNAME', 'destination': 'example.com'}, ...]
```

This function returns a list of dictionaries represnting each subdomain.

### Register a New Subdomain (Auth+Captcha Needed):
Use the `client.create_subdomain` function to register a new subdomain. The function accepts the following arguments:
- `record_type` - The type of record to create (for example `CNAME` or `A`).
- `subdomain` - The subdomain to create (does not include the domain name).
- `domain_id` - The ID of the domain to use. You can get this with `client.get_registry`, as documented earlier.
- `destination` - The destination for the record. 
- `captcha_code` - The solution for the last captcha requested.

The function will not return anything on success, but it'll raise a `RuntimeError` if the subdomain creation has failed.

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