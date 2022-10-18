[_metadata_:menu_title]:- "Checking your balances"
[_metadata_:order]:- "4"

# Checking your balances
This guides shows you how to check how much money you hold in various foreign currencies in your Currencycloud account.

## TL;DR

The steps and endpoints for checking your currency balances are:
1. Get the balance for a specific currency by calling [Get Balance](/api-reference/#balances), passing the currency as a parameter.
2. Get the balances for all currencies you hold by calling [Find Balances](/api-reference/#find-balances).

Detailed instructions are given below.

## Workflow diagrams

### 1. For house-account balance:
![house account balances](/images/workflow_diagrams/10_balances_house_account.jpg)

### 2. For sub-account balance:
![sub-account balances](/images/workflow_diagrams/11_balances_sub_account.jpg)


## Integration guide

## Step 1: Login

Please refer to the [Authentication guide](/guides/integration-guides/authentication) for instructions for starting a new API session.

## Step 2: Check your balance for a specific currency

To find out how many Euros you have in your main Currencycloud account, call the [Get Balance endpoint](/api-reference/#get-balance), passing `EUR` as the currency path parameter.

```
GET /v2/balances/EUR
X-Auth-Token: ea6d13c7bc50feb46cf978d137bc01a2

```

The following response shows that you've got €15,458.12 in your main Currencycloud account.

```
HTTP/1.1 200 OK
Content-Type: application/json
{
  "id": "ad6411db-1e00-44fd-b4e8-194c74cf2f83",
  "account_id": "d22073a6-4c56-4980-8699-504b0c70003f",
  "currency": "EUR",
  "amount": "15458.12",
  "created_at": "2018-12-10T16:05:20+00:00",
  "updated_at": "2018-12-10T16:05:20+00:00"
}

```

To get a balance for any of your client sub-accounts, simply provide the sub-account UUID via the `on_behalf_of` query string parameter.

```
GET /v2/balances/EUR?on_behalf_of=d5eba0d5-ef7e-48c9-9a19-44638e2470c2
X-Auth-Token: ea6d13c7bc50feb46cf978d137bc01a2

```

## Step 3: Get detailed currency balances

Alternatively, the [Find Balances endpoint](/api-reference/#find-balances) will tell you the value of all foreign currencies that you hold in your main Currencycloud account.

```
GET /v2/balances/find
X-Auth-Token: ea6d13c7bc50feb46cf978d137bc01a2

```

The following response shows that you hold **£10,750.00**, **US$1,500.24** and **€15,458.12** in your main Currencycloud account.

```
{
  "balances": [
    {
      "id": "c52128a4-3918-40dc-a92a-7225cef3a4a6",
      "account_id": "d22073a6-4c56-4980-8699-504b0c70003f",
      "currency": "GBP",
      "amount": "10750.00",
      "created_at": "2018-12-10T16:05:19+00:00",
      "updated_at": "2018-12-10T16:05:19+00:00"
    },
    {
      "id": "349a2b87-9455-4808-9e68-515daf1f7298",
      "account_id": "d22073a6-4c56-4980-8699-504b0c70003f",
      "currency": "USD",
      "amount": "1550.24",
      "created_at": "2018-12-10T16:05:19+00:00",
      "updated_at": "2018-12-10T16:05:19+00:00"
    },
    {
      "id": "ad6411db-1e00-44fd-b4e8-194c74cf2f83",
      "account_id": "d22073a6-4c56-4980-8699-504b0c70003f",
      "currency": "EUR",
      "amount": "15458.12",
      "created_at": "2018-12-10T16:05:20+00:00",
      "updated_at": "2018-12-10T16:05:20+00:00"
    }
  ],
  "pagination": {
    "total_entries": 3,
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

To fetch balances for any of your client sub-accounts, simply provide the sub-account UUID via the `on_behalf_of` query string parameter. Further information on using `on_behalf_of` is available in our [Sub-account activity](/guides/integration-guides/sub-account-activity) guide.

```
GET /v2/balances/find?on_behalf_of=d5eba0d5-ef7e-48c9-9a19-44638e2470c2
X-Auth-Token: ea6d13c7bc50feb46cf978d137bc01a2
```
