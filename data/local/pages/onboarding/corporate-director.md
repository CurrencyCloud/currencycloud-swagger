[_metadata_:menu_title]:- "Onboarding a business: director"
[_metadata_:order]:- "5"
# Onboarding a business: director

Use this flow when a director of the company is completing the application themselves. This is the usual corporate flow. If the applicant isn't a director, use [Onboarding a business: authorised person](/guides/onboarding/corporate-authorised-person). If the applicant is a sole trader, use [Onboarding a business: sole trader](/guides/onboarding/corporate-sole-trader).

The applicant is a director of the company. They provide the application details, confirm they are authorised to act for the company, and are the person whose identity is verified at the end. The application also lists the company's other directors and its ultimate business owners.

## The steps at a glance

| **Step** | **You send** | **Then complete** |
|---|---|---|
| [1. Create the application](#step-1-create-the-application) | `POST /v2/applications` | — |
| [2. Applicant details](#step-2-applicant-details) | `PUT /v2/applications/{application_id}` | `basic_info_corp` |
| [3. Business information](#step-3-business-information) | `PUT /v2/applications/{application_id}/business_information` | `business_information_corp` |
| [4. Account usage](#step-4-account-usage) | `PUT /v2/applications/{application_id}/account_usage` | `account_usage_corp` |
| [5. People](#step-5-people) | `POST /v2/applications/{application_id}/people` once per person | `people_corp` |
| [6. Documents](#step-6-documents) | [Create Document](/api-reference/#create-document), then [Create Document File](/api-reference/#create-document-file) | `documents_corp` |
| [7. Submit](#step-7-submit) | `POST /v2/identity_verifications`, then `POST /v2/applications/{application_id}/submit` | `form_submit_corp` |
| [8. Verify the director's identity](#step-8-verify-the-directors-identity) | Send the director to the `whitelabel_url` | — |

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

The [API reference](/api-reference/#onboard) lists every field and its format.

## Step 1: Create the application

Creates the application and its workflow, and records the applicant's email, consent and business role.

`POST /v2/applications`

```
{
  "entity_type": "corporate",
  "email": "jane.smith@example.com",
  "agreed_to_terms_and_conditions": true,
  "business_role": "director_controller"
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
  "phone_number": "+447700900123",
  "contact_name": "Jane Smith",
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

Adds everyone the application needs: the applicant, the company's other directors, and its ultimate business owners.

| **Role** | **Who holds it** |
|---|---|
| `user` | The applicant. At least one person must hold it |
| `director` | A director of the company. At least one person must hold it, and only a director's identity can be verified |
| `ultimate_business_owner` | Someone who owns 25% or more of the company |

Add each person once, with all of their roles. In this flow the applicant is a director, so they hold both `user` and `director`.

<span id="5a-add-the-applicant"></span>

### 5a. Add the applicant

`POST /v2/applications/{application_id}/people`

```
{
  "roles": ["user", "director"],
  "first_name": "Jane",
  "last_name": "Smith",
  "dob": "1985-06-15",
  "email": "jane.smith@example.com",
  "phone_number": "+447700900123",
  "home_country": "GB",
  "citizenship": "GB",
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

The applicant holds `user` and `director`. Add `ultimate_business_owner` too if they own 25% or more, with their `ownership_percentage`.

Some fields depend on where the applicant lives:

| **If** | **Also required** |
|---|---|
| `home_country` is the United States | `id_number`: their 9-digit Social Security number |
| The address is in the United States or Canada | `personal_address_attributes.state_or_province`: the two-letter state or province code, such as `NY` or `ON` |

### 5b. Add the other directors and owners

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

### 5c. Complete `people_corp`

```
PUT /v2/workflows/{workflow_id}/steps/people_corp/completion?application_id={application_id}

{ "status": "completed" }
```

The step needs at least one `user` and one `director`. Every `user` needs their `dob`, `email` and `personal_address`, and the address must be in a permitted jurisdiction.

## Step 6: Documents

Uploads the documents for the company and its people, and attaches each one to what it's evidence for.

### What to upload

[Onboarding a business](/guides/onboarding/corporate#documents) lists the documents a company needs. Upload everything you have: our compliance review decides what's finally needed.

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

Every `document_type` and `category` value is listed in the [API reference](/api-reference/).

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

For example, the applicant's photo ID:

```
{
  "roles": ["user", "director"],
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

Completing `documents_corp` checks nothing, so it completes even if no documents were uploaded or attached: do both first. A document you don't attach with `document_ids` is submitted as a general file, not as a person's or the business's document.

## Step 7: Submit

Sends the application for compliance review. It takes three calls, in this order:

- **7a requests identity verification.** It names the director whose identity is verified, and returns the link to the hosted page they verify on.
- **7b submits the application.** It locks the application and starts our compliance review. It doesn't move the workflow on.
- **7c completes `form_submit_corp`.** It moves the workflow on, and starts nothing else.

Completing `form_submit_corp` before you've submitted is refused with a `422` on `state`. If you stop after submitting, the workflow stays on `form_submit_corp`.

### 7a. Request identity verification

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

`person_id` is the applicant's, from step 5. Only a person with the `director` role can be verified. Calling it again returns the same verification, so it's safe to retry.

### 7b. Submit the application

`POST /v2/applications/{application_id}/submit`

Complete steps 2 to 6 and 7a first: submit checks every earlier step is complete and that identity verification has been requested, then validates the whole application.

**Submitting is final.** The application is locked once submitted, so review it before you make this call.

<span id="7c-complete-form_submit_corp"></span>

### 7c. Complete `form_submit_corp`

```
PUT /v2/workflows/{workflow_id}/steps/form_submit_corp/completion?application_id={application_id}

{ "status": "completed" }
```

Submit first: this step checks the application has already been submitted. Once it completes, `steps` comes back empty and the workflow is finished. Then the director verifies their identity in [step 8](#step-8-verify-the-directors-identity).

## Step 8: Verify the director's identity

The director proves they are who they say they are, using their photo ID and a selfie. This happens once the application is submitted.

### 8a. Send the director to the hosted page

Send the director to the `whitelabel_url` from [7a](#7a-request-identity-verification). The hosted page verifies their email address, then takes them through the terms and biometric consent, and the identity check itself.

### 8b. Email verification

The hosted page asks the director for their email address, then emails a one-time code to it. It must be the email address you gave in [5a](#5a-add-the-applicant): an address that isn't on the application is refused. They enter the code on the page to verify the address.

**Only the director can do this.** The API has no call to send, enter or skip the code, so you can't complete this step for them or automate it.

## After submission

The application's `state` moves from `submitted` to `approved` or `rejected` once our review is done. To be told when that happens, subscribe to the `end_client_application_decisioned_notification` [push notification](/guides/platform-specifics/push-notifications/), or read `state` from [Get Application](/api-reference/#get-application).

See [Troubleshooting & FAQ](/guides/onboarding/faq) for what to do if an application stalls.
