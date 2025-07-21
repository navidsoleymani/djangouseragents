from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoUseragentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangouseragents'
    verbose_name = _('Django User Agents')
