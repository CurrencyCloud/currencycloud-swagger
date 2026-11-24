[_metadata_:menu_title]:- "Onboarding an individual"
[_metadata_:order]:- "3"
# Onboarding an individual

Use this flow to open an account for a single person applying on their own behalf, rather than for a company.

An individual application has exactly **one person**: the applicant. The applicant completes the application, accept the terms, and are the person whose identity is verified at the end.

## The steps at a glance

| **Step** | **You send** | **Then complete** |
|---|---|---|
| [1. Create the application](#step-1-create-the-application) | `POST /v2/applications` | — |
| [2. Applicant details](#step-2-applicant-details) | `PUT /v2/applications/{application_id}` | `basic_info` |
| [3. Personal details](#step-3-personal-details) | `POST /v2/applications/{application_id}/people` | `personal_details` |
| [4. Account usage](#step-4-account-usage) | `PUT /v2/applications/{application_id}/account_usage` | `account_usage` |
| [5. Documents](#step-5-documents) | [Create Document](/api-reference/#create-document), then [Create Document File](/api-reference/#create-document-file) | `documents` |
| [6. Submit](#step-6-submit) | `POST /v2/applications/{application_id}/submit` | `form_submit` |
| [7. Verify the applicant's identity](#step-7-verify-the-applicants-identity) | `POST /v2/identity_verifications` | — |

Every completion request uses the same endpoint and request body. Only the `step_id` changes:

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
  "steps": ["personal_details"]
}
```

The [API reference](/api-reference//#onboard) lists every field and its format.

## Step 1: Create the application

Creates the application and its workflow, and records the applicant's email address and consent.

`POST /v2/applications`

```
{
  "entity_type": "individual",
  "email": "jane.smith@example.com",
  "agreed_to_terms_and_conditions": true
}
```

```
201 Created
{
  "application_id": "3f1c2a8e-…",
  "workflow_id": "9b7d4e10-…",
  "steps": ["basic_info"]
}
```

These three fields are the complete create request for an individual. `email` and `agreed_to_terms_and_conditions` can't be changed afterward.

**Store both IDs.** You need `application_id` on every call, and `workflow_id` on every workflow call, so save both now.

There's nothing to complete for this step. The workflow starts at `basic_info`.

## Step 2: Applicant details

Records where the applicant lives and how to reach them.

### 2a. Send the applicant details

`PUT /v2/applications/{application_id}`

```
{
  "country": "GB",
  "phone_number": "+447700900123",
  "agreed_to_marketing_emails": false
}
```

Note that `country` must be a permitted jurisdiction and must match the `home_country` and address country you provide in [step 3](#step-3-personal-details). `phone_number` is optional at this point, but the applicant's `phone_number` is required in step 3.

PUT replaces the application, so send the full body every time you update it.

### 2b. Complete basic_info

```
PUT /v2/workflows/{workflow_id}/steps/basic_info/completion?application_id={application_id}

{ "status": "completed" }
```

The step needs `country` and `agreed_to_marketing_emails` on the application, plus the `email` and consent you gave at create.

## Step 3: Personal details

Adds the applicant as the only person on the application.

### 3a. Add the applicant

`POST /v2/applications/{application_id}/people`

```
{
  "roles": ["user"],
  "first_name": "Jane",
  "last_name": "Smith",
  "dob": "1985-06-15",
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

The response returns the person under `data`. Keep `data.id`, this is the `person_id` you need in steps 5 and 7.

The `roles` is `["user"]`, the applicant's only role. The `home_country` must match the country in `personal_address_attributes` and the application's `country`. The address must also be in a permitted jurisdiction.

The applicant's email comes from the application and is set when you create it.

Some fields depend on where the applicant lives:

| **If the applicant's home_country is** | **Also required** |
|---|---|
| The United States | `id_number`: their 9-digit Social Security number. `personal_address_attributes.state_or_province`: the two-letter state code, such as 'NY' |
| Canada | `personal_address_attributes.state_or_province`: the two-letter province code, such as 'ON' |

An individual application has exactly one person. To correct the applicant's details, update them with [Update Person](/api-reference/#update-person) and the full body, including `document_ids` once you've attached documents.

### 3b. Complete personal_details

```
PUT /v2/workflows/{workflow_id}/steps/personal_details/completion?application_id={application_id}

{ "status": "completed" }
```

This step needs the person's `dob`, `personal_address` and email, and the address must be in a permitted jurisdiction.

## Step 4: Account usage

Describes how the applicant intends to use the account.

### 4a. Send the account usage

`PUT /v2/applications/{application_id}/account_usage`

```
{
  "collections_account": false,
  "collection_currencies": ["GBP"],
  "payment_currencies": ["EUR"],
  "source_of_funds": "salary",
  "primary_purpose": "payment_to_an_individual",
  "estimated_monthly_transaction_currency": "GBP",
  "estimated_monthly_transaction_value": 2000
}
```

`purpose_details` is required when `primary_purpose` is `other`.

`estimated_monthly_transaction_volume` and `transaction_countries` are optional for an individual.<br><br>

PUT replaces the account usage, so send the full body every time you update it.

### 4b. Complete `account_usage`

```
PUT /v2/workflows/{workflow_id}/steps/account_usage/completion?application_id={application_id}

{ "status": "completed" }
```

This step needs the account usage from 4a.

## Step 5: Documents

Uploads the applicant's documents and attaches them to the applicant.

### What to upload

| **Need** | **Documents** |
|---|---|
| Always | Photo ID, such as a passport, driver's license or national ID |
| Often | Proof of address, dated within the last 3 months |
| Can speed up approval | Source of funds, such as payslips, proof of investment or inheritance, a bank statement or a tax return |

Upload everything the applicant has, our compliance review decides what's finally needed.

### 5a. Create the document

`POST /v2/applications/{application_id}/documents`

```
{
  "document_type": "passport",
  "category": "proof_of_identity"
}
```

`category` says what the document is evidence of. For the checklist above, use `proof_of_identity` for photo ID, `proof_of_address` for proof of address, and `proof_of_source_of_funds` for source of funds. Every `document_type` and `category` value is listed in the [API reference](/api-reference/).

Keep `data.id` from the response: it's the `document_id`.

### 5b. Upload its files

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
| Files per document | At most three. `side` is `front`, `back` or `face` (a selfie of the applicant) |
| Two-sided documents | `driving_licence`, `residence_id`, `state_id` and `biometric_state_id` need both `front` and `back`, one image each. To replace either side, delete its image and upload again |
| Image quality | Files on a `proof_of_identity` document are quality-checked on upload. Use a clear photo that shows the whole document |

### 5c. Attach the documents to the applicant

Send the applicant again with the document IDs in `document_ids`. PUT replaces the person, so send the full body from step 3:

`PUT /v2/applications/{application_id}/people/{person_id}`

```
{
  "roles": ["user"],
  "first_name": "Jane",
  …
  "document_ids": ["5d2e8f61-…"]
}
```

`document_ids` is the complete list: an ID you leave out is detached, not deleted. A two-sided document must have both sides uploaded before you can attach it. Each resource holds up to 20 documents.

You can also upload documents before step 3 and send `document_ids` when you first add the applicant.

### 5d. Complete `documents`

```
PUT /v2/workflows/{workflow_id}/steps/documents/completion?application_id={application_id}

{ "status": "completed" }
```

Completing `documents` checks nothing, so it completes even if no documents were uploaded or attached: do both first. A document you don't attach with `document_ids` is submitted as a general file, not as the applicant's document.

## Step 6: Submit

Sends the application for compliance review. This takes two calls, in this order:

- **6a submits the application.** It locks the application and starts our compliance review. It does not advance the workflow.
- **6b completes `form_submit`.** This advances the workflow, and does not trigger anything else.

Completing `form_submit` before you've submitted is refused with a `422` response on `state`. If you stop after submitting, the workflow stays on `form_submit`.

### 6a. Submit the application

`POST /v2/applications/{application_id}/submit`

Complete steps 2 to 5 first. Submission checks that every earlier step is complete, then validates the whole application.

**Submitting is final.** The application is locked once submitted, so review it before you making this call.

<span id="6b-complete-form_submit"></span>

### 6b. Complete form_submit

```
PUT /v2/workflows/{workflow_id}/steps/form_submit/completion?application_id={application_id}

{ "status": "completed" }
```

Submit the application first. This step checks the application has already been submitted. Once it completes, `steps` is empty and the workflow is finished. Then verify the applicant's identity in [step 7](#step-7-verify-the-applicants-identity).

## Step 7: Verify the applicant's identity

The applicant proves they are who they say they are, using their photo ID and a selfie. This only works once the application is submitted.

### 7a. Start the verification

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

Use the applicant's `person_id` from step 3. Calling this endpoint again returns the same verification, so it's safe to retry.

### 7b. Send the applicant to the hosted page

Send the applicant to the `whitelabel_url`. The hosted page verifies their email address, then takes them through the terms and biometric consent, and the identity check itself.

### 7c. Email verification

The hosted page asks the applicant for their email address, then sends a one-time code to that address. It must be the email address on the application, any other address is refused. The applicant enters the code on the page to verify the address.

**Only the applicant can do this.** There is no API call to send, enter, or skip the code, so you can't complete or automate this step for them.

There's no workflow step to complete here, `id_verification` isi completed automatically when you complete `form_submit` in step [6b](#6b-complete-form_submit).

## After submission

The application's `state` moves from `submitted` to `approved` or `rejected` once our review is done. To be told when that happens, subscribe to the `end_client_application_decisioned_notification` [push notification](/guides/platform-specifics/push-notifications/), or read `state` from [Get Application](/api-reference/#get-application).

See [Troubleshooting & FAQ](/guides/onboarding/faq) for what to do if an application stalls.
