{
    'Parser': {
        'required': True,
        'type': 'list',
        'has_start': True,
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'type': 'string', 'required': True},
                'start': {'type': 'boolean'},
                'type': {'type': 'parsermodel', 'coerce': 'toparsermodel', 'required': True},
                'name': {'type': 'string', 'required': True},
                'args': {'type': ['string', 'list'], 'schema': {'type': ['string', 'integer']}, 'nullable': True},
                'branch_model_dict': {'type': 'list', 'schema': {'type': 'dict', 'schema': {'id': {
                    'type': ['boolean', 'float', 'integer', 'string']}, 'model': {'type': 'string'}}}},
                'date_formats': {'type': 'list', 'schema': {'type': 'dict', 'schema': {'format': {'type': 'list', 'schema': {
                    'type': 'string', 'nullable': True}}}}},
                'value_sign_type': {'type': 'string', 'allowed': ['none', 'optional', 'mandatory'], 'default': 'none'},
                'value_pad_type': {'type': 'string', 'allowed': ['none', 'zero', 'blank'], 'default': 'none'},
                'exponent_type': {'type': 'string', 'allowed': ['none', 'optional', 'mandatory'], 'default': 'none'},
                'start_year': {'type': 'integer', 'nullable': True, 'default': None},
                'delimiter': {'type': 'string'},
                'escape': {'type': 'string', 'nullable': True, 'default': None},
                'consume_delimiter': {'type': 'boolean', 'default': False},
                'key_parser_dict': {'type': 'dict'},
                'optional_key_prefix': {'type': 'string', 'default': 'optional_key_'},
                'nullable_key_prefix': {'type': 'string', 'default': '+'},
                'strict': {'type': 'boolean', 'default': False},
                'ignore_null': {'type': 'boolean', 'default': True},
                'date_format': {'type': 'string', 'minlength': 2},
                'text_locale': {'type': 'string', 'nullable': True, 'default': None},
                'max_time_jump_seconds': {'type': 'integer', 'default': 86400},
                'timestamp_scale': {'type': 'integer', 'default': 1},
                'allow_all_fields': {'type': 'boolean', 'default': False}
            }
        }
    },
}
