# Encoding
Most endpoints accept ``multipart/form-data`` encoded payloads, and return JSON.

In requests, if the declared media type or encoding is unsupported by an endpoint, the Currencycloud API service will return a ``415 Unsupported Media Type`` status.

Client applications must use UTF-8 encoding for all requests. There is no need to declare the encoding using the ``charset`` parameter in the value of the ``Content-Type`` header, as the Currencycloud API service assumes UTF-8 encoding.

```
Content-Type: multipart/form-data; charset=UTF-8
```

This is also the encoding for all response messages. Client applications may assume that all HTTP response messages are UTF-8 encoded. It is not necessary to interrogate the ``Content-Type`` header or to otherwise verify a message's encoding.

```
Content-Type: application/json; charset=UTF-8
```

Client applications are required to support gzip compression. The payloads of most response messages are compressed using gzip. Where this is the case, the following header will be included in the response:

```
Content-Encoding: gzip
```
