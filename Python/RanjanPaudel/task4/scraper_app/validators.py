import datetime


def validate_signin_form(signin_data):
    if len(signin_data['userFullName']) < 3:
        return {
            "has_error": True,
            "error": {
                "userFullName": "Full name length should be 3 to 100 characters"
            }
        }

    try:
        datetime.datetime.strptime(signin_data['userDOB'], '%Y-%m-%d')
    except ValueError:
        return {
            "has_error": True,
            "error": {
                "userDOB": "Date format should be YYYY-MM-DD"
            }
        }

    if len(signin_data['username']) < 6 or len(signin_data['username']) > 100:
        return {
            "has_error": True,
            "error": {
                "username": "Username length should be 6 to 100 characters"
            }
        }

    if len(signin_data['userPasswordCreate']) < 8:
        return {
            "has_error": True,
            "error": {
                "userPasswordCreate": "Password length should be at least 8 characters"
            }
        }

    if signin_data['userPasswordCreate'] != signin_data['userPasswordConfirm']:
        return {
            "has_error": True,
            "error": {
                "userPasswordConfirm": "Passwords do not match"
            }
        }

    return {
        "has_error": False
    }


def validate_login_form(login_data):
    if len(login_data['username']) < 1:
        return {
            "has_error": True,
            "error": {
                "username": "Username is required"
            }
        }

    if len(login_data['userPassword']) < 1:
        return {
            "has_error": True,
            "error": {
                "userPassword": "Password is required"
            }
        }

    return {
        "has_error": False
    }
