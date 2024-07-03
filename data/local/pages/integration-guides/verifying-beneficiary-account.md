[_metadata_:menu_title]:- "Confirmation of Payee Outbound (UK)"
[_metadata_:order]:- "10"

# Confirmation of Payee Outbound (UK)

## Introduction

#### Learn how to verify beneficiary bank account details before creating a beneficiary in order to improve customer experience and reduce misdirected payments in the UK.

This guide is designed to help you verify beneficiary bank account details for outbound local GBP payments, via the Verify Beneficiary our Confirmation of Payee service. Verifying beneficiaries helps avoid payments being sent to the wrong account and adds another layer of protection in the fight against fraud and scams.

For clients under the Sponsored and Treasury service model and contracted with The Currency Cloud Limited, it is a **mandatory** requirement to integrate with this API if you offer local GBP payments to your end-customers.

**Beta notice**:

Please be aware that this API is in beta. Some response codes and reasons may change during this period. We will always provide at least **10 days advance notice** before implementing any changes that may be breaking during the beta period.

**What is it?**

The Verify Beneficiary Account API can be used to verify a beneficiary's bank account number and, in some markets, check the name of the individual or company provided.

**How does it work?**

1.  The end-customer inputs the beneficiary's account details.
2.  Currencycloud forwards this request to the beneficiary's bank or cross-references it against a dataset.
3.  For the UK market, we return a response displaying the result of the verification with the following fields: `answer`, `actual_name`, `reason_code`, `reason` and `reason_type`.

**Who is an end-customer, and where does the verification need to take place?**  

In most cases, an end-customer will be an individual or business that we contract with and provide regulated payment services to. The requirement is that the end-customer must be able to receive a verification response before they proceed to create the beneficiary on your interface. For example, if you are an accounts payable platform, the end-customer using the platform must be able to verify the beneficiary details before creating the beneficiary and submitting the invoice payment.

However, in some use-cases, the end-customer cannot create a beneficiary but you are still technically in scope to provide this service. An example of this might be a Wealthtech that automatically populates the same account details used to pay-in. If this applies to you, please consult your Customer Success Manager and Solutions consultant and we'll work with you to understand your usecase.

**Availability**  

We currently offer the Verify Beneficiary Account API in the UK in Beta. We will support more countries in the future. Contact customer support or your Customer Success Manager to find out more.

## Step 1: Login

Please refer to the [Authentication guide](https://developer.currencycloud.com/guides/integration-guides/authentication/) for instructions for starting a new API session. Make sure your Contact ID is enabled to access this product in our Demo environment.

## Step 2: Verify Beneficiary

### Requests

To verify a beneficiary's bank account details in the UK, make a POST request to the [Account Verification](/api-reference/#verify-beneficiary-account) endpoint.

`POST /v2/beneficiaries/account_verification.`

The request body includes the following  parameters: 

`Content-Type: multipart/form-data`  


| Parameter Name | Parameter Type | Mandatory | Example Value | Notes|
|---|---|---|---|---|
| payment_type| Form Data | No | regular | "priority" (Swift network) or "regular" (Local) |
| bank_country | Form Data | Yes | GB | Two-letter code for the country in which the beneficiary's bank account is held |
| currency | Form Data | Yes | GBP | Three-letter currency code | Currency in which money will be sent to the beneficiary's bank account |
| account_number | Form Data | Yes | 73515966 | UK bank account number |
| beneficiary_entity_type | Form Data | Yes | individual | "individual" or "company". If individual then 'beneficiary_first_name' and 'beneficiary_last_name' are mandatory. If company then 'beneficiary_company_name' is mandatory. |
| beneficiary_company_name | Form Data | No | Sousa Ltd | Mandatory if entity is "company".|
| beneficiary_first_name | Form Data | No | Ricardo | Mandatory if entity is "individual". |
| beneficiary_last_name | Form Data | No | Sousa | Mandatory if entity is "individual". |
| routing_code_type_1 | Form Data | No | sort_code | Local payment routing system e.g. sort_code, aba, bsb_code, institution_no, bank_code, branch_code, clabe, cnaps |
| routing_code_value_1 | Form Data | No | 015561 | Routing code for routing_code_type_1. |
| routing_code_type_2 | Form Data | No |  |  Local payment routing system |
| routing_code_value_2 | Form Data | No |   | Routing code for routing_code_type_2  |
| bic_swift | Form Data | No |   |  BIC/Swift Code |
| iban | Form Data | No |   | IBAN |
| secondary_reference_data | Form Data | No | | Customer accounts that are not uniquely addressable by a sort code and account number, but instead rely on their PSP to credit their account via SRD – i.e. using the reference field in the payment with a further unique identifier.|



 Example Request:

 ```
 {
  "payment_type": "regular",
  "bank_country": "GB",
  "currency": "GBP",
  "account_number": "73515966",
  "beneficiary_entity_type": "individual",
  "beneficiary_company_name": null,
  "beneficiary_first_name": "Ricardo",
  "beneficiary_last_name": "Sousa",
  "routing_code_type_1": "sort_code",
  "routing_code_value_1": "015561,
  "routing_code_type_2": null,
  "routing_code_value_2": null,
  "bic_swift": null,
  "iban": null
}

```

### Responses
Please note that you **must** disable you interface's ability to cache data so that no end-customer is able to access data previously obtained under a Confirmation of Payee request without undertaking a further Confirmation of Payee request.

Example Responses

```
200
{
  "answer": "full_match",
  "actual_name": "Ricardo Sousa",
  "reason_code": "AV100",
  "reason": "Full match.",
  "reason_type": "okay"
}
```

```
200
{
  "answer": "close_match",
  "actual_name": "Ricardo Sous",
  "reason_code": "AV300",
  "reason": "String is a close match to the account name.",
  "reason_type": "warning"
}
```

The following parameters are included in the JSON response body:

| Parameter Name |  Data Type | Example Value | Description |
|---|---|---|---|
| answer | string | full_match | Indicator of whether the verification has resulted in a match. Possible values are 'full_match', 'close_match' or 'no_match' |
| actual_name | string | Ricardo Sousa | The actual name of the account holder. Present if reason_code is AV100, AV300, AV301 or AV302. |
| reason_code | string | AV100 | Encoded reasons. Present if answer is full_match , close_match or no_match. |
| reason | string | Full match | Metadata for reason_code. Only populated if reason_code is present. Values correspond to description for the reason_code. |
| reason_type | string | okay | Metadata for reason. Only populated if reason_code is present. Type corresponds to suggested warning message requirements in client UI. Possible values are 'okay', 'rejected' and 'warning'. |

### Guidance on reflecting API responses in the UI

When integrating with our Verify Beneficiary Account API, it is important to handle the various responses effectively in order to provide a seamless user experience. Below are suggestions for implementing each response in your interface, with copy and UX handling suggestions.

Reminder: If you're a 'Sponsored' or 'Treasury' model client that contracts with The Currency Cloud Limited using the API then you **must** include the beneficiary account verification step **as part of your UK beneficiary creation flow** before paying out to a beneficiary via our create payment API.

### 1. AV100 (Full match)

Request:

```
{
  "payment_type": "regular",
  "bank_country": "GB",
  "currency": "GBP",
  "account_number": "73515966",
  "beneficiary_entity_type": "individual",
  "beneficiary_company_name": null,
  "beneficiary_first_name": "Ricardo",
  "beneficiary_last_name": "Sousa",
  "routing_code_type_1": "sort_code",
  "routing_code_value_1": "015561",
  "routing_code_type_2": null,
  "routing_code_value_2": null,
  "bic_swift": null,
  "iban": null
}
```

Response:

```
200
{
  "answer": "full_match",
  "actual_name": "Ricardo Sousa",
  "reason_code": "AV100",
  "reason": "Full match.",
  "reason_type": "okay"
}
```

**API Reason**: Full Match<br><br>

**Description:** The beneficiary's bank was able to confirm a full name and account match.  <br><br>

**Handling:** The end-customer can proceed with creating the beneficiary.  <br><br>

**UI Suggestion:** <br><br>

<img src="/images/account_verification/account_verification_full_match.png" width=100%>

### 2. AV300 (Close match)

Request:

```
{
  "payment_type": "regular",
  "bank_country": "GB",
  "currency": "GBP",
  "account_number": "73515966",
  "beneficiary_entity_type": "individual",
  "beneficiary_company_name": null,
  "beneficiary_first_name": "Ricardo",
  "beneficiary_last_name": "Sous",
  "routing_code_type_1": "sort_code",
  "routing_code_value_1": "015561",
  "routing_code_type_2": null,
  "routing_code_value_2": null,
  "bic_swift": null,
  "iban": null
}
```

Response:

```
200
{
        "answer": "close_match",
        "actual_name": "Ricardo Sousa",
        "reason_code": "AV300",
        "reason": "String is a close match to the account name.",
        "reason_type": "warning"
}
```

**API Response:** AV300<br><br>  

**Description:** This is a close match. Display a message highlighting the error, and the risk of proceeding with creation. The actual account_name will be provided in the response.  <br><br>

**Handling:** In the event of a close match, display the actual `account_name` to the end-customer. Consider providing a call to action or button to nudge the user into submitting the correct details. This reduces cognitive load and makes it easier for them to adjust their choice.  

In the event of a close match, it's important that you explain the problem and solution clearly. However, if the end-customer decides to proceed, present a dialogue box with a secondary warning indicating that they do so at their own discretion and risk.  

**UI Suggestion:**<br><br>

<img src="/images/account_verification/account_verification_close_match.png" width=100%>


### 3. AV201 (No match)

Request:

```
{
  "payment_type": "regular",
  "bank_country": "GB",
  "currency": "GBP",
  "account_number": "11235813",
  "beneficiary_entity_type": "individual",
  "beneficiary_company_name": null,
  "beneficiary_first_name": "Ricardo",
  "beneficiary_last_name": "Smith",
  "routing_code_type_1": "sort_code",
  "routing_code_value_1": "314159",
  "routing_code_type_2": null,
  "routing_code_value_2": null,
  "bic_swift": null,
  "iban": null
}
```

Response:  

```
200
{
  "answer": "no_match",
  "actual_name": null,
  "reason_code": "AV201",
  "reason": "String does not match the account name.",
  "reason_type": "rejected"
}
```

API Response: AV201  

**Response:** String does not match the account name. <br><br>  

**Handling:** There is no match. Display a negative notice highlighting the error. The actual account_name will not be provided in the response. Create a button to give the end-customer the choice to edit the account details or keep what they entered. <br><br>

In the event of a no match, it's important that you explain the problem clearly. However, if the end-customer decides to proceed, present a dialogue box with a secondary warning indicating that they do so at their own discretion and risk.  

**UI Suggestion:** <br><br>

<img src="/images/account_verification/account_verification_no_match.png" width=100%>

### Reason codes

This section provides a full list of reason codes along with recommendations for reflecting them on your User Interface.

The style and tone of the Currencycloud Direct platform serves as the basis for our copy and handling suggestions. Although it's not necessary to match this exactly, your integration should closely mirror it to maintain a consistent user experience.

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
    <td>Full match</td>
    <td>Okay</td>
    <td><img src="/images/account_verification/check.svg"> <b>Beneficiary details confirmed</b><br><br>
      The details entered for the beneficiary have been confirmed as an exact match. Please proceed with beneficiary creation.<br><br>
      [Back] <br>
      [Cancel] <br>
      [Create Beneficiary]  
    </td>
    <td>Display a positive notice to end-customer, indicating successful verification.</td>
  </tr>
  <tr>
    <td><span style="color:#BB271A">no_match</span></td>
    <td><span style="color:#BB271A">AV200</span></td>
    <td>There is no account with the given account number.</td>
    <td>Rejected</td>
    <td><img src="/images/error.svg"> <b>Unable to confirm the account details</b><br><br>
      The account number and sort code provided for the beneficiary do not match those on record. Please check the information you have entered and click 'Back' to update if necessary, or click 'Create Beneficiary' if you are sure the details are correct.<br><br>
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
    <td><span style="color:#BB271A">AV201</span></td>
    <td>String does not match the account name. </td>
    <td>Rejected</td>
    <td><img src="/images/account_verification/error.svg"> <b>No match for beneficiary name</b><br><br>
      The name you have provided for the beneficiary does not match that on record. Please check the information you have entered and click 'Back' to update if necessary, or click 'Create Beneficiary' if you are sure the details are correct.<br><br>
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
    <td><span style="color:#BB271A">AV202<br> AV203<br> AV204<br> AV205</span></td>
    <td>Unable to check account details.</td>
    <td>Rejected</td>
    <td><img src="/images/account_verification/error.svg"> <b>Unable to check provided details</b><br><br>
      It has not been possible to check the beneficiary details you have provided. Please check the information you have entered and click 'Back' to update if necessary, or click 'Create Beneficiary' if you are sure the details are correct.<br><br>
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
    <td><span style="color:#BB271A">no_match</span></td>
    <td><span style="color:#BB271A">AV206</span></td>
    <td>Invalid secondary customer reference data.</td>
    <td>Rejected</td>
    <td><img src="/images/account_verification/error.svg"> <b>No match for provided details</b><br><br>
      The reference details you have provided for the beneficiary do not match those on record. Please check the information you have entered and click 'Back' to update if necessary, or click 'Create Beneficiary' if you are sure the details are correct.<br><br>
      [Back] <br>
      [Cancel] <br>
      [Create Beneficiary]  
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
    <td><span style="color:orange">close_match</span></td>
    <td><span style="color:orange">AV300</td>
    <td>String is a close match to the account name</td>
    <td>Warning</td>
    <td><img src="/images/account_verification/warning.svg"> <b>Incorrect beneficiary name</b><br><br>
      The details you have provided for the beneficiary closely match those on record, however the name is '[actual_name]'. Please check the information you have entered and click 'Back' to update the Beneficiary Name to '[actual_name]' if necessary, or click 'Create Beneficiary' if you are sure the details are correct.<br><br>
      [Back] <br>
      [Cancel] <br>
      [Create Beneficiary] (disabled until selection is made)<br>
      <hr>
      <b>Are you sure you want to continue? </b><br><br>
      Paying this person or business may lead to your money being sent to the wrong account. We may not be able to recover the money for you.<br><br>
      [Cancel]<br>
      [Continue Anyway] <br>
    </td>
    <td>   1. Display a negative notice highlighting the error. <br>
      2. The actual account_name will be provided. Wrap the provided copy around the [actual_name].<br>
      3. Create a button to give the end-customer the choice to go Back, Cancel or Create Beneficiary.<br>
      4. If the user clicks/taps 'Back' a new API request must be submitted to check the new details.
      5. If the user clicks/taps 'Create Beneficiary', end-customer should receive a secondary warning via a dialogue box.
    </td>
  </tr>
  <tr>
    <td><span style="color:orange">close_match</span></td>
    <td><span style="color:orange">AV301</td>
    <td>String is a close match to the account name. The type of account is Business when Personal was indicated in the request.</td>
    <td>Warning</td>
    <td><img src="/images/account_verification/warning.svg"> <b>Incorrect company name</b><br><br>
      The details you have provided for the beneficiary closely match those on record, however the company name is '[actual_name]'. Please check the information you have entered and click 'Back' to update the Company Name to '[actual_name]' if necessary, or click 'Create Beneficiary' if you are sure the details are correct.<br><br>
      [Back] <br>
      [Cancel] <br>
      [Create Beneficiary] (disabled until selection is made)
      <hr>
      <b>Are you sure you want to continue? </b><br><br>
      Paying this person or business may lead to your money being sent to the wrong account. We may not be able to recover the money for you.<br><br>
      [Cancel]<br>
      [Continue Anyway] <br>
    </td>
    <td>
      1. Display a negative notice highlighting the error. <br>
      2. The actual account_name will be provided. Wrap the provided copy around the [actual_name].<br>
      3. Create a button to give the end-customer the choice to go Back, Cancel or Create Beneficiary.<br>
      4. If the user clicks/taps 'Back' a new API request must be submitted to check the new details.
      5. If the user clicks/taps 'Create Beneficiary', end-customer should receive a secondary warning via a dialogue box.
    </td>
  </tr>
  <tr>
    <td><span style="color:orange">close_match</span></td>
    <td><span style="color:orange">AV302</td>
    <td>String is a close match to the account name. The type of account is Personal when Business was indicated in the request.</td>
    <td>Warning</td>
    <td><img src="/images/account_verification/warning.svg"> <b>Incorrect beneficiary name</b><br><br>
      The details you have provided for the beneficiary closely match those on record, however the name is '[actual_name]'. Please check the information you have entered and click 'Back' to update the Beneficiary Name to '[actual_name]' if necessary, or click 'Create Beneficiary' if you are sure the details are correct.<br><br>
      [Back] <br>
      [Cancel] <br>
      [Create Beneficiary] (disabled until selection is made)
      <hr>
      <b>Are you sure you want to continue? </b><br><br>
      Paying this person or business may lead to your money being sent to the wrong account. We may not be able to recover the money for you.<br><br>
      [Cancel]<br>
      [Continue Anyway] <br></td>
      <td>1. Display a negative notice highlighting the error. <br>
        2. The actual account_name will be provided. Wrap the provided copy around the [actual_name].<br>
        3. Create a button to give the end-client the choice to go Back, Cancel or Create Beneficiary. <br>
        4. If the user clicks/taps 'Back' a new API request must be submitted to check the new details.
        5. If the user clicks/taps 'Create Beneficiary', the end-customer should receive s secondary warning via a dialogue box.
    </td>
  </tr>
  <tr>
    <td><span style="color:orange">close_match</span></td>
    <td><span style="color:orange">AV303</td>
    <td>String is a match to the account name, but the type of account is Business when Personal was indicated in the request.</td>
    <td>Warning</td>
    <td><img src="/images/account_verification/warning.svg"> <b>Incorrect beneficiary type</b><br><br>
      The details you have provided for the beneficiary closely match those on record, however the beneficiary is recognised as a company not an individual. Please check the information you have entered and click 'Back' to update the Beneficiary Type to 'Company' if necessary, or click 'Create Beneficiary' if you are sure the details are correct.<br><br>
      [Back] <br>
      [Cancel] <br>
      [Create Beneficiary]  
      <hr>
      <b>Are you sure you want to continue? </b><br><br>
      Paying this person or business may lead to your money being sent to the wrong account. We may not be able to recover the money for you.<br><br>
      [Cancel]<br>
      [Continue Anyway] <br>
    </td>
    <td>1. Display a negative notice highlighting the error.<br>
      2. Create a button to give the end-customer the choice to go Back, Cancel or Create Beneficiary.<br>
      3. If the user clicks/taps 'Back' a new API request must be submitted to check the new details.<br>
      4. If the user clicks/taps 'Create Beneficiary', the end-customer should receive a secondary warning via a dialogue box.</td>
  </tr>
  <tr>
    <td><span style="color:orange">close_match</span></td>
    <td><span style="color:orange">AV304</td>
    <td>String is a close match to the account name, but the type of account is Personal when Business was indicated in the request.</td>
    <td>Warning</td>
    <td><img src="/images/account_verification/warning.svg"> <b>Incorrect beneficiary type</b><br><br>
    The details you have provided for the beneficiary closely match those on record, however it is recognised as an individual not a company. Please check the information you have entered and click 'Back' to update the Beneficiary Type to 'Individual' if necessary, or click 'Create Beneficiary' if you are sure the details are correct.<br><br>
    [Back] <br>
    [Cancel] <br>
    [Create Beneficiary] <br>
    <hr>
    <b>Are you sure you want to continue? </b><br><br>
    Paying this person or business may lead to your money being sent to the wrong account. We may not be able to recover the money for you.<br><br>
    [Cancel]<br>
    [Continue Anyway] <br></td>
    <td>1. Display a negative notice highlighting the error. <br>
      2. Create a button to give the end-customer the choice to go Back, Cancel or Create Beneficiary.<br>
      3. If the user clicks/taps 'Back' a new API request must be submitted to check the new details.
      4. If the user clicks/taps 'Create Beneficiary', end-customer should receive a secondary warning via a dialogue box.
    </td>
  </tr>
  <tr>
    <td><span style="color:orange">close_match</span></td>
    <td><span style="color:orange">AV305</td>
    <td>Account has been switched to a different organisation.</td>
    <td>Warning</td>
    <td>
      <img src="/images/account_verification/warning.svg"> <b>Account has been switched</b><br><br>
      The details you have provided for the beneficiary closely match those on record, however the account has been switched to a different organisation. Please check the information you have entered and click 'Back' to update if necessary, or click 'Create Beneficiary' if you are sure the details are correct.<br><br>
      [Back] <br>
      [Cancel] <br>
      [Create Beneficiary]  
      <hr>
      <b>Are you sure you want to continue? </b><br><br>
      Paying this person or business may lead to your money being sent to the wrong account. We may not be able to recover the money for you.<br><br>
      [Cancel]<br>
      [Continue Anyway] <br>
    </td>
    <td> 1. Display a negative notice highlighting the error. <br>
      2. Create a button to give the end-customer the choice to go Back, Cancel or Create Beneficiary.<br>
      3. If the user clicks/taps 'Back' a new API request must be submitted to check the new details.<br>
      4. If the user clicks/taps 'Create Beneficiary', end-customer should receive a secondary warning via a dialogue box.  <br>
    </td>
  </tr>

</table>

#### Technical Errors

##### HTTP 503 - Service Unavailable**

<table style="width:100%">
  <tr>
    <td style="width:21%">Error Code</th>
    <td style="width:15%">Error<br> Reason</td>
    <td style="width:32%">Required Copy</td>
    <td style="width:32%">How to handle</td>
  </tr>
  <tr>
    <td><span style="color:#BB271A;">service_unavailable</span></td>
    <td>Service is temporarily unavailable</td>
    <td><img src="/images/account_verification/error.svg"> <b>Unable to check provided details</b><br><br>
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
      3. If the user clicks/taps 'Back to details, the end-customer goes back to the beneficiary creation screen.<br>
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
| <span style="color:#BB271A;">invalid_field_bank_country</span> | bank_country must match \"^[A-Z]{2}\$\|
| <span style="color:#BB271A;">invalid_field_account_number</span> | account_number must match \^[0-9]{1,8}$\|
| <span style="color:#BB271A;">invalid_field_routing_code_value_1</span> |routing_code_value_1 must match \^[0-9]{6}\$\ |
| <span style="color:#BB271A;">invalid_field_beneficiary_type</span> | beneficiary_entity_type must be either 'individual' or 'company'.|
| <span style="color:#BB271A;">expect_individual_names_only</span> |beneficiary_company_name must not be supplied when beneficiary_entity_type is individual. |
| <span style="color:#BB271A;">expect_company_name_only</span> |beneficiary_first_name and beneficiary_last_name must not be supplied when beneficiary_entity_type is company. |
| <span style="color:#BB271A;">missing_individual_names</span> |beneficiary_first_name and beneficiary_last_name are required when beneficiary_entity_type is individual. |
| <span style="color:#BB271A;">missing_company_name</span> |beneficiary_company_name is required when beneficiary_entity_type is company. |

## Step 3: Create Beneficiary

After verifying the details, you can set up a beneficiary record. Make a POST request to the [Create Beneficiary](/api-reference/#create-beneficiary) endpoint.

Remember, if there's a 'close match' during Account Verification and the user picks the account name from the response, you need to use those details when setting up the beneficiary.

`POST /v2/beneficiaries/create`


If the beneficiary is successfully created, the response message will contain the full details about the beneficiary as recorded in your Currencycloud account.

Note the beneficiary's unique ID (`id`). You'll need this to make a payment to the beneficiary.

```
HTTP/1.1 200 OK
Content-Type: application/json
{
  "id": "aea097c2-39e4-49b5-aaa6-c860ca55ca0b",
  "bank_account_holder_name": "Acme GmbH",
  "name": "Acme GmbH",
  "email": null,
  "payment_types": [
    "regular"
  ],
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
  "account_number": null,
  "routing_code_type_1": null,
  "routing_code_value_1": null,
  "routing_code_type_2": null,
  "routing_code_value_2": null,
  "bic_swift": "COBADEFF",
  "iban": "[Sensitive data redacted]",
  "default_beneficiary": "false",
  "creator_contact_id": "1993263d-be07-42d4-b75b-ae4ea18bcb6c",
  "bank_address": [],
  "created_at": "2021-02-02T11:52:23+00:00",
  "updated_at": "2021-02-02T11:52:23+00:00",
  "beneficiary_external_reference": null
}
```

## Step 4: Develop your User Journey
The following best practices are recommended when integrating Verify Beneficiary Account API into your application:

- **Clear Messaging:** Ensure that the message accompanying each response is succinct, informative, and user-friendly.

- **Visual Feedback:** Use visual elements such as icons, colours, and message banners to provide clear feedback to users.

- **Error Handling:** Implement robust error handling to gracefully deal with unexpected responses or errors from the Verify Beneficiary Account API.

- **Accessibility:** Design the UI to be accessible to all users, ensuring that response messages are perceivable and understandable.

By following these guidelines you can seamlessly integrate the Verify Beneficiary Account API responses with your interface, providing users with a smooth and intuitive experience when verifying beneficiary details.

Here is an example:

![user journey](/images/account_verification/account_verification_user_journey.png)
