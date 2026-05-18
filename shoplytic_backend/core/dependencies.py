from fastapi import Request

from core.config import settings


def get_settings(request: Request = None) -> Settings:
    return settings
