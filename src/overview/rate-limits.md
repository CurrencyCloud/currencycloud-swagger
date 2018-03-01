# Rate Limits
To ensure a stable service for all users, the number of requests you can make to the Currencycloud API — both the test and live [environments](/overview/environments) — is restricted.

Rate limiting is applied on a per-user basis in one minute intervals.

Requests to the [authentication endpoints](/reference/authenticate) are limited to 10 per minute.

Other endpoints have higher rate limits. Requests for [foreign exchange rates](/reference/rates) are limited to 75 per minute, while every other resource is capped at 100.

If you make too many requests, you will receive a status code of ``429 Too Many Requests``. Client applications should be programmed to handle this scenario gracefully.

All endpoints return information about the rate limitations on the requested resource. The following headers are provided:

- ``X-Rate-Limit-Limit``: The rate limit ceiling for the requested resource.
- ``X-Rate-Limit-Remaining``: The number of requests you have left in the current one minute window.
- ``X-Rate-Limit-Reset``: The remaining window, in seconds, before the rate limit resets.
