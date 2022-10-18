[_metadata_:menu_title]:- "Maintenance Windows"
[_metadata_:order]:- "8"

# Maintenance Windows

All maintenance windows are announced on our [status page](https://status.currencycloud.com/).

When a maintenance window is in effect, the API will return a HTTP status code of [503 -- "Service Unavailable"](https://datatracker.ietf.org/doc/html/rfc7231#section-6.6.4) with a JSON response body as per the example below for the duration of the maintenance window:

```
HTTP/1.1 503 Service Unavailable
Date: Mon, 25 Jan 2021 13:16:59 GMT
Content-Type: application/json; charset=UTF-8
{
  "error_code": "service_unavailable",
  "error_messages": {
    "base": [
     {
      "code": "service_unavailable",
      "message": "Service is temporarily unavailable due to maintenance",
      "params": {}
     },
    ]
  }
}
```
