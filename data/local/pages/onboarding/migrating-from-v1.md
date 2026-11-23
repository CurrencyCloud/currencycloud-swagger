[_metadata_:menu_title]:- "Migrate from v1"
[_metadata_:order]:- "9"
# Migrate from v1

If you onboard applicants with `/v1/forms` today, this page tells you what changes when you move to v2: the endpoints, the workflow, the new validation rules, and the response format. For the full journey, follow the page for [your flow](/guides/onboarding/overview#choose-your-flow).

## What changes

- **Forms become applications.** Every `/v1/forms` path has a `/v2/applications` equivalent, and `form_id` becomes `application_id`. Your token and the base URL stay the same.
- **You move through a workflow.** On v1 you send the data, then submit. On v2 every application has a [workflow](/guides/onboarding/workflows): you send each step's data, then complete the step, one step at a time.
- **Some rules are stricter.** v2 refuses some values that v1 accepts. See [New validation rules](#new-validation-rules).
- **You can verify identity through the API.** After you submit, `POST /v2/identity_verifications` gives you a link to a hosted page where the person verifies their identity.
- **Responses are more consistent.** Lists are wrapped in `data`, deletes return `204`, and each error names the field it's about.

## Endpoint map

Each v2 path takes the same methods as its v1 path. The second table lists what v2 adds.

| **Resource** | **v1** | **v2** |
|---|---|---|
| Applications | `/v1/forms`, `/v1/forms/{form_id}` | `/v2/applications`, `/v2/applications/{application_id}` |
| Submit | `/v1/forms/{form_id}/submit` | `/v2/applications/{application_id}/submit` |
| People | `/v1/forms/{form_id}/people`, `.../people/{person_id}` | `/v2/applications/{application_id}/people`, `.../people/{person_id}` |
| Account usage | `/v1/forms/{form_id}/account_usage` | `/v2/applications/{application_id}/account_usage` |
| Business information | `/v1/forms/{form_id}/business_information` | `/v2/applications/{application_id}/business_information` |
| Documents | `/v1/forms/{form_id}/documents`, `.../documents/{document_id}` | `/v2/applications/{application_id}/documents`, `.../documents/{id}` |
| Document files | `.../documents/{document_id}/document_images`, `.../document_images/{document_image_id}` | `.../documents/{document_id}/document_files`, `.../document_files/{id}` |

Some endpoints are new on v2:

| **Endpoint** | **What it does** |
|---|---|
| `GET /v2/applications/{application_id}/documents/{id}` | Reads one document |
| `PUT /v2/workflows/{workflow_id}/steps/{step_id}/completion` | Completes a step |
| `GET /v2/workflows/{workflow_id}/steps/current` | Tells you which step you're on |
| `GET /v2/workflows/{workflow_id}/steps/previous` | Tells you the step before the one you're on |
| `PUT /v2/workflows/{workflow_id}/steps/current` | Moves you to a step you've completed, or to any step before the one you're on |
| `POST /v2/identity_verifications` | Starts identity verification, once the application is submitted |

`POST /v1/validations`, which runs the pre-flight validations you ask for before you create an application, stays on v1. It takes the same token and works for v2 applications too.

## Create the application

`POST /v2/applications` takes fewer fields than `POST /v1/forms`. Send the rest with your first update:

| **Field** | **On v2** |
|---|---|
| `entity_type`, `email`, `agreed_to_terms_and_conditions` | Required at create, as on v1 |
| `business_role` | Required at create on a corporate application |
| `country`, `phone_number`, `contact_name`, `agreed_to_marketing_emails`, `agreed_to_corporate_authority`, `affiliate_code`, `referred_by` | Send with `PUT /v2/applications/{application_id}`, before you complete the first step |

Create only takes the fields in the first three rows, so move the fields in the last row from your v1 create body into that update.

**`email`, `agreed_to_terms_and_conditions` and `business_role` are fixed at create.** On v1 you could change them with an update. On v2 you can't, so collect them, and the applicant's consent, before you create the application.

**The create response is new.** It returns the application's ID, its workflow's ID and the first step, at the top level:

```
201 Created
{
  "application_id": "3f1c2a8e-…",
  "workflow_id": "9b7d4e10-…",
  "steps": ["basic_info"]
}
```

You need `application_id` on every call and `workflow_id` on every workflow call, so save both straight away.

## Complete the workflow

**Every step is two calls.** You send the step's data with the same kind of call you use on v1, then complete the step:

```
PUT /v2/workflows/{workflow_id}/steps/{step_id}/completion?application_id={application_id}

{ "status": "completed" }
```

These are the steps, in order:

| **Individual** | **Corporate** | **You send first** |
|---|---|---|
| `basic_info` | `basic_info_corp` | `PUT /v2/applications/{application_id}` |
| — | `business_information_corp` | `PUT .../business_information` |
| `personal_details` | — | `POST .../people` |
| `account_usage` | `account_usage_corp` | `PUT .../account_usage` |
| — | `people_corp` | `POST .../people`, once per person |
| `documents` | `documents_corp` | `POST .../documents`, then `POST .../document_files`, then attach them with `document_ids` |
| `form_submit` | `form_submit_corp` | `POST .../submit` |

**Submitting only works once every earlier step is complete.** Then complete `form_submit` or `form_submit_corp`, and the workflow is finished.

Before a step will complete, the data behind it is checked. See [What each step checks](/guides/onboarding/workflows#what-each-step-checks-before-it-will-complete) for what each step needs, and [Workflows](/guides/onboarding/workflows) for how to go back a step.

## Update a resource

**`PUT` replaces, as on v1.** Send the full body every time, not just the fields you're changing. A field you leave out is cleared.

One thing is new on the application. Once `country`, `phone_number`, `contact_name`, `agreed_to_marketing_emails` or `agreed_to_corporate_authority` has a value, leaving it out keeps that value, and sending it as `null` is refused. See [Key concepts](/guides/onboarding/overview#key-concepts) for every exception.

## Documents

You attach documents by listing their IDs in `document_ids` on the person, account usage or business information, as on v1. What's different:

- **Files are `document_files`.** Upload them with `POST .../documents/{document_id}/document_files`, and send the content as `file`, where v1 used `image`.
- **A document takes up to 3 files**, where v1 allowed 19.
- **A two-sided document needs both sides first.** `driving_licence`, `residence_id`, `state_id` and `biometric_state_id` take one `front` and one `back`, and you can only list them in `document_ids` once both are uploaded.
- **A document in a list doesn't include its files.** Call `GET .../documents/{document_id}/document_files` to list them. `document_image_ids`, `form_section_type` and `form_section_id` are gone.

## Verify identity

Identity verification is a call of its own on v2. Once the application is submitted, call `POST /v2/identity_verifications` with its `application_id` and the `person_id` of the person to verify. It returns a `whitelabel_url`, a hosted page where that person proves who they are.

- On an individual application, you verify the applicant.
- On a corporate application, you verify a director. Only a person with the `director` role can be verified.

People on v2 don't take `impersonation_check_required`: identity verification is its own call. Your flow page shows the call in full.

## New validation rules

These rules are new on v2, so a request that v1 accepted can be refused with a `422` that names the field. Every other rule is the same on both versions.

### The application

| **Field** | **Rule** |
|---|---|
| `email`, `agreed_to_terms_and_conditions`, `business_role` | Set at create, and can't be changed afterward |
| `business_role` | Required at create on a corporate application |
| `contact_name` | Between 2 and 100 characters, using the same characters as a person's name. Required on a corporate application |
| `phone_number` | E.164 format, such as `+447700900123`. A `+44` or `+1` number has 10 digits after the country code. On a corporate application it's required every time you update the application, where v1 only required it at submit |
| `country`, `phone_number`, `contact_name`, `agreed_to_marketing_emails`, `agreed_to_corporate_authority` | Once set, can't be cleared with `null` |
| `country` | On an individual application, must match the applicant's `home_country` |

### People

| **Field** | **Rule** |
|---|---|
| `first_name`, `middle_name`, `last_name` | Only the letters `A`–`Z`, accented letters from Western European languages, such as `é`, `ñ` or `ü`, spaces, apostrophes, hyphens and periods. No digits |
| `first_name`, `last_name` | Up to 100 characters each, and not an initial, such as `J` or `J.` |
| `last_name` | On an individual application, can't end in a company signifier such as `Ltd` |
| `dob` | Must give an age between 18 and 100. The upper limit is new |
| `roles` | On an individual application, `user` only. On a sole trader application, the one person holds `user`, `director` and `ultimate_business_owner` |
| `ownership_percentage` | At least 25 for an `ultimate_business_owner`. All owners together can't exceed 100 |
| `home_country` | On an individual application, must match the country of the applicant's `personal_address` and the application's `country` |

### Addresses

| **Field** | **Rule** |
|---|---|
| `postal_code` | At most 12 characters, where v1 allowed 20 |
| `building_number` | At most 10 characters |

### Business information

| **Field** | **Rule** |
|---|---|
| `business_website` | Required |
| `vat_number` | For a business registered in the US, the EIN: 9 digits, written as `123456789` or `12-3456789`. Also required for the legal entity types `other` and `unincorporated_partnership` |
| `legal_entity_type` | `sole_trader` if, and only if, `business_role` is `sole_trader_business_role` |

### Account usage

| **Field** | **Rule** |
|---|---|
| `estimated_monthly_transaction_currency`, `estimated_monthly_transaction_value` | Required every time you send the account usage, on individual and corporate applications |
| `estimated_monthly_transaction_volume`, `transaction_countries` | Required every time you send the account usage, on a corporate application |
| `estimated_monthly_transaction_value`, `estimated_monthly_transaction_volume` | Zero or more |
| `purpose_details` | Required when `primary_purpose` is `other` |

### Document files

| **What** | **Rule** |
|---|---|
| Files on a document | At most 3 |
| A two-sided document | One `front` and one `back`, both uploaded before you list it in `document_ids` |

## Responses

| **Response** | **v1** | **v2** |
|---|---|---|
| A list | Under `forms`, `people`, `documents` or `document_images` | Under `data` |
| A single resource | Under `data` | Under `data`, as on v1 |
| Create the application | The application, under `data` | `application_id`, `workflow_id` and `steps`, at the top level |
| Read the application | Includes its `people`, `account_usage` and `business_information` | The application only. Read each of those with its own `GET` |
| A person, account usage or business information | Carries `form_id` | Carries `application_id` |
| A delete | `200`, with a message | `204`, with no body |
| Deleting account usage or business information that doesn't exist | `200` | `404` |

The workflow endpoints and identity verification also return their fields at the top level.

## Errors

**Each error names its field.** v1 reported a request it couldn't accept as one block of text. v2 reports each field under its own key, with a stable `error_code`. Here's the same business information, sent without `company_name`. On v1:

```
422 Unprocessable Content
{
  "status": "failed",
  "error_code": "request_invalid",
  "reason": "Request validation error",
  "error_messages": {
    "request_body_json": [
      {
        "error_code": "validation",
        "reason": "[\"The property '#/' did not contain a required property of 'company_name'\"]"
      }
    ]
  }
}
```

On v2:

```
422 Unprocessable Content
{
  "status": "failed",
  "error_code": "record_invalid",
  "reason": "Record invalid",
  "error_messages": {
    "company_name": [
      {
        "error_code": "missing",
        "reason": "Company name is required"
      }
    ]
  }
}
```

- **A missing field is usually `missing`**, where v1 said `blank`.
- **A nested field has a dotted key**, such as `personal_address.country`.
- **Treat `error_code` as an open set**: new codes can be added.

Two status codes are new. A `409` means the workflow refused the call, such as completing a step that isn't the current one. A `502` means a temporary failure on our side. Before you retry it, check whether the first call landed: see [Is it safe to retry a call?](/guides/onboarding/faq#is-it-safe-to-retry-a-call).
