LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DEFAULT_HANDLERS = [
    "console",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": LOG_FORMAT},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": LOG_DEFAULT_HANDLERS,
            "level": "INFO",
        },
        "werkzeug": {
            "propagate": False,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": LOG_DEFAULT_HANDLERS,
    },
}
