from datetime import date


def convert_date_to_iso_8601(dt: date) -> str:
    return dt.strftime("%m/%d/%Y, %H:%M:%S")
