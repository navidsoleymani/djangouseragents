from django.contrib import admin
from django.utils.timezone import now, timedelta
from django.utils.translation import gettext_lazy as _

from djangouseragents.models import UserAgentDeviceModel


@admin.register(UserAgentDeviceModel)
class UserAgentDeviceModelAdmin(admin.ModelAdmin):
    ordering = ('-created_dt',)
    permission_resource = "user_agent_device"

    list_display = (
        'name',
        'ip',
        'user_id_display',
        'device_type_display',
        'device_display',
        'browser_display',
        'os_display',
        'total_requests',
        'requests_last_24h',
        'requests_last_hour',
        'created_dt',
    )

    search_fields = (
        'id',
        'user_id',
        'ip',
        'key',
        'name',
    )
    list_filter = (
        'is_mobile',
        'is_tablet',
        'is_touch_capable',
        'is_pc',
        'is_bot',
        'browser_family',
        'os_family',
        'device_family',
    )
    readonly_fields = (
        'id',
        'created_dt',
        'key',
        'name',
    )
    fieldsets = (
        (_('Base Info'), {
            'fields': (
                'name',
                'user_id',
                'key',
                'ip',
            )
        }),
        (_('User Agent'), {
            'fields': (
                'is_mobile',
                'is_tablet',
                'is_touch_capable',
                'is_pc',
                'is_bot',
                'browser_family',
                'browser_version',
                'os_family',
                'os_version',
                'device_family',
                'device_brand',
                'device_model',
            )
        }),
    )

    # Disabling any manual change/add/delete in admin panel
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    # Display user_id or "Anonymous"
    def user_id_display(self, obj):
        return obj.user_id or 'Anonymous'

    user_id_display.short_description = _('User ID')

    # Create human-readable summary of the device type
    def device_type_display(self, obj):
        parts = []
        if obj.is_pc:
            parts.append('PC')
        if obj.is_mobile:
            parts.append('Mobile')
        if obj.is_tablet:
            parts.append('Tablet')
        if obj.is_bot:
            parts.append('Bot')
        if obj.is_touch_capable:
            parts.append('TouchCapable')
        return ' / '.join(parts) if parts else 'Unknown'

    device_type_display.short_description = _('Device Type')

    # Concatenate browser info
    def browser_display(self, obj):
        return f'{obj.browser_family} {obj.browser_version or ""}'.strip()

    browser_display.short_description = _('Browser')

    # Concatenate OS info
    def os_display(self, obj):
        return f'{obj.os_family} {obj.os_version or ""}'.strip()

    os_display.short_description = _('Operating System')

    # Concatenate device info
    def device_display(self, obj):
        return f'{obj.device_family or ""} {obj.device_brand or ""} {obj.device_model or ""}'.strip()

    device_display.short_description = _('Device')

    # Total number of requests for this device
    def total_requests(self, obj):
        return obj.requests.count()

    total_requests.short_description = _('Total Requests')

    # Requests made in the last 24 hours
    def requests_last_24h(self, obj):
        return obj.requests.filter(created_dt__gte=now() - timedelta(hours=24)).count()

    requests_last_24h.short_description = _('Requests (24h)')

    # Requests made in the last 1 hour
    def requests_last_hour(self, obj):
        return obj.requests.filter(created_dt__gte=now() - timedelta(hours=1)).count()

    requests_last_hour.short_description = _('Requests (1h)')
