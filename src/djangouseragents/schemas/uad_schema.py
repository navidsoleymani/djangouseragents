from datetime import datetime
from hashlib import md5

from django.http.request import HttpRequest
from pydantic import BaseModel

from djangouseragents.models import UserAgentDeviceModel


def _user_agent_device_key_creator(**kwargs):
    keys = [
        'user_id', 'is_mobile', 'is_tablet', 'is_touch_capable',
        'is_pc', 'is_bot', 'browser_family', 'browser_version',
        'os_family', 'os_version', 'device_family',
        'device_brand', 'device_model', 'ip'
    ]
    str_ = '-'.join(str(kwargs.get(k) or '') for k in keys)
    return md5(str_.encode('utf-8')).hexdigest()


def get_client_ip(request: HttpRequest) -> str | None:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class UADSchema(BaseModel):
    id: int | None = None
    user_id: str | None = None
    is_mobile: bool | None = None
    is_tablet: bool | None = None
    is_touch_capable: bool | None = None
    is_pc: bool | None = None
    is_bot: bool | None = None
    browser_family: str | None = None
    browser_version: str | None = None
    os_family: str | None = None
    os_version: str | None = None
    device_family: str | None = None
    device_brand: str | None = None
    device_model: str | None = None
    ip: str | None = None
    key: str | None = None
    created_dt: datetime | None = None

    @classmethod
    def from_model(cls, model: UserAgentDeviceModel) -> 'UADSchema':
        return cls(
            id=model.id,
            user_id=model.user_id,
            is_mobile=model.is_mobile,
            is_tablet=model.is_tablet,
            is_touch_capable=model.is_touch_capable,
            is_pc=model.is_pc,
            is_bot=model.is_bot,
            browser_family=model.browser_family,
            browser_version=model.browser_version,
            os_family=model.os_family,
            os_version=model.os_version,
            device_family=model.device_family,
            device_brand=model.device_brand,
            device_model=model.device_model,
            ip=model.ip,
            key=model.key,
            created_dt=model.created_dt,
        )

    @classmethod
    def from_request(cls, request: HttpRequest) -> 'UADSchema':
        kw = {
            'user_id': str(request.user.id) if (
                    hasattr(request, 'user') and request.user.is_authenticated) else None,
            'ip': get_client_ip(request),
        }

        if hasattr(request, 'user_agent'):
            ua = request.user_agent
            kw.update({
                'is_mobile': ua.is_mobile,
                'is_tablet': ua.is_tablet,
                'is_touch_capable': ua.is_touch_capable,
                'is_pc': ua.is_pc,
                'is_bot': ua.is_bot,
                'browser_family': ua.browser.family,
                'browser_version': ua.browser.version_string,
                'os_family': ua.os.family,
                'os_version': ua.os.version_string,
                'device_family': ua.device.family,
                'device_brand': ua.device.brand,
                'device_model': ua.device.model,
            })

        kw['key'] = _user_agent_device_key_creator(**{k: v or '' for k, v in kw.items()})
        return cls(**kw)

    def to_dict(self) -> dict:
        data = self.model_dump(exclude_none=True)

        if 'id' in data:
            data['id'] = str(data['id'])
        if 'user_id' in data:
            data['user_id'] = str(data['user_id'])

        if 'created_dt' in data:
            data['created_dt'] = (
                data['created_dt'].isoformat()
                if isinstance(data['created_dt'], datetime)
                else str(data['created_dt']))

        return data
