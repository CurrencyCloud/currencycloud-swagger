[_metadata_:menu_title]:- "Overview"
[_metadata_:order]:- "1"
# Onboarding API

The Onboarding API lets you open Currencycloud accounts for your own customers, whether they're individuals or companies, from inside your product. You collect the applicant's details, documents and consent, send them to us one step at a time, and we review the application.

This section covers version 2 of the API. In v2, each application follows a **workflow**: a fixed sequence of steps that you fill in and complete in order, so you always know what to send next and nothing reaches review half-finished.

Every application goes through the same four stages:

1. Create the application, which also creates its workflow.
2. For each step, send its data, then complete the step.
3. Submit the application.
4. Verify the identity of the applicant, or of a director on a corporate application.

## Before you start

- [Base URLs](#base-urls): where to send requests.
- [Authentication](#authentication): how to get the token every request needs.
- [Accepted format](#accepted-format): how to send request bodies, country codes and files.
- [Terms & conditions](#terms-conditions): what you must show the applicant, and the consent you must record.
- [Key concepts](#key-concepts): five things that shape every integration.
- [Endpoints](#endpoints): every call the API offers.
- [Choose your flow](#choose-your-flow): the page to follow for your applicant.

## Base URLs

| **Environment** | **Base URL** |
|---|---|
| Demo | `https://devapi.currencycloud.com/onboarding` |
| Production | `https://api.currencycloud.com/onboarding` |

`/onboarding` is part of the base URL. Every path in this section, such as `/v2/applications`, is relative to it.

## Authentication

To use the Onboarding API, you first [authenticate](/api-reference/#authenticate) to Currencycloud. Rather than sending your login ID and API key with every request, you sign in once and get a temporary token. Pass it as `X-Auth-Token` on every request. See the [Authentication guide](/guides/integration-guides/authentication) for step-by-step instructions.

## Accepted format

- Send request bodies as JSON. Strings are UTF-8.
- Enum values, maximum lengths and minimum lengths are listed in each field's description in the [API reference](/api-reference/).
- Country codes are uppercase ISO 3166-1 alpha-2 codes, such as `GB`.
- Uploaded files must be JPG, PNG or PDF, up to 10MB each.
- Send file content as a plain base64 string, without a `data:` prefix.
- Send addresses as `personal_address_attributes`, `registered_address_attributes` and `trading_address_attributes`. They come back as `personal_address`, `registered_address` and `trading_address`.

## Terms & conditions

It's **really important** that any applicant you onboard through the Onboarding API:

- has seen, understands and accepts [Currencycloud's terms and conditions](https://onboarding.paydirect.io/currencycloud/terms_and_conditions); and
- understands that Currencycloud is providing them with a regulated service.

You **must** present the following wording to users signing up for Currencycloud's service:

_Payment and foreign currency exchange service are provided by The Currency Cloud Ltd. The Currency Cloud Ltd is authorised by the Financial Conduct Authority for issuing of electronic money and the provision of payment services with FCA registration number 900199. If you are located in the European Economic Area, payment services are provided by Currencycloud B.V. Currencycloud B.V. is authorised by De Nederlandsche Bank N.V. for issuing of electronic money and the provision of payment services with DNB registration number R142701._

_Payment services in the United States are provided by Visa Global Services Inc. (VGSI), a licensed money transmitter (NMLS ID 181032) in the states listed [here](https://www.visa.com/en-us/legal/visa-global-services-licenses). VGSI is licensed as a money transmitter by the New York Department of Financial Services. Mailing address: 900 Metro Center Blvd, Mailstop 1Z, Foster City, CA 94404. VGSI is also a registered Money Services Business (“MSB”) with FinCEN and a registered Foreign MSB with FINTRAC._

Your build must also show users Currencycloud's terms and conditions, get their consent, and record it on the application:

| **Field** | **When** | **Rule** |
|---|---|---|
| `agreed_to_terms_and_conditions` | `POST /v2/applications` | Required, `true`. Record it when you create the application: it can't be set or changed afterward, so get consent before you make the call |
| `agreed_to_corporate_authority` | `PUT /v2/applications/{application_id}` | Corporate applications only. Set it to `true` to confirm the person filling in the application has the right to apply on behalf of the company |
| `contact_name` | `PUT /v2/applications/{application_id}` | Corporate applications only. The name of the person who agreed to the terms and confirmed corporate authority, meaning the person filling in the application |

On a corporate application, both `agreed_to_corporate_authority` and `contact_name` are needed before you can complete the first step. See [What each step checks](/guides/onboarding/workflows#what-each-step-checks-before-it-will-complete) for everything that step needs.

## Key concepts

**Every step is two calls.** You send the data, then complete the step it belongs to. Sending the data on its own doesn't move the workflow on. See [Workflows](/guides/onboarding/workflows) for the steps and how to navigate them.

**PUT replaces, it doesn't patch.** Send the full body every time, not just the fields you're changing. A field you leave out is cleared. The one exception is on [Update Application](/api-reference/#update-application), for `country`, `phone_number`, `contact_name`, `agreed_to_marketing_emails` and `agreed_to_corporate_authority`: once one of these has a value, leaving it out keeps that value, and sending it as `null` is refused. A person has two of its own exceptions: leaving out `personal_address_attributes` keeps the stored address, and on an individual or sole-trader application the email always comes from the application. Everything else is cleared. Leave out a person's `dob` and it's cleared; leave out `document_ids` and their documents are detached.

**Store `workflow_id` when you create the application.** The create response returns both `application_id` and `workflow_id`. You need `application_id` on every call and `workflow_id` on every workflow call, so save both straight away.

**Submission is one-shot.** Submitting locks the application, and a second submission is refused. Review the application before you submit it.

**Most responses are wrapped in `data`.** The application and its resources, such as people and documents, are returned under `data`. The create response, the workflow endpoints and identity verification return their fields at the top level instead.

## Endpoints

The application and its resources:

```
POST   /v2/applications
GET    /v2/applications
GET    /v2/applications/{application_id}
PUT    /v2/applications/{application_id}
DELETE /v2/applications/{application_id}
POST   /v2/applications/{application_id}/submit

GET    /v2/applications/{application_id}/account_usage
PUT    /v2/applications/{application_id}/account_usage
DELETE /v2/applications/{application_id}/account_usage

GET    /v2/applications/{application_id}/business_information
PUT    /v2/applications/{application_id}/business_information
DELETE /v2/applications/{application_id}/business_information

GET    /v2/applications/{application_id}/people
POST   /v2/applications/{application_id}/people
GET    /v2/applications/{application_id}/people/{person_id}
PUT    /v2/applications/{application_id}/people/{person_id}
DELETE /v2/applications/{application_id}/people/{person_id}

GET    /v2/applications/{application_id}/documents
POST   /v2/applications/{application_id}/documents
GET    /v2/applications/{application_id}/documents/{id}
DELETE /v2/applications/{application_id}/documents/{id}
GET    /v2/applications/{application_id}/documents/{document_id}/document_files
POST   /v2/applications/{application_id}/documents/{document_id}/document_files
DELETE /v2/applications/{application_id}/documents/{document_id}/document_files/{id}

POST   /v2/identity_verifications
```

The workflow, which needs `application_id` as a query parameter on every call:

```
PUT    /v2/workflows/{workflow_id}/steps/{step_id}/completion?application_id={application_id}
GET    /v2/workflows/{workflow_id}/steps/current?application_id={application_id}
PUT    /v2/workflows/{workflow_id}/steps/current?application_id={application_id}
GET    /v2/workflows/{workflow_id}/steps/previous?application_id={application_id}
```

[Find Applications](/api-reference/#find-applications) takes `order`, `order_asc_desc`, `application_status`, `entity_type`, `page` and `per_page`. `per_page` is from 1 to 50.

The reference data, such as permitted jurisdictions, supported currencies and the photo ID types each country accepts, comes from three v1 endpoints. They take the same token. Each flow page lists them under Reference data.

## Choose your flow

| **Your applicant** | **Follow** |
|---|---|
| A person applying on their own behalf | [Onboard an individual](/guides/onboarding/individual). Your account must be enabled for individual onboarding; your Solutions Manager can enable it |
| A company, with a director filling in the application | [Onboard a business: director](/guides/onboarding/corporate-director) |
| A company, with someone other than a director filling in the application, and a director verified later | [Onboard a business: authorised person](/guides/onboarding/corporate-authorised-person) |
| A sole trader | [Onboard a business: sole trader](/guides/onboarding/corporate-sole-trader) |

For a company or a sole trader, read [Onboard a business](/guides/onboarding/corporate) first. It covers the rules all three corporate flows share: business information, the people on the application, and documents.

## More help

- [Troubleshooting & FAQ](/guides/onboarding/faq): what happens after submission, and fixes for common problems.
- [Migrating from v1](/guides/onboarding/migrating-from-v1): what changes if you already use `/v1/forms`.
