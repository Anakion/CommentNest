from pydantic import BaseModel, EmailStr, HttpUrl, validator, field_validator
from typing import Optional
import re

USERNAME_REGEX = r"^[a-zA-Z0-9]{1,60}$"
CAPTCHA_REGEX = r"^[a-zA-Z0-9]{1,10}$"
ALLOWED_TAGS = ["a", "code", "i", "strong"]


class CommentCreateSchema(BaseModel):
    user_name: str
    email: EmailStr
    home_page: Optional[HttpUrl] = None
    captcha: str
    text: str

    # Проверка User name
    @field_validator("user_name")
    def validate_user_name(cls, value):
        if not re.match(USERNAME_REGEX, value):
            raise ValueError(
                "User name must be between 1 and 60 characters long and contain only letters and numbers"
            )

    # Проверка CAPTCHA
    @field_validator("captcha")
    def validate_captcha(cls, value):
        if not re.match(CAPTCHA_REGEX, value):
            raise ValueError(
                "CAPTCHA must be between 1 and 10 characters long and contain only letters and numbers"
            )

    # Проверка текста на разрешенные HTML-теги
    @field_validator("text")
    def validate_text(cls, value):
        tags = re.findall(r"</?(\w+)", value)
        for tag in tags:
            if tag not in ALLOWED_TAGS:
                raise ValueError(f"HTML tag <{tag}> is not allowed")
        return value
