from corsheaders.defaults import default_headers

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://localhost:5173",
    "https://127.0.0.1:5173",
]

# Allow phones/other devices on the same Wi-Fi to reach the dev frontend
# (e.g. https://192.168.x.x:5173, served over TLS via the self-signed
# dev cert in certs/) so they can hit this API cross-origin.
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https?://192\.168\.\d{1,3}\.\d{1,3}:5173$",
    r"^https?://10\.\d{1,3}\.\d{1,3}\.\d{1,3}:5173$",
    r"^https?://172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}:5173$",
]

# Django's CSRF middleware checks the Origin header against this list for any
# unsafe request (e.g. the admin login POST) served over HTTPS. Needed here
# because the TLS proxy (scripts/tls_proxy.py) fronts the admin on :8000.
CSRF_TRUSTED_ORIGINS = [
    "https://localhost:8000",
    "https://127.0.0.1:8000",
    "https://192.168.31.181:8000",
]

# The device ingest endpoint is authenticated via a custom X-API-Key header,
# which isn't in django-cors-headers' default allow-list.
CORS_ALLOW_HEADERS = list(default_headers) + ["x-api-key"]