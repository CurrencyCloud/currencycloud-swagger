# Status Codes
The Currencycloud API uses conventional HTTP response codes to indicate the success or failure of an HTTP request.


## 1xx Informational
No endpoints in the Currencycloud API emit 1xx informational statuses.


## 2xx Success
Any status codes between 200 and 299 must be treated by client applications as ``200 OK``.


## 3xx Redirection
The Currencycloud API service does not emit 3xx redirection responses.


## 4xx Client Error
Appropriate client error codes are returned for malformed API calls or where input is found to be invalid.

``400 Bad Request`` is returned when the HTTP headers, query string parameters or the syntax of the payload are found to be invalid, for example a mandatory input parameter is missing or of the wrong type.

``401 Unauthorized`` is returned for requests that do not provide a valid authentication key. ``403 Forbidden`` is returned when a user does not have the necessary privileges required to access the requested resource.

``404 Not Found`` or ``405 Method Not Allowed`` are returned following calls to non-existent URI paths.

``415 Unsupported Media Type`` is returned if a request's MIME type or character encoding (as declared in the ``Content-Type`` header) or the compression format (as declared in the ``Content-Encoding`` header) are not supported by the server.

``429 Too Many Requests`` will be returned when a client reaches its request quota (see [Rate Limits](rate-limits.md)).

In the future, ``410 Gone`` will be returned from all endpoints in the current version of the Currencycloud API, when [this version is finally retired](versioning.md).

Client applications should log 4xx errors to facilitate debugging. Applications should not retry client errors. Applications should address the issue before submitting the request again.


## 5xx Server Error
In the event of a server error, clients should retry the original request at least once.

Exponential backoff, whereby clients use progressively longer waits before retrying a failed request, is recommended. For example, an application might wait 400 milliseconds before a first retry, 1600 milliseconds before a second retry, and 6400 milliseconds before a third and final retry.

If a request continues to fail, applications should fail gracefully, for example by rendering a polite and appropriate message to users whenever a user-initiated API call fails unexpectedly.
