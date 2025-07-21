from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from djangouseragents.models import UserAgentRequestModel


@admin.register(UserAgentRequestModel)
class UserAgentRequestModelAdmin(admin.ModelAdmin):
    ordering = ('-created_dt',)
    permission_resource = "user_agent_request"

    list_display = (
        'uad',
        'created_dt',
        'status_display',
        'endpoint',
        'response_status_code_display',
        'rn',
        'rn_ph',
        'rn_24h',
    )

    search_fields = (
        'uad__id',
        'uad__user_id',
        'uad__ip',
        'uad__key',
    )
    list_filter = (
        'status',
        'response_status_code',
    )
    readonly_fields = (
        'created_dt',
    )

    fieldsets = (
        (_('Base Info'), {
            'fields': (
                'uad',
                ('method', 'endpoint', 'response_status_code'),
                'get',
                'headers',
                'cookies',
                ('rn', 'rn_ph', 'rn_24h'),
                ('status', 'status_color'),
                'created_dt',
            )
        }),
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    # Display status with background color
    def status_display(self, obj):
        return format_html(
            '<span style="background-color:{}; padding: 2px 6px; border-radius: 4px;">{}</span>',
            obj.status_color or '#fff',
            obj.status or 'N/A'
        )

    status_display.short_description = _('Status')

    # Color-coded response status code display
    def response_status_code_display(self, obj):
        color_map = {
            1: '#8093f1',  # 1xx
            2: '#72ddf7',  # 2xx
            3: '#fdc5f5',  # 3xx
            4: '#f7aef8',  # 4xx
            5: '#b388eb',  # 5xx
        }
        code = obj.response_status_code or 0
        base = code // 100
        bg_color = color_map.get(base, '#fff')
        return format_html(
            '<span style="background-color:{}; padding: 2px 6px; border-radius: 4px;">{}</span>',
            bg_color,
            code
        )

    response_status_code_display.short_description = _('HTTP Status Code')
