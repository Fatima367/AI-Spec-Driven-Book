"""
Logging utilities for the personalization service
"""
import logging
import os
from datetime import datetime
from typing import Any

# Create a custom logger
logger = logging.getLogger('personalization_service')
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('personalization_service.log')

# Set levels for handlers
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

# Create formatters and add them to handlers
console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')

console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Add handlers to the logger
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

def log_personalization_request(chapter_id: str, user_id: str, response_time: float, success: bool = True, error: str = None):
    """
    Log personalization request details
    """
    if success:
        logger.info(f"Personalization request completed - Chapter: {chapter_id}, User: {user_id}, Response time: {response_time:.2f}ms")
    else:
        logger.error(f"Personalization request failed - Chapter: {chapter_id}, User: {user_id}, Response time: {response_time:.2f}ms, Error: {error}")

def log_performance_metrics(metrics: dict):
    """
    Log performance metrics
    """
    logger.info(f"Performance Metrics - Total Requests: {metrics['total_requests']}, "
                f"Avg Response Time: {metrics['avg_response_time']:.2f}ms, "
                f"P95 Response Time: {metrics['p95_response_time']:.2f}ms, "
                f"Percent under 500ms: {metrics['percent_under_500ms']:.2f}%")

def log_error(error: Exception, context: str = ""):
    """
    Log error with context
    """
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)

def log_warning(message: str, context: str = ""):
    """
    Log warning message
    """
    logger.warning(f"Warning in {context}: {message}")

def log_info(message: str):
    """
    Log info message
    """
    logger.info(message)

def setup_logging():
    """
    Setup logging configuration
    """
    # Set the logging level based on environment variable
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logger.setLevel(getattr(logging, log_level))

    # Set up log rotation to prevent large log files
    try:
        from logging.handlers import RotatingFileHandler

        # Remove existing file handler
        for handler in logger.handlers[:]:
            if isinstance(handler, logging.FileHandler) and not isinstance(handler, RotatingFileHandler):
                logger.removeHandler(handler)

        # Add rotating file handler
        rotating_handler = RotatingFileHandler(
            'personalization_service.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        rotating_handler.setFormatter(file_format)
        logger.addHandler(rotating_handler)
    except ImportError:
        # If RotatingFileHandler is not available, continue with regular file handler
        pass

# Setup logging when module is imported
setup_logging()