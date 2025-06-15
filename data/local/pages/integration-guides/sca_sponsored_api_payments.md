[_metadata_:menu_title]:- "SCA for API Payments"
[_metadata_:order]:- "12"
# Strong Customer Authentication for API Payments

<p style="border-width:3px; border-style:solid; border-color:#FF5000; padding: 1em;"> This guide is only relevant to sponsored model clients.</p>  

To make payments using our API, sponsored model clients are required to apply
Strong Customer Authentication (SCA) when making payments on behalf of their
customers. If you are in-scope, this guide outlines the changes needed to your
payment workflow to accommodate the additional authentication.

## Workflow diagram


![collections](/images/workflow_diagrams/13_sca_api_payments.jpg)

## Step 1: Ensure that we have the correct phone number
When you initiate the payment process on behalf of your customers, we will send
a one-time password (OTP) via SMS to your customer that you will need to provide
in a subsequent request header. It is therefore crucial that we have the correct
mobile phone numbers for your customers.

To update their contact details, please contact support through the Currencycloud Direct platform. We encourage you to raise a single ticket to update the contact details for your customers.

## Step 2: Validate the Payment
Before initiating a payment, call the [Validate Payment](/api-reference/#validate-payment)
endpoint, passing the payment details. Set the Boolean header, `x-sca-opt-in`,
to `true` if you have been informed by Currencycloud that your service model is
in-scope for SCA for API payments. If the payment passes the validation and you
are in-scope for SCA then your customer will receive a OTP via SMS to their
phone which is valid for 10 minutes. The response object will contain the
following headers:

| **Header Name** | **Description**|
| --- | --- |
| `x-sca-id`| UUID for the SCA request.  This will need to be sent when the payment is created.|
| `x-sca-type`| The type of 2FA that was used - SMS or NONE.|
| `x-sca-required`| Indicates whether SCA is required for the payment -true or false.|

Calling the Validate Payment endpoint subsequent times will send a new OTP SMS.

### Example Response:

```
Content-Type: application/json
x-sca-id: 123e4567-e89b-12d3-a456-426614174000
x-sca-type: SMS
x-sca-required: true
{
    "validation_result": "success"
}
```


### Error Codes (sca_check_failed)

**HTTP 400**

| **Error Code**            | **Error Message**                                              | **Description**                                                |
|---------------------------|---------------------------------------------------------------|----------------------------------------------------------------|
| invalid_beneficiary       | Beneficiary could not be found for given id.                  | Beneficiary not found.                                          |
| invalid_extra_x_sca_id    | Validate request should not include `x-sca-id` in header.   | `x-sca-id` header provided in request during validate process.   |
| missing_account           | Account could not be found for given id.                      | Account data could not be found.                                |
| amount_type_is_wrong      | Amount should be of numeric type.                             | Amount in request body is not a numeric.                       |

**HTTP 401**
| **Error Code**            | **Error Message**                                              | **Description**                                                |
|---------------------------|---------------------------------------------------------------|----------------------------------------------------------------|
| internal_server_error | Authentication failed with the supplied credentials | Couldn’t authenticate with the provided `x-auth-token` header.

**HTTP 422**
| **Error Code**            | **Error Message**                                              | **Description**                                                |
|---------------------------|---------------------------------------------------------------|----------------------------------------------------------------|
| internal_server_error | Contact has invalid mobile phone number | Contact has invalid mobile phone number |
| internal_server_error | Contact doesn’t have mobile phone number | Contact doesn’t have mobile phone number |



**HTTP 429**

| **Error Code**            | **Error Message**              | **Description**           |
|---------------------------|--------------------------------|---------------------------|
| internal_server_error | Too many requests for 2FA approval status. | Too many SMS notification sent for same payment data. |



**HTTP 500**
| **Error Code**            | **Error Message**                                              | **Description**                                                |
|---------------------------|---------------------------------------------------------------|----------------------------------------------------------------|
| internal_server_error     | Error getting beneficiary.                    | Error while fetching the beneficiary.                     |
| internal_server_error     | Error validating SCA signature.               | Unable to generate a signature for the payment request body. |
| internal_server_error     | Error getting account.                         | Error while trying to fetch account data.                |
| internal_server_error     | Error sending 2FA token request.               | Unable to send SMS.                    |

## Step 3:  Submit the Payment
When you are ready to [make the payment](/guides/integration-guides/make-simple-payments), call our [Create Payment](/api-reference/#create-payment) endpoint, passing the payment details and the following additional header parameters:

| **Header Name**   | **Description**                                                                                                         |
|-------------------|-------------------------------------------------------------------------------------------------------------------------|
| `x-sca-opt-in`      | Set to true if you have been informed by Currencycloud that your service model is in-scope for SCA for API payments.     |
| `x-sca-id`          | The UUID returned by the Validate Payment request (step 2 above).                                                       |
| `x-sca-token`       | The OTP received following the Validate Payment request.                                                                |

If the OTP is successfully validated, then the payment will be processed.

### Error Codes (sca_check_failed)

**HTTP 400**

| **Error Code**          | **Error Message**                                    | **Description**                                                      |
|-------------------------|------------------------------------------------------|----------------------------------------------------------------------|
| invalid_beneficiary     | Beneficiary could not be found for given id.         | Beneficiary not found.                                                |
| missing_x_sca_token     | SCA required but no token included in request.        | `x-sca-token` header expected but none provided.                       |
| invalid_request_body    | Invalid request body for given `x-sca-id`.              | Request body doesn’t match the one provided for validate request.    |
| invalid_x_sca_id        | Invalid `x_sca_id`.                                     | Provided `x-sca-id` cannot be found in the database.                   |
| x-account-identifier    | Account could not be found for given id.             | Account data couldn’t be found.                                      |
| missing_beneficiary     | Beneficiary was not defined in the request.          | Missing beneficiary id in request body.                              |
| missing_amount          | Amount was not defined.                              | Missing amount in request body.                                      |
| missing_currency        | Currency was not defined.                            | Missing currency in request body.                                    |
| mmount_type_is_wrong    | Amount should be of numeric type.                    | Amount in request body is not of numeric type.                       |

**HTTP 401**

| **Error Code**          | **Error Message**                        | **Description**                    |
|-------------------------|------------------------------------------|------------------------------------|
| sca_required            | Payment denied. Strong Customer Authentication required. | `x-sca-id` header not provided when SCA is needed.   |
| x-sca-token  | Invalid x-sca-token.                                  | This occurs in these circumstances:<br>• the SMS token was not valid <br>• the 2FA validation was attempted incorrectly more than 5 times<br>• the SCA attempt was already used to create a payment. |
| internal_server_error | `x-sca-token` has expired.| Occurs when the 2FA attempt has expired – 10 minutes for SMS and 5 minutes for push notification.|    |
| internal_server_error   | Authentication failed.                    | Couldn't authenticate with provided `x-auth-token` header.       |  

**HTTP 429**

| **Error Code**            | **Error Message**      | **Description**         |
|---------------------------|------------------------|-------------------------|
| internal_server_error | Too many requests for 2FA approval status. | Too many attempts to validate SMS token. |

**HTTP 500**

| **Error Code**            | **Error Message**                     | **Description**                                               |
|---------------------------|---------------------------------------|---------------------------------------------------------------|
| internal_server_error     | Error getting beneficiary.            | Error while fetching the beneficiary.                         |
| internal_server_error     | Invalid 2FA Type.                      | Error while saving data during the validate process.                    |
| internal_server_error     | Error validating SCA signature.        | Problem generating signature for payment request body.        |
| internal_server_error     | Error getting contact.                | Problem fetching contact data with provided `x-auth-token`.      |
| internal_server_error     | Error getting account.                | Error while fetching account data.                            |
| internal_server_error     | An error occurred retrieving 2FA approval status. | Couldn’t validate SMS token.                |
