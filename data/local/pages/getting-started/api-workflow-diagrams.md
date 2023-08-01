[_metadata_:menu_title]:- "API Workflow Diagrams"
[_metadata_:order]:- "3"

# API Workflow Diagrams

The workflow diagrams below demonstrate using our APIs for common use cases.

## Useful Definitions

### **House Account**

This refers to your Currencycloud Account or Master Account - a multi-currency eWallet available in all currencies supported by Currencycloud.

### **Sub-account**

This refers to the capability of creating multi-currency eWallets for your customers, which sit within your **House Account**.

### **On behalf of**

This refers to the capability to execute transactions on behalf of your customers. A contact needs to be created before any activity is undertaken on the sub-account. Once a contact is created, the `on_behalf_of` parameter should be used in the transactional events (conversion, payment, transactions, searching) at the sub-account level.

### Table of Contents

1. [House account only diagrams](#house-account)  
2. [House and sub-account  diagrams](#house-and-sub-account)


## House account
The following diagrams show API workflows for common convert and pay use cases for house account or payment aggregators.

### Authentication
![authentication](/images/workflow_diagrams/1_authenticate.jpg)


### Rates and conversions - house account level
![rates and conversions](/images/workflow_diagrams/4_rates_and_conversions_house_account_level.jpg)

### Beneficiaries and payments
#### when creating a new beneficiary
![beneficiaries and payments](/images/workflow_diagrams/8_beneficiaries_and_payments_new_beneficiary.jpg)

### Beneficiaries and payments
#### when using a beneficiary that already exists
![beneficiaries and payments](/images/workflow_diagrams/9_beneficiaries_and_payments_existing_beneficiary.jpg)  

### Balances
![balances](/images/workflow_diagrams/10_balances_house_account.jpg)

---

## House and sub account
The diagrams below show the API workflows for common collect, convert and pay use cases for sub-accounts.

### Authentication
![authentication](/images/workflow_diagrams/1_authenticate.jpg)

### Sub-account and contact creation
![create sub-account](/images/workflow_diagrams/3_sub_account_and_contact_creation.jpg)

### Find funding account (collections and settlements)
![find funding account](/images/workflow_diagrams/2_find_funding_account_collections-and-settlements.jpg)

### Rates and conversions - on behalf of
![rates and conversions](/images/workflow_diagrams/5_rates_and_conversions_on_behalf_of.jpg)

### Beneficiaries and payments - on behalf of
#### when creating a new beneficiary
![beneficiaries and payments](/images/workflow_diagrams/6_beneficiaries_and_payments_on_behalf_of_new_beneficiary.jpg)

### Beneficiaries and payments - on behalf of
#### when using a beneficiary that already exists
![beneficiaries and payments](/images/workflow_diagrams/7_beneficiaries_and_payments_on_behalf_of_existing_beneficiary.jpg)

### Balances
![balances](/images/workflow_diagrams/11_balances_sub_account.jpg)
