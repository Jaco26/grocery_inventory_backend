import uuid
from .regex_patterns import email

def is_email(val):
  if val and email.match(val):
    return val
  raise ValueError

def is_uuid(val):
  if val:
    return uuid.UUID(val)
  return None
