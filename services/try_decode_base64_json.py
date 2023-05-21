import base64
import json


def try_decode_base64_json(base64_json):
    d = {}
    try:
        json_str = base64.b64decode(base64_json.encode()).decode()
        d = json.loads(json_str)
    except Exception as e:
        print(f"Error decoding base64 json: {e}")
    return d


def test_try_decode_base64_json():
    # Valid base64 encoded JSON string
    base64_json = base64.b64encode('{"key": "value"}'.encode()).decode()
    assert try_decode_base64_json(base64_json) == {"key": "value"}

    # Invalid base64 encoded JSON string results in empty dict by default
    base64_json = "invalid_base64_string"
    assert try_decode_base64_json(base64_json) == {}

    # Invalid JSON string after decoding
    base64_json = base64.b64encode('{"key": "value"'.encode()).decode()
    assert try_decode_base64_json(base64_json) == {}
