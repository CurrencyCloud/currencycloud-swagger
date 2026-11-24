[_metadata_:menu_title]:- "Workflows"
[_metadata_:order]:- "2"
# Workflows

Every application has a workflow: a fixed sequence of steps that you complete one at a time, in order. Creating the application creates its workflow, and you move through it by sending each step's data and then completing the step.

This page explains the steps and the rules every onboarding flow shares. For a step-by-step walkthrough, see the page for your flow:

- [Onboard an individual](/guides/onboarding/individual)
- [Onboard a business](/guides/onboarding/corporate) - as a [director](/guides/onboarding/corporate-director), an [authorised person](/guides/onboarding/corporate-authorised-person) or a [sole trader](/guides/onboarding/corporate-sole-trader)

Every path on this page is relative to the Onboarding API base URL. See the [Overview guide](/guides/onboarding/overview) for the base URLs and how to authenticate.

## Key concepts

**Every step is two calls.** <br>
First you send the step's data, for example with [Update Account Usage](/api-reference/#update-account-usage). Then you complete the step with [Complete Step](/api-reference/#complete-step). Sending the data doesn't move the workflow on: nothing advances until you complete the step.<br><br>

**PUT replaces, it doesn't patch.** <br>
Send the full body every time, not just the fields you're changing. Most fields you leave out are cleared.<br><br>

**Save `workflow_id` when you create the application.** <br>
The create response gives you `application_id`, `workflow_id` and the first step:<br>

```
201 Created
{
  "application_id": "3f1c2a8e-…",
  "workflow_id": "9b7d4e10-…",
  "steps": ["basic_info"]
}
```

Store both IDs together. You need `application_id` for every call, and `workflow_id` for every workflow call.

**Every workflow call needs both IDs.**<br>
The workflow endpoints take `workflow_id` in the path and `application_id` as a query parameter. If you leave out `application_id` and you'll get a `400` keyed `application_id`.<br><br>

**Steps come one at a time.** <br>
You can only complete the step the workflow is on. Completing a later one early is refused.<br><br>

**Step IDs are exact.** <br>
A step ID that isn't in your application's workflow, or a `workflow_id` that doesn't belong to the `application_id`, returns a `404` error.<br><br>

