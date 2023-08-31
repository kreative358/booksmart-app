from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from accounts.models import Account

# class ActivityLog(models.Model):
#     # Here we want to track everything that other users do. So, I'll add GenericForeignKey
#     content_type = models.ForeignKey(
#         ContentType, default=None, null=True, on_delete=models.SET_NULL, related_name='activity_logs')
#     object_id = models.BigIntegerField(default=None, null=True)
#     object = GenericForeignKey(ct_field="content_type", fk_field="object_id")
