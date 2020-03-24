# Changelog

## [2.12.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.12.0) (2020-03-24)
   - Adds /payments/assign_payment_fee endpoint
   - Adds /payments/payment_fees endpoint
   - Adds /payments/unassign_payment_fee endpoint
   - Adds payment_fee_id and payment_fee_name to PaymentFeeRule response definition

## [2.11.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.11.0) (2020-03-09)
   - Adds top_up_margin endpoint definition

## [2.10.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.10.0) (2020-01-22)
   - Makes currency required for /funding_accounts/find 
   - Adds "margin" to action enum in transactions find
   - Adds awaiting_balance to status enum of find payments 
   - Adds unsupported_beneficiary_country_code error response to payments/create
   - Updates the routing_code parameters in Funding Accounts object

## [2.9.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.9.0) (2019-10-21)
   - Updates Payments endpoints for payment fee parameters
   - Updates transaction find endpoint for payment_fee action
   
## [2.8.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.8.0) (2019-10-11)
   - Updates error response on bank_details endpoint for invalid cnaps
   - Adds find funding accounts end point
   - Adds get payment level fees endpoint
   - Adds get quote payment fee endpoint
   
## [2.7.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.7.0) (2019-08-01)
   - Adds additional supported identifier types to bank details end point
   - Adds contacts generate_hmac_key end point
   - Fixes duplicated operation Id for Pull Funds From Withdrawal Account

## [2.6.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.6.0) (2019-06-25)
   - Adds find withdrawal_accounts end point
   - Adds pull_funds from withdrawal_accounts end point
   - Adds bic_swift option to identifier_type of bank_details end point

## [2.5.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.5.0) (2019-04-25)
   - Adds get bank_details endpoint
   - Adds beneficiary_external_reference parameter to beneficiaries create and update endpoints
   - Fixes missing parameters in BeneficiaryRequirements definition

## [2.4.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.4.0) (2019-04-25)
   - Removes support for deprecated VANS and IBANS operations
   - Deprecates all settlement operations
   - Adds action_type deposit_refund to transaction find operation
   - Updates error codes on beneficiaries/find operation
   - Fixes type of deposit_required and deposit_amount in Conversion model
   - Fixes indentation of default value for payment_types parameter
   - Fixes description of id parameter on transactions/sender operation


## [2.3.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.3.0b) (2019-03-11)
   - Adds currency as an optional field in the 'Get Requirements for Payers' API
   - Adds beneficiary_external_reference as an optional field in the 'Find Beneficiaries' API
   - Bugfix to 'Create Beneficiary' beneficiary_identification_type enum list
   - Bugfix to 'Find Payments' charge_type parameter 'in' type
    
    
## [2.2.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.2.0) (2019-02-19)
   - Adds enum and default values for scope parmeter on find-ibans and find-vans
   - Adds missing actions to the enum of the action parameter of transactions/find
   - Updates documentation for transactions/find, payments/find and payments/create
   - Add Payment Charge Settings
   - Create beneficiary enum list fix
   - Fix Beneficiary Payment Type Defaults
   - Adds get payment delivery date to api definition



## [2.1.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.1.0) (2019-02-05)
   - Fixes documentation of *Get Payer Requirements*
   - Documents 403 Error
   - Adds wire_routing_code to VANS Definition


## [2.0.0](https://github.com/CurrencyCloud/currencycloud-swagger/releases/tag/rel-2.0.0) (2109-01-30)


## Initial Release (2018-05-16)
