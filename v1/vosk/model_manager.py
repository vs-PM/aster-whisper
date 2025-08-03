from vosk import Model
from v1.config.vosk_config import vosk_settings

class VoskModelManager:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VoskModelManager, cls).__new__(cls)
            cls._model = None
        return cls._instance

    @property
    def model(self):
        if self._model is None:
            raise RuntimeError("Vosk model not loaded - call load_model() first")
        return self._model

    def load_model(self):
        if self._model is None:
            if not vosk_settings.MODEL_PATH:
                raise RuntimeError("Vosk model path not specified!")
            self._model = Model(str(vosk_settings.MODEL_PATH))
        return self._model

# Готовый singleton
vosk_model = VoskModelManager()












# from vosk import Model
# from v1.config.vosk_config import vosk_settings
# from typing import Optional

# class VoskModelManager:
#     _instance = None
#     _model = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(VoskModelManager, cls).__new__(cls)
#             cls._model = Model(str(vosk_settings.MODEL_PATH)) if vosk_settings.MODEL_PATH else None
#         return cls._instance

#     @property
#     def model(self):
#         if self._model is None:
#             raise RuntimeError("Vosk model not loaded - check VOSK_MODEL_PATH")
#         return self._model

# vosk_model = VoskModelManager()
