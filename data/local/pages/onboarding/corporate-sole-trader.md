[_metadata_:menu_title]:- "Onboard a business: sole trader"
[_metadata_:order]:- "7"
# Onboard a business: sole trader

Use this flow when a sole trader applies: someone who runs a business on their own, rather than through a company. It follows the corporate steps. For a company, use [Onboard a business: director](/guides/onboarding/corporate-director) or [Onboard a business: authorised person](/guides/onboarding/corporate-authorised-person).

A sole trader application holds exactly **one person**: the sole trader. They're the applicant, the director and the owner. They fill in the application, confirm they can act for the business, and are the person whose identity is verified at the end.

## The steps at a glance

| **Step** | **You send** | **Then complete** |
|---|---|---|
| [1. Create the application](#step-1-create-the-application) | `POST /v2/applications` | — |
| [2. Applicant details](#step-2-applicant-details) | `PUT /v2/applications/{application_id}` | `basic_info_corp` |
| [3. Business information](#step-3-business-information) | `PUT /v2/applications/{application_id}/business_information` | `business_information_corp` |
| [4. Account usage](#step-4-account-usage) | `PUT /v2/applications/{application_id}/account_usage` | `account_usage_corp` |
| [5. The sole trader](#step-5-the-sole-trader) | `POST /v2/applications/{application_id}/people` | `people_corp` |
| [6. Documents](#step-6-documents) | `POST .../documents`, then `POST .../document_files` | `documents_corp` |
| [7. Submit](#step-7-submit) | `POST /v2/applications/{application_id}/submit` | `form_submit_corp` |
| [8. Verify the sole trader's identity](#step-8-verify-the-sole-traders-identity) | `POST /v2/identity_verifications` | — |

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
  "email": "jane.smith@example.com",
  "agreed_to_terms_and_conditions": true,
  "business_role": "sole_trader_business_role"
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

These four fields are the complete create request for this flow. `email`, `agreed_to_terms_and_conditions` and `business_role` can't be changed afterward, and with this `business_role`, the `legal_entity_type` you send in [step 3](#step-3-business-information) must be `sole_trader`.

**Store both IDs.** You need `application_id` on every call, and `workflow_id` on every workflow call, so save both now.

There's nothing to complete for this step. The workflow starts at `basic_info_corp`.

## Step 2: Applicant details

Records how to reach the applicant, and their confirmation that they can act for the business.

### 2.a Send the applicant details

`PUT /v2/applications/{application_id}`

```
{
  "country": "GB",
  "phone_number": "+447700900123",
  "contact_name": "Jane Smith",
  "agreed_to_marketing_emails": false,
  "agreed_to_corporate_authority": true
}
```

`PUT` replaces the application, so send the full body every time you update it.

### 2.b Complete `basic_info_corp`

```
PUT /v2/workflows/{workflow_id}/steps/basic_info_corp/completion?application_id={application_id}

{ "status": "completed" }
```

The step needs `country`, `contact_name`, `agreed_to_marketing_emails` and `agreed_to_corporate_authority` on the application, plus the `email`, consent and `business_role` you gave at create.

## Step 3: Business information

Describes the business: what it is, where it's registered and what it does.

### 3.a Send the business information

`PUT /v2/applications/{application_id}/business_information`

```
{
  "company_name": "Jane Smith Design",
  "business_country": "GB",
  "legal_entity_type": "sole_trader",
  "sector": "computer_software",
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

Send `sole_trader` as the `legal_entity_type`.

Some fields depend on where the business is:

| **If** | **Also required** |
|---|---|
| `business_country` is the United States | `company_registration_number`, and `vat_number` holding the business's EIN: 9 digits, written as `123456789` or `12-3456789` |
| An address is in the United States or Canada | That address's `state_or_province`: the two-letter state or province code, such as `NY` or `ON` |

`PUT` replaces the business information, so send the full body every time you update it.

### 3.b Complete `business_information_corp`

```
PUT /v2/workflows/{workflow_id}/steps/business_information_corp/completion?application_id={application_id}

{ "status": "completed" }
```

The step needs the business information from 3.a, with its registered address in a permitted jurisdiction.

## Step 4: Account usage

Describes how the business intends to use the account.

### 4.a Send the account usage

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

`purpose_details` is required when `primary_purpose` is `other`, and `initial_capital` when the business's `incorporation_date` is in the last 12 months.

`PUT` replaces the account usage, so send the full body every time you update it.

### 4.b Complete `account_usage_corp`

```
PUT /v2/workflows/{workflow_id}/steps/account_usage_corp/completion?application_id={application_id}

{ "status": "completed" }
```

The step needs the account usage from 4.a, with `initial_capital` if the business's `incorporation_date` is in the last 12 months.

## Step 5: The sole trader

Adds the sole trader as the application's one person.

### 5.a Add the sole trader

`POST /v2/applications/{application_id}/people`

```
{
  "roles": ["user", "director", "ultimate_business_owner"],
  "first_name": "Jane",
  "last_name": "Smith",
  "dob": "1985-06-15",
  "phone_number": "+447700900123",
  "home_country": "GB",
  "citizenship": "GB",
  "ownership_percentage": 100,
  "personal_address_attributes": {
    "building_number": "10",
    "street": "Park Road",
    "city": "London",
    "postal_code": "NW1 4SA",
    "country": "GB"
  }
}
```

The response returns the person under `data`. Keep `data.id`: it's the `person_id` you need in steps 6 and 8.

The sole trader holds all three roles, `user`, `director` and `ultimate_business_owner`, with an `ownership_percentage` between 25 and 100.

The sole trader's email comes from the application, set at create.

Some fields depend on where the sole trader lives:

| **If** | **Also required** |
|---|---|
| `home_country` is the United States | `id_number`: their 9-digit Social Security number |
| The address is in the United States or Canada | `personal_address_attributes.state_or_province`: the two-letter state or province code, such as `NY` or `ON` |

A sole trader application holds exactly one person. To correct the sole trader's details, update them with `PUT .../people/{person_id}` and the full body, including `document_ids` once you've attached documents.

### 5.b Complete `people_corp`

```
PUT /v2/workflows/{workflow_id}/steps/people_corp/completion?application_id={application_id}

{ "status": "completed" }
```

The step needs one person holding `user` and `director`, with their `dob`, `personal_address` and email, and the address must be in a permitted jurisdiction.

## Step 6: Documents

Uploads the documents for the business and the sole trader, and attaches each one to what it's evidence for.

### What to upload

[Onboard a business](/guides/onboarding/corporate#documents) lists the documents a business needs. Upload everything you have: our compliance review decides what's finally needed.

### 6.a Create the document

`POST /v2/applications/{application_id}/documents`

```
{
  "document_type": "passport",
  "category": "proof_of_identity"
}
```

`category` says what the document is evidence of, and decides where you attach it in 6.c:

| **Document** | **`category`** | **Attach it to** |
|---|---|---|
| Photo ID of the sole trader | `proof_of_identity` | The sole trader |
| Proof of address of the sole trader | `proof_of_address` | The sole trader |
| Registration documents, such as a business registration certificate | `proof_of_business_identity` | The business information |
| Source of funds, such as financial statements or business bank statements | `proof_of_source_of_funds` | The account usage |

Every `document_type` and `category` value is listed in the [API reference](/api-reference/).

Keep `data.id` from the response: it's the `document_id`.

### 6.b Upload its files

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

### 6.c Attach the documents

Send each resource again with its document IDs in `document_ids`. `PUT` replaces the resource, so send its full body:

| **Attach to** | **Call** |
|---|---|
| The sole trader | `PUT /v2/applications/{application_id}/people/{person_id}` |
| The business information | `PUT /v2/applications/{application_id}/business_information` |
| The account usage | `PUT /v2/applications/{application_id}/account_usage` |

For example, the sole trader's photo ID:

```
{
  "roles": ["user", "director", "ultimate_business_owner"],
  "first_name": "Jane",
  "last_name": "Smith",
  …
  "document_ids": ["5d2e8f61-…"]
}
```

`document_ids` is the complete list: an ID you leave out is detached, not deleted. A two-sided document must have both sides uploaded before you can attach it. Each resource holds up to 20 documents. Attach the photo ID to the sole trader.

You can also upload documents earlier and send `document_ids` when you first send the sole trader, business information or account usage.

### 6.d Complete `documents_corp`

```
PUT /v2/workflows/{workflow_id}/steps/documents_corp/completion?application_id={application_id}

{ "status": "completed" }
```

## Step 7: Submit

Sends the application for compliance review.

### 7.a Submit the application

`POST /v2/applications/{application_id}/submit`

Complete steps 2 to 6 first: submit checks every earlier step is complete, then validates the whole application.

**Submitting is final.** The application is locked once submitted, so review it before you make this call.

<span id="7b-complete-form_submit_corp"></span>

### 7.b Complete `form_submit_corp`

```
PUT /v2/workflows/{workflow_id}/steps/form_submit_corp/completion?application_id={application_id}

{ "status": "completed" }
```

Submit first: this step checks the application has already been submitted. Once it completes, `steps` comes back empty and the workflow is finished. Then verify the sole trader's identity in [step 8](#step-8-verify-the-sole-traders-identity).

## Step 8: Verify the sole trader's identity

The sole trader proves they are who they say they are, using their photo ID and a selfie. They hold the `director` role, so they can be verified once the application is submitted.

### 8.a Start the verification

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

`person_id` is the sole trader's, from step 5. Calling this again returns the same verification, so it's safe to retry.

### 8.b Send the sole trader to the hosted page

Send the sole trader to `whitelabel_url`. The hosted page verifies their email address, then takes them through the terms and biometric consent, and the identity check itself.

### 8.c Email verification

The hosted page asks the sole trader for their email address, then emails a one-time code to it. It must be the email address on the application: any other address is refused. They enter the code on the page to verify the address.

**Only the sole trader can do this.** The API has no call to send, enter or skip the code, so you can't complete this step for them or automate it.

There's no step to complete here: `id_verification` completes on its own when you complete `form_submit_corp` in [7.b](#7b-complete-form_submit_corp).

## After submission

The application's `state` moves from `submitted` to `approved` or `rejected` once our review is done. To be told when that happens, subscribe to the `end_client_application_decisioned_notification` [push notification](/guides/platform-specifics/push-notifications/), or read `state` from `GET /v2/applications/{application_id}`.

See [Troubleshooting & FAQ](/guides/onboarding/faq) for what to do if an application stalls.
