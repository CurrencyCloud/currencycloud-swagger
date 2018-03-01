# FAQs

## What is the difference between the test and live environments?
The Currencycloud API is served from two environments: a test environment, and the live production environment.

The base URI for the test environment is:

```
https://devapi.currencycloud.com/v2
```

The base URI for the production environment is:

```
https://api.currencycloud.com/v2
```

[API keys](/overview/api-keys) are environment-specific. You cannot use a test API key to access the production environment, and vice versa.

On the surface, both API environments appear to behave identically. But there are important differences in how they process data. When you use the test environment, you are connected to a trading simulator, not the real thing. You cannot exchange or transfer real money in the test environment. However, the test environment returns the same real time foreign exchange rate data as the production environment.
