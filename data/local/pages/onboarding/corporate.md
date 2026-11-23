[_metadata_:menu_title]:- "Onboard a business"
[_metadata_:order]:- "4"
# Onboard a business

Companies and sole traders both apply as corporate applications, through one of three corporate flows. This page covers what those flows share: choosing a flow, the people on the application, the business information rules, and the documents a business needs. Each flow page then takes you through the calls step by step.

## Choose a flow

`business_role` says who is filling in the application, and decides which flow you follow. You set it when you [create the application](/guides/onboarding/corporate-director#step-1-create-the-application), and it can't be changed afterwards.

| **Who fills in the application** | **`business_role`** | **Flow** |
|---|---|---|
| A director of the company | `director_controller` | [Onboard a business: director](/guides/onboarding/corporate-director) |
| Someone who isn't a director, such as an employee. A director is verified later | `authorised_person` | [Onboard a business: authorised person](/guides/onboarding/corporate-authorised-person) |
| A sole trader | `sole_trader_business_role` | [Onboard a business: sole trader](/guides/onboarding/corporate-sole-trader) |

A `sole_trader_business_role` application must use the legal entity type `sole_trader`, and only that business role can use it.

## People

A corporate application lists the people behind the business. Each person holds one or more roles:

| **Role** | **Who holds it** | **Rule** |
|---|---|---|
| `user` | The applicant: the person filling in the application | At least one person must hold it |
| `director` | A director of the company | At least one person must hold it. Only a director's identity can be verified |
| `ultimate_business_owner` | Someone who owns 25% or more of the business | Needs an `ownership_percentage` of at least 25. All owners together can't exceed 100 |

- **Add each person once, with all of their roles.** A director who owns 25% or more of the company is one person holding `director` and `ultimate_business_owner`.
- **Add owners of 25% or more.** If we need details of anyone who owns less, we'll contact you.
- **An application holds at most 50 people.**

Who you add depends on the flow:

| **Flow** | **The applicant holds** | **Also add** |
|---|---|---|
| Director | `user` and `director` | The company's other directors, and its owners |
| Authorised person | `user` | The director who will be verified, with their own `email` and `dob`, plus the company's other directors and its owners |
| Sole trader | `user`, `director` and `ultimate_business_owner` | Nobody. A sole trader application holds exactly one person |

## Business information

Every corporate application sends its business information with `PUT /v2/applications/{application_id}/business_information`. The [API reference](/api-reference/) lists every field. These are the rules that are easiest to get wrong.

**`business_website` is always required.** It's the business's website or other online presence, as a URL, and the scheme is optional, so `example.com` works. A business with no online presence can't be onboarded through the API.

**The registered address must be in a permitted jurisdiction.** The country the business is registered in, `business_country`, can be any ISO 3166-1 alpha-2 code.

**Registration and VAT numbers depend on where the business is registered and its legal entity type:**

| **If `business_country` is** | **`company_registration_number` is required for** | **`vat_number` is required for** |
|---|---|---|
| `GB` | `limited_liability_company`, `limited_liability_partnership`, `public_limited_company`, `registered_charity`, `scottish_limited_partnership` | `limited_liability_company`, `limited_liability_partnership`, `public_limited_company`, `scottish_limited_partnership` |
| `US` | `sole_trader`, `limited_liability_company`, `limited_liability_partnership`, `public_limited_company`, `registered_charity`, `trust` | `sole_trader`, `limited_liability_company`, `limited_liability_partnership`, `public_limited_company`, `registered_charity`, `trust`, `unincorporated_partnership`, `other` |
| Any other country | `limited_liability_company`, `limited_liability_partnership`, `public_limited_company`, `registered_charity` | `limited_liability_company`, `limited_liability_partnership`, `public_limited_company` |

**For a business registered in the US, `vat_number` holds its EIN:** 9 digits, written as `123456789` or `12-3456789`. VAT numbers for other countries aren't format-checked.

## Documents

### What to upload

| **Need** | **Documents** |
|---|---|
| Always | Photo ID for each director and owner. Depending on the country and legal entity type, the company registration number too, which you send as `company_registration_number` in the [business information](#business-information) |
| Can speed up approval: source of funds | Annual financial statements, loan agreements, corporate bank statements, sales agreements or contracts, invoices and receipts |
| Can speed up approval: registration and ownership | Articles or certificate of incorporation, certificate of good standing (US), an extract from the local companies register, shareholder register, operating agreement, change-of-ownership documents |

Upload everything you have: our compliance review decides what's finally needed.

### Where to attach them

You create each document with `POST /v2/applications/{application_id}/documents` and upload its files with `POST .../documents/{document_id}/document_files`. Then you attach it by listing its ID in `document_ids` on the resource it's evidence for. Its `category` says which resource that is:

| **Document** | **`category`** | **Attach it to** |
|---|---|---|
| Photo ID of a director or owner | `proof_of_identity` | That person |
| Proof of address of a director or owner | `proof_of_address` | That person |
| Registration documents, such as a certificate of incorporation or a companies register extract | `proof_of_business_identity` | The business information |
| Lists of directors and of shareholders | `proof_of_directors`, `proof_of_owners` | The business information |
| Source of funds, such as financial statements or corporate bank statements | `proof_of_source_of_funds` | The account usage |

- **Attach each photo ID to the person it identifies.**
- **`document_ids` is the complete list.** An ID you leave out is detached, not deleted, and `PUT` replaces the resource, so send its full body.
- **Each resource holds up to 20 documents.**
- **To move a document to another resource, take its ID out of the first resource's `document_ids`.**
- **A two-sided document needs both sides first.** `driving_licence`, `residence_id`, `state_id` and `biometric_state_id` need a `front` and a `back` uploaded before you can attach them.

Each flow page's documents step shows the calls in full. Every `document_type` and `category` value is listed in the [API reference](/api-reference/).
