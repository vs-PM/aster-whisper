import json
import queue
import threading
import asyncio
import socket
import logging
from typing import Optional
from vosk import KaldiRecognizer

from v1.db.whisper_dao import WhisperTranscriptDAO
from v1.config.ari_config import app_settings
from v1.vosk.model_manager import vosk_model
import aioari

logger = logging.getLogger(__name__)

class ARIWorker:
    """
    Основной воркер для работы c Asterisk ARI и Vosk
    """
    def __init__(self):
        self.transcript_queue = queue.Queue()
        self.audio_thread: Optional[threading.Thread] = None
        self.ari_thread: Optional[threading.Thread] = None
        self.model = vosk_model
        # client будет сохраняться после коннекта, если пригодится
        self.client = None
        logger.info("ARIWorker initialized, Vosk model %s", "loaded" if self.model else "not loaded")

    def process_audio(self) -> None:
        """
        Потоковая обработка аудиочанков из очереди через Vosk и запись текста в БД
        """
        logger.info("Starting audio processing thread")
        try:
            recognizer = KaldiRecognizer(self.model, 8000)
            chunk = b''

            while True:
                data = self.transcript_queue.get()
                if data is None:  # Сигнал останова
                    logger.debug("Received termination signal in audio processor")
                    break
                chunk += data
                if recognizer.AcceptWaveform(chunk):
                    self._process_recognition_result(recognizer.Result())
                    chunk = b''

            if chunk:
                self._process_recognition_result(recognizer.FinalResult())
        except Exception as e:
            logger.error(f"Audio processing error: {e}", exc_info=True)
        finally:
            logger.info("Audio processing thread stopped")

    def _process_recognition_result(self, result: str) -> None:
        """
        Парсинг результата от Vosk и сохранение в БД
        """
        try:
            res = json.loads(result)
            text = res.get("text", "").strip()
            if text:
                logger.debug(f"Recognized text: {text}")
                WhisperTranscriptDAO.create(
                    file_name=None,
                    channel_id=None,
                    text=text
                )
        except Exception as e:
            logger.error(f"Recognition result processing error: {e}")

    def audio_server(self) -> None:
        """
        Поток приёма аудиоданных через TCP сокет
        """
        logger.info("Starting audio server thread")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind((app_settings.ARI_MEDIA_HOST, app_settings.ARI_MEDIA_PORT))
                sock.listen(1)
                logger.info(f"Audio server listening on {app_settings.ARI_MEDIA_HOST}:{app_settings.ARI_MEDIA_PORT}")

                conn, addr = sock.accept()
                logger.info(f"Accepted audio connection from {addr}")
                try:
                    while True:
                        data = conn.recv(320)
                        if not data:
                            logger.debug("Received empty data, closing connection")
                            break
                        self.transcript_queue.put(data)
                finally:
                    self.transcript_queue.put(None)
                    conn.close()
                    logger.info("Audio connection closed")
        except Exception as e:
            logger.error(f"Audio server error: {e}", exc_info=True)
        finally:
            logger.info("Audio server thread stopped")

    # ------------- ARI EVENT HANDLERS -------------

    async def on_start(self, channel, event):
        """
        Обработчик захода канала в Stasis (начало звонка)
        """
        logger.info(f"on_start: channel={channel}, event={event}")

        try:
            bridge = await self.client.bridges.create(type='mixing')
            logger.debug(f"Created bridge: {bridge.id}")

            media = await self.client.externalMedia.originate(
                endpoint=f"Local/{app_settings.ARI_MEDIA_HOST}@default",
                app=app_settings.ARI_APP,
                external_host=f'socket:{app_settings.ARI_MEDIA_HOST}:{app_settings.ARI_MEDIA_PORT}',
                format='slin',
                appArgs='media'
            )
            logger.debug(f"Originated media: {media.id}")

            await bridge.addChannel(channelId=channel.id)
            await bridge.addChannel(channelId=media.id)
            logger.info(f"Added channels to bridge {bridge.id}")

            self.audio_thread = threading.Thread(
                target=self.audio_server,
                daemon=True,
                name="Audio-Thread"
            )
            self.audio_thread.start()
            logger.info("Started audio server thread")

        except Exception as e:
            logger.error(f"Call start error: {e}", exc_info=True)

    async def on_end(self, channel, event):
        """
        Обработчик окончания звонка
        """
        logger.info(f"on_end: channel={channel}, event={event}")
        # Тут можно (при необходимости) остановить сопутствующие потоки и т.д.

    async def on_any_event(self, event):
        """
        Лог всех событий ARI для отладки
        """
        logger.debug(f"on_any_event: event={event}")

    # ------------- ARI MAIN LOOP -------------

    async def run_ari(self) -> None:
        """
        Основная асинхронная петля работы с ARI
        """
        try:
            logger.info(f"Connecting to ARI at {app_settings.ARI_WS_URL}")
            client = await aioari.connect(
                str(app_settings.ARI_WS_URL),
                app_settings.ARI_USER,
                app_settings.ARI_PASSWORD
            )
            self.client = client  # теперь client доступен во всех обработчиках
            logger.info("Successfully connected to ARI")

            try:
                # Регистрируем обработчики БЕЗ partial и только с нужными сигнатурами!
                client.on_channel_event('StasisStart', self.on_start)
                client.on_channel_event('StasisEnd', self.on_end)
                client.on_event('*', self.on_any_event)

                logger.info(f"Starting ARI worker for app: {app_settings.ARI_APP}")
                await client.run(apps=app_settings.ARI_APP)
            except asyncio.CancelledError:
                logger.info("ARI worker stopped by cancellation")
            except Exception as e:
                logger.error(f"ARI worker runtime error: {e}", exc_info=True)
            finally:
                await client.close()
                logger.info("Disconnected from ARI")
        except Exception as e:
            logger.error(f"ARI connection error: {e}", exc_info=True)
            raise

    def _run_ari_in_thread(self):
        """
        Отдельный поток для арбитража ARI
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.run_ari())
        except Exception as e:
            logger.error(f"ARI thread error: {e}", exc_info=True)
        finally:
            loop.close()
            logger.info("ARI thread stopped")

    def start(self) -> None:
        """
        Запуск всех компонентов: аудио и ARI
        """
        if not self.model:
            logger.error("Vosk model not loaded")
            raise RuntimeError("Vosk model not available")

        logger.info("Starting ARI worker components")
        threading.Thread(
            target=self.process_audio,
            daemon=True,
            name="Audio-Processor"
        ).start()

        self.ari_thread = threading.Thread(
            target=self._run_ari_in_thread,
            daemon=True,
            name="ARI-Worker"
        )
        self.ari_thread.start()
        logger.info("ARI worker started successfully")

# ---- Публичный запуск:

_worker = ARIWorker()

def start_ari_worker():
    _worker.start()

# ---- Healthcheck:

async def check_ari_connection() -> bool:
    """
    Проверка коннекта к ARI (для диагностики)
    """
    try:
        logger.info("Testing ARI connection")
        client = await aioari.connect(
            str(app_settings.ARI_WS_URL),
            app_settings.ARI_USER,
            app_settings.ARI_PASSWORD,
        )
        await client.close()
        logger.info("ARI connection test successful")
        return True
    except Exception as e:
        logger.error(f"ARI connection test failed: {e}")
        return False
