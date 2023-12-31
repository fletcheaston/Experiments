import uuid

from django.db import models


class DjangoModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        editable=False,
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        db_index=True,
        editable=False,
    )

    class Meta:
        abstract = True
