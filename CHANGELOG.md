# Changelog

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
