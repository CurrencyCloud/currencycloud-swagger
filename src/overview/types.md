# Types
The Currencycloud API supports three primitive types in the payloads of request and response messages:

- Strings
- Numbers
- Booleans (``true`` and ``false``)

Other custom types are encoded as strings. The following custom types recur in various endpoints throughout the Currencycloud API.


## BIC/SWIFT codes

BIC/SWIFT codes follow the ISO 9362 standard. The codes are 8 or 11 characters long. For example, the SWIFT code for Barclays UK bank accounts is "BARCGB22".


## Countries
Country codes are two-letter strings defined by the ISO 3166 standard. Country codes are case insensitive, but we tend to write them uppercase: "GB".

A full list of codes and corresponding country names can be found on the following web page: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2.


## Currencies
Currencies are represented using three-character ISO 4217 codes. For example, "GBP" represents the Pound Sterling, "EUR" the Euro, and "DKK" the Danish Krone.

A list of active currency codes can be found on the following web page: https://en.wikipedia.org/wiki/ISO_4217


## Dates and Times

The Currencycloud API accepts dates and times written in various subsets of the ISO 8601 format.

```
YYYY
YYYY-MM
YYYY-MM-DD
YYYY-MM-DDThh:mmTZD
YYYY-MM-DDThh:mm:ssTZD
```

The time zone designator (TZD) may be in the format +hh:mm or -hh:mm, or the letter Z to represent UTC.

Examples:

- ``1994-11-05T08:15:30-05:00`` is 8:15:30 am, 5 Nov 1994, US Eastern Standard Time.
- ``1994-11-05T13:15:30Z`` corresponds to the same instant.


## IBAN codes

IABN codes follow the ISO 13616:1997 standard and are up to 34 characters long. The format and length varies from country to country. For UK banks the format is "GB29 RBOS 6016 1331 9268 19".


## Locales

Locales are represented by two- or five-character strings, a combination of an ISO 639-1 language code and optional ISO 3166-1 regional code. Examples: ``en``, ``en-US``, ``fr-FR``.


## Timezones

Timezones are represented using standard codes from the IANA TZ database. Examples: ``Europe/London``, ``America/New_York``.


## UUID

Currencycloud exposes Universally Unique Identifiers (UUIDs) to identify pieces of information in our computer systems. In their canonical textual representation, UUIDs are represented as 32 hexadecimal digits, displayed in five groups separated by hyphens, for a total of 36 characters. Example:

```
123e4567-e89b-12d3-a456-426655440000
```
