import os

ALLOW_ALL = "*"

def add_access_control_headers(response):
  response["Access-Control-Allow-Origin"] = ALLOW_ALL
  response["Access-Control-Allow-Origin"] = ALLOW_ALL
  response["Access-Control-Allow-Methods"] = ALLOW_ALL
  response["Access-Control-Max-Age"] = os.environ['ADMIN_SERVER_CORS_MAX_AGE']
  response["Access-Control-Allow-Headers"] = ALLOW_ALL
  return response
