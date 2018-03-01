# Errors
Currencycloud uses conventional HTTP [status codes](/overview/status-codes) to indicate the success or failure of an API request. In general, status codes in the ``2xx`` range indicate success, codes in the ``4xx`` range indicate invalid input such as a missing parameter, and codes in the ``5xx`` range indicate an error with our servers.

Still, even more granular information on the source of an error is often desirable. So, where there has been a problem processing a request due to a client error, the response payload will typically provide precise information on the input parameters that failed. The payload of ``4xx`` responses will have the following structure:

```
{
  "error_code": "<error_code>",
  "error_messages": {
    "<field_name>": [
      {
        "code": "<error_code>",
        "message": "",
        "params": {
          "<param_name>": "<restraint>"
        }
      }
    ]
  }
}
```
