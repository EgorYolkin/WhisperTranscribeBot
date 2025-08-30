import typing
from abc import ABC, abstractmethod

from src.types.app import TranscribeResponse
from src.types.models import model_type
import whisper

empty_result_type = typing.NewType("empty_result_type", str)

EMPTY_RESULT: empty_result_type = empty_result_type("")
WHISPER_RESULT_FIELD_NAME: str = "text"


class AbstractTranscribeUseCase(ABC):
    """
    abstract class for use-cases for TranscribeResponse.
    """

    def __init__(self, model_type_raw):
        self.model_type = model_type_raw

    @abstractmethod
    def transcribe(self, audio_path: str) -> TranscribeResponse:
        """
        make a file transcribe
        """
        raise NotImplementedError

    @abstractmethod
    def _transcribe(self, audio_path: str) -> TranscribeResponse:
        """
        hidden logic for transcribe
        """
        raise NotImplementedError

    @abstractmethod
    def _load_model(self):
        """
        load model (whisper or analogs)
        """
        raise NotImplementedError


class TrabscribeUseCase(AbstractTranscribeUseCase):
    """
    provide a class with application functions
    """

    def __init__(self, model_type_raw: model_type):
        super().__init__(model_type_raw)
        self.model_type = model_type_raw

    def transcribe(
            self,
            audio_path: str,
    ) -> TranscribeResponse:
        return self._transcribe(audio_path)

    def _transcribe(
            self,
            audio_path: str
    ) -> TranscribeResponse:

        if len(audio_path) == 0:
            return TranscribeResponse(
                is_empty=True,
            )

        loaded_model = self._load_model()

        result = whisper.transcribe(
            loaded_model,
            audio_path
        )

        if result.get(
                WHISPER_RESULT_FIELD_NAME,
                False
        ):
            result = TranscribeResponse(
                is_empty=False,
                result=result[WHISPER_RESULT_FIELD_NAME]
            )
            return result

        return TranscribeResponse(
            is_empty=True,
        )

    def _load_model(self) -> whisper.Whisper:
        model_type_str: str = str(self.model_type)

        model = whisper.load_model(model_type_str)

        return model
