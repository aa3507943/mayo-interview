from dataclasses import dataclass

@dataclass
class User:
    username: str
    password: str = "secret_sauce"
    description: str = ""

class Users:
    STANDARD_USER = User("standard_user", description="Normal user")
    LOCKED_OUT_USER = User("locked_out_user", description="Locked user")
    PROBLEM_USER = User("problem_user", description="User with image issues")
    PERFORMANCE_GLITCH_USER = User("performance_glitch_user", description="User with delay issues")
    ERROR_USER = User("error_user", description="User with JS errors")
    VISUAL_USER = User("visual_user", description="User with layout issues")

    ALL_USERS = [
        STANDARD_USER,
        LOCKED_OUT_USER,
        PROBLEM_USER,
        PERFORMANCE_GLITCH_USER,
        ERROR_USER,
        VISUAL_USER
    ]
