from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now as dj_now, timedelta


class StatusChoices(models.TextChoices):
    NORMAL = 'Normal', _('Normal')
    BUSY = 'Busy', _('Busy')
    VERY_BUSY = 'Very Busy', _('Very Busy')
    ABNORMAL = 'Abnormal', _('Abnormal')


class UserAgentRequest(models.Model):
    uad = models.ForeignKey(
        verbose_name=_('User Agent Device'),
        to='UserAgentDevice',
        on_delete=models.CASCADE,
        related_name='requests',
    )
    endpoint = models.TextField(
        verbose_name=_('Endpoint'),
    )
    response_status_code = models.IntegerField(
        verbose_name=_('Response Status Code'),
    )

    rn = models.IntegerField(
        verbose_name=_('Request Number'),
        default=0,
        help_text=_('Total request count'),
    )
    rn_ph = models.IntegerField(
        verbose_name=_('Requests Per Hour'),
        default=0,
        help_text=_('Last 1 hour'),
    )
    rn_24h = models.IntegerField(
        verbose_name=_('Requests Last 24h'),
        default=0,
        help_text=_('Last 24 hours'),
    )

    status_color = models.CharField(
        verbose_name=_('Status Color'),
        max_length=255,
        default='#06d6a0',
    )
    status = models.CharField(
        verbose_name=_('Status'),
        choices=StatusChoices.choices,
        max_length=64,
        default=StatusChoices.NORMAL,
    )

    method = models.CharField(
        verbose_name=_('HTTP Method'),
        max_length=64,
        blank=True,
        null=True,
    )
    get = models.JSONField(
        verbose_name=_('GET'),
        blank=True,
        null=True,
    )
    headers = models.JSONField(
        verbose_name=_('Headers'),
        blank=True,
        null=True,
    )
    cookies = models.JSONField(
        verbose_name=_('Cookies'),
        blank=True,
        null=True,
    )
    created_dt = models.DateTimeField(
        verbose_name=_('Created Datetime'),
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        return f'{self.endpoint} → {self.response_status_code}'

    class Meta:
        verbose_name = _('User Agent Request')
        verbose_name_plural = _('User Agent Requests')
        indexes = [
            models.Index(fields=['uad', 'created_dt'], name='idx_uad_created_dt'),
        ]

    def save(self, **kwargs):
        qs = self.uad.requests.all()
        now = dj_now()
        self.rn = qs.count() + 1
        self.rn_ph = qs.filter(created_dt__gte=now - timedelta(hours=1)).count() + 1
        self.rn_24h = qs.filter(created_dt__gte=now - timedelta(hours=24)).count() + 1

        if self.rn_ph < 50:
            self.status_color = '#06d6a0'
            self.status = StatusChoices.NORMAL
        elif self.rn_ph < 100:
            self.status_color = '#ffba08'
            self.status = StatusChoices.BUSY
        elif self.rn_ph < 500:
            self.status_color = '#f48c06'
            self.status = StatusChoices.VERY_BUSY
        else:
            self.status_color = '#d00000'
            self.status = StatusChoices.ABNORMAL

        super().save(**kwargs)
