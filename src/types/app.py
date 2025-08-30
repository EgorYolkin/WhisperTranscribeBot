import dataclasses


@dataclasses.dataclass
class TranscribeResponse:
    is_empty: bool = False
    result: str = ""
