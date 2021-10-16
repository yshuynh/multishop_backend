# Python 3 code to demonstrate the
# working of MD5 (string - hexadecimal)
# The above code takes string and converts it into the byte equivalent using encode() so that it can be accepted by the
# hash function. The md5 hash function encodes it and then using hexdigest(), hexadecimal equivalent encoded string
# is printed.
import hashlib


def encrypt_string(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()


def check_encrypted_string(input_string, encrypted_string):
    return hashlib.md5(input_string.encode()).hexdigest() == encrypted_string
