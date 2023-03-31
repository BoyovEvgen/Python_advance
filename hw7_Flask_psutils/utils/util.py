bool_key = {'true': True, 'false': False }


def convert_str_to_bool(**kwargs):
    for key, value in kwargs.items():
        if value.lower() in bool_key.keys():
            kwargs[key] = bool_key.get(value.lower())
    return kwargs


