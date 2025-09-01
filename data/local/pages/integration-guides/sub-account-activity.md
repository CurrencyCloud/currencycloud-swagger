[_metadata_:menu_title]:- "Sub-Account Activity (on_behalf_of)"
[_metadata_:order]:- "10"

# Sub-Account Activity (on_behalf_of)

Named accounts, also known as sub-accounts, are accounts that represent your end customers. If you are operating as a regulated entity (RFXB, MSB, etc), we would anticipate that you are performing your own KYC/due diligence on these customers and may have a need to set up accounts for each customer where Collection, Payment, and Conversion activity is conducted out of each individual account and where these accounts can hold multi-currency wallets. 

You may also use sub-accounts if you are operating as an unregulated entity where we, Currencycloud, own the direct relationship with your end customer and we undertake the onboarding/KYC and creation of sub-accounts.

When sub-accounts are utilized, in order to access and transact any activity on the sub-account a contact needs to be created. Once a contact is created, the `on_behalf_of` parameter should be used in the transactional events (conversion, payment, transactions, searching) at the sub-account level. 

This cookbook will consider the initial setup of a sub-account along with a basic conversion and payment use case for a regulated entity.

## Pre-conditions
You need to have authenticated and have an authentication token before accessing any of Currencycloud's endpoints. Please refer to the [authentication guide](/guides/integration-guides/authentication) for instructions to start a new API session.

## Establishing a sub-account for a customer

## Step 1: Create a sub-account

