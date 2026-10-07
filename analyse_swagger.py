import yaml
import csv


field_info_fallback = {
    'X-Auth-Token': {'format': 'uuid', 'minLength': 36, 'maxLength': 36},
    'on_behalf_of': {'format': 'uuid', 'minLength': 36, 'maxLength': 36},
    'currency': {'pattern': '^[A-Z]{3}$', 'format': 'iso-4217', 'minLength': 3, 'maxLength': 3},
    'buy_currency': {'pattern': '^[A-Z]{3}$', 'format': 'iso-4217', 'minLength': 3, 'maxLength': 3},
    'sell_currency': {'pattern': '^[A-Z]{3}$', 'format': 'iso-4217', 'minLength': 3, 'maxLength': 3},
    'fee_currency': {'pattern': '^[A-Z]{3}$', 'format': 'iso-4217', 'minLength': 3, 'maxLength': 3},
    'currency_pair': {'pattern': '^[A-Z]{6}$', 'minLength': 6, 'maxLength': 6},
    'api_key': {'pattern': '^[a-f0-9]{64}$', 'minLength': 64, 'maxLength': 64},
    'account_id':         {'format': 'uuid',        'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'id':                 {'format': 'uuid',        'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'charge_settings_id': {'format': 'uuid',        'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'linked_account_id':  {'format': 'uuid',        'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'account_name':       {'minLength': 1, 'maxLength': 150, 'pattern': '\\S+'},
    'brand':              {'minLength': 1, 'maxLength': 255},
    'street':             {'maxLength': 150},
    'city':               {'maxLength': 100},
    'state_or_province':  {'maxLength': 100},
    'postal_code':        {'maxLength': 20},
    'spread_table':       {'maxLength': 100},
    'industry_type':      {'maxLength': 255},
    'business_website_url': {'maxLength': 400},
    'trading_address_street':    {'maxLength': 150},
    'trading_address_city':      {'maxLength': 100},
    'trading_address_state':     {'maxLength': 100},
    'trading_address_postalcode':{'maxLength': 20},
    'tax_identification':        {'maxLength': 100},
    'national_identification':   {'maxLength': 100},
    'identification_value':      {'maxLength': 255, 'minLength': 1},
    'identification_issuer':     {'minLength': 1},
    'country': {'pattern': '^[A-Z]{2}$', 'format': 'iso3166-1-alpha-2', 'minLength': 2, 'maxLength': 2},
    'bank_account_holder_name': {'minLength': 1, 'maxLength': 255},
    'account_number': {'minLength': 1, 'maxLength': 50},
    'bic_swift': {'pattern': r'^(\w{8}|\w{11})$'},
    'iban': {'minLength': 1, 'maxLength': 34, 'pattern': r'([A-Z0-9]\s*){15,34}'},
    'name': {'minLength': 1, 'maxLength': 100, 'pattern': r'\S+'},
    'bank_name': {'minLength': 1},
    'bank_address': {'minLength': 1, 'maxLength': 100},
    'beneficiary_external_reference': {'minLength': 1, 'maxLength': 255},
    'beneficiary_postcode': {'maxLength': 12},
    'email': {'minLength': 6, 'maxLength': 255, 'pattern': r'^[\w\.\_\%\-\+]+@([\w-]+\.)+\w{2,}+$'},
    'company_website': {'maxLength': 255},
    'business_nature': {'maxLength': 255},
    'routing_code_value_1': {'minLength': 1, 'maxLength': 50},
    'routing_code_value_2': {'minLength': 1, 'maxLength': 50},
    'bank_country': {'pattern': '^[A-Z]{2}$', 'format': 'iso3166-1-alpha-2', 'minLength': 2, 'maxLength': 2},
    'contact_id': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'first_name': { 'minLength': 1, 'maxLength': 100 },
    'last_name':  { 'minLength': 1, 'maxLength': 100 },
    'email_address': { 'minLength': 6, 'maxLength': 255, 'pattern': r'^[\w\.\_\%\-\+]+@([\w-]+\.)+\w{2,}+$' },  # some GET uses /\A.+@.+\..+\z/
    'phone_number':   { 'minLength': 1, 'maxLength': 100 },
    'mobile_phone_number': { 'minLength': 1, 'maxLength': 100 },
    'your_reference': { 'minLength': 1, 'maxLength': 255 },
    'login_id': { 'minLength': 1, 'maxLength': 50 },
    'locale':   { 'minLength': 2, 'maxLength': 5 },
    'timezone': { 'minLength': 7, 'maxLength': 35 },
    'fuzzy_search_string': { 'minLength': 3, 'maxLength': 255 },
    'password': { 'minLength': 1, 'maxLength': 255 },
    'effective_contact_password': {'minLength': 8, 'maxLength': 255},
    'token': {'maxLength': 64},
    'security_answer_one': { 'minLength': 1, 'maxLength': 25 },
    'security_answer_two': { 'minLength': 1, 'maxLength': 25 },
    'security_answer_three': { 'minLength': 1, 'maxLength': 25 },
    'settlement_id': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'conversion_id': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'beneficiary_id': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'payer_id': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'payment_id': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'payment_fee_id': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'payment_currency': {'pattern': '^[A-Z]{3}$', 'format': 'iso-4217'},
    'conversion_pair': {'pattern': '^[A-Z]{6}$'},
    'bank_account_country': {'pattern': '^[A-Z]{2}$', 'format': 'iso3166-1-alpha-2'},
    'beneficiary_country': {'pattern': '^[A-Z]{2}$', 'format': 'iso3166-1-alpha-2'},
    'destination_country_code': {'pattern': '^[A-Z]{2}$', 'format': 'iso3166-1-alpha-2'},
    'payer_country': {'pattern': '^[A-Z]{2}$', 'format': 'iso3166-1-alpha-2'},
    'date_of_birth':{'format': 'date'},
    'beneficiary_first_name': { 'minLength': 1, 'maxLength': 255 },
    'ultimate_beneficiary_name': { 'minLength': 1, 'maxLength': 255 },
    'sender_country': {'pattern': '^[A-Z]{2}$', 'format': 'iso3166-1-alpha-2'},
    'x-sca-id': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'payer_city': { 'minLength': 1, 'maxLength': 255 },
    'bulk_upload_reference': { 'minLength': 1, 'maxLength': 255 },
    'x-sca-token': { 'minLength': 6, 'maxLength': 6, 'pattern': '^\d{6}$' },
    'creator_contact_id': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'payment_destination_country': {'pattern': '^[A-Z]{2}$', 'format': 'iso3166-1-alpha-2'},
    'unique_request_id': { 'minLength': 1, 'maxLength': 255 },
    'related_entity_id': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'beneficiary_address': { 'minLength': 1, 'maxLength': 255 },
    'beneficiary_date_of_birth':{'format': 'date'},
    'withdrawal_account_id': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'payer_last_name': { 'minLength': 1, 'maxLength': 255 },
    'payer_state_or_province': { 'minLength': 1, 'maxLength': 255 },
    'payer_date_of_birth':{'format': 'date'},
    'beneficiary_last_name': { 'minLength': 1, 'maxLength': 255 },
    'transactionId': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'beneficiary_city': { 'minLength': 1, 'maxLength': 255 },
    'payer_postcode': { 'minLength': 1, 'maxLength': 255 },
    'beneficiary_state_or_province': { 'minLength': 1, 'maxLength': 255 },
    'partner_sell_amount_to':{'pattern': '^\d+(\.\d{1,3})?$'},
    'amount_to':{'pattern': '^\d+(\.\d{1,3})?$'},
    'buy_amount_to':{'pattern': '^\d+(\.\d{1,3})?$'},
    'sell_amount_from':{'pattern': '^\d+(\.\d{1,3})?$'},
    'sell_amount_to':{'pattern': '^\d+(\.\d{1,3})?$'},
    'amount_from':{'pattern': '^\d+(\.\d{1,3})?$'},
    'partner_buy_amount_from':{'pattern': '^\d+(\.\d{1,3})?$'},
    'client_buy_amount':{'pattern': '^\d+(\.\d{1,2})?$'},
    'client_sell_amount':{'pattern': '^\d+(\.\d{1,2})?$'},
    'partner_sell_amount_from':{'pattern': '^\d+(\.\d{1,3})?$'},
    'partner_buy_amount_to':{'pattern': '^\d+(\.\d{1,3})?$'},
    'buy_amount_from':{'pattern': '^\d+(\.\d{1,3})?$'},
    'fee_amount':{'pattern': '^\d+(\.\d{1,3})?$'},
    'conversion_date_to':{'format': 'date'},
    'payment_date':{'format': 'date'},
    'settlement_date_from':{'format': 'date'},
    'created_at_from':{'format': 'date'},
    'conversion_date_from':{'format': 'date'},
    'settlement_date_to':{'format': 'date'},
    'updated_at_to':{'format': 'date'},
    'created_at_to':{'format': 'date'},
    'updated_at_from':{'format': 'date'},
    'event_date_time_from':{'format': 'date-time'},
    'event_date_time_to':{'format': 'date-time'},
    'source_account_id': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'destination_account_id': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'payer_first_name': { 'minLength': 1, 'maxLength': 255 },
    'new_settlement_date':{'format': 'date'},
    'sender_name': { 'minLength': 1, 'maxLength': 255 },
    'reference_id': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'creator_account_id': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'page':{'pattern': '^\d+$'},
    'per_page':{'pattern': '^\d+$'},
    'payment_ids': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'conversion_ids': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'short_reference': { 'minLength': 1, 'maxLength': 25},
    'related_entity_short_reference': { 'minLength': 1, 'maxLength': 25},
    'receiver_routing_code': { 'minLength': 1, 'maxLength': 255},
    'receiver_account_number': { 'minLength': 1, 'maxLength': 255},
    'purpose_code': { 'minLength': 1, 'maxLength': 255},
    'payment_group_id': { 'minLength': 1, 'maxLength': 255},
    'amount':{'pattern': '^\d+(\.\d{1,3})?$'},
    'beneficiary_company_name': { 'minLength': 1, 'maxLength': 255},
    'order': { 'minLength': 1, 'maxLength': 255},
    'invoice_number': { 'minLength': 1, 'maxLength': 30, 'pattern': '^[a-zA-Z0-9]{1,30}$'},
    'reason': { 'minLength': 1, 'maxLength': 255},
    'notes': { 'minLength': 1, 'maxLength': 255},
    'invoice_date': {'format': 'date'},
    'payer_identification_value': { 'minLength': 1, 'maxLength': 255},
    'sender_reference': { 'minLength': 1, 'maxLength': 255},
    'identifier_value': { 'minLength': 1, 'maxLength': 255},
    'bulk_upload_id': { 'minLength': 1, 'maxLength': 255},
    'description': { 'minLength': 1, 'maxLength': 255},
    'payer_address': { 'minLength': 1, 'maxLength': 255},
    'sender_routing_code': { 'minLength': 1, 'maxLength': 255},
    'routing_code_value[0]': { 'minLength': 1, 'maxLength': 50},
    'beneficiary_identification_value': { 'minLength': 1, 'maxLength': 255},
    'conversion_ids[]': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'sender_address': { 'minLength': 1, 'maxLength': 255},
    'reference': { 'minLength': 1, 'maxLength': 255},
    'sender_account_number': { 'minLength': 1, 'maxLength': 255},
    'payment_ids[]': {'format': 'uuid', 'minLength': 36, 'maxLength': 36, 'pattern': '^[0-9a-fA-F-]{36}$'},
    'payer_company_name': { 'minLength': 1, 'maxLength': 255},
}

if __name__ == '__main__':
    with open('reference_original.yaml', 'r') as f:
        data = yaml.safe_load(f)

    fields = []
    method_path_set = set()
    fields_without_info = 0
    fields_without_info_set = set()
    paths = data.get('paths', {})

    for path, methods in paths.items():
        for method, meta in methods.items():
            method_upper = method.upper()
            method_path_set.add((method_upper, path))
            params = meta.get('parameters', [])
            for p in params:
                field_name = p.get('name', '')
                swagger_type = p.get('type', '')
                # Get info for field_name
                info = field_info_fallback.get(field_name, {})
                extra_format = info.get('format', '')
                extra_min = info.get('minLength', '')
                extra_max = info.get('maxLength', '')
                extra_pattern = info.get('pattern', '')
                # Get Data from yaml
                default_format = p.get('format', '')
                default_min = p.get('minLength', '')
                default_max = p.get('maxLength', '')
                default_pattern = p.get('pattern', '')

                format_to_write = default_format if default_format != '' else extra_format
                min_to_write = default_min if default_min != '' else extra_min
                max_to_write = default_max if default_max != '' else extra_max
                pattern_to_write = default_pattern if default_pattern != '' else extra_pattern

                is_enum = 'enum' in p and bool(p['enum'])
                has_enum = 'enum' in p
                excluded_type = swagger_type in ['boolean', 'integer', 'number']
                has_no_data = format_to_write == '' and max_to_write == '' and min_to_write == '' and pattern_to_write == ''
                if not excluded_type and not has_enum and has_no_data:
                    fields_without_info += 1
                    fields_without_info_set.add(field_name)

                fields.append([
                    method_upper,
                    path,
                    field_name,
                    swagger_type,
                    'required' if p.get('required', False) else 'optional',
                    p.get('in', ''),
                    format_to_write,
                    min_to_write,
                    max_to_write,
                    pattern_to_write,
                    'true' if is_enum else None
                ])

    with open('currencycloud_api_request_fields.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'method',
            'path',
            'field_name',
            'field_type',
            'required_optional',
            'param_location',
            'format',
            'minLength',
            'maxLength',
            'pattern',
            'is_enum'
        ])
        writer.writerows(fields)

    print(f"Number of method/path combinations: {len(method_path_set)}")
    print(f"Total number of fields: {len(fields)}")
    print(f"Number of non-boolean/non-enum/non-formatted fields not assigned values from the dict: {fields_without_info}")
    print(fields_without_info_set)