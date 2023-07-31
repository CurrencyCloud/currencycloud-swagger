[_metadata_:menu_title]:- "Preserving Beneficiary Details"
[_metadata_:order]:- "5"

# Preserving Beneficiary Details 

Payments are made to a specific beneficiary. As beneficiary details can be changed at any time, we clone the beneficiary object once the payment is released in order to preserve an exact record of what the details were at the time of the payment. 

## At what point is the beneficiary cloned?   

The beneficiary is cloned once the payment is released. This means that you can make changes to the beneficiary details while a payment has a `ready_to_send` status. As soon as the status is updated the beneficiary is cloned and any changes made to the beneficiary will not affect the beneficiary details held against the payment, although the updated details will be used for any other payments with a `ready_to_send` status. 

## How does it work? 

The cloned beneficiary will be allocated a new UUID which will be referenced from  the released payment, no changes can be made to this beneficiary. Any payments not released yet (`ready_to_send` status) will reference the original beneficiary whose details can be updated. 

Example:

__Payment Created API Response:__  


```
{
    "id": "286bbc9e-5224-4290-a538-2d6282549de6",
    "amount": "1.00",
    "beneficiary_id": "140068cd-d6d6-4ead-8c2d-df9cc5ff3911",  
    "currency": "GBP",
    "reference": "Test Bene Details",
    "reason": "Test Bene Details",
    "status": "ready_to_send",
    "creator_contact_id": "669b4860-4bb3-4636-8ee4-9e672810d350", "payment_type": "regular", 
    "payment_date": "2020-01-16",
    "transferred_at": "",
    "authorisation_steps_required": "0",
    "last_updater_contact_id": "669b4860-4bb3-4636-8ee4-9e672810d350", "short_reference": "200116-BYNXQW001", 
    "conversion_id": null,
    "failure_reason": "",
    "payer_id": "0cda56cc-0b62-4171-841e-4003402801e8", "payer_details_source": "account",
    "created_at": "2020-01-16T11:38:55+00:00", "updated_at": "2020-01-16T11:38:55+00:00", "payment_group_id": null,
    "unique_request_id": null,
    "failure_returned_amount": "0.00", "ultimate_beneficiary_name": null,
    "purpose_code": null,
    "charge_type": null,
    "fee_amount": null,
    "fee_currency": null 
}
```
__Push notification:__  


```
{
    "id": "286bbc9e-5224-4290-a538-2d6282549de6",
    "amount": "1.00",
    "failure_returned_amount": "",
    "beneficiary_id": "140068cd-d6d6-4ead-8c2d-df9cc5ff3911", "conversion_id": null,
    "currency": "GBP",
    "reference": "Test Bene Details",
    "reason": "Test Bene Details",
    "status": "ready_to_send",
    "payment_type": "regular",
    "payment_date": "2020-01-16T00:00:00+00:00",
    "transferred_at": null,
    "authorisation_steps_required": 0,
    "creator_contact_id": "669b4860-4bb3-4636-8ee4-9e672810d350", "last_updater_contact_id": "669b4860-4bb3-4636-8ee4-9e672810d350", "short_reference": "200116-BYNXQW001",
    "failure_reason": "",
    "payment_group_id": null,
    "unique_request_id": null,
    "fee_amount": null,
    "fee_currency": null
}
```

In this example, while the payment has a `ready_to_send` status, both the API response and the push notification show __beneficiary_id = 140068cd-d6d6-4ead-8c2d-df9cc5ff3911__.

When the payment is completed the API Response and Push Notification show an updated `status` and a new `beneficiary_id`.

__API Response:__  

```
{
    "id": "286bbc9e-5224-4290-a538-2d6282549de6",
    "amount": "1.00",
    "beneficiary_id": "fc3c3ca7-08fe-41bd-acc9-baec129c8a98",
    "currency": "GBP",
    "reference": "Test Bene Details",
    "reason": "Test Bene Details",
    "status": "completed",
    "creator_contact_id": "669b4860-4bb3-4636-8ee4-9e672810d350", "payment_type": "regular",
    "payment_date": "2020-01-16",
    "transferred_at": "2020-01-16T12:30:02Z", "authorisation_steps_required": "0",
    "last_updater_contact_id": "669b4860-4bb3-4636-8ee4-9e672810d350", "short_reference": "200116-BYNXQW001",
    "conversion_id": null,
    "failure_reason": "",
    "payer_id": "0cda56cc-0b62-4171-841e-4003402801e8", "payer_details_source": "account",
    "created_at": "2020-01-16T11:38:55+00:00",
    "updated_at": "2020-01-16T12:30:02+00:00",
    "payment_group_id": null,
    "unique_request_id": null,
    "failure_returned_amount": "0.00",
    "ultimate_beneficiary_name": null,
    "purpose_code": null,
    "charge_type": null,
    "fee_amount": null,
    "fee_currency": null
}
```

__Push Notification__  

```
{
    "id": "286bbc9e-5224-4290-a538-2d6282549de6", "amount": "1.00",
    "failure_returned_amount": "",
    "beneficiary_id": "fc3c3ca7-08fe-41bd-acc9-baec129c8a98", "conversion_id": null,
    "currency": "GBP",
    "reference": "Test Bene Details",
    "reason": "Test Bene Details",
    "status": "completed",
    "payment_type": "regular",
    "payment_date": "2020-01-16T00:00:00+00:00",
    "transferred_at": "2020-01-16T12:30:02+00:00", "authorisation_steps_required": 0,
    "creator_contact_id": "669b4860-4bb3-4636-8ee4-9e672810d350", "last_updater_contact_id": "669b4860-4bb3-4636-8ee4-9e672810d350", "short_reference": "200116-BYNXQW001",
    "failure_reason": "",
    "payment_group_id": null,
    "unique_request_id": null,
    "fee_amount": null,
    "fee_currency": null
}
```

The same payment has progressed to a `completed` payment status and the beneficiary id has been changed:  

__beneficiary_id = fc3c3ca7-08fe-41bd-acc9- baec129c8a98__  


This new beneficiary_id is the ID of the cloned beneficiary which is read-only. This means that while you can use [Get Beneficiary](/api-reference/#get-beneficiary) to view it, it will not appear in searches when using the [Find Beneficiaries](/api-reference/#find-beneficiaries) endpoint and you cannot update or delete the cloned beneficiary. Searching for the read-only beneficiary will fail with an error response:  

```
{
  "error_code": "beneficiary_not_found",
  "error_messages": {
      "id": [
        {
            "code": "beneficiary_not_found",
            "message": "Beneficiary was not found for this id",
            "params": {}
        }
      ]
    }  
}
```
