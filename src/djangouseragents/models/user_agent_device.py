from django.db import models
from django.utils.translation import gettext_lazy as _

from djangouniquetoolkit.services import get_unique_username


def get_unique_name():
    return get_unique_username()


class UserAgentDevice(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        blank=False,
        null=False,
        max_length=255,
        default=get_unique_name,
        unique=True,
        db_index=True,
        editable=False,
        help_text=_(
            "A unique name is assigned to each agent completely "
            "randomly so that each agent can be called by the same name."),
    )
    key = models.CharField(
        verbose_name=_('Key'),
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
    )
    user_id = models.CharField(
        verbose_name=_('User ID'),
        blank=True,
        null=True,
        max_length=255,
    )
    is_mobile = models.BooleanField(
        verbose_name=_('Mobile'),
        blank=True,
        null=True,
    )
    is_tablet = models.BooleanField(
        verbose_name=_('Tablet'),
        blank=True,
        null=True,
    )
    is_touch_capable = models.BooleanField(
        verbose_name=_('Touch Capable'),
        blank=True,
        null=True,
    )
    is_pc = models.BooleanField(
        verbose_name=_('PC'),
        blank=True,
        null=True,
    )
    is_bot = models.BooleanField(
        verbose_name=_('Bot'),
        blank=True,
        null=True,
    )

    browser_family = models.CharField(
        verbose_name=_('Browser Family'),
        max_length=255,
        blank=True,
        null=True,
    )
    browser_version = models.CharField(
        verbose_name=_('Browser Version'),
        max_length=255,
        blank=True,
        null=True,
    )
    os_family = models.CharField(
        verbose_name=_('OS Family'),
        max_length=255,
        blank=True,
        null=True,
    )
    os_version = models.CharField(
        verbose_name=_('OS Version'),
        max_length=255,
        blank=True,
        null=True,
    )
    device_family = models.CharField(
        verbose_name=_('Device Family'),
        max_length=255,
        blank=True,
        null=True,
    )
    device_brand = models.CharField(
        verbose_name=_('Device Brand'),
        max_length=255,
        blank=True,
        null=True,
    )
    device_model = models.CharField(
        verbose_name=_('Device Model'),
        max_length=255,
        blank=True,
        null=True,
    )

    ip = models.CharField(
        verbose_name=_('IP'),
        max_length=255,
        blank=True,
        null=True,
    )

    created_dt = models.DateTimeField(
        verbose_name=_('First Visit DateTime'),
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('User Agent Device')
        verbose_name_plural = _('User Agent Devices')
