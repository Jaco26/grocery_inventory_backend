import re
from .api_response import ApiResponse

def uniform_name(name):
  return re.sub(r'\s+', '_', name.lower())