import time
import ollama

from src.usecase.trabscribe_usecase import TrabscribeUseCase
from src.types.app import TranscribeResponse
from src.types.models import Models, model_type

PRESENTATION_ANSWER_NO_TRANSCRIPT_RESULT = (
    "No transcription result"
)

PRESENTATION_ANSWER_MESSAGE_TEMPLATE: str = (
    "Transcribed:\n\n%s\n\n"
)

PRESENTATION_ANSWER_WITH_DURATION_MESSAGE_TEMPLATE: str = (
    "Transcribed:\n\n%s\n\n"
    "Duration:\n\n%s seconds"
)

DISABLE_FILTER_WARNINGS_PARAM = "ignore"


class AppPresentation:
    def __init__(
            self,
            model_type_raw: model_type,
            audio_path: str,

            disable_warnings: bool = True,
            duration_showing: bool = False,
    ):
        self.model_type_raw: model_type = model_type_raw
        self.audio_path: str = audio_path

        self.duration_showing: bool = duration_showing

        if disable_warnings:
            import warnings
            warnings.filterwarnings(DISABLE_FILTER_WARNINGS_PARAM)

    def __call__(self, *args, **kwargs) -> str:
        time_start: float = 0.0
        if self.duration_showing:
            time_start = time.time()

        app: TrabscribeUseCase = TrabscribeUseCase(
            model_type_raw=self.model_type_raw,
        )

        transcribe_result: TranscribeResponse = app.transcribe(
            audio_path=self.audio_path
        )

        if transcribe_result.is_empty:
            return PRESENTATION_ANSWER_NO_TRANSCRIPT_RESULT

        transcript: str = transcribe_result.result.strip()

        if self.duration_showing:
            time_end: float = time.time()
            result_time: str = f"{float(time_end - time_start):.2f}"

            result_str: str = PRESENTATION_ANSWER_WITH_DURATION_MESSAGE_TEMPLATE % (
                transcript,
                result_time,
            )

        else:
            result_str: str = PRESENTATION_ANSWER_MESSAGE_TEMPLATE % transcript

        return result_str
