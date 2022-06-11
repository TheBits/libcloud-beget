from libcloud.common.base import ConnectionUserAndKey, JsonResponse
from libcloud.common.types import InvalidCredsError
from libcloud.dns.base import DNSDriver, Zone
from libcloud.utils.py3 import httplib


class BegetResponse(JsonResponse):
    def success(self):
        self.object = self.parse_body()
        if self.object["status"] == "error":
            return False
        if self.object["status"] == "success":
            return True
        return super().success()

    def parse_body(self):
        if self.object:
            return self.object
        return super().parse_body()

    def parse_error(self):
        body = super().parse_error()

        # INFO: пример ответа:{ "status": "error", "error_text": "No such method", "error_code": "NO_SUCH_METHOD"}
        # https://beget.com/ru/kb/api/obshhij-princzip-raboty-s-api#obrabotka-otveta
        code = body["error_code"]
        if code == "AUTH_ERROR":
            raise InvalidCredsError(value=body["error_text"])

        # TODO: добавить ошибки
        # INCORRECT_REQUEST - ошибка, говорящая о некорректном запросе к API;
        # NO_SUCH_METHOD - указанного метода не существует.

        # TODO: ServiceUnavailableError и RateLimitReachedError

        return body["error_text"]


class BegetConnection(ConnectionUserAndKey):
    responseCls = BegetResponse
    host = "api.beget.com"

    def add_default_headers(self, headers) -> dict:
        headers["Accept"] = "application/json"
        return headers

    def add_default_params(self, params) -> dict:
        params["login"] = self.user_id
        params["passwd"] = self.key
        params["output_format"] = "json"
        return params


class BegetDNSDriver(DNSDriver):
    connectionCls = BegetConnection
    name = "Beget"
    website = "https://beget.com/"

    # TODO: RECORD_TYPE_MAP

    def iterate_zones(self):
        zones = []
        response = self.connection.request("api/domain/getList")
        for element in response.object["answer"]["result"]:
            zone_id = element.pop("id")
            domain = element.pop("fqdn")
            zone_type = "master"
            zone = Zone(
                id=zone_id,
                domain=domain,
                type=zone_type,
                ttl=None,
                driver=self,
                extra=element,
            )
            zones.append(zone)
        return zones

    def list_zones(self):
        return self.iterate_zones()
