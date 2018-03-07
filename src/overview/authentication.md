# Authentication
All endpoints in the Currencycloud API require authentication to access. Rather than providing your username and [API key](/overview/api-key) with every request, you sign in once to get a temporary authentication token.

To get an authentication token, submit your email address and API key to the [Login](/reference/authenticate/api) endpoint.

``POST /v2/authenticate/api`` \
``Content-Type: multipart/form-data``

| Parameter Name  | Example Value                                                         |
| --------------- | --------------------------------------------------------------------- |
| ``api_key``     | ``1f6a3e944f8c4ebdc6658d6fc1103f12ebbc33f5ed05ca3549fdbc3883556544``  |
| ``login_id``    | ``your.login@example.com``                                            |

If your credentials are validated, the response payload will contain a fresh authentication token.

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "auth_token": "ca3ca0ace18f07fa3c6a508fda646287"
}
```

Authentication is thereafter undertaken via by submitting the authentication token via the ``X-Auth-Token`` header in all subsequent requests to the Currencycloud API. The token acts as a proxy for your username and password.

```
POST /v2/beneficiaries/create HTTP/1.1
Host: devapi.currencycloud.com
X-Auth-Token: ca3ca0ace18f07fa3c6a508fda646287
```

Authentication tokens automatically expire after 30 minutes of inactivity. When your authentication token has expired, the Currencycloud API service will return this response:

```
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error_code": "auth_failed",
  "error_messages": {
    "username": [
      {
        "code": "invalid_supplied_credentials",
        "message": "Authentication failed with the supplied credentials",
        "params": {}
      }
    ]
  }
}
```

If authentication fails, clients must request a fresh authentication token by calling the [Login](/reference/authenticate/api) endpoint.

It is good security practice to retire authentication tokens when they are no longer needed, rather than let them expire. Send a request to the [Logout](/reference/authenticate/logout) endpoint to terminate an authentication token.
