import base64

data_encoded = "eyJhY3Rpb24iOiJwYXkiLCJzdGF0dXMiOiJmYWlsdXJlIiwiZXJyX2NvZGUiOiJjYW5jZWwiLCJlcnJfZGVzY3JpcHRpb24iOiJjYW5jZWwiLCJ2ZXJzaW9uIjozLCJ0eXBlIjoiYnV5IiwicHVibGljX2tleSI6InNhbmRib3hfaTEwMjE4MDk2MDMyIiwib3JkZXJfaWQiOiIxNDEiLCJsaXFwYXlfb3JkZXJfaWQiOiIxNDEiLCJkZXNjcmlwdGlvbiI6IlRleHQiLCJhbW91bnQiOiIxMTExIiwiY3VycmVuY3kiOiJVQUgiLCJpc18zZHMiOmZhbHNlLCJsYW5ndWFnZSI6InJ1IiwiY3JlYXRlX2RhdGUiOjE2ODc4NzEzNzI1NjcsImNvZGUiOiJjYW5jZWwifQ=="
data_decoded = base64.b64decode(data_encoded).decode('utf-8')

import json

data_json = json.loads(data_decoded)

signature_encoded = "AwNVUrew3mxfCC1G4EE9CZcY350="
signature_decoded = base64.b64decode(signature_encoded).decode('utf-8')


print(data_decoded)