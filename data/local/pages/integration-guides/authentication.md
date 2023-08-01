[_metadata_:menu_title]:- "Authenticating"
[_metadata_:order]:- "2"

# Authenticating

All endpoints in the Currencycloud API require authentication. Rather than providing your username and API key with every request, you sign in once to obtain a temporary authentication token.

## TL;DR
To authenticate, follow the steps below.
1. Get a temporary authentication token by calling the [Login endpoint](/api-reference/#authenticate), passing in your Currencycloud login ID (which is usually your email address) and your unique [API key](/register-for-an-api-key/).
2. Extract the `auth_token` from the response payload. This is your authentication token and will be used as a proxy for your login credentials. You will need to submit your authentication token via the `X-Auth-Token` header with all subsequent API calls.
3. To terminate your session and retire your access token, send a request to the [Logout endpoint](/api-reference/#logout).

Detailed instructions are given in the authentication guide below.

## Workflow diagram

![authentication](/images/workflow_diagrams/1_authenticate.jpg)

## Authentication guide

## 1. Login

Call the [Login endpoint](/api-reference/#authenticate), passing in your Currencycloud login ID - which is usually your email address - and your unique API key. If you don't yet have an API key, you can register for one [here](/register-for-an-api-key/). An email will be sent to you that will provide instructions for obtaining your API key.

```
POST /v2/authenticate/api
Content-Type: multipart/form-data
```

| Parameter Name | Parameter Type | Example Value |
| --- | --- | --- |
| `api_key` | Form Data | `1f6a3e944f8c4ebdc6658d6fc1103f12ebbc33f5ed05ca3549fdbc3883556544` |
| `login_id` | Form Data | `your.login@example.com` |

If your credentials are validated, the response payload will contain a fresh authentication token.

```
HTTP/1.1 200 OK
Content-Type: application/json
{
    "auth_token": "ea6d13c7bc50feb46cf978d137bc01a2"
}
```  

## 2. Keep the authentication token

Extract the `auth_token` from the response payload. This is your authentication token. From now on, your authentication token will be used as a proxy for your login credentials. You will need to submit your authentication token with all subsequent API calls. You do this via the `X-Auth-Token` header. Example:

```
POST /v2/beneficiaries/create HTTP/1.1
X-Auth-Token: ea6d13c7bc50feb46cf978d137bc01a2
```

Authentication tokens expire after 30 minutes of inactivity. When your authentication token has expired, the Currencycloud API service will return this response:

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

In this situation, you should request a fresh authentication token by calling the [Login endpoint](https://developer.currencycloud.com/docs/item/login/) again.

We recommend that you wait until your authentication token has expired before re-authenticating.

## 3. Logout

It is good security practice to retire authentication tokens when they are no longer needed, rather than let them expire. Send a request to the [Logout endpoint](/api-reference/#logout) to terminate an authentication token immediately.

```
POST /v2/authenticate/close_session
X-Auth-Token: ea6d13c7bc50feb46cf978d137bc01a2
```
