def get_documentation(func):
    return func.__doc__.replace('\n', '<p>')
