
import logging
from config.config import LOG_DIR

def configurar_logs():
    """

    :return:
    """
    arquivo_log = LOG_DIR / "importacao.log"
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.FileHandler(
                arquivo_log,
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ]
    )
