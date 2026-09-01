import csv
from ruamel.yaml import YAML

if __name__ == '__main__':
    # 1. Load your CSV into a lookup dictionary
    update_map = {}  # (method, path, field_name, param_location) -> data dict

    with open('currencycloud_api_request_fields.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['method'].upper(), row['path'], row['field_name'], row['param_location'])
            update_map[key] = row

    # 2. Load the YAML
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 437
    # This line ensures None is output as 'null'
    yaml.representer.add_representer(
        type(None),
        lambda self, _: self.represent_scalar('tag:yaml.org,2002:null', 'null')
    )
#    yaml.default_flow_style = False
#    yaml.indent(sequence=2, offset=2)  # array indent 2 more than parent, align first
# map/sequence/offset: all set to 2 for strict block alignment
    yaml.indent(mapping=2, sequence=4, offset=2)
    with open('reference_original.yaml', encoding='utf-8') as f:
        doc = yaml.load(f)

    # 3. Update parameters as needed
    for path, path_item in doc.get('paths', {}).items():
        for method in path_item:
            op = path_item[method]
            params = op.get('parameters', [])
            for p in params:
                param_name = p.get('name')
                param_in = p.get('in')
                key = (method.upper(), path, param_name, param_in)
                if key in update_map:
                    row = update_map[key]
                    # Only add if value present and not already set
                    if row.get('format') and 'format' not in p:
                        p['format'] = row['format']
                    #Only add additional data if format is not a standard one
                    if 'format' not in p or p['format'] not in ['uuid','date','date-time']:
                        if row.get('pattern') and 'pattern' not in p:
                            p['pattern'] = row['pattern']
                        #Only add length if pattern is not defined
                        if 'pattern' not in p or p['pattern'] == '' or p['pattern'] == '\S+' or 'email' in param_name:
                            if row.get('minLength') and 'minLength' not in p:
                                try:
                                    p['minLength'] = int(row['minLength'])
                                except ValueError:
                                    pass
                            if row.get('maxLength') and 'maxLength' not in p:
                                try:
                                    p['maxLength'] = int(row['maxLength'])
                                except ValueError:
                                    pass
                    # Add 'enum' support if is_enum has a value (for you to implement)
                    # and so on for other CSV fields

    # 4. Save the updated YAML, preserving as much formatting as possible
    with open('swagger_enriched.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(doc, f)

    print("YAML update complete (swagger_enriched.yaml)")
#    found_tags = False
#    found_schemes = False
#    with open('swagger_enriched.yaml', 'r', encoding='utf-8') as infile, open('swagger_enriched2.yaml', 'w', encoding='utf-8') as outfile:
#        for line in infile:
#            if not found_schemes and "schemes:" in line:
#                found_schemes = True
#            if found_tags and not found_schemes:
#                outfile.write('  ' + line)
#            else:
#                outfile.write(line)
#            if not found_tags and "tags:" in line:
#                found_tags = True
#    print("All Done")