from src.types.app import TranscribeResponse
from src.usecase.trabscribe_usecase import AbstractTranscribeUseCase, WHISPER_RESULT_FIELD_NAME


class MockTranscribeUseCase(AbstractTranscribeUseCase):
    def __init__(self, model_type_raw=None, response: TranscribeResponse | None = None):
        super().__init__(model_type_raw)
        self._response = response or TranscribeResponse(is_empty=True)

    def transcribe(self, audio_path: str) -> TranscribeResponse:
        return self._response

    def _transcribe(self, audio_path: str) -> TranscribeResponse:
        return self._response

    def _load_model(self):
        return None


import unittest
from unittest.mock import patch, MagicMock
from src.usecase.trabscribe_usecase import TrabscribeUseCase
from src.types.app import TranscribeResponse
from src.types.models import model_type


class TestTrabscribeUseCase(unittest.TestCase):

    def setUp(self):
        self.use_case = TrabscribeUseCase(model_type_raw=model_type('small'))

    @patch('src.your_module.whisper')
    def test_transcribe_empty_audio_path(self, mock_whisper):
        # is_empty = True
        result = self.use_case.transcribe('')
        self.assertTrue(result.is_empty)
        mock_whisper.transcribe.assert_not_called()

    @patch('src.your_module.whisper')
    @patch.object(TrabscribeUseCase, '_load_model')
    def test_transcribe_successful(self, mock_load_model, mock_whisper):
        mock_model = MagicMock()
        mock_load_model.return_value = mock_model
        mock_whisper.transcribe.return_value = {
            WHISPER_RESULT_FIELD_NAME: "Привет это тест транскребация"
        }

        audio_path = 'src/tests/data/test_audio.ogg'
        result = self.use_case.transcribe(audio_path)

        mock_load_model.assert_called_once()
        mock_whisper.transcribe.assert_called_once_with(mock_model, audio_path)
        self.assertFalse(result.is_empty)
        self.assertEqual(result.result, "Привет это тест транскребация")

    @patch('src.your_module.whisper')
    @patch.object(TrabscribeUseCase, '_load_model')
    def test_transcribe_no_result(self, mock_load_model, mock_whisper):
        # Если в результате нет текста, вернется is_empty=True
        mock_model = MagicMock()
        mock_load_model.return_value = mock_model
        mock_whisper.transcribe.return_value = {}

        audio_path = 'src/tests/data/test_audio.ogg'
        result = self.use_case.transcribe(audio_path)

        self.assertTrue(result.is_empty)
        self.assertIsNone(getattr(result, 'result', None))

    @patch('src.your_module.whisper')
    def test_load_model_calls_whisper_load_model(self, mock_whisper):
        self.use_case.model_type = model_type("small")
        self.use_case._load_model()
        mock_whisper.load_model.assert_called_once_with("small")


if __name__ == '__main__':
    unittest.main()
