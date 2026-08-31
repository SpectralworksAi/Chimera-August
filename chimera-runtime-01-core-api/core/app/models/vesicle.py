from pydantic import BaseModel, Field, field_validator


class Vesicle(BaseModel):
    """Minimal PION/Vesicle transport object used by the runtime boundary."""

    id: str = Field(min_length=1)
    payload: dict

    @field_validator("payload")
    @classmethod
    def validate_payload(cls, value):
        if not isinstance(value, dict):
            raise ValueError("payload must be an object")
        return value

    def validated_state(self) -> dict:
        """Return only validated state for injection into a model request."""
        return self.model_dump(mode="json")