from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class PionHeader(BaseModel):
    model_config = ConfigDict(extra="allow")

    iteration: int
    source_engine: str
    execution_mode: Literal["OON", "OOFF", "CCCC"]
    timestamp: str | None = None


class PionState(BaseModel):
    model_config = ConfigDict(extra="allow")

    current_objective: str
    active_uncertainty: str
    next_executable_step: str
    held_contradictions: str
    implementation_status: str


class PionPacket(BaseModel):
    model_config = ConfigDict(extra="allow")

    protocol: Literal["CPS/1.0 PION"]
    header: PionHeader
    state: PionState
    payload: dict[str, Any] = Field(default_factory=dict)


class Vesicle(BaseModel):
    """Transport envelope for a PION packet.

    The public shape remains ``id + payload`` for compatibility.  Before a
    generation request is sent to a model, ``validated_pion()`` converts the
    payload into the typed PION object so malformed state cannot silently reach
    the provider.
    """

    id: str
    payload: dict[str, Any]

    def validated_pion(self) -> PionPacket:
        return PionPacket.model_validate(self.payload)
