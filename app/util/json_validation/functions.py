from flask import request
from voluptuous import Schema, Required, REMOVE_EXTRA

# NOTE:
# When using Required(field_name, default=<something>): predicate
# The value assigned to `default` is passed to the predicate if there is no value
# associated with `field_name` in the source

def create_schema(template_dict):
  accum = {}
  for key in template_dict:
    predicate = template_dict[key]
    if type(key) is tuple:
      try:
        field_name, default_value = key
        accum.update({ Required(field_name, default=default_value): predicate })
      except:
        raise 'Tuple must contain two items, (<field_name>, <default_value>)'
    elif type(key) is str:
      accum.update({ Required(key, default=None): predicate })
  return Schema(accum, extra=REMOVE_EXTRA)


def should_look_like(schema_func, source=None):
  if not source:
    source = request.get_json()
  return schema_func(dict(source))
