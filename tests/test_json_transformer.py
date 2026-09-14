import pytest

from ai_cli.jsonTransformer import JsonTransformer


def test_valid_input_transforms_end_to_end():
    transformer = JsonTransformer()

    payload = {
        "EventName": "user_created",
        "UserID": "12345",
        "Timestamp": "2026-09-13T21:00:00Z",
        "description": "  New user created  ",
        "count": 3,
    }

    result = transformer.transform(payload)

    assert result == {
        "event_name": "user_created",
        "user_id": "12345",
        "timestamp": "2026-09-13T21:00:00Z",
        "description": "New user created",
        "count": 3,
    }

    assert transformer.get_json_data() == result


@pytest.mark.parametrize(
    "payload, expected_message",
    [
        (
            {
                "UserID": "12345",
                "Timestamp": "2026-09-13T21:00:00Z",
            },
            "event_name is required",
        ),
        (
            {
                "EventName": "user_created",
                "Timestamp": "2026-09-13T21:00:00Z",
            },
            "user id is required",
        ),
    ],
)
def test_missing_required_fields_raise_validation_error(payload, expected_message):
    transformer = JsonTransformer()

    with pytest.raises(ValueError, match=expected_message):
        transformer.transform(payload)


def test_mixed_case_keys_are_normalized():
    transformer = JsonTransformer()

    payload = {
        "EventName": "user_created",
        "USER_ID": "12345",
        "CreatedBy": "system",
        "RequestID": "req-001",
    }

    result = transformer.transform(payload)

    assert "event_name" in result
    assert "user_id" in result
    assert "created_by" in result
    assert "request_id" in result


def test_whitespace_is_stripped_from_string_values():
    transformer = JsonTransformer()

    payload = {
        "EventName": "  user_created  ",
        "UserID": "  12345  ",
        "Description": "\thello world\n",
        "Count": 10,
    }

    result = transformer.transform(payload)

    assert result["event_name"] == "user_created"
    assert result["user_id"] == "12345"
    assert result["description"] == "hello world"
    assert result["count"] == 10
