# Authenticate
Start a new API session.


Call the [Login](/reference/login) endpoint, passing in your Currencycloud login ID (usually your email address) and API key.

``POST /v2/authenticate/api`` \
``Content-Type: multipart/form-data``

| Parameter Name | Parameter Type | Example Value                                                        |
| -------------- | -------------- | -------------------------------------------------------------------- |
| ``api_key``    | Payload        | ``1f6a3e944f8c4ebdc6658d6fc1103f12ebbc33f5ed05ca3549fdbc3883556544`` |
| ``login_id``   | Payload        | ``your.login@example.com``                                           |

Extract the ``auth_token`` from the response payload and pass this to the ``X-Auth-Token`` header in all subsequent requests to the Currencycloud API.

```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "auth_token": "ea6d13c7bc50feb46cf978d137bc01a2"
}
```

Authentication tokens expire after 30 minutes of inactivity, after which time you will need to login again. If you don't need a token that long, [Logout](/reference/logout) to retire the token early.

``POST /v2/authenticate/close_session`` \
``Content-Type: multipart/form-data``

| Parameter Name   | Parameter Type | Example Value                        |
| ---------------- | -------------- | ------------------------------------ |
| ``X-Auth-Token`` | Header         | ``ea6d13c7bc50feb46cf978d137bc01a2`` |


## Next Step

[Check your Euros balance.](/cookbook/check-balance)
