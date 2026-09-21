import logging


def logger_configure() -> None:
    """Hjälper skapa konsol och fil logger"""

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("dashboard.log", encoding="utf-8"),
        ],
    )