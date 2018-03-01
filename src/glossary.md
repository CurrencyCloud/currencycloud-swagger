# Glossary
Definitions for financial and proprietary terms used throughout the Currencycloud API documentation.


## Accounts and Sub-Accounts
A Currencycloud account can be opened via [the website](/register). Initially, new Currencycloud accounts are given access to the [Currencycloud test API](/overview/environments). Account owners can [request an upgrade](/support) to get access to our production environment, which enables the transfer of real money around the world.

An account is a multi-currency digital wallet, capable of holding money in multiple currencies simultaneously.

Optionally, a Currencycloud account may open one or more client sub-accounts. Sub-accounts enable Currencycloud services to be white labeled, so you can offer cross-border payment services to your own customers. Where an account has sub-accounts, the main parent account is called the house account.

Accounts and sub-accounts have three states: enabled, disabled, and non-trading. A non-trading account is enabled but cannot be used to make real-world trades.


## Balance
A currency balance for a Currencycloud account or sub-account. An account may hold money in multiple currencies, in which case the account will have multiple balances, one for each currency.


## Beneficiary
To speed up payments, you can store the details of your most regular recipients. For each beneficiary you can store bank details, personal details, and notification preferences. Currencycloud validates beneficiary bank details and completes all necessary compliance checks ahead of time, so payments are processed faster.


## BIC/SWIFT
A SWIFT code, also known as a Bank Identifier Code (BIC), is a unique string that identifies particular banks worldwide.


## Contact
A contact is any individual person whose personal details are stored in our computer systems. A contact may exist in our system for any number of reasons. A contact may be an account owner, an additional user of an account, a beneficiary of one or more payments, and so on.


## Conversion
A conversion is a process whereby money held in one currency is traded for money in another currency. Currencycloud can convert money into currencies of all the world's major economies.

A conversion has five possible states:

- Awaiting funds
- Funds sent
- Funds arrived
- Trade settled
- Closed

A "closed" conversion means the trade was canceled before it completed.


## IBAN
An International Bank Account Number (IBAN) is an industry standard for identifying bank accounts worldwide, to facilitate the processing of cross-border transactions.

An IBAN consists of up to 34 alphanumeric characters, though the particular length and format varies from country to country.


## Foreign Exchange (FX) Rates
A foreign exchange (FX) rate is a rate at which one currency is exchanged for another.

For example, an exchange rate of 114 Japanese Yen to the US DOllar means that ¥114 can be bought for US$1, or US$1 can be bought for ¥114.


## Payer
A payer is any individual or company who makes a payment to another beneficiary.


## Payment
A payment is a transfer of money from a payer's account to a beneficiary.

Payments cannot be made in one currency and received in another. To pay a beneficiary in a particular currency, the payer must hold funds in that currency. If necessary, the payer must convert funds from one currency to another before making a payment.

Currencycloud supports two types of payments:

- Regular payment, which are made using our trusted network of in-country banking partners. Regular payments are normally received by beneficiary's within five working days of the settlement date. This is a good choice for low-value, non-urgent transactions.
- Priority payment, which are made using the SWIFT network. Payments can be made to over 212 countries, and 95% of payments arrive within one working day.

A payment record has eight possible states:

- New
- Completed
- Failed
- Released
- Suspended
- Awaiting authorization
- Submitted
- Authorised

A failed payment means that the funds failed to reach the beneficiary and were returned to the payer. In some cases, a submitted payment may require authorization from a contact with the necessary privileges, before the payment can be executed.


## Payment routing
Regular payments, which are transferred using the local bank network, are routed from one bank to another using different standards depending on the country. For example, the UK uses sort codes, Singapore uses branch codes, and Hong Kong uses BSB codes.


## Settlement
In the Currencycloud platform, multiple currency conversions may be bundled together and settled in bulk. This is called a settlement.

A settlement has five possible states:

- Open, which indicates the settlement does not yet have any conversions added to it
- Released, which indicates the settlement has been released for processing and no further conversions can be added
- Funds arrived, which indicates that the necessary funds for the settlement have arrived
- Part paid, which indicates that some of the necessary funds have arrived, but not enough to complete the settlement
- Paid, which indicates a completed state


## Spread Table
A spread table is a markup that is applied to conversions. It represents brokerage service costs. Spread is traditionally denoted in "pips", a percentage in point, meaning a fourth decimal place in a currency quotation.


## Transaction
In the Currencycloud platform, a transaction is a catch-all term for all types of debits and credits affecting the balance of an account or sub-account. Transactions include currency conversions, payments made to third party beneficiaries, and transfers of funds between accounts and sub-accounts.


## Transfer
In the Currencycloud platform, a transfer is the movement of money between Currencycloud accounts. Money can be transferred:

- From a house account to its sub-accounts
- From a sub-account to its house account
- Between sub-accounts under the same house account