Once you have completed your own KYC processes on your end customer, you will need to create a sub-account in the Currencycloud ecosystem using the [Create Accounts](/api-reference/#create-account) endpoint. An example of a successful request and response looks like this:

**`POST /v2/accounts/create`**

| **Parameter Name** | **Parameter Type** | **Example Value** |
| --- | --- | --- |
| `account_name` | Form Data | `Jimmy's Burritos` |
| `legal_entity_type` | Form Data | `company` |
| `street` | Form Data | `123 Main Street` |
| `city` | Form Data | `Denver` |
| `country` | Form Data | `US` |
| `postal_code` | Form Data | `80209` |
| `your_reference` | Form Data | `12345678` |
| `status` | Form Data | `enabled` |
| `state_or_province` | Form Data | `CO` |
| `identification_type` | Form Data | `incorporation_number` |
| `identification_value` | Form Data | `123456789` |
| `X-Auth-Token` | header | `ea6d13c7bc50feb46cf978d137bc01a2` |

Response:

```

{
    "id": "53d15949-b1e9-4335-a4e4-56ae8adef95e",
    "account_name": "Jimmy's Burritos",
    "brand": "currencycloud",
    "your_reference": "123456789",
    "status": "enabled",
    "street": "123 Main Street",
    "city": "Denver",
    "state_or_province": "CO",
    "country": "US",
    "postal_code": "80209",
    "spread_table": "flat_0.00",
    "legal_entity_type": "company",
    "created_at": "2025-03-25T15:22:47.276+00:00",
    "updated_at": "2025-03-25T15:22:47.275+00:00",
    "identification_type": "incorporation_number",
    "identification_value": "123456789",
    "short_reference": "210325-03783",
    "api_trading": true,
    "online_trading": true,
    "phone_trading": true,
    "process_third_party_funds": false,
    "settlement_type": "net",
    "agent_or_reliance": false,
    "terms_and_conditions_accepted": null
}
```

From the response payload  you will need to parse and retain the Account UUID, (`id`) parameter from the above example.  This value will be used in the next API call to create a contact on this specific sub-account. 

## Step 2: Create a Contact

The next step is to create a contact for the new sub-account you just created using the [Create Contact](/api-reference/#create-contact) endpoint. Creating a contact that is attached to the sub-account will allow you to conduct a conversion, payment, and reporting activity at the sub-account level. 

Please be aware that `login_id` must be unique, `email_address` is used if no `login_id` is specified.

An example of a successful request and response payload looks like this:

**`POST /v2/contacts/create`**

| **Parameter Name** | **Parameter Type** | **Example Value** |
| --- | --- | --- |
| `account_id` | Form Data | `53d15949-b1e9-4335-a4e4-56ae8adef95e` |
| `first_name` | Form Data | `Eric` |
| `last_name` | Form Data | `Johnson` |
| `email_address` | Form Data | `eric@aol.com` |
| `phone_number` | Form Data | `99999999` |
| `your_reference` | Form Data | `123456789` |
| `status` | Form Data | `enabled` |
| `timezone` | Form Data | `America/New York` |
| `date_of_birth` | Form Data | `1993-01-01` |
| `X-Auth-Token` | header | `ea6d13c7bc50feb46cf978d137bc01a2` |

Response: 

```
{
    "login_id": "eric@aol.com",
    "id": "ce404ead-1936-4f54-ac2a-b26ec03d5560",
    "first_name": "Eric",
    "last_name": "Johnson",
    "account_id": "53d15949-b1e9-4335-a4e4-56ae8adef95e",
    "account_name": "Jimmy's Burritos",
    "status": "enabled",
    "locale": "en",
    "timezone": "America\/New_York",
    "email_address": "eric@aol.com",
    "mobile_phone_number": null,
    "phone_number": "99999999",
    "your_reference": "123456789",
    "date_of_birth": "1993-01-01",
    "created_at": "2025-03-25T15:45:22.325+00:00",
    "updated_at": "2025-03-25T15:45:22.320+00:00"
}

```

You will need to parse and obtain the `id` parameter from the example response payload above. This value will be used for the `on_behalf_of` parameter for subsequent API calls. 

## Making a conversion on behalf of your customer

## Step 1: Get a quote on behalf of your customer

This basic flow assumes that the sub-account has available funds in a multi currency account. For testing purposes in our Demo environment, please work with your dedicated Solutions Consultant so they can assist you in having fake funds credited to individual sub-account wallets.  

Let's see how much it will cost to buy 10,000 EUR using funds from your customer's GBP balance, by making a call to the [Get Detailed Rates](/api-reference/#get-detailed-rates) endpoint.

**`GET /v2/rates/detailed`**

| **Parameter Name** | **Parameter Type** | **Example Value** |
| --- | --- | --- |
| buy_currency | Query String | EUR |
| sell_currency | Query String | GBP |
| amount | Query String | 10000.00 |
| fixed_side | Query String | buy |
| on_behalf_of | Query String | ce404ead-1936-4f54-ac2a-b26ec03d5560 |
| X-Auth-Token | Header | ea6d13c7bc50feb46cf978d137bc01a2 |

On success, the response payload will contain details of Currencycloud's quotation to make the conversion on behalf of your customer. The following example tells you that your customer can sell £8037.00 to buy €10,000. Please note, the quote is only indicative and a conversion must be booked to lock a rate.

```
{

    "settlement_cut_off_time": "2025-03-29T14:30:00Z",
    "currency_pair": "EURGBP",
    "client_buy_currency": "EUR",
    "client_sell_currency": "GBP",
    "client_buy_amount": "10000.00",
    "client_sell_amount": "8037.00",
    "fixed_side": "buy",
    "client_rate": "0.8037",
    "partner_rate": null,
    "core_rate": "0.8037",
    "deposit_required": false,
    "deposit_amount": "0.0",
    "deposit_currency": "GBP",
    "mid_market_rate": "0.8036"
}
```

##  Step 2: Making a conversion on behalf of your customer

If you and your customer are happy with the quote, you can create the conversion for your customer by calling the [Create Conversion](/api-reference/#create-conversion) endpoint.

Optionally, you may provide an idempotency key (via the `unique_request_id` parameter). This helps protect against accidental duplicate conversions.

**`POST /v2/conversions/create`**

| **Parameter Name** | **Parameter Type** | **Example Value** |
| --- | --- | --- |
| buy_currency | Form Data | EUR |
| sell_currency | Form Data | GBP |
| amount | Form Data | 10000.00 |
| fixed_side | Form Data | buy |
| reason | Form Data | Top up Euros balance |
| term_agreement | Form Data | true |
| on_behalf_of | Form Data | ce404ead-1936-4f54-ac2a-b26ec03d5560 |
| unique_request_id | Form Data | 5f022044-1277-4f7e-a68e-c68783647748 |
| X-Auth-Token | Header | ea6d13c7bc50feb46cf978d137bc01a2 |

On success, the payload of the response message will contain full details of the conversion as recorded against the customer's Currencycloud named sub-account. Example response: 

```
{
    "id": "0e716494-3688-499a-8391-38096582aad5",
    "settlement_date": "2025-03-29T14:30:00+00:00",
    "conversion_date": "2025-03-29T00:00:00+00:00",
    "short_reference": "20210325-XPWDTQ",
    "creator_contact_id": "ce404ead-1936-4f54-ac2a-b26ec03d5560",
    "account_id": "53d15949-b1e9-4335-a4e4-56ae8adef95e",
    "currency_pair": "EURGBP",
    "status": "awaiting_funds",
    "buy_currency": "EUR",
    "sell_currency": "GBP",
    "client_buy_amount": "10000.00",
    "client_sell_amount": "8037.00",
    "fixed_side": "buy",
    "core_rate": "0.8037",
    "partner_rate": "",
    "partner_buy_amount": "0.00",
    "partner_sell_amount": "0.00",
    "client_rate": "0.8037",
    "deposit_required": false,
    "deposit_amount": "0.00",
    "deposit_currency": "",
    "deposit_status": "not_required",
    "deposit_required_at": "",
    "payment_ids": [],
    "unallocated_funds": "10000.00",
    "unique_request_id": null,
    "created_at": "2025-03-25T20:53:47+00:00",
    "updated_at": "2025-03-25T20:53:48+00:00",
    "mid_market_rate": "0.8036"
}
```

This conversion will settle automatically on the  `settlement_date`  as long as there are sufficient funds in the sub-account's GBP balance to cover the `client_sell_amount`. Please use your Cash Manager to top up your customer's sub-account GBP balance if necessary.

## Sending a payment on behalf of your customer

Now that you have converted funds into EUR,  you can make a payment on behalf of your customer to a beneficiary. This next section will walk you through adding beneficiaries at the sub-account level, checking account balances, and making a payment. 

## Step 1: Check available balances

To find out how many Euros your customer has in their currency wallet, call the [Get Balance](/api-reference/#get-balance) endpoint, passing EUR as the third URI path parameter and include `on_behalf_of` as a query string parameter.

```
GET /v2/balances/EUR/?on_behalf_of=ce404ead-1936-4f54-ac2a-b26ec03d5560
X-Auth-Token: ea6d13c7bc50feb46cf978d137bc01a2
```

The following response shows that your customer's sub-account holds €987,456.00.

Response:

```
HTTP/1.1 200 OK

Content-Type: application/json

{
    "id": "a1c6c7dc-430c-438c-b7e2-60d33b517ab8",
    "account_id": "53d15949-b1e9-4335-a4e4-56ae8adef95e",
    "currency": "EUR",
    "amount": "987456.00",
    "created_at": "2025-03-25T21:17:08+00:00",
    "updated_at": "2025-03-25T22:02:57+00:00"
}
```

Alternatively,  you can check the balances for all foreign currencies that your customer is holding by calling the [Find Balances endpoint](/api-reference/#find-balances). Again, you will need to pass `on_behalf_of` as a query string parameter.



```
GET /v2/balances/find?on_behalf_of=ce404ead-1936-4f54-ac2a-b26ec03d5560
X-Auth-Token: ea6d13c7bc50feb46cf978d137bc01a2
```

The following response shows that your customer is holding £557,685.00, and €987,456.00 in their Currencycloud sub-account.

```
{

    "balances": [
        {
            "id": "a1c6c7dc-430c-438c-b7e2-60d33b517ab8",
            "account_id": "53d15949-b1e9-4335-a4e4-56ae8adef95e",
            "currency": "EUR",
            "amount": "987456.00",
            "created_at": "2025-03-25T21:17:08+00:00",
            "updated_at": "2025-03-25T22:02:57+00:00"
        },
        {
            "id": "e08bdda0-18b0-4425-aabe-2c3da28cca89",
            "account_id": "53d15949-b1e9-4335-a4e4-56ae8adef95e",
            "currency": "GBP",
            "amount": "557685.00",
            "created_at": "2025-03-25T21:18:22+00:00",
            "updated_at": "2025-03-25T22:02:58+00:00"
        }
    ],
    "pagination": {
        "total_entries": 2,
        "total_pages": 1,
        "current_page": 1,
        "per_page": 25,
        "previous_page": -1,
        "next_page": -1,
        "order": "created_at",
        "order_asc_desc": "asc"
    }

}
```

## Step 2: Add a beneficiary at the sub-account level

If you are a client under the Sponsored or Treasury service model and contracted with The Currency Cloud Limited, then you must [verify the beneficiary's account](/guides/integration-guides/verifying-beneficiary-account) details before creating a beneficiary.

If you and your customer know the required details, you can go ahead and create a record for the beneficiary via the [Create Beneficiary](/api-reference/#create-beneficiary) endpoint.

**`POST /v2/beneficiaries/create`**

If the beneficiary is successfully created, the response message will contain full details about the beneficiary as recorded in your customer's Currencycloud sub-account. Note the beneficiary's unique ID (`id`). You'll need this to make a payment to the beneficiary, in the next step.

Response:

```
{
    "id": "33bb1228-20fc-4569-b5b2-234c3fd9e492",
    "bank_account_holder_name": "Joe Bob",
    "name": "Joe Bob",
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
    "bank_name": "TEST BANK NAME",
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
    "creator_contact_id": "ce404ead-1936-4f54-ac2a-b26ec03d5560",
    "bank_address": [
        "TEST BANK ADDRESS",
        " NOT USING EXTERNAL SERVICE",
        " DEVELOPMENT ENVIRONMENT."
    ],
    "created_at": "2025-03-25T22:52:30+00:00",
    "updated_at": "2025-03-25T22:52:30+00:00",
    "beneficiary_external_reference": null
}
```

## Step 3: Make a payment on behalf of your customer

Create a payment by calling the [Create Payment](/api-reference/#create-payment) endpoint. Optionally, you may provide an idempotency key (via the `unique_request_id` parameter). This helps protect against accidental duplicate payments.

**`POST /v2/payments/create`**

| **Parameter Name** | **Parameter Type** | **Example Value** |
| --- | --- | --- |
| currency | Form Data | EUR |
| beneficiary_id | Form Data | 33bb1228-20fc-4569-b5b2-234c3fd9e492 |
| amount | Form Data | 10000 |
| reason | Form Data | Invoice Payment |
| payment_type | Form Data | regular |
| reference | Form Data | 2021-014 |
| on_behalf_of | Form Data | ce404ead-1936-4f54-ac2a-b26ec03d5560 |
| unique_request_id | Form Data | 5f022044-1277-4f7e-a68e-c68783647748 |
| X-Auth-Token | Header | ea6d13c7bc50feb46cf978d137bc01a2 |

If the payment is successfully queued, the response payload will contain all the information about the payment as recorded in your customer's Currencycloud sub-account. This does not mean that the payment has been made, it just means that it is ready for processing.

Response:

```
{
    "id": "33efe062-ead2-4781-81a7-72563475603f",
    "amount": "10000.00",
    "beneficiary_id": "33bb1228-20fc-4569-b5b2-234c3fd9e492",
    "currency": "EUR",
    "reference": "2021-014",
    "reason": "Invoice Payment",
    "status": "ready_to_send",
    "creator_contact_id": "ce404ead-1936-4f54-ac2a-b26ec03d5560",
    "payment_type": "regular",
    "payment_date": "2025-03-29",
    "transferred_at": "",
    "authorisation_steps_required": "0",
    "last_updater_contact_id": "ce404ead-1936-4f54-ac2a-b26ec03d5560",
    "short_reference": "210326-0PC0TV750",
    "conversion_id": null,
    "failure_reason": "",
    "payer_id": "45cc568d-a837-4538-b1d8-882a367c8d46",
    "payer_details_source": "account",
    "created_at": "2025-03-26T20:32:59+00:00",
    "updated_at": "2025-03-26T20:32:59+00:00",
    "payment_group_id": null,
    "unique_request_id": "5f022044-1277-4f7e-a68e-c68783647748",
    "failure_returned_amount": "0.00",
    "ultimate_beneficiary_name": null,
    "purpose_code": null,
    "charge_type": null,
    "fee_amount": null,
    "fee_currency": null
}
```
