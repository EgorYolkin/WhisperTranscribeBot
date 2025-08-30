import typing
import dataclasses

model_type = typing.NewType("model_type", str)


@dataclasses.dataclass
class Models:
    tiny: model_type = "tiny"
    base: model_type = "base"
    small: model_type = "small"
    medium: model_type = "medium"
    large: model_type = "large"
