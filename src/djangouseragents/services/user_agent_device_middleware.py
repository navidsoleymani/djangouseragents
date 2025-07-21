from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest, HttpResponse

from djangouseragents.models import UserAgentDeviceModel, UserAgentRequestModel
from djangouseragents.schemas import UADSchema


class UserAgentDeviceMiddleware(MiddlewareMixin):
    """
    Middleware to detect and persist user agent and device information.
    It attaches UADSchema (parsed info) and UAD object (DB model) to the request,
    sets a cookie for identification, and logs the request metadata.
    """

    def process_request(self, request: HttpRequest) -> None:
        """
        Parse user-agent data from the request and attach it to the request object.
        """
        self._init_user_agent_data(request)
        setattr(request, 'uad', self.uad_schema)  # UADSchema instance
        setattr(request, 'uad_obj', self.uad_obj)  # UserAgentDeviceModel instance

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        """
        Store a cookie for UAD identification and log the request metadata.
        """
        # Ensure request is parsed (in case process_request wasn't explicitly called)
        self._init_user_agent_data(request)

        if hasattr(request, 'uad') and request.uad.key:
            response.set_cookie(
                key='UAD',
                value=request.uad.key,
                max_age=60 * 60 * 24 * 365,  # 1 year
                httponly=False,
                secure=False
            )

        self._log_user_agent_request(request, response)
        return response

    def _init_user_agent_data(self, request: HttpRequest) -> None:
        """
        Get or create a UserAgentDeviceModel instance based on request and cookie.
        """
        cookie_key = request.COOKIES.get('UAD')
        user_id = request.user.id if hasattr(request, 'user') and request.user.is_authenticated else None

        # Attempt to find existing UAD record
        obj = self._get_existing_uad(cookie_key, user_id)

        # Fallback to creation if not found
        if not obj:
            schema = UADSchema.from_request(request)
            obj = self._get_or_create_uad(schema)
        else:
            schema = UADSchema.from_model(obj)

        self.uad_schema = schema
        self.uad_obj = obj

    def _get_existing_uad(self, key: str | None, user_id: int | None) -> UserAgentDeviceModel | None:
        """
        Attempt to retrieve an existing UAD record from the database.
        Only return it if it's linked to a user or no user is expected.
        """
        if not key:
            return None
        try:
            obj = UserAgentDeviceModel.objects.get(key=key)
            if obj.user_id is None and user_id is not None:
                return None
            return obj
        except UserAgentDeviceModel.DoesNotExist:
            return None

    def _get_or_create_uad(self, schema: UADSchema) -> UserAgentDeviceModel:
        """
        Retrieve an existing UAD record by key or create a new one.
        """
        try:
            return UserAgentDeviceModel.objects.get(key=schema.key)
        except UserAgentDeviceModel.DoesNotExist:
            return UserAgentDeviceModel.objects.create(**schema.to_dict())
        except Exception as e:
            raise e

    def _log_user_agent_request(self, request: HttpRequest, response: HttpResponse) -> None:
        """
        Create a record in UserAgentRequestModel to log the request info.
        """
        try:
            UserAgentRequestModel.objects.create(
                uad=request.uad_obj,
                endpoint=request.path,
                response_status_code=response.status_code,
                method=request.method,
                get=dict(request.GET),
                headers=dict(request.headers),
                cookies=dict(request.COOKIES),
            )
        except Exception:
            # Silently fail to avoid interrupting the response cycle
            pass
