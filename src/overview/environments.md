# Environments
The Currencycloud API is served from two environments: a test environment, and the live production environment.

The base URI for all endpoints in the test environment is:

```
https://devapi.currencycloud.com/v2
```

The base URI for all endpoints in the production environment is:

```
https://api.currencycloud.com/v2
```

[API keys](api-keys.md) are environment-specific. You cannot use a test API key to access the production environment, and vice versa.
