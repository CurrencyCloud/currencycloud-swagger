# URIs
The base URI for all endpoints in the test environment is:

```
https://devapi.currencycloud.com/v2
```

The base URI for all endpoints in the production environment is:

```
https://api.currencycloud.com/v2
```

The Currencycloud API consists of multiple endpoints. Endpoints are grouped into categories such as "authentication" and "contacts". The endpoint category is identified by the second URI path segment. For example, URI paths for all endpoints in the "accounts" collection have the following format:

```
https://devapi.currencycloud.com/v2/accounts/\*\*/\*
```

URI paths are case sensitive, and they never have a trailing slash or file extension.

## Query Strings
Query string keys and their values must be URL encoded as per [RFC 3986](https://tools.ietf.org/html/rfc3986). This means that space characters must be encoded as %20, not + (an older standard).

In general, query string parameters are optional. But this is not always the case. There are some resources in the Currencycloud API that can be retrieved only using the ``GET`` HTTP method and mandatory query string parameters.

See also [Pagination](/overview/pagination).
