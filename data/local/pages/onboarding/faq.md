[_metadata_:menu_title]:- "Troubleshooting & FAQ"
[_metadata_:order]:- "8"
# Troubleshooting & FAQ

Answers to the questions integrators ask once they're live: what happens after you submit, how you hear about the decision, and how to fix the problems that come up most often.

## What happens after I submit?

Submitting hands the application to our compliance review. Its `state`, returned by [Get Application](/api-reference/#get-application), then moves on:

| **`state`** | **Meaning** |
|---|---|
| `new` | Not submitted yet |
| `submitted` | Submitted and waiting for a decision |
| `approved` | Approved |
| `rejected` | Rejected |

**A submitted application can't be changed.** Every update or delete, on the application or any of its resources, is refused with a `422`, and that stays true after the decision. You can still read the application, and you can still start identity verification with [Create Identity Verification](/api-reference/#create-identity-verification). See your flow page for that step:

- [Onboard an individual](/guides/onboarding/individual#step-7-verify-the-applicants-identity)
- [Onboard a business: director](/guides/onboarding/corporate-director#step-8-verify-the-directors-identity)
- [Onboard a business: authorised person](/guides/onboarding/corporate-authorised-person#step-8-verify-the-directors-identity)
- [Onboard a business: sole trader](/guides/onboarding/corporate-sole-trader#step-8-verify-the-sole-traders-identity)

## How do I find out the decision?

Subscribe to the `end_client_application_decisioned_notification` [push notification](/guides/platform-specifics/push-notifications/#notifications-and-events). Your Solutions Manager can set it up. Its `decision` field carries the new `state`, `approved` or `rejected`, and its `form_id` is the `application_id`.

If you'd rather poll, read `state` from [Get Application](/api-reference/#get-application), at a modest interval rather than in a tight loop.

## Common issues

| **What you see** | **Why** | **What to do** |
|---|---|---|
| You no longer have the application's `workflow_id` | Only the create response returns it | Delete the application with [Delete Application](/api-reference/#delete-application) and create it again. Save both IDs from the create response straight away. If you've already submitted it, contact support with the `application_id` |
| Completing a step returns a `409` with `step_not_started` | You've already completed that step, or it isn't the current one | Call [Get Current Steps](/api-reference/#get-current-steps) and complete the step it returns |
| Submitting returns a `422` with `validation` on `workflow` | Earlier steps aren't complete | Call [Get Current Steps](/api-reference/#get-current-steps), complete each step from there, then submit again |
| Completing `form_submit` or `form_submit_corp` returns a `422` with `validation` on `state` | The application isn't submitted yet | Call [Submit Application](/api-reference/#submit-application) first, then complete the step |
| A photo ID upload returns a `422` with a code on `image`, such as `detect_blur` or `detect_cutoff` | The image failed the quality check, which runs on `proof_of_identity` documents | Take a new, clear photo of the whole document and upload it again |
| Fields you set earlier come back empty | PUT replaces the resource, so fields you left out were cleared | Send the full body every time: read the resource, change it, and send all of it back |
| A person's documents are no longer attached | An update to the person left out `document_ids` | Send `document_ids` every time you update the person |
| Starting identity verification returns a `422` with `validation` on `form` | The application isn't submitted yet | Submit it first |

## Is it safe to retry a call?

Not always. If a call times out or returns a `500` or `502`, check whether it landed before you send it again:

| **Call** | **Safe to retry?** |
|---|---|
| `POST /v2/applications` | No. Each call creates a new application, and a call that fails can still create one without giving you its ID. Call [Find Applications](/api-reference/#find-applications) with `order_asc_desc=desc` to see your newest applications first, and look for one with the `email` you sent, checking every page until you're past the time of the failed call. If you find it, delete it with [Delete Application](/api-reference/#delete-application) and create the application again: only a successful create returns the `workflow_id` you need. If you don't find it, contact support before you create another one |
| PUT on any resource | Yes. It replaces the resource with the same body |
| [Create Person](/api-reference/#create-person), [Create Document](/api-reference/#create-document), [Create Document File](/api-reference/#create-document-file) | No. Each call creates a new record, so list the collection first to see whether the first call landed. A repeated person is refused: with `duplicate_person` on a company application, or `person_limit_exceeded` on an individual or sole trader one |
| `PUT .../steps/{step_id}/completion` | No. Repeating it returns a `409`: `step_not_started`, or `workflow_already_completed` after the last step. Call [Get Current Steps](/api-reference/#get-current-steps) first: if the step has moved on, the first call landed |
| `POST .../submit` | No, but a second call is refused with `already_submitted` and changes nothing. If the first call returned a `500` or `502`, contact support with the `application_id` before you complete `form_submit` or `form_submit_corp` |
| `POST /v2/identity_verifications` | Yes. It returns the same verification. On an authorised person application, each call also emails the link to the director again |
