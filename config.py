# Master public and private key information for server
RSA_PRIVKEY = '-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAmHUNg8moyA5MiqoYboWzYNQ5/S5gmbioZ07c7tCsYiiFmgMH\nOCd7mVXvCC3eJIi1d96kexS2Pwfa9gsNCS6CcJTqAhYzYcbyFABcKENdBcRCX3xz\nX2Ins8XYqv4SJ1BQJ0wnxgrw4DCvJqzgvrReh/rOIBXZVSTfCggEtjb5fpWtlQAm\n+zgmpBEi1SlHj/u6/wJyJmyfjXhYGB2OPvn9ibWY8aRM0yAub58iKmhxHA+TI+n8\noi6ktt7/KF2mBPKNl5I3BqHFlHBXI3bN3Rqf8j/HDOq6VSlxypWrmJmV15eoZq5y\naoiS9dOtKbmwGVcuMUdiCcVeEFMEJAiON2ymzQIDAQABAoIBABmIgRrxSzM2MduH\nYVAhVEmDQbMFcWhNZOboblgQ2s4Vu0pv92WQN0MXAVF9XRcBTmMlBqcWcO9dgW5z\nq1s+TtpMFmUDEtftWd2/sa+MmKe+lt8nGKuA5OVW3VLF+oRbDxGFz6N7cZwaizsO\n+RT3YF2lw5/cCOoZosErVp6t1ls8s/z1DwcGMgjoNbs/lqlkHdek8cIAuaph6BDM\nPjGUxH3aCiifnylewkt1xKPpQWYt9b1gw4OkIhaKFtisN0NHYdXVVv3K3vKJHs+R\nwP6GXA/FLaO1LfqE731R7bZ4mBMc4eLsl4B5puIXuCi8DtewCuHR2ZLCkEJlQ8/L\noJOlPIECgYEAvjtvpLoU6yP+GmRY8eODwwvfviePad6gqplS5+BBe9cscqCyODNp\npLvpMTgZOfHGbxptzfWuwBllFxeyVoZ+g+ixCCaR2gr6tNYFduC9FpWWLh9ruklc\nKTxnOhGAmFD3wiv9UacELVbOFQmY6Fp//eSC7+9LETRTYKKdPc511msCgYEAzSpV\nRGX13dqEgsMpesg0oLmZ5pXxdltamyWAaTg2303P3duKJ9HEclOdrqsU4DpY6M99\np3sPzllGGIOJWlPxTmmso5taobVOaz4hF+mI85MeFtrFfdBmDYpqpBWBJBA2LGQm\nb5KanbJ1roFt2fGeZ9wk1ULe/OI2uWeu2cGlFacCgYAnp0INZ1CG91i3baVwvokv\ntiDshViKrAJ3rUAv33om82Jrfn3H40epNBZW0SfJAVHoxOyQmx7TIjgFSUY+bQig\nPHfyh/+tIM7DtT0sW4pu072bXadaDIKugc3Ot+lDVtVeX0cNpy/it457qiV6gare\nZKy6kPnn2y1qHluCj6/WgwKBgAEftT3drR4c/1LUDNseU6N5wM0RjzQNxg5Jg02Q\nQESy4Wues0AKlx/lM1zslP2xdCE6Wb7cHrcLqCWkOtFi2lSKoaZ3yGRQYPCXc4j0\n/4oOCUEoy6InzRdP5cumToHLEPDnT4qW6//nJVviW56xAyQggZcleaE6//++AKgy\ntlvLAoGBAKN601l7n8ApeC2umraXygJhpjX6geX9TA0cns+i2flrRSCAW0elgBjK\nNpqCBeoBMsPTY0m5fJ7+5Cyt62a9f+b+jFNy6fcCPPrhMImuYsFIxM/K4kk7DZ97\njXbxJ4nFs+R9LBToGBQ7s6Tje+zocxHtMh/55R/huI40a2y3zE8c\n-----END RSA PRIVATE KEY-----'
RSA_PUBKEY = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmHUNg8moyA5MiqoYboWz\nYNQ5/S5gmbioZ07c7tCsYiiFmgMHOCd7mVXvCC3eJIi1d96kexS2Pwfa9gsNCS6C\ncJTqAhYzYcbyFABcKENdBcRCX3xzX2Ins8XYqv4SJ1BQJ0wnxgrw4DCvJqzgvrRe\nh/rOIBXZVSTfCggEtjb5fpWtlQAm+zgmpBEi1SlHj/u6/wJyJmyfjXhYGB2OPvn9\nibWY8aRM0yAub58iKmhxHA+TI+n8oi6ktt7/KF2mBPKNl5I3BqHFlHBXI3bN3Rqf\n8j/HDOq6VSlxypWrmJmV15eoZq5yaoiS9dOtKbmwGVcuMUdiCcVeEFMEJAiON2ym\nzQIDAQAB\n-----END PUBLIC KEY-----'

GAME_LENGTH_SECONDS = 300 # The desired game length in seconds
BOOKKEEPING_PERIOD = 120   # we recommend at least 120 to prevent host being able to modify result by including transactions in last block (after known entropy)

WEBAPP_PORT = 5000
