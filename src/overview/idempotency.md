# Idempotency Keys
Idempotency keys are unique tokens, created and submitted by client applications, that guarantee only one resource will be created regardless of how many times the request to create the resource is repeated.

Two endpoints in the Currencycloud API support optional idempotency keys:

- [Create Conversion](/reference/create-conversion)
- [Create Payment](/reference/create-payment)

It is recommended that you submit a unique idempotency key with every discrete request to these endpoints. Use the optional ``unique_request_id`` field to submit your keys. Should you receive an error response, such as a 500 Internal Server Error, you can safely retry the request without running the risk of creating duplicate conversions or payments.

The format of your idempotency keys can be any string, though we recommend using 36-digit UUIDs.

Example:

``POST /v2/payments/create`` \
``Content-Type: multipart/form-data``

| Parameter Name        | Parameter Type | Example Value                            |
| --------------------- | -------------- | ---------------------------------------- |
| ``currency``          | Payload        | ``GBP``                                  |
| ``beneficiary_id``    | Payload        | ``c12955d5-9253-4168-b5eb-97cc8e3ce92e`` |
| ``amount``            | Payload        | ``950.00``                               |
| ``reason``            | Payload        | ``Invoice``                              |
| ``reference``         | Payload        | ``2018-015``                             |
| ``unique_request_id`` | Payload        | ``11b88b7f-59b7-4002-852a-c4c82fb127eb`` |
| ``X-Auth-Token``      | Header         | ``f657d9d091fbe54bf2c7288ac205ad06``     |
