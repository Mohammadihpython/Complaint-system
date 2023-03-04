import base64

from fastapi import HTTPException


def decode_photo(path, encoded_string):
    """ this function  decode an encoded photo and write it as binary in path,  as a string"""
    with open(path, 'wb') as f:
        try:
            f.write(base64.b64decode(encoded_string.encode('utf-8')))
        except Exception as ex:
            raise HTTPException(400,"invalid photo encoding") from ex