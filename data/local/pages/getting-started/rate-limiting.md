[_metadata_:menu_title]:- "Rate Limiting"
[_metadata_:order]:- "7"

# Rate Limiting

The API is rate limited per minute and different resources have different limits on a client account basis. Consider a resource that has a rate limit of 10 requests per minute; anything over 10 requests within the same minute (e.g. between 16:20:00 to 16:21:00) will return an error. The rate limiter allows bursting so if no requests are received in the first 50 seconds, for example, but 10 are received over the next 10 seconds, they will all succeed.

You must implement suitable error handling for HTTP 429 response codes in your API client. Using an exponential backoff with a random jitter is the recommended way to handle HTTP 429 response codes.

Different rate limits apply to different resources depending on whether an API client is making an authenticated request or not, as listed below.

| Request Type | Request Path | Rate Limit |
| --- | --- | --- |
| Authenticate | `/v2/authenticate/api` | 60 requests per minute |
| Rate Requests | `/v2/rates/find` , `/v2/rates/detailed` | 150 requests per minute |
| All other authenticated requests | `/v2/*` | 500 requests per minute |
| All other unauthenticated requests | `/v2/*` | 150 requests per minute |

### Exceeding the rate limit

When the rate limit is exceeded, the API will return a HTTP status code of [429 -- "Too Many Requests"](https://tools.ietf.org/html/rfc6585) with a JSON response body as per the example below:

```
HTTP/1.1 429 Too Many Requests
Date: Mon, 25 Jan 2021 13:16:59 GMT
Content-Type: application/json; charset=UTF-8
{
  "error_code": "too_many_requests",
  "error_messages": {
    "base": [
     {
      "code": "too_many_requests",
      "message": "Too many requests have been made to the api. Please refer to the Developer Center for more information",
      "params": {}
     },
    ]
  }
}
```

You should wait 60 seconds before retrying the request.

### Different requirements

If you have different requirements, please contact our [team](https://www.currencycloud.com/contact/) so we can better address your needs.
