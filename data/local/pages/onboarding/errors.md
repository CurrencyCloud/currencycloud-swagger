[_metadata_:menu_title]:- "Common errors"
[_metadata_:order]:- "8"
# Common errors

This page lists the errors the Onboarding API returns, what each one means and what to do about it. Most of them you can fix yourself by changing the request. The few you can't, you can retry once you've checked whether the first call landed: see [Status codes](#status-codes).

Every path on this page is relative to the Onboarding API base URL. See [Onboarding API](/guides/onboarding/overview) for the base URLs and how to authenticate.

## The error body

Every error the Onboarding API returns has the same shape:

```
422 Unprocessable Content
{
  "status": "failed",
  "error_code": "record_invalid",
  "reason": "Record invalid",
  "error_messages": {
    "ownership_percentage": [
      {
        "error_code": "ubo_total_exceeded",
        "reason": "Ownership percentage would take the total ultimate business owner ownership above 100%"
      }
    ]
  }
}
```

There are two levels of code:

- **The top-level `error_code`** says what kind of failure it is, and goes with the HTTP status. See [Status codes](#status-codes).
- **Each entry in `error_messages`** is keyed by the field it's about and has its own `error_code` and a readable `reason`. A nested field is keyed by its path, such as `registered_address.state_or_province`. One request can return several fields, and several entries for one field.

`status` is `failed` when the request can be fixed, and `error` when the failure is on our side. `error_messages` is `null` when there's nothing to add to the top-level code.

**Treat `error_code` as an open set.** New codes can be added at any time, so match on the ones you handle and fall back to the HTTP status for the rest. Don't parse `reason`: it's there for people, and its wording can change.

## Status codes

| **Status** | **Top-level `error_code`** | **What it means** | **What to do** |
|---|---|---|---|
| `400` | `request_invalid` | A query parameter is missing or not one of its permitted values | Fix the request. `error_messages` names the parameter |
| `400` | `bad_request` | The body isn't valid JSON, or identity verification couldn't be started | Fix the body and send it with `Content-Type: application/json`. For identity verification, see [Identity verification](#identity-verification) |
| `400` | Relayed from the workflow | The workflow refused the request | See [Workflow errors](#workflow-errors) |
| `401` | — | The token is missing, invalid or expired | Authenticate again and retry with the new token. See [Authentication](/guides/integration-guides/authentication) |
| `404` | `record_not_found` | The application, person or document doesn't exist, or isn't yours | Check the ID. You can only reach applications created with your account |
| `404` | Relayed from the workflow | The workflow doesn't exist, or the step ID isn't in this application's workflow | See [Workflow errors](#workflow-errors) |
| `409` | Relayed from the workflow | The workflow refused the call, for example because the step isn't the current one | See [Workflow errors](#workflow-errors) |
| `413` | `payload_too_large` | The file is over 10MB once decoded | Upload a smaller file |
| `422` | `record_invalid` | The data broke a rule. The reasons are in `error_messages` | Fix the fields it names and send the request again |
| `422` | `request_invalid` | The request failed a check: a step that can't complete yet, an update to an application that's already submitted, a name with characters we don't accept, or an account that can't create individual applications | Fix what `error_messages` names. See [Error codes by step](#error-codes-by-step) |
| `429` | — | You've sent too many requests in a short time | Wait, then retry. Use the `Retry-After` header if it's there, and spread out bursts of calls |
| `500` | `internal_server_error` | Something went wrong on our side, or the workflow couldn't be reached | Retry. If it keeps happening, contact support with the time of the request |
| `502` | `workflow_service_request_failed` | The workflow refused our call to it. Creating an application, submitting it and every workflow call depend on the workflow | Retry. There's nothing to fix in your request. If it keeps happening, contact support |

A `401` or `429` is returned before your request reaches the Onboarding API, so its body may be empty or not follow the shape above. Rely on the status.

**Before you retry a `500` or a `502`, check whether the first call landed.** Completing a step twice is refused with a `409`, and submitting twice is refused with a `422`, so a blind retry can fail even though the first call worked:

- **For a step**, call `GET /v2/workflows/{workflow_id}/steps/current?application_id={application_id}`. Every workflow call needs `application_id`, including the shortened `GET .../steps/current` calls on this page.
- **For an update**, read back the resource you changed: `GET /v2/applications/{application_id}` for the application, or the resource's own `GET`, such as `GET /v2/applications/{application_id}/people/{person_id}`, `.../account_usage` or `.../business_information`. The application doesn't include its people, account usage or business information.
- **For a submission**, read `state` from `GET /v2/applications/{application_id}`. If it's `submitted`, the submission was saved, but the processing that follows it may not have finished. Contact support with the `application_id` before you complete `form_submit` or `form_submit_corp`.
- **For `POST /v2/applications`**, the application can be created even when the call fails, and the error doesn't give you its ID. It may not show up when you list your applications either. Call `GET /v2/applications?order_asc_desc=desc` to see your newest applications first, and look for one with the `email` you sent, checking every page until you're past the time of the failed call. If you find it, carry on with it. If you don't, contact support before you create another one.

## Field error codes

These are the `error_code` values inside `error_messages`. Any of them can come back for any field the rule applies to.

| **Field `error_code`** | **What it means** | **What to do** |
|---|---|---|
| `missing` | A required field wasn't sent, or is empty | Send the field. On a `PUT`, send the full body: a field you leave out is cleared. See [Onboarding API](/guides/onboarding/overview#key-concepts) for the few fields `PUT /v2/applications/{application_id}` keeps |
| `invalid` | The value is the wrong type or format, such as a date, an email address or a UUID | Fix the format. Dates are `YYYY-MM-DD` |
| `inclusion` | The value isn't one of the permitted values | Use one of the values the field accepts |
| `too_long`, `too_short` | Text or a list is outside its length limits | Shorten or lengthen it |
| `greater_than_or_equal_to`, `less_than_or_equal_to` | A number or date is outside its range. For example, the person must be 18 to 100, and amounts can't be negative | Send a value inside the range |
| `accepted` | A consent must be `true` | Get the consent and send `true` |
| `blank` | Something the application needs is missing, such as a user's address | Add it, then try again |
| `present` | A field was sent that this kind of application doesn't take | Leave the field out |
| `validation` | A step can't complete yet, or the request failed a check. The field names what's wrong | See [Error codes by step](#error-codes-by-step) |
| `validation` on `request_body_json` | A name field has characters we don't accept. `reason` names the field, such as `Unsupported characters in: first_name` | See [Name codes](#name-codes) for the characters we accept |
| `not_unique` on `record` | The request collided with something that already exists, usually because the same request was sent twice at once. `record` isn't a field you sent | Read the application to see what's already there, then carry on from it |

An unknown field isn't an error: the API ignores any field it doesn't accept. So a misspelled field is ignored too, and its value is lost. If a value you sent doesn't appear in the response, check the field name.

## Error codes by step

Each section covers the errors from sending a step's data and from completing it. A completion that's refused returns a `422`, with `request_invalid` and `validation` on the field that's missing. See [What each step checks](/guides/onboarding/workflows#what-each-step-checks-before-it-will-complete) for what each step needs.

### Creating the application

`POST /v2/applications`

| **Field** | **`error_code`** | **What it means** | **What to do** |
|---|---|---|---|
| `account_eligibility` | `not_eligible_to_create_individual_accounts` | Your account can't create individual applications. Returned as `422` `request_invalid` | Ask your Solutions Manager to enable it |
| `agreed_to_terms_and_conditions` | `missing`, `accepted` | You didn't send the field, or sent `false` | Get the applicant's consent before you create the application, then send `true` |
| `business_role` | `present` | You sent `business_role` on an individual application | Leave it out. It's for corporate applications only |

### Applicant details

`basic_info`, `basic_info_corp`: `PUT /v2/applications/{application_id}`

| **Field** | **`error_code`** | **What it means** | **What to do** |
|---|---|---|---|
| `country`, `phone_number`, `contact_name`, `agreed_to_marketing_emails`, `agreed_to_corporate_authority` | `cannot_be_cleared` | You sent `null` or `""` for a field that already has a value | Send the stored value, or a new one. Leaving the field out keeps it |
| `country` | `jurisdiction_not_permitted` | We can't onboard applications from this country | Check the country in `GET /v1/countries`: its `permitted_jurisdiction` must be `true` |
| `country` | `country_mismatch` | Individual applications only: the new country doesn't match the applicant's `home_country` | Keep the application's `country` and the applicant's `home_country` the same |
| `phone_number` | `missing` | Corporate only: the application has no phone number yet | Send `phone_number` |
| `phone_number` | `invalid` | The number isn't in E.164 format, or its country code isn't recognized | Send `+`, the country code and the number, digits only with no spaces, such as `+447700900123` |
| `phone_number` | `wrong_length` | A `+1` or `+44` number doesn't have 10 digits after the country code | Check the number |
| `agreed_to_corporate_authority` | `present` | You sent `agreed_to_corporate_authority: true` on an individual application | Leave it out on an individual application |
| `contact_name` | Any of the [name codes](#name-codes), or `too_short` | The name breaks a name rule, or is under 2 characters | See [Name codes](#name-codes) |

Completing the step returns `validation` on whichever of these is missing: `country`, `email`, `agreed_to_marketing_emails` or `agreed_to_terms_and_conditions`. On `basic_info_corp`, also `agreed_to_corporate_authority`, `business_role` or `contact_name`.

### Business information

`business_information_corp`: `PUT /v2/applications/{application_id}/business_information`

| **Field** | **`error_code`** | **What it means** | **What to do** |
|---|---|---|---|
| `form` | `entity_type_mismatch` | You sent business information on an individual application | Only corporate applications have business information |
| `incorporation_date` | `not_past_or_current` | The date is in the future | Send the date the company was incorporated |
| `company_registration_number`, `vat_number` | `required_for_legal_entity_type` | The `business_country` and `legal_entity_type` you sent need the field | Send it |
| `vat_number` | `invalid` | For a US business, the EIN isn't 9 digits | Send it as `123456789` or `12-3456789` |
| `business_website` | `invalid` | The website isn't a valid web address with a domain | Send an address such as `example.com` or `https://example.com` |
| `legal_entity_type` | `sole_trader_mismatch` | `legal_entity_type` and the `business_role` you gave at create disagree about whether this is a sole trader | Send `sole_trader` only when `business_role` is `sole_trader_business_role`, and always then. `business_role` can't change after create |
| `legal_entity_type`, `people` | `user_role_limit_exceeded`, `person_limit_exceeded`, `sole_trader_roles_required` | You sent `sole_trader`, but the application's people don't fit a sole trader. These come with `sole_trader_mismatch` | See `sole_trader_mismatch` above. If this isn't a sole trader, don't send `sole_trader` |
| `registered_address`, `trading_address` | Any of the [address codes](#address-codes) | The address breaks an address rule | See [Address codes](#address-codes) |

Completing the step returns `validation` on `business_information` when there's none yet, and on `registered_address` when its country isn't a permitted jurisdiction.

### Account usage

`account_usage`, `account_usage_corp`: `PUT /v2/applications/{application_id}/account_usage`

| **Field** | **`error_code`** | **What it means** | **What to do** |
|---|---|---|---|
| `collections_account`, `primary_purpose`, `source_of_funds`, `collection_currencies`, `payment_currencies`, `estimated_monthly_transaction_currency`, `estimated_monthly_transaction_value` | `missing` | These are required every time you send account usage | Send them on every `PUT` |
| `estimated_monthly_transaction_volume`, `transaction_countries` | `missing` | Corporate only, and required every time. An empty `transaction_countries` counts as missing | Send them on every `PUT` |
| `purpose_details` | `missing` | `primary_purpose` is `other`, so it needs details | Describe the purpose in `purpose_details` |

Completing the step returns `validation` on `account_usage` when there's none yet. On `account_usage_corp`, if you've already sent business information, it also returns `validation` on `initial_capital` when the company was incorporated in the last 12 months and `initial_capital` is missing.

### People

`personal_details`, `people_corp`: `POST /v2/applications/{application_id}/people`, `PUT /v2/applications/{application_id}/people/{person_id}`

| **Field** | **`error_code`** | **What it means** | **What to do** |
|---|---|---|---|
| `roles` | `not_valid_for_individual` | You gave the person `director` or `ultimate_business_owner` on an individual application | Use `user` only |
| `person` | `person_limit_exceeded` | You added a second person to an individual or sole trader application | Update the existing person instead |
| `person` | `limit_exceeded` | The application already has 50 people | Remove someone before you add another |
| `person` | `duplicate_person` | A person with the same first and last name and the same roles is already on the application | Find them with `GET /v2/applications/{application_id}/people` and update that person instead |
| `roles` | `sole_trader_roles_required` | A sole trader's person must hold `user`, `director` and `ultimate_business_owner` | Send all three roles |
| `ownership_percentage` | `required_for_ultimate_business_owner` | An `ultimate_business_owner` needs an `ownership_percentage` | Send it |
| `ownership_percentage` | `greater_than_or_equal_to` | An `ultimate_business_owner` must own at least 25% | Check the percentage. Only owners of 25% or more are ultimate business owners |
| `ownership_percentage` | `ubo_total_exceeded` | The owners' percentages would add up to more than 100% | Correct the percentages |
| `home_country` | `country_mismatch` | Individual applications only: `home_country` doesn't match the person's address country, or the application's `country` | Make all three match |
| `id_number` | `wrong_length` | A US user's Social Security number must be 9 digits | Send the 9 digits, with or without dashes |
| `phone_number` | `invalid`, `wrong_length` | The number isn't in E.164 format, or a `+1` or `+44` number doesn't have 10 digits after the country code | Send `+`, the country code and the number, digits only |
| `first_name`, `last_name` | Any of the [name codes](#name-codes) | The name breaks a name rule | See [Name codes](#name-codes) |
| `last_name` | `company_signifier` | Individual applications only: for some countries, the surname ends in a company word such as `Ltd` | Send the person's own surname |
| `personal_address` | Any of the [address codes](#address-codes) | The address breaks an address rule | See [Address codes](#address-codes) |

Completing the step returns `validation` on `people` when there's no person yet. On `people_corp`, it also does so when no one has the `user` role or no one has the `director` role, or when a sole trader has more than one person. It returns `validation` on `dob`, `email` or `personal_address` when a user is missing one, and on `personal_address` when its country isn't a permitted jurisdiction.

<span id="name-codes"></span>

#### Name codes

These apply to `first_name`, `last_name` and `contact_name`.

We accept the letters A to Z, accented letters from the Latin-1 set such as `é`, `ñ` and `ü`, apostrophes, hyphens, periods, and single spaces between words. Letters outside that set, such as `Ł` or `ř`, aren't accepted yet. Neither are digits, symbols or emoji.

Most characters we don't accept are caught before the name rules run. You get a `422` `request_invalid`, with `validation` on `request_body_json` and a `reason` that names the field. The rest of the name rules return these codes on the field itself:

| **`error_code`** | **What it means** | **What to do** |
|---|---|---|
| `initial` | The name is a single initial | Send the full name |
| `no_letters` | The name has no letters at all, such as `--` | Send the real name |
| `invalid_characters` | The name has a character we don't accept, such as a line break | Use only the characters above |
| `too_long` | The name is over 100 characters | Shorten it |

<span id="address-codes"></span>

#### Address codes

These apply to `personal_address`, `registered_address` and `trading_address`.

| **Field** | **`error_code`** | **What it means** | **What to do** |
|---|---|---|---|
| The address itself, such as `personal_address` | `either_building_number_or_name` | The address has neither a `building_number` nor a `building_name` | Send one or both |
| The address's `state_or_province`, such as `personal_address.state_or_province` | `required_for_country` | US and Canadian addresses need a state or province | Send it |
| The address's `state_or_province` | `inclusion` | The state or province isn't a valid one for the country | Send its two-letter uppercase code, such as `NY` or `ON` |

### Documents

`documents`, `documents_corp`: `POST .../documents`, `POST .../documents/{document_id}/document_files`, and `document_ids` on a person, business information or account usage

| **Field** | **`error_code`** | **What it means** | **What to do** |
|---|---|---|---|
| `file` | `missing` | You didn't send `file` | Send the file, base64-encoded |
| `file` | `payload_too_large` | The file is over 10MB once decoded. Returned as a `413` | Upload a smaller file |
| `side` | `duplicate_side` | That side of a two-sided document already has a file | Upload the other side, or delete the existing file and upload it again |
| `image` | A quality code, such as `detect_blur`, `detect_cutoff` or `document_detection` | A photo ID image failed the quality check. Returned as a `422` `request_invalid` | Take a new, clear photo of the whole document and upload it |
| `document_ids` | `not_found` | A document you listed isn't on this application, or is already attached to someone or something else | Check the IDs. A document can be attached to one person, business information or account usage at a time |
| `document_ids` | `missing_sides` | A two-sided document you listed is missing its `front` or `back` | Upload both sides before you attach it |
| `document_ids` | `limit_exceeded` | You listed more than 20 documents | Attach 20 or fewer to each person, business information or account usage |

The quality check only runs on documents with the `proof_of_identity` category.

Two file checks don't have a short code yet. They return a readable message as the `error_code` on `image`:

- The file isn't a JPEG, PNG or PDF.
- The document already has 3 files.

Fix the file or use another document, then upload it again.

### Submit

`form_submit`, `form_submit_corp`: `POST /v2/applications/{application_id}/submit`

**Submit checks the whole application again**, so any code from the earlier steps can come back here, for example `missing` on a field you never sent. The checks run one part at a time, so you get one part's errors per response: fix them and submit again.

| **Field** | **`error_code`** | **What it means** | **What to do** |
|---|---|---|---|
| `workflow` | `validation` | Earlier steps aren't complete yet. Returned as a `422` `request_invalid`, and `reason` lists the steps | Complete them, then submit |
| `base` | `already_submitted` | The application has already been submitted | If your earlier submit succeeded, call `GET .../steps/current`, and if it returns `form_submit` or `form_submit_corp`, complete it. If your earlier submit returned a `500` or `502`, contact support with the `application_id` before you complete the step: see [Status codes](#status-codes) |
| `people` | `missing` | The application has no people | Add the applicant, or the company's people |
| `people` | `missing_user_role` | No one on the application has the `user` role | Give the applicant the `user` role |
| `people` | `missing_director_role` | Corporate only: no one has the `director` role | Add a director |
| `form` | `missing_initial_capital` | Corporate only: a company incorporated in the last 12 months needs `initial_capital` | Send `initial_capital` with `PUT .../account_usage` |
| `country` | `jurisdiction_not_permitted` | The application's country isn't one we can onboard from | Check the country in `GET /v1/countries` |
| `personal_address` | `jurisdiction_not_permitted` | Individual applications only: the applicant's address is in a country we can't onboard from | Correct the address |
| `registered_address` | `jurisdiction_not_permitted` | Corporate only: the company's registered address is in a country we can't onboard from | Correct the address |

**Once an application is submitted, it can't be changed.** Any update or delete returns a `422` `request_invalid`, with `validation` on `form`.

Completing `form_submit` or `form_submit_corp` before you've submitted returns `validation` on `state`.

<span id="identity-verification"></span>

### Identity verification

`POST /v2/identity_verifications`

| **Field** | **`error_code`** | **What it means** | **What to do** |
|---|---|---|---|
| `application_id`, `person_id` | `missing`, `invalid` | A field is missing, or isn't a UUID | Send both IDs |
| `form` | `validation` | The application isn't submitted yet | Submit it first |
| `person_id` | `validation` | Corporate only: only a person with the `director` role can be verified | Send a director's `person_id` |
| `identity_verification` | `bad_request` | The verification couldn't be started. Returned as a `400` | Retry. If it keeps failing, contact support with the `application_id` and `person_id` |

An application or person that doesn't exist, or isn't yours, returns a `404`.

The application is locked by the time you verify, so check before you submit that every person you'll verify has a `dob` and an `email`. Submit only requires them for users, so a director who isn't a user can be missing them.

## Workflow errors

The workflow endpoints pass the workflow's own errors through unchanged. They usually have `error_messages` set to `null`:

```
409 Conflict
{
  "status": "failed",
  "error_code": "step_not_started",
  "reason": "…",
  "error_messages": null
}
```

| **Status** | **`error_code`** | **What it means** | **What to do** |
|---|---|---|---|
| `409` | `step_not_started` | You completed a step that isn't the current one: one you haven't reached, or one you've already completed | Call `GET .../steps/current` and complete the step it returns |
| `409` | `step_navigation_not_allowed` | You moved to a step you haven't reached yet | Move only to a step you've already completed |
| `409` | `step_not_actionable` | You tried to complete or move to `id_verification` | Don't. It completes on its own when you complete `form_submit` or `form_submit_corp` |
| `409` | `workflow_already_completed` | The workflow is finished | Nothing. This is the normal end of the journey |
| `409` | `no_previous_step` | There's no earlier step to go back to | Carry on from the current step |
| `404` | `invalid_step` | The step ID isn't in this application's workflow, for example a corporate step on an individual application | Use a step from your flow. See [Workflows](/guides/onboarding/workflows#the-steps) |
| `404` | `workflow_not_found`, `application_id_mismatch` | The workflow doesn't exist, or doesn't belong to this `application_id` | Check you've paired the `workflow_id` with the `application_id` it was created with |

The workflow can return other codes too. Treat any you don't recognize by their status. See [Workflows](/guides/onboarding/workflows) for how steps and navigation work.
