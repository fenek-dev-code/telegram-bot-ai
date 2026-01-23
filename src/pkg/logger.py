# app/logger.py
import json
import os
import sys

from loguru import logger

from src.core.config import config as conf


def serialize(record):
    """Сериализация в JSON для Docker/ELK"""
    subset = {
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "module": record["name"],
        "function": record["function"],
        "line": record["line"],
        "service": os.getenv("SERVICE_NAME", "myapp"),
        "environment": os.getenv("ENVIRONMENT", "development"),
    }
    if record.get("extra"):
        subset.update(record["extra"])

    sensitive_keys = ["password", "token", "secret", "key", "authorization"]
    for key in list(subset.keys()):
        if any(s in key.lower() for s in sensitive_keys):
            subset[key] = "[REDACTED]"

    return json.dumps(subset, ensure_ascii=False)


def setup_production_logger():
    """Production логгер для Docker"""
    logger.remove()
    logger.add(
        sys.stdout,
        format=serialize,
        level=conf.LOG_LEVEL,
        serialize=True,
        backtrace=True,
        catch=True,
    )

    return logger


log = setup_production_logger()
