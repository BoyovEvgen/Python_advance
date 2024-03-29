import functools
from enum import Enum

import psutil as ps
import json, toml, yaml

# (!) Note: depends on PIP packages: psultil toml pyyaml


__all__ = ('methods')

def get_doc(name_func):
    return getattr(ps, name_func).__doc__

def _parse_spec(spec):
    """Convert library-internal data structures.
    
    Conversion is done intogeneral Python types.
    """

    if hasattr(spec, '_asdict'):
        # assume namedtuple
        spec = spec._asdict()

    if isinstance(spec, dict):
        return {k: _parse_spec(v) for k, v in spec.items()}
    if isinstance(spec, list):
        return [_parse_spec(itm) for itm in spec]
    if isinstance(spec, Enum):
        return spec.name
    return spec


# Dict of a form:
# formatter_name: (mimetype, format_function)
# ...
formatters = {
    'json': ('application/json', json.dumps),
    'toml': ('text', toml.dumps),
    'yaml': ('text', functools.partial(yaml.dump, sort_keys=False)),
    'repr': ('text', repr)
}


def method_api(method, *args,  format='json', **kwargs):
    """Call method, parse result and format it accordingly."""
    # TODO: add args handling
    if format not in formatters:
        raise ValueError(f'Format is not defined!\nUse: json, yaml, toml, repr')
    spec = method(*args, **kwargs)
    parsed = _parse_spec(spec)  # convert to Python native structures

    mime, func = formatters.get(format)
    res = func(parsed)

    return res, mime


# dict of methods wrapped for api calls of a form:
# method_name: method_callable

# start building
methods = dict.fromkeys([
    'boot_time', 'cpu_count', 'cpu_freq', 'cpu_percent', 'cpu_stats',
    'cpu_times', 'cpu_times_percent', 'disk_io_counters', 'disk_partitions',
    'getloadavg', 'net_if_stats', 'net_io_counters', 'sensors_battery',
    'sensors_fans', 'sensors_temperatures', 'swap_memory', 'virtual_memory',
    'wait_procs'
])
# get original methods by name
methods = {name: getattr(ps, name) for name in methods}
# patch one as it requires argument
methods['disk_usage'] = functools.partial(ps.disk_usage, '/')

# now wrap methods
methods = {
    name: functools.partial(method_api, func, )
    for name, func in methods.items()
}

if __name__ == '__main__':
    spec = ps.sensors_temperatures()
    res = _parse_spec(spec)

    mtd = methods['sensors_temperatures']
    res, mime = mtd(format='yaml')
    print(f'Yaml res:\n{res}')
