# Headers
HTTP header keys are case insensitive. The Currencycloud API service will process the headers ``X-Auth-Token`` and ``X-AUTH-TOKEN`` and ``x-auth-token`` in the same way. 

Client applications also must process the headers of response messages in a case insensitive manner. For example, the headers ``Content-Type`` and ``content-type`` are equivalent.

For the most part, HTTP header values are also case insensitive. For example, the values ``text/html`` and ``TEXT/HTML`` are interchangeable on the ``Content-Type`` header. There will be some exceptions. For example, the value of the ``X-Auth-Token`` header is case sensitive, of course.
