# Make Payment
Make a payment to Germany from your Euros balance.


## First Steps

1. [Authenticate](authenticate.md)
2. [Check your currency balances](check-balance.md)
3. [Buy more Euros using funds from your Pound Sterling balance](convert.md)


## Check Requirements
You want to make a priority payment to a supplier based in Germany. First, check what details are required to make a priority payment in Euros to a beneficiary with a bank account in Germany. Call the **Get Beneficiary Requirements** endpoint.

``GET /v2/reference/beneficiary_required_details`` \
``Content-Type: multipart/form-data``

| Parameter Name           | Parameter Type | Example Value                        |
| ------------------------ | -------------- | ------------------------------------ |
| ``currency``             | Payload        | ``EUR``                              |
| ``bank_account_country`` | Payload        | ``DE``                               |
| ``X-Auth-Token``         | Header         | ``ea6d13c7bc50feb46cf978d137bc01a2`` |

Example response:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "details": [
        {
            "payment_type": "priority",
            "beneficiary_entity_type": "individual",
            "beneficiary_address": "^.{1,255}",
            "beneficiary_city": "^.{1,255}",
            "beneficiary_country": "^[A-z]{2}$",
            "beneficiary_first_name": "^.{1,255}",
            "beneficiary_last_name": "^.{1,255}",
            "iban": "([A-Z0-9]\\s*){15,34}",
            "bic_swift": "^[0-9A-Z]{8}$|^[0-9A-Z]{11}$"
        },
        {
            "payment_type": "priority",
            "beneficiary_entity_type": "company",
            "beneficiary_address": "^.{1,255}",
            "beneficiary_city": "^.{1,255}",
            "beneficiary_country": "^[A-z]{2}$",
            "beneficiary_company_name": "^.{1,255}",
            "iban": "([A-Z0-9]\\s*){15,34}",
            "bic_swift": "^[0-9A-Z]{8}$|^[0-9A-Z]{11}$"
        },
        {
            "payment_type": "regular",
            "iban": "([A-Z0-9]\\s*){15,34}",
            "bic_swift": "^[0-9A-Z]{8}$|^[0-9A-Z]{11}$",
            "beneficiary_entity_type": "individual"
        },
        {
            "payment_type": "regular",
            "iban": "([A-Z0-9]\\s*){15,34}",
            "bic_swift": "^[0-9A-Z]{8}$|^[0-9A-Z]{11}$",
            "beneficiary_entity_type": "company"
        }
    ]
}
```

The response tells us that, to make a regular payment to a German bank account in Euros, we need two pieces of information: the IBAN and BIC/SWIFT numbers for the beneficiary.


## Create Beneficiary
If you know the required details, you can go ahead and create a record for the beneficiary via the **Create Beneficiary** endpoint.

``POST /v2/beneficiaries/create`` \
``Content-Type: multipart/form-data``

| Parameter Name               | Parameter Type | Example Value                        |
| ---------------------------- | -------------- | ------------------------------------ |
| ``name``                     | Payload        | ``Acme GmbH``                        |
| ``bank_account_holder_name`` | Payload        | ``Acme GmbH``                        |
| ``currency``                 | Payload        | ``EUR``                              |
| ``beneficiary_country``      | Payload        | ``DE``                               |
| ``bank_country``             | Payload        | ``DE``                               |
| ``bic_swift``                | Payload        | ``COBADEFF``                         |
| ``iban``                     | Payload        | ``DE89370400440532013000``           |
| ``X-Auth-Token``             | Header         | ``ea6d13c7bc50feb46cf978d137bc01a2`` |

If the beneficiary is successfully created, the response message will contain full details about the beneficiary as recorded in your Currencycloud account, including a unique ID for the new beneficiary.

```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "aea097c2-39e4-49b5-aaa6-c860ca55ca0b",
    "bank_account_holder_name": "Acme GmbH",
    "name": "Acme GmbH",
    "email": null,
    "payment_types": [
        "regular"
    ],
    "beneficiary_address": [],
    "beneficiary_country": "DE",
    "beneficiary_entity_type": null,
    "beneficiary_company_name": null,
    "beneficiary_first_name": null,
    "beneficiary_last_name": null,
    "beneficiary_city": null,
    "beneficiary_postcode": null,
    "beneficiary_state_or_province": null,
    "beneficiary_date_of_birth": null,
    "beneficiary_identification_type": null,
    "beneficiary_identification_value": null,
    "bank_country": "DE",
    "bank_name": "Test Bank Plc",
    "bank_account_type": null,
    "currency": "EUR",
    "account_number": null,
    "routing_code_type_1": null,
    "routing_code_value_1": null,
    "routing_code_type_2": null,
    "routing_code_value_2": null,
    "bic_swift": "COBADEFF",
    "iban": "DE89370400440532013000",
    "default_beneficiary": "false",
    "creator_contact_id": "1993263d-be07-42d4-b75b-ae4ea18bcb6c",
    "bank_address": [],
    "created_at": "2018-02-02T11:52:23+00:00",
    "updated_at": "2018-02-02T11:52:23+00:00",
    "beneficiary_external_reference": null
}
```


## Make a Payment
Authorize a payment by calling the **Create Payment** endpoint. It is strongly recommended that you provide an [idempotency key](../overview/idempotency.md) to prevent duplicate payments.

``POST /v2/payments/create`` \
``Content-Type: multipart/form-data``

| Parameter Name        | Parameter Type | Example Value                            |
| --------------------- | -------------- | ---------------------------------------- |
| ``currency``          | Payload        | ``EUR``                                  |
| ``beneficiary_id``    | Payload        | ``aea097c2-39e4-49b5-aaa6-c860ca55ca0b`` |
| ``amount``            | Payload        | ``10000``                                |
| ``reason``            | Payload        | ``Invoice Payment``                      |
| ``payment_type``      | Payload        | ``regular``                              |
| ``reference``         | Payload        | ``2018-014``                             |
| ``unique_request_id`` | Payload        | ``4abd730f-bb50-4b4a-8890-f46addff222b`` |
| ``X-Auth-Token``      | Header         | ``ea6d13c7bc50feb46cf978d137bc01a2``     |

You can instruct payments even if you don't hold enough money in the relevant currency. Payments will not be processed until your account balance is topped up.

If the payment is successfully queued, the response payload will contain all the information about the payment as recorded in your Currencycloud account. This does not mean that the payment was made. It just means that it is ready for processing. Payments are processed asynchronously. Currencycloud will process payments on the ``payment_date`` specified, provided you still hold enough money in the relevant currency at the time.

```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "bea05ec4-8c6b-4ec9-80e5-65c0cd257473",
    "amount": "10000.00",
    "beneficiary_id": "aea097c2-39e4-49b5-aaa6-c860ca55ca0b",
    "currency": "EUR",
    "reference": "2018-014",
    "reason": "Invoice Payment",
    "status": "ready_to_send",
    "creator_contact_id": "1993263d-be07-42d4-b75b-ae4ea18bcb6c",
    "payment_type": "regular",
    "payment_date": "2018-02-02",
    "transferred_at": "",
    "authorisation_steps_required": "0",
    "last_updater_contact_id": "1993263d-be07-42d4-b75b-ae4ea18bcb6c",
    "short_reference": "180202-RDRWGQ001",
    "conversion_id": null,
    "failure_reason": "",
    "payer_id": "49d44eff-af91-45b0-a32e-84c7c1750ca0",
    "payer_details_source": "account",
    "created_at": "2018-02-02T11:56:05+00:00",
    "updated_at": "2018-02-02T11:56:05+00:00",
    "payment_group_id": null,
    "unique_request_id": "4abd730f-bb50-4b4a-8890-f46addff222b",
    "failure_returned_amount": "0.00",
    "ultimate_beneficiary_name": null
}
```


## Next Step

So far in this cookbook you have [converted money from GBP to Euros](convert.md) and made a payment to Germany from your topped-up Euros balance. But, before the payment can be processed, the conversion from GBP to Euros needs to be completed, so you have enough money in Euros when the payment goes through. To complete the conversion, you must **settle**.
