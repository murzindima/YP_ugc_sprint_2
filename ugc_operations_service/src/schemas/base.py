from pydantic import BaseModel, Field
from pydantic_mongo import ObjectIdField


class ObjectIDMixin(BaseModel):
    """Mixin for models with an ObjectIdField."""

    id: ObjectIdField = Field(alias="_id")


class AcknowledgedMixin(BaseModel):
    acknowledged: bool


class BaseUpdate(ObjectIDMixin, AcknowledgedMixin):
    matched_count: int
    modified_count: int
    upserted_id: ObjectIdField | str


class BaseDelete(ObjectIDMixin, AcknowledgedMixin):
    deleted_count: int
