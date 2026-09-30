from pydantic import BaseModel
from pypresence import ActivityType, StatusDisplayType

class RPCDataModel(BaseModel):
    activity_type: ActivityType | None = None
    status_display_type: StatusDisplayType | None = None

    client_id: str | None = None
    name: str | None = None
    state: str | None = None
    details: str | None = None

    large_image: str | None = None
    large_text: str | None = None

    small_image: str | None = None
    small_text: str | None = None

    start: int | None = None
    end: int | None = None

    buttons: list[dict[str, str]] | None = None

    state_url: str | None = None
    details_url: str | None = None

    large_url: str | None = None
    small_url: str | None = None

    party_id: str | None = None
    party_size: list[int] | None = None

    join: str | None = None
    spectate: str | None = None
    match: str | None = None

    instance: bool | None = None