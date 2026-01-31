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


def setup_dev_logger():
    """Development логгер с цветами и эмодзи"""

    # Удаляем стандартные обработчики
    logger.remove()

    # Формат с эмодзи и цветами
    format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level.icon} {level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # Добавляем эмодзи для уровней
    logger.level("TRACE", color="<fg #666666>", icon="🔍")
    logger.level("DEBUG", color="<cyan>", icon="🐛")
    logger.level("INFO", color="<bold><fg #34eb58>", icon="ℹ️")
    logger.level("SUCCESS", color="<bold><green>", icon="✅")
    logger.level("WARNING", color="<bold><yellow>", icon="⚠️")
    logger.level("ERROR", color="<bold><red>", icon="❌")
    logger.level("CRITICAL", color="<bold><fg #ff00ff>", icon="💀")

    # Основной консольный вывод
    logger.add(
        sys.stdout,
        format=format,
        level="DEBUG",
        colorize=True,
        backtrace=True,
        diagnose=True,
        catch=True,
    )
    return logger


log = setup_dev_logger()
if conf.PROD:
    log = setup_production_logger()
