[_metadata_:menu_title]:- "Verification of Payee Outbound (EU)"
[_metadata_:order]:- "13"

# Verification of Payee (EU)

#### Use the Verify Beneficiary Account API and Create Beneficiary API together to reduce misdirected EUR SEPA payments

## Introduction

**Learn how to verify beneficiary bank account details before creating a beneficiary to improve customer experience and reduce misdirected payments.**  <br><br>


This guide is designed to help you verify beneficiary bank account details for outbound EUR SEPA payments, via the Verify Beneficiary Account API on our Verification of Payee Outbound service. Verifying beneficiaries helps avoid payments being sent to the wrong account and adds another layer of protection in the fight against fraud and scams.

For clients under the Sponsored or Treasury service model and contracted with Currencycloud BV, it is a **mandatory** requirement to integrate with this API if you offer EUR SEPA payments to your customers.


<p style="border-width:3px; border-style:solid; border-color:#FF5000; padding: 1em;"><strong>Beta notice</strong> <br><br>
Please be aware this API is in beta. Some response codes and reasons may change during this period. We will always provide at least 10 days notice before implementing any changes that may be breaking during the beta period.</p> <br><br>


**What is it?**

The [Verify Beneficiary Account](/api-reference/#verify-beneficiary-account) API endpoint can be used to verify a beneficiary's bank account details, and in the SEPA Euro market verify the name of the individual or company provided.

**How does it work?**

1 The end-customer inputs the beneficiary’s account details.

2 Currencycloud forwards this request to the beneficiary’s bank, or cross-references it against a dataset.

3 For the EU market, we will return a response displaying the result of the verification that may include `answer`, `actual_name`, `reason_code`, `reason`, `reason_type`.


**Who is an end-customer, and where does the verification need to take place?**  

In most cases, an end-customer will be an individual or business that we contract with and provide regulated payment services to. The requirement is that the end-customer must be able to receive a verification response before they proceed to create the beneficiary on your interface. For example, if you are an accounts payable platform, the end-customer using the platform must be able to verify the beneficiary details before creating the beneficiary and submitting the invoice payment.

However, in some use cases the end-customer cannot create a beneficiary, but you are still technically in scope to provide this service. An example of this might be a Wealthtech that automatically populates the same account details used to pay-in. If this applies to you, please consult your Account Manager and Solutions Consultant who will work with you to understand your use case.

**Availability**

We already offer the [Verify Beneficiary Account](/api-reference/#verify-beneficiary-account) API in the UK, and are now expanding to the SEPA EUR regions in Beta. We will support more countries in the future. Please contact customer support or your Account Manager to find out more.

----------

## Step 1: Login

Please refer to the [Authentication guide](https://developer.currencycloud.com/guides/integration-guides/authentication/ "https://developer.currencycloud.com/guides/integration-guides/authentication/") for instructions for starting a new API session. Make sure your Contact ID is enabled to access this product in our Demo environment.

----------

## Step 2: Verify Beneficiary

You will be required to verify your beneficiaries in the following scenarios:

a. Before you create a new beneficiary

b. Before you update details of an existing beneficiary

c. Before you send a payment to an existing beneficiary

d. Before you send a payment to a new beneficiary

To verify a beneficiary’s bank account details in the SEPA EUR regions, make a POST request to the [Verify Beneficiary Account](/api-reference/#verify-beneficiary-account) endpoint.

`POST /v2/beneficiaries/account_verification.`

### Requests

The request body includes the following parameters:

`Content-Type: multipart/form-data`

| Parameter Name | Parameter Type | Mandatory | Example Value | Notes|
|---|---|---|---|---|
| payment_type| Form Data | Yes | regular | Regular for Local payments. |
| bank_country | Form Data | Yes | NL | Two-letter code for the country in which the beneficiary's bank account is held. |
| currency | Form Data | Yes | EUR | Three-letter currency code. <br><br> Currency in which money will be sent to the beneficiary's bank account. |
| beneficiary_entity_type | Form Data | Yes | individual | "individual" or "company".<br> If individual then 'beneficiary_first_name' and 'beneficiary_last_name' are mandatory. <br> If company then 'beneficiary_company_name' is mandatory. |
| beneficiary_company_name | Form Data | --- | ---| Must include this if the entity is a Company.|
| beneficiary_first_name | Form Data | --- | Ricardo | Must include this if the entity is an Individual. |
| beneficiary_last_name | Form Data | --- | Sousa | Must include this if the entity is an Individual. |
| iban | Form Data | Yes | [Sensitive data redacted]  | Must include this in the request |

**Example Request:**  

```
{
  "payment_type": "regular",
  "bank_country": "NL",
  "currency": "EUR",
  "beneficiary_entity_type": "individual",
  "beneficiary_company_name": null,
  "beneficiary_first_name": "Ricardo",
  "beneficiary_last_name": "Sousa",
  "iban": [Sensitive data redacted]
}
```

### **Responses**

**Example Responses**  

```
200
{
	"answer": "full_match",
	"actual_name": "Ricardo Sousa",
	"reason_code": "AV100",
	"reason": "Beneficiary details confirmed.", 			
	"reason_type": "okay"
}
```

The following parameters are included in the response body.

<p style="border-width:3px; border-style:solid; border-color:gray; padding: 1em;">You must disable the ability of your interface to cache data so that no end-customer is able to access data previously obtained under a VoP Request without undertaking a further VoP Request.</p> <br><br>


| Parameter Name |  Parameter Type |Type | Example Value | Field Description |
| --- |--- | --- | --- | ---|
| answer | FormData | enum | full_match | Indicates whether the verification resulted in a match. Possible values are `full_match`, `close_match`, or `no_match`. |
| actual_name | Form Data | string | Ricardo Sousa | The actual name of the account holder. Present if reason_code is `AV100` or `AV300`  |
| reason_code |  FormData | enum | AV100 | Encoded reasons. Present if answer is `full_match` , `close_match` or `no_match`. <br> See reason code tab for full list and handling requirements. |
| reason | FormData | string | Beneficiary details confirmed | Metadata for reason_code. Only populated if reason_code is present. Values correspond to code descriptions for the reason_code. |
| reason_type | FormData | enum | okay | Metadata for reason. Only populated if `reason_code` is present. Type corresponds to suggested warning message requirements in client UI. Possible values are `okay`, `rejected` and `warning`. |

### Guidance on reflecting API responses in the UI

When integrating with our Verify Beneficiary Account API it is important to handle the various responses effectively in order to provide a seamless user experience. Below are suggestions for implementing each response in your interface, with copy and UX handling suggestions.

<p style="border-width:3px; border-style:solid; border-color:gray; padding: 1em;">If you’re a Sponsored or Treasury model client that contracts with Currencycloud BV using the API then you <b>must</b> include this step as part of your EUR beneficiary creation flow before paying out to a beneficiary via our create payment API.</p> <br><br>

### 1. AV100 (Full match)


**Request:**  

```
{
	"payment_type": "regular", 	
	"bank_country": "NL",
	"currency": "EUR",
	"beneficiary_entity_type": "individual",
	"beneficiary_company_name": null,
	"beneficiary_first_name": "Ricardo",
	 "beneficiary_last_name": "Sousa",
	 "iban": "[Sensitive data redacted]"
}
```

**Response:**  

```
200
{
	"answer": "full_match",
	"actual_name": "Ricardo Sousa",
	"reason_code": "AV100",
	 "reason": "Beneficiary details confirmed.",
	 "reason_type": "okay"
}
```

**API Reason**: Beneficiary details confirmed.<br><br>

**Description**: The beneficiary details provided match those on record. <br><br>

**Handling**: The end-customer can proceed with creating the beneficiary. <br><br>

**UI Suggestion:** <br><br>

<img src="/images/account_verification/VoP-eu-1.png" width=100%>

### 2. AV300 (Close match)

Request:

```
{
  "payment_type": "regular",
  "bank_country": "NL",
  "currency": "EUR",
  "beneficiary_entity_type": "individual",
  "beneficiary_company_name": null,
  "beneficiary_first_name": "Ricardo",
  "beneficiary_last_name": "Sous",
  "iban": "[Sensitive data redacted]"
}
```

Response:

```
200
{
    "answer": "close_match",
    "actual_name": "Ricardo Sousa",
    "reason_code": "AV300",
    "reason": "The beneficiary details provided closely match those on record, however the beneficiary name is Ricardo Sousa. By authorising this payment, you may be transferring funds to a payment account that does not belong to the intended recipient. Please double-check the beneficiary details before proceeding.",
    "reason_type": "warning"

}
```
**API Response**: AV300<br><br>  

**Description**: The beneficiary details provided closely match those on record, however the beneficiary name is [actual_name]. By authorising this payment, you may be transferring funds to a payment account that does not belong to the intended recipient. Please double-check the beneficiary details before proceeding. <br><br>

**Handling**: In the event of a close match, display the `actual_name` to the end-customer. Consider providing a call to action or button to nudge the user into submitting the correct details. This reduces cognitive load and makes it easier for them to adjust their choice.<br><br>  

In the event of a close match, it’s important that you explain the problem and solution clearly. However, if the end-customer decides to proceed, present a dialogue box with a secondary warning indicating that they do so at their own discretion and risk.<br><br>

**UI Suggestion:** <br><br>

<img src="/images/account_verification/VoP-eu-2.png" width=100%>

### 3. AV201 (No match)

Request:

```
{
  "payment_type": "regular",
  "bank_country": "NL",
  "currency": "EUR",
  "beneficiary_entity_type": "individual",
  "beneficiary_company_name": null,
  "beneficiary_first_name": "Ricardo",
  "beneficiary_last_name": "Smith",
  "iban": "[Sensitive data redacted]"
}
```

Response:  

```
200
{
  "answer": "no_match",
  "actual_name": null,
  "reason_code": "AV201",
  "reason": "Beneficiary details provided do not match those on record. By authorising this payment, you may be transferring funds to a payment account that does not belong to the intended recipient. Please double-check the beneficiary details before proceeding.",
  "reason_type": "rejected"
}
```

**API Response**: AV201 <br><br>

**Response:** Beneficiary details provided do not match those on record. By authorising this payment, you may be transferring funds to a payment account that does not belong to the intended recipient. Please double-check the beneficiary details before proceeding. <br><br>  

**Handling:** There is a no match. Display a negative notice highlighting the error. The actual_name will not be provided in the response. Create a button to give the end-customer the choice to edit the account details or keep what they entered. <br><br>

In the event of a no match, it’s important that you explain the problem clearly. However, if the end-customer decides to proceed, present a dialogue box with a secondary warning indicating that they do so at their own discretion and risk.

**UI Suggestion:** <br><br>

<img src="/images/account_verification/VoP-eu-3.png" width=100%>

### 4. AV208 (No match)

Request:

```
{
  "payment_type": "regular",
  "bank_country": "NL",
  "currency": "EUR",
  "beneficiary_entity_type": "Company",
  "beneficiary_company_name": "ABC Corp",
  "beneficiary_first_name": "null",
  "beneficiary_last_name": "null",
  "iban": "[Sensitive data redacted]"
}
```

Response:  

```
200
{
  "answer": "no_match",
  "actual_name": null,
  "reason_code": "AV208",
  "reason": "The beneficiary details provided could not be verified, as the beneficiary's bank does not perform the check. By continuing with this payment, you may be transferring funds to a payment account that does not belong to the intended recipient. Please double-check the beneficiary details before proceeding.",
  "reason_type": "rejected"
}
```

**API Response:** AV208

**Response:** The beneficiary details provided could not be verified, as the beneficiary's bank does not perform the check. By continuing with this payment, you may be transferring funds to a payment account that does not belong to the intended recipient. Please double-check the beneficiary details before proceeding. <br><br>  

**Handling:** It’s not a match. Display a negative notice highlighting the error. The actual_name will not be provided in the response. Create a button to give the end-customer the choice to edit the account details or keep what they entered. <br><br>

In the event of a no match, it’s important that you explain the problem clearly. However, if the end-customer decides to proceed, present a dialogue box with a secondary warning indicating that they do so at their own discretion and risk.

**UI Suggestion:** <br><br>

<img src="/images/account_verification/VoP-eu-4.png" width=100%>

**Full list of reason codes:**

<p style="border-width:3px; border-style:solid; border-color:gray; padding: 1em;">The style and tone of the Currencycloud Direct platform serve as the basis for our copy and handling suggestions. Although it's not necessary to match this exactly, your integration should closely mirror it to maintain a consistent user experience.</p>


#### Successful Responses (HTTP 200)

<table style="width:100%">
  <tr>
    <td style="width:15%">Answer</th>
    <td style="width:11%">Reason<br> Code</td>
    <td style="width:13%">Reason</td>
    <td style="width:12%">Reason Type</td>
    <td style="width:27%">Suggested Copy</td>
    <td style="width:24%">How to handle</td>
  </tr>
  <tr>
    <td><span style="color:#78A75A;">full_match</span></td>
    <td><span style="color:#78A75A;">AV100</span></td>
    <td>Beneficiary details confirmed.</td>
    <td>Okay</td>
    <td><img src="/images/account_verification/check.svg"> <b>Beneficiary details confirmed</b><br><br>
      The beneficiary details provided match those on record..<br><br>
      [Back] <br>
      [Cancel] <br>
      [Create Beneficiary]  
    </td>
    <td>Display a positive notice to end-customer, indicating successful verification.</td>
  </tr>
  <tr>
    <td><span style="color:#BB271A">no_match</span></td>
    <td><span style="color:#BB271A">AV201</span></td>
    <td>Beneficiary details provided do not match those on record. By authorising this payment, you may be transferring funds to a payment account that does not belong to the intended recipient. Please double-check the beneficiary details before proceeding.</td>
    <td>Rejected</td>
    <td><img src="/images/account_verification/error.svg"> <b>Unable to match beneficiary details</b><br><br>
      The beneficiary details provided do not match those on record. By continuing with this payment, you may be transferring funds to a payment account that does not belong to the intended recipient. Please double-check the beneficiary details before proceeding.<br><br>
      [Back] <br>
      [Cancel] <br>
      [Create beneficiary]<br>
      <hr>
      <b>Are you sure you want to continue? </b><br><br>
      Paying this person or business may lead to your money being sent to the wrong account. We may not be able to recover the money for you.<br><br>
      [Cancel]<br>
      [Continue Anyway] <br>
    </td>
    <td>1. Display a negative notice highlighting the error. <br>
       2. Create a button to give the end-customer the choice to go Back, Cancel or Create Beneficiary.<br>
       3. If the user clicks/taps 'Back' a new API request must be submitted to check the new details.<br>
       4. If the user clicks/taps 'Create Beneficiary', end-customer should receive a secondary warning via a dialogue box.
    </td>
  </tr>
  <tr>
    <td><span style="color:#BB271A">no_match</span></td>
    <td><span style="color:#BB271A">AV202</span></td>
    <td>The beneficiary details provided could not be verified at this time. By continuing with this payment, you may be transferring funds to a payment account that does not belong to the intended recipient. Please double-check the beneficiary details before proceeding. </td>
    <td>Rejected</td>
    <td><img src="/images/account_verification/error.svg"> <b>Unable to verify beneficiary details</b><br><br>
      The beneficiary details provided could not be verified at this time. By continuing with this payment, you may be transferring funds to a payment account that does not belong to the intended recipient. Please double-check the beneficiary details before proceeding.<br><br>
      [Back] <br>
      [Cancel] <br>
      [Create Beneficiary]<br>
      <hr>
      <b>Are you sure you want to continue? </b><br><br>
      Paying this person or business may lead to your money being sent to the wrong account. We may not be able to recover the money for you.<br><br>
      [Cancel]<br>
      [Continue Anyway] <br>
    </td>
    <td>1. Display a negative notice highlighting the error. <br>
       2. Create a button to give the end-customer the choice to go Back, Cancel or Create Beneficiary.<br>
       3. If the user clicks/taps 'Back' a new API request must be submitted to check the new details.<br>
       4. If the user clicks/taps 'Create Beneficiary', end-customer should receive a secondary warning via a dialogue box.
    </td>
  </tr>
  <tr>
    <td><span style="color:#BB271A">no_match</span></td>
    <td><span style="color:#BB271A">AV208</span></td>
    <td>The beneficiary details provided could not be verified, as the beneficiary's bank does not perform the check. By continuing with this payment, you may be transferring funds to a payment account that does not belong to the intended recipient. Please double-check the beneficiary details before proceeding.</td>
    <td>Rejected</td>
    <td><img src="/images/account_verification/error.svg"> <b>Unable to verify beneficiary details</b><br><br>
      The beneficiary details provided could not be verified, as the beneficiary's bank does not perform the check. By continuing with this payment, you may be transferring funds to a payment account that does not belong to the intended recipient. Please double-check the beneficiary details before proceeding.<br><br>
      [Back] <br>
      [Cancel] <br>
      [Create Beneficiary]<br>
      <hr>
      <b>Are you sure you want to continue? </b><br><br>
      Paying this person or business may lead to your money being sent to the wrong account. We may not be able to recover the money for you.<br><br>
      [Cancel]<br>
      [Continue Anyway] <br>
    </td>
    <td>1. Display a negative notice highlighting the error. <br>
       2. Create a button to give the end-customer the choice to go Back, Cancel or Create Beneficiary.<br>
       3. If the user clicks/taps 'Back' a new API request must be submitted to check the new details.<br>
       4. If the user clicks/taps 'Create Beneficiary', end-customer should receive a secondary warning via a dialogue box.</td>
  </tr>
<tr>
    <td><span style="color:orange">close_match</span></td>
    <td><span style="color:orange">AV300</span></td>
    <td>The beneficiary details provided closely match those on record, however the beneficiary name is `[actual_name]`. By authorising this payment, you may be transferring funds to a payment account that does not belong to the intended recipient. Please double-check the beneficiary details before proceeding.</td>
    <td>Warning</td>
    <td><img src="/images/account_verification/warning.svg"> <b>Incorrect beneficiary name</b><br><br>
      The beneficiary details provided closely match those on record, however the beneficiary name is `[actual_name]`. By authorising this payment, you may be transferring funds to a payment account that does not belong to the intended recipient. Please double-check the beneficiary details before proceeding.<br><br>
      [Back] <br>
      [Cancel] <br>
      [Create Beneficiary]<br>
   _(disabled until selection is made)_
      <hr>
      <b>Are you sure you want to continue? </b><br><br>
      Paying this person or business may lead to your money being sent to the wrong account. We may not be able to recover the money for you.<br><br>
      [Cancel]<br>
      [Continue Anyway] <br>
    </td>
    <td>1. Display a negative notice highlighting the error. <br>
       2.   The `actual_name` will be provided. Wrap the provided copy around the [`actual_name`].<br>
       3. Create a button to give the end-customer the choice to go Back, Cancel or Create Beneficiary.<br>
       4.  If the user clicks/taps Back a new API request must be submitted to check the new details.<br>
       5. If the user clicks/taps “Create Beneficiary”, end-customer should receive secondary warning via a dialogue box.
    </td>
  </tr>

</table>

#### Full list of technical Errors

##### HTTP 503 - Service Unavailable

<table style="width:100%">
  <tr>
    <td style="width:21%">Error Code</th>
    <td style="width:15%">Error<br> Error reason</td>
    <td style="width:32%">Required Copy</td>
    <td style="width:32%">How to handle</td>
  </tr>
  <tr>
    <td><span style="color:#BB271A;">service_unavailable</span></td>
    <td>Service is temporarily unavailable</td>
    <td><img src="/images/account_verification/warning.svg"> <b>Unable to verify beneficiary details</b><br><br>
      It has not been possible to check the beneficiary details you have provided at this time. Please try creating the beneficiary again later, or click 'Create Beneficiary' if you are sure the details are correct.<br><br>
      [Back] <br>
      [Cancel] <br>
      [Create Beneficiary]  
      <hr>
      <b>Are you sure you want to continue? </b><br><br>
      Paying this person or business may lead to your money being sent to the wrong account. We may not be able to recover the money for you.<br><br>
      [Cancel]<br>
      [Continue Anyway] <br>
    </td>
    <td> <b>Connection has failed</b><br><br>
      1. Display a negative notice highlighting the issue.<br>
      2. Introduce an internal retry mechanism, before presenting the error back to the user.<br>
      3. If the user clicks/taps 'Back to details', the end-customer goes back to the beneficiary creation screen.<br>
      4. A new request is required to check the new details.<br>
      5. If the user clicks/taps 'Continue Anyway', the end-customer should receive a secondary warning.<br>
    </td>
  </tr>
</table>

##### HTTP 400 - Bad Request

Required copy and handling requirements are not applicable for HTTP 400 errors as the end-customer should not be able to trigger these validations.  

| Error Code | Error Reason |
|--- | --- |
| <span style="color:#BB271A;">invalid_bank_country</span> | bank country is not supported|
| <span style="color:#BB271A;">invalid_field_bank_country</span> | bank_country must match `\"^[A-Z]{2}\$\`|
| <span style="color:#BB271A;">invalid_field_iban</span> | iban must match `^[a-zA-Z]{2}[0-9]{2}[a-zA-Z0-9]{1,30}$``|
| <span style="color:#BB271A;">invalid_field_beneficiary_type</span> | beneficiary_entity_type must be either 'individual' or 'company'.|
| <span style="color:#BB271A;">expect_individual_names_only</span> |beneficiary_company_name must not be supplied when beneficiary_entity_type is individual. |
| <span style="color:#BB271A;">expect_company_name_only</span> |beneficiary_first_name and beneficiary_last_name must not be supplied when beneficiary_entity_type is company. |
| <span style="color:#BB271A;">missing_individual_names</span> |beneficiary_first_name and beneficiary_last_name are required when beneficiary_entity_type is individual. |
| <span style="color:#BB271A;">missing_company_name</span> |beneficiary_company_name is required when beneficiary_entity_type is company. |

----------

## Step 3: Create Beneficiary

After verifying the details, you can then set up a beneficiary record by making a POST request to the '[Create Beneficiary](https://developer.currencycloud.com/api-reference/#create-beneficiary "https://developer.currencycloud.com/api-reference/#create-beneficiary")' endpoint at `/v2/beneficiaries/create` and proceed with sending your payments.

<p style="border-width:3px; border-style:solid; border-color:gray; padding: 1em;">If there's a 'close match' during Account Verification and the user picks the account name from the response, you need to use those details when setting up the beneficiary.</p>

`POST /v2/beneficiaries/account_verification.`

`Content-Type: multipart/form-data` <br><br>

| **Parameter Name** | **Parameter Type** | **Example Value** |
|--- | --- | --- |
| name | Form Data | Ricardo Sousa |
| bank_account_holder_name | Form Data | Ricardo Sousa |
| currency | Form Data | EUR |
| beneficiary_country | Form Data | FR |
| bank_country | Form Data | FR |
| iban | Form Data | [Sensitive data redacted] |


If the beneficiary is successfully created, the response message will contain full details about the beneficiary as recorded in your Currencycloud account.

<p style="border-width:3px; border-style:solid; border-color:gray; padding: 1em;">Note the beneficiary's unique ID (`id`). You'll need this to make a payment to the beneficiary.</p>

```
HTTP/1.1 200 OK Content-Type: application/json

{
  "id": "aea097c2-39e4-49b5-aaa6-c860ca55ca0b",
  "bank_account_holder_name": "Acme GmbH",
  "name": "Acme GmbH", "email": null,
  "payment_types": [ "regular" ],
  "beneficiary_address": [],
  "beneficiary_country": "DE",
  "beneficiary_entity_type": null,
  "beneficiary_company_name": null,
  "beneficiary_first_name": null,
  "beneficiary_last_name": null,
  "beneficiary_city": null,
  "beneficiary_postcode": null,
  "beneficiary_state_or_province": null,
  "beneficiary_date_of_birth": null,
  "beneficiary_identification_type": null,
  "beneficiary_identification_value": null,
  "bank_country": "DE",
  "bank_name": "Test Bank Plc",
  "bank_account_type": null,
  "currency": "EUR",
  "iban": "[Sensitive data redacted]",
  "default_beneficiary": "false",
  "creator_contact_id": "1993263d-be07-42d4-b75b-ae4ea18bcb6c",
  "bank_address": [],
  "created_at": "2021-02-02T11:52:23+00:00",
  "updated_at": "2021-02-02T11:52:23+00:00",
  "beneficiary_external_reference": null
}
```

----------

## Step 4: Develop your User Journey

The following best practices are recommended when integrating  Verify Beneficiary Account API into your application:

1  **Clear Messaging**: Ensure that the message accompanying each response is succinct, informative, and user-friendly.

2  **Visual Feedback**: Use visual elements such as icons, colours, and message banners to provide clear feedback to users.

3  **Error Handling**: Implement robust error handling to gracefully deal with unexpected responses or errors from the Verify Beneficiary Account API.

4  **Accessibility**: Design the UI to be accessible to all users, ensuring that response messages are perceivable and understandable.


By following these guidelines you can seamlessly integrate the  Verify Beneficiary Account API responses with your interface, providing users with a smooth and intuitive experience when verifying beneficiary details.

**Here are examples**<br><br>
Example 1 - Paying a new beneficiary
<img src="/images/account_verification/VoP-eu-5.png" width=100%>

Example 2 - Paying an existing beneficiary
<img src="/images/account_verification/VoP-eu-6.png" width=100%>
