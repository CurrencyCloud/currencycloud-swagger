[_metadata_:menu_title]:- "Onboard a business: authorised person"
[_metadata_:order]:- "6"
# Onboard a business: authorised person

Use this flow when someone who isn't a director fills in the application on the company's behalf. If a director fills it in themselves, use [Onboard a business: director](/guides/onboarding/corporate-director). If a sole trader is applying, use [Onboard a business: sole trader](/guides/onboarding/corporate-sole-trader).

Two people take part:

| **Person** | **What they do** |
|---|---|
| The authorised person | The applicant. They fill in the application, confirm they can act for the company, and submit it |
| A director | They verify their email address and their identity on a link you send them once the application is submitted. Only they can do this |

The application also lists the company's other directors and its ultimate business owners.

## The steps at a glance

| **Step** | **You send** | **Then complete** |
|---|---|---|
| [1. Create the application](#step-1-create-the-application) | `POST /v2/applications` | — |
| [2. Applicant details](#step-2-applicant-details) | `PUT /v2/applications/{application_id}` | `basic_info_corp` |
| [3. Business information](#step-3-business-information) | `PUT /v2/applications/{application_id}/business_information` | `business_information_corp` |
| [4. Account usage](#step-4-account-usage) | `PUT /v2/applications/{application_id}/account_usage` | `account_usage_corp` |
| [5. People](#step-5-people) | `POST /v2/applications/{application_id}/people` once per person | `people_corp` |
| [6. Documents](#step-6-documents) | `POST .../documents` then `POST .../document_files` | `documents_corp` |
| [7. Submit](#step-7-submit) | `POST /v2/applications/{application_id}/submit` | `form_submit_corp` |
| [8. Verify the director's identity](#step-8-verify-the-directors-identity) | `POST /v2/identity_verifications` then send the link to the director | — |

Every completion call has the same shape. Only the `step_id` changes:

```
PUT /v2/workflows/{workflow_id}/steps/{step_id}/completion?application_id={application_id}

{ "status": "completed" }
```

It returns the next step, and an empty `steps` array once the workflow is finished:

```
200 OK
{
  "application_id": "3f1c2a8e-…",
  "workflow_id": "9b7d4e10-…",
  "steps": ["business_information_corp"]
}
```

The [API reference](/api-reference/) lists every field and its format.

## Step 1: Create the application

Creates the application and its workflow, and records the applicant's email, consent and business role.

`POST /v2/applications`

```
{
  "entity_type": "corporate",
  "email": "alex.jones@example.com",
  "agreed_to_terms_and_conditions": true,
  "business_role": "authorised_person"
}
```

```
201 Created
{
  "application_id": "3f1c2a8e-…",
  "workflow_id": "9b7d4e10-…",
  "steps": ["basic_info_corp"]
}
```

These four fields are the complete create request for this flow. `email`, `agreed_to_terms_and_conditions` and `business_role` can't be changed afterward.

**Store both IDs.** You need `application_id` on every call, and `workflow_id` on every workflow call, so save both now.

There's nothing to complete for this step. The workflow starts at `basic_info_corp`.

## Step 2: Applicant details

Records how to reach the applicant, and their confirmation that they can act for the company.

### 2a. Send the applicant details

`PUT /v2/applications/{application_id}`

```
{
  "country": "GB",
  "phone_number": "+447700900456",
  "contact_name": "Alex Jones",
  "agreed_to_marketing_emails": false,
  "agreed_to_corporate_authority": true
}
```

PUT replaces the application, so send the full body every time you update it.

### 2b. Complete `basic_info_corp`

```
PUT /v2/workflows/{workflow_id}/steps/basic_info_corp/completion?application_id={application_id}

{ "status": "completed" }
```

The step needs `country`, `contact_name`, `agreed_to_marketing_emails` and `agreed_to_corporate_authority` on the application, plus the `email`, consent and `business_role` you gave at create.

## Step 3: Business information

Describes the company: what it is, where it's registered and what it does.

### 3a. Send the business information

`PUT /v2/applications/{application_id}/business_information`

```
{
  "company_name": "Example Trading Ltd",
  "business_country": "GB",
  "legal_entity_type": "limited_liability_company",
  "sector": "computer_software",
  "company_registration_number": "12345678",
  "vat_number": "GB123456789",
  "incorporation_date": "2019-04-01",
  "business_website": "https://example.com",
  "registered_address_attributes": {
    "building_number": "1",
    "street": "High Street",
    "city": "London",
    "postal_code": "EC1A 1BB",
    "country": "GB"
  }
}
```

Use any `legal_entity_type` except `sole_trader`, which belongs to the [sole trader flow](/guides/onboarding/corporate-sole-trader).

Whether the registration and VAT numbers are required depends on where the company is registered and its legal entity type:

| **If `business_country` is** | **`company_registration_number` is required for** | **`vat_number` is required for** |
|---|---|---|
| `GB` | `limited_liability_company`, `limited_liability_partnership`, `public_limited_company`, `registered_charity`, `scottish_limited_partnership` | `limited_liability_company`, `limited_liability_partnership`, `public_limited_company`, `scottish_limited_partnership` |
| `US` | `limited_liability_company`, `limited_liability_partnership`, `public_limited_company`, `registered_charity`, `trust` | `limited_liability_company`, `limited_liability_partnership`, `public_limited_company`, `registered_charity`, `trust`, `unincorporated_partnership`, `other` |
| Any other country | `limited_liability_company`, `limited_liability_partnership`, `public_limited_company`, `registered_charity` | `limited_liability_company`, `limited_liability_partnership`, `public_limited_company` |

For a company registered in the US, `vat_number` holds its EIN: 9 digits, written as `123456789` or `12-3456789`.

An address in the United States or Canada also needs its `state_or_province`: the two-letter state or province code, such as `NY` or `ON`.

PUT replaces the business information, so send the full body every time you update it.

### 3b. Complete `business_information_corp`

```
PUT /v2/workflows/{workflow_id}/steps/business_information_corp/completion?application_id={application_id}

{ "status": "completed" }
```

The step needs the business information from 3a, with its registered address in a permitted jurisdiction.

## Step 4: Account usage

Describes how the company intends to use the account.

### 4a. Send the account usage

`PUT /v2/applications/{application_id}/account_usage`

```
{
  "collections_account": false,
  "collection_currencies": ["GBP"],
  "payment_currencies": ["EUR", "USD"],
  "transaction_countries": ["DE", "US"],
  "source_of_funds": "business_revenue",
  "primary_purpose": "paying_suppliers_or_bills",
  "estimated_monthly_transaction_currency": "GBP",
  "estimated_monthly_transaction_value": 50000,
  "estimated_monthly_transaction_volume": 20
}
```

`purpose_details` is required when `primary_purpose` is `other`, and `initial_capital` when the company was incorporated in the last 12 months.

PUT replaces the account usage, so send the full body every time you update it.

### 4b. Complete `account_usage_corp`

```
PUT /v2/workflows/{workflow_id}/steps/account_usage_corp/completion?application_id={application_id}

{ "status": "completed" }
```

The step needs the account usage from 4a, with `initial_capital` if the company was incorporated in the last 12 months.

## Step 5: People

Adds everyone the application needs: the authorised person, the director who will be verified, the company's other directors, and its ultimate business owners.

| **Role** | **Who holds it** |
|---|---|
| `user` | The applicant. At least one person must hold it |
| `director` | A director of the company. At least one person must hold it, and only a director's identity can be verified |
| `ultimate_business_owner` | Someone who owns 25% or more of the company |

Add each person once, with all of their roles. In this flow the authorised person isn't a director, so they hold `user` but not `director`.

### 5a. Add the authorised person

`POST /v2/applications/{application_id}/people`

```
{
  "roles": ["user"],
  "first_name": "Alex",
  "last_name": "Jones",
  "dob": "1990-03-22",
  "email": "alex.jones@example.com",
  "phone_number": "+447700900456",
  "home_country": "GB",
  "citizenship": "GB",
  "personal_address_attributes": {
    "building_number": "22",
    "street": "Mill Lane",
    "city": "London",
    "postal_code": "N1 7AB",
    "country": "GB"
  }
}
```

The response returns the person under `data`. Keep `data.id`: it's the `person_id` you need in step 6.

The authorised person holds `user`. Add `ultimate_business_owner` too if they own 25% or more, with their `ownership_percentage`.

Some fields depend on where the authorised person lives:

| **If** | **Also required** |
|---|---|
| `home_country` is the United States | `id_number`: their 9-digit Social Security number |
| The address is in the United States or Canada | `personal_address_attributes.state_or_province`: the two-letter state or province code, such as `NY` or `ON` |

<span id="5b-add-the-director"></span>

### 5b. Add the director

Add the director who will be verified with the same call, including their own email address and date of birth:

```
{
  "roles": ["director"],
  "first_name": "Jane",
  "last_name": "Smith",
  "dob": "1985-06-15",
  "email": "jane.smith@example.com",
  "home_country": "GB",
  "citizenship": "GB"
}
```

The director holds `director`. Add `ultimate_business_owner` too if they own 25% or more, with their `ownership_percentage`.

Send both `email` and `dob` now: the identity check in step 8 needs them, and people can't be changed once the application is submitted.

Keep `data.id` from the response: it's the director's `person_id`, which you need in steps 6 and 8.

### 5c. Add the other directors and owners

Add every other director, and every ultimate business owner, with the same call. A person who isn't a `user` needs only their names, countries and roles, plus `ownership_percentage` for an owner:

```
{
  "roles": ["ultimate_business_owner"],
  "first_name": "Sam",
  "last_name": "Patel",
  "home_country": "GB",
  "citizenship": "GB",
  "ownership_percentage": 40
}
```

Give each person `director`, `ultimate_business_owner` or both. An owner needs an `ownership_percentage` of at least 25, and all owners together can't exceed 100.

An application holds at most 50 people. To correct someone's details, update them with [Update Person](/api-reference/#update-person) and the full body, including `document_ids` once you've attached documents.

### 5d. Complete `people_corp`

```
PUT /v2/workflows/{workflow_id}/steps/people_corp/completion?application_id={application_id}

{ "status": "completed" }
```

The step needs at least one `user` and one `director`. Every `user` needs their `dob`, `email` and `personal_address`, and the address must be in a permitted jurisdiction.

## Step 6: Documents

Uploads the documents for the company and its people, and attaches each one to what it's evidence for.

### What to upload

[Onboard a business](/guides/onboarding/corporate#documents) lists the documents a company needs. Upload everything you have: our compliance review decides what's finally needed.

### 6a. Create the document

`POST /v2/applications/{application_id}/documents`

```
{
  "document_type": "passport",
  "category": "proof_of_identity"
}
```

`category` says what the document is evidence of, and decides where you attach it in 6c:

| **Document** | **`category`** | **Attach it to** |
|---|---|---|
| Photo ID of a director or owner | `proof_of_identity` | That person |
| Proof of address of a director or owner | `proof_of_address` | That person |
| Registration documents, such as a certificate of incorporation or a companies register extract | `proof_of_business_identity` | The business information |
| Lists of directors and of shareholders | `proof_of_directors`, `proof_of_owners` | The business information |
| Source of funds, such as financial statements or corporate bank statements | `proof_of_source_of_funds` | The account usage |

Every `document_type` and `category` value is listed in the [API reference](/api-reference/), and the [document types endpoint](#reference-data) returns the photo ID types a country accepts.

Keep `data.id` from the response: it's the `document_id`.

### 6b. Upload its files

`POST /v2/applications/{application_id}/documents/{document_id}/document_files`

```
{
  "file": "<base64-encoded file>",
  "side": "front"
}
```

| **Rule** | |
|---|---|
| File type and size | JPG, PNG or PDF, up to 10MB |
| Files per document | At most three. `side` is `front`, `back` or `face` (a selfie of the person) |
| Two-sided documents | `driving_licence`, `residence_id`, `state_id` and `biometric_state_id` need both `front` and `back`, one image each. To replace either side, delete its image and upload again |
| Image quality | Files on a `proof_of_identity` document are quality-checked on upload. Use a clear photo that shows the whole document |

### 6c. Attach the documents

Send each resource again with its document IDs in `document_ids`. PUT replaces the resource, so send its full body:

| **Attach to** | **Call** |
|---|---|
| A person | `PUT /v2/applications/{application_id}/people/{person_id}` |
| The business information | `PUT /v2/applications/{application_id}/business_information` |
| The account usage | `PUT /v2/applications/{application_id}/account_usage` |

For example, the director's photo ID:

```
{
  "roles": ["director"],
  "first_name": "Jane",
  "last_name": "Smith",
  …
  "document_ids": ["5d2e8f61-…"]
}
```

`document_ids` is the complete list: an ID you leave out is detached, not deleted. A two-sided document must have both sides uploaded before you can attach it. Each resource holds up to 20 documents. Attach each photo ID to the person it identifies.

You can also upload documents earlier and send `document_ids` when you first send the person, business information or account usage.

### 6d. Complete `documents_corp`

```
PUT /v2/workflows/{workflow_id}/steps/documents_corp/completion?application_id={application_id}

{ "status": "completed" }
```

## Step 7: Submit

Sends the application for compliance review.

### 7a. Submit the application

`POST /v2/applications/{application_id}/submit`

Complete steps 2 to 6 first: submit checks every earlier step is complete, then validates the whole application.

**Submitting is final.** The application is locked once submitted, so review it before you make this call.

<span id="7b-complete-form_submit_corp"></span>

### 7b. Complete `form_submit_corp`

```
PUT /v2/workflows/{workflow_id}/steps/form_submit_corp/completion?application_id={application_id}

{ "status": "completed" }
```

Submit first: this step checks the application has already been submitted. Once it completes, `steps` comes back empty and the workflow is finished. Then verify the director's identity in [step 8](#step-8-verify-the-directors-identity).

## Step 8: Verify the director's identity

The director proves they are who they say they are, using their photo ID and a selfie. You start the verification and send the director its link, and the director completes it. Only a person with the `director` role can be verified, and only once the application is submitted.

### 8a. Start the director's verification

`POST /v2/identity_verifications`

```
{
  "application_id": "3f1c2a8e-…",
  "person_id": "7a4b9c21-…"
}
```

```
200 OK
{
  "whitelabel_url": "https://…"
}
```

`person_id` is the director's, from [5b](#5b-add-the-director). Calling this again returns the same verification, so it's safe to retry. Each call also emails the link to the director again.

### 8b. Send the link to the director

We email `whitelabel_url` to the director's `email` when you start the verification. Send it to them yourself as well, for example by email.

The director opens the link in their own browser. The hosted page verifies their email address, then takes them through the terms and biometric consent, and the identity check itself.

### 8c. Email verification

The hosted page asks the director for their email address, then emails a one-time code to it. It must be the email address you gave for them in [5b](#5b-add-the-director): an address that isn't on the application is refused. They enter the code on the page to verify the address.

**Only the director can do this.** The API has no call to send, enter or skip the code, so you can't complete this step for them or automate it. Send the link to the director only: only the address you gave for them lets them through to the identity check.

There's no step to complete here: `id_verification` completes on its own when you complete `form_submit_corp` in [7b](#7b-complete-form_submit_corp).

## After submission

The application's `state` moves from `submitted` to `approved` or `rejected` once our review is done. To be told when that happens, subscribe to the `end_client_application_decisioned_notification` [push notification](/guides/platform-specifics/push-notifications/), or read `state` from [Get Application](/api-reference/#get-application).

See [Troubleshooting & FAQ](/guides/onboarding/faq) for what to do if an application stalls.

## Reference data

These endpoints list the values the rules above check against. They're on v1, take the same token, and work for any application.

| **Endpoint** | **Returns** |
|---|---|
| `GET /v1/countries` | Every country, with its `permitted_jurisdiction` flag |
| `GET /v1/countries/{country_code}/document_types` | The photo ID types a country accepts, such as `passport` or `driving_licence` |
| `GET /v1/currencies/supported` | The supported currency codes |
