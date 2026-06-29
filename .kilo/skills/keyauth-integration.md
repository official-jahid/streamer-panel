# KeyAuth Integration for REGIX Studio

## Description
License authentication system using KeyAuth for application access control.

## Quick Start

```python
# keyauth.py
from KeyAuth import api
import sys
import hashlib
import os

def getchecksum():
    md5_hash = hashlib.md5()
    file = open(''.join(sys.argv), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest

keyauthapp = api(
    name="REGIX Studio",
    ownerid="GIgun4Td7t",
    secret="your-secret-key",
    version="1.0",
    hash_to_check=getchecksum()
)
```

## Authentication Flow

```python
@app.post('/auth')
def auth():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    reply = keyauthapp.login(username, password)
    if reply:
        user['username'] = keyauthapp.user_data.username
        user['hwid'] = keyauthapp.user_data.hwid
        user['ip'] = keyauthapp.user_data.ip
        return jsonify(status=200, message="logged in")
    else:
        return jsonify(status=301, message="Credentials MisMatch")
```

## KeyAuth Functions

| Function | Description |
|----------|-------------|
| `login(username, password)` | Authenticate user |
| `logout()` | End session |
| `fetchOnline()` | Get online users |
| `user_data.username` | Get logged in username |
| `user_data.hwid` | Get hardware ID |
| `user_data.ip` | Get user IP |
| `user_data.expires` | Get subscription expiry |

## Session Management

```python
# Global session data
user = {
    'username': None,
    'hwid': None,
    'ip': None,
    'expiry': None
}

# Check session
if keyauthapp.user_data.username:
    # User is authenticated
    pass
else:
    # Redirect to login
    return redirect('/')
```

## Security Notes

- Application hash verification prevents tampering
- HWID binding prevents account sharing
- Session-based authentication with auto-logout

## References
- REGIX Studio keyauth.py
- REGIX Studio app.py auth endpoints