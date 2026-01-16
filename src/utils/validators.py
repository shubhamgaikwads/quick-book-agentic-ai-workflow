def validate_date(date_str):
    if not date_str:
        return False
    return True

def validate_time(time_str):
    if not time_str:
        return False
    return True

def validate_user_input(user_input):
    return bool(user_input and user_input.strip())