**Completion isn't idempotent.** <br>
Completing a step you've already completed is refused with a `409` error. If a completion call times out or you're not sure it succeeded, call [Get Current Steps](/api-reference/#get-current-steps) before you retry.<br><br>

**You never complete the `id_verification` step.** <br>
It completes on its own when you complete `form_submit` or `form_submit_corp`, so the workflow is finished at that point and the step never appears in a response. Verifying identity is still a separate call, which you make after submitting. On an individual application you verify the applicant. On a corporate application you verify a director, and only a person with the `director` role can be verified, which may not be the person filling in the application. Each flow page covers it.<br><br>

**Submission can only happen once.** <br>
Submitting locks the application, any further attempts to submit it fail. Review the application before you submit it.<br><br>

**Most responses are wrapped in `data`.** <br>
The application and its resources, such as people and documents, are returned under `data`. The create response, the workflow endpoints and identity verification return their fields at the top level instead.

## Workflow steps

### Individual

| **Step** | **What it's for** | **You send first** |
|---|---|---|
| `basic_info` | The applicant's country, phone number and marketing preference | `PUT /v2/applications/{application_id}` |
| `personal_details` | The applicant personal details: name, date of birth, address and citizenship | `POST /v2/applications/{application_id}/people` |
| `account_usage` | How the applicant will use the account | `PUT /v2/applications/{application_id}/account_usage` |
| `documents` | The applicant's documents | [Create Document](/api-reference/#create-document), then [Create Document File](/api-reference/#create-document-file), then attach them to the applicant with `document_ids` |
| `form_submit` | Confirms the application has been submitted | `POST /v2/applications/{application_id}/submit` |
| `id_verification` | Completes on its own. See [Key concepts](#key-concepts) | — |

### Corporate

| **Step** | **What it's for** | **You send first** |
|---|---|---|
| `basic_info_corp` | The contact details of the person filling in the application, and their consents | `PUT /v2/applications/{application_id}` |
| `business_information_corp` | The company: name, registration, sector and addresses | `PUT /v2/applications/{application_id}/business_information` |
| `account_usage_corp` | How the company will use the account | `PUT /v2/applications/{application_id}/account_usage` |
| `people_corp` | Every user, director and owner on the application | `POST /v2/applications/{application_id}/people` once per person |
| `documents_corp` | The company's and its people's documents | [Create Document](/api-reference/#create-document), then [Create Document File](/api-reference/#create-document-file), then attach them to the person or business with `document_ids` |
| `form_submit_corp` | Confirms the application has been submitted | `POST /v2/applications/{application_id}/submit` |
| `id_verification` | Completes on its own. See [Key concepts](#key-concepts) | — |

## Navigating the workflow

| **Call** | **What it does** |
|---|---|
| `PUT /v2/workflows/{workflow_id}/steps/{step_id}/completion` | Completes a step |
| `GET /v2/workflows/{workflow_id}/steps/current` | Tells you which step you're on |
| `GET /v2/workflows/{workflow_id}/steps/previous` | Tells you the step before the one you're on |
| `PUT /v2/workflows/{workflow_id}/steps/current` | Moves you to a step you've completed, or to any step before the one you're on |

Note that all four need `?application_id={application_id}`. None of their responses are wrapped in `data`.

### 1. Complete a step

```
PUT /v2/workflows/{workflow_id}/steps/basic_info/completion?application_id={application_id}

{ "status": "completed" }
```

```
200 OK
{
  "application_id": "3f1c2a8e-…",
  "workflow_id": "9b7d4e10-…",
  "steps": ["personal_details"]
}
```

The `steps` field in the response shows the next step to take. Once you complete `form_submit` or `form_submit_corp`, it comes back empty as the workflow is finished.

Note that `completed` is the only `status` you can send. Any other value, or no `status`, returns a `422` error.

Before the step completes, its data is checked. If something is missing, you get a `422` error naming the field, and the step stays where it was:

```
422 Unprocessable Content
{
  "status": "failed",
  "error_code": "request_invalid",
  "reason": "Request invalid error",
  "error_messages": {
    "agreed_to_marketing_emails": [
      {
        "error_code": "validation",
        "reason": "agreed_to_marketing_emails must be present to complete this step"
      }
    ]
  }
}
```

Send the missing data, then complete the step again.

### 2. Check where you are

```
GET /v2/workflows/{workflow_id}/steps/current?application_id={application_id}
```

```
200 OK
{
  "step_ids": ["personal_details"]
}
```

This call only reads, so it's safe at any point. Use it to confirm that a step was completed successfully, or to pick up where you left off.

The `step_ids` field holds at most one step. **An empty `step_ids` means the workflow is finished.**

A note about the field name: the completion response calls it `steps`, while this call and the previous-step call it `step_ids`. Both are lists of step IDs.

### 3. Go back a step

Going back takes two calls. First, find the step before the one you're on:

```
GET /v2/workflows/{workflow_id}/steps/previous?application_id={application_id}
```

```
200 OK
{
  "step_ids": ["basic_info"]
}
```

Field `step_ids` holds at most one step. At this point, an empty `step_ids` means you're at the first step. It doesn't mean the workflow is finished, only [Get Current Steps](/api-reference/#get-current-steps) tells you that.

To move to that step, call:

```
PUT /v2/workflows/{workflow_id}/steps/current?application_id={application_id}

{ "step_id": "basic_info" }
```

```
200 OK
{
  "application_id": "3f1c2a8e-…",
  "workflow_id": "9b7d4e10-…",
  "steps": ["basic_info"]
}
```

Going back resets the step you were on, so you'll need to complete it again. The step you moved back to is reopened. Send its data again using the full request body, since PUT replaces the existing data. Then complete the step and continue from there.

Make corrections before you submit. Once [Submit Application](/api-reference/#submit-application) succeeds, the application and its resources are locked. Until you complete `form_submit` or `form_submit_corp` you can still move between steps, but any update to the data is refused with a `422` error.

You can move to a step you've completed, or to any step before the one you're on. The step you leave is reset, even if you'd completed it. After going back, don't move forward. Complete the step you went back to instead. The workflow takes you to the earliest step that isn't completed, usually the step you left. Attempting to move to an uncompleted step ahead of your current step returns a `409` error.

## Workflow-specific errors

When the workflow itself refuses a call, you get a `409` with an `error_code` that says why:

| **Situation** | **`error_code`** |
|---|---|
| You completed a step other than the current step, either one you haven't reached yet or one you've already completed. If the step's data fails its checks, a `422` error is returned instead | `step_not_started` |
| You moved to a step ahead of the one you're on that isn't completed, including the one you just left | `step_navigation_not_allowed` |
| You tried to complete or move to `id_verification` | `step_not_actionable` |
| The workflow is finished | `workflow_already_completed` |

Treat `error_code` as an open set: new codes may be added.
