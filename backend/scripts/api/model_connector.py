from pathlib import Path

from log import logger
from main import Pipeline


PROJECT_ROOT_DIR = str(Path(__file__).parent.parent)

obj = Pipeline()

class ModelConnector:
    """Connects model operations to endppoint-router"""

    def __init__(self) -> None:
        pass

    def train(self):
        res = []
        try:
            obj.run()
        except Exception as e:
            logger.error(str(e))
        return res

    def predict(self, landmarks):
        res = {}
        try:
            res = obj.predict(landmarks)
        except Exception as e:
            logger.error(str(e))
        return res
