[_metadata_:unlisted]:-
# Held FX Rates – Integration Guide

This guide explains how to integrate **Held FX Rates**, which enable you to lock in an FX rate for a defined period and execute a conversion at that guaranteed rate.

Held FX Rates are intended for payment journeys where there is a delay between pricing and execution, such as checkout flows, beneficiary setup, or invoice payments.

## Overview

Held FX Rates follow a **two-step process**:

- Create a held FX quote
- Create a conversion using the held quote

## Key Concepts

Before integrating, it’s important to understand the following:

- Held quotes lock an FX rate for a predefined **hold period**
- Hold periods must be **pre‑provisioned** for your account (contact your Account Manager or our <a href="mailto:support@currencycloud.com">support team</a>)
- Quotes are currently **single‑use only**
- Quotes are **amount‑specific** — the conversion amount must match the quoted amount
- Pricing includes **risk‑based markups**, delivered as an **all‑in rate**
- Not all currency pairs are available initially (contact us for coverage)

## Integration Flow

### Step 1: Create a Held FX Quote

Use the POST `/v2/quotes/create` endpoint to request a held FX rate.

This request is similar to creating a conversion, with the addition of the **`hold_period`** field.

#### Endpoint Detail

`POST /v2/quotes/create`

##### Headers

| Field | Type | Description |
|------|------|-------------|
| `X-Auth-Token` | string | Authentication token |

##### Form Parameters

| Field | Type | Description |
|------|------|-------------|
| `buy_currency` | string | ISO currency code being bought |
| `sell_currency` | string | ISO currency code being sold |
| `fixed_side` | string | Currency to fix (`buy` or `sell`) |
| `amount` | string | Amount of the fixed currency |
| `hold_period` | string | Duration the quote is valid for (e.g. `5m`, `1h`) |
| `conversion_date` | string | Earliest delivery date (`YYYY-MM-DD`) |
| `conversion_date_preference` | string | `default`, `earliest`, `next_day`, or `optimize_liquidity` |
| `on_behalf_of` | string | Sub-account contact UUID |

> **Note:** The `hold_period` value must be enabled on your account before use.

##### Quote Response

The response mirrors the existing conversion response with the addition of quote‑specific fields:

| Field | Description |
|------|-------------|
| `quote_id` | Unique identifier for the held quote |
| `created_at` | Timestamp indicating when the quote was created |
| `expires_at` | Timestamp indicating when the quote expires |
| `core_rate` | All‑in FX rate (includes risk markup) |

### Step 2: Book a Conversion Using the Held Quote

To execute a trade at the held rate, call the existing conversion creation endpoint with the **`quote_id`**.

#### Endpoint

`POST /v2/conversions/create`

##### Headers

| Field | Type | Description |
|------|------|-------------|
| `X-Auth-Token` | string | Authentication token |

##### Form Parameters

| Field | Type | Description |
|------|------|-------------|
| `buy_currency` | string | Must match the currency specified in the held quote |
| `sell_currency` | string | Must match the currency specified in the held quote |
| `fixed_side` | string | Must match the  fixed side specified in the held quote |
| `amount` | string | Must match the amount specified in the held quote |
| `quote_id` | string | ID returned by the  `/v2/quotes/create` endpoint |
| `conversion_date` | string | Earliest delivery date (`YYYY-MM-DD`) |
| `conversion_date_preference` | string | `default`, `earliest`, `next_day`, or `optimize_liquidity` |
| `term_agreement` | boolean | Indicates acceptance of the Terms and Conditions |
| `reason` | string | Free‑form reason for the conversion  |
| `unique_request_id` | string | Idempotency key |
| `on_behalf_of` | string | Sub-account contact UUID |
