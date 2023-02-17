__all__ = (
    "NAME_INDEX",
    "CONTENT_TYPE",
    "MOBILE_INDEX",
    "REQUEST_TYPE",
    "ADDRESS_INDEX",
    "HOSPITAL_INDEX",
    "QUANTITY_INDEX",
    "DATA_INTEGRITY",
    "BLOOD_TYPES_MAP",
    "BLOOD_TYPE_INDEX",
    "LAST_INPUT_INDEX",
    "ACTUAL_BLOOD_TYPE",
    "MAX_REQUEST_HISTORY",
    "CONFIRMED_INTEGRITY",
    "END_OF_REQUEST_INDEX",
    "HUMAN_READABLE_BLOOD_TYPE",
)

NAME_INDEX = 1
REQUEST_TYPE = 0
MOBILE_INDEX = 2
ADDRESS_INDEX = 3
QUANTITY_INDEX = 5
DATA_INTEGRITY = 7
BLOOD_TYPE_INDEX = 4
HOSPITAL_INDEX = 6
LAST_INPUT_INDEX = -1
ACTUAL_BLOOD_TYPE = 0
CONFIRMED_INTEGRITY = 7
MAX_REQUEST_HISTORY = 10
END_OF_REQUEST_INDEX = 8
CONTENT_TYPE = "text/plain"
HUMAN_READABLE_BLOOD_TYPE = 1

BLOOD_TYPES_MAP = {
    1: ("o_positive", "O Positive"),
    2: ("o_negative", "O Negative"),
    3: ("a_positive", "A Positive"),
    4: ("a_negative", "A Negative"),
    5: ("b_positive", "B Positive"),
    6: ("b_negative", "B Negative"),
    7: ("ab_positive", "AB Positive"),
    8: ("ab_negative", "AB Negative"),
}
