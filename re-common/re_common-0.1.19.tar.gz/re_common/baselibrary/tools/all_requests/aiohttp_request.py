import aiohttp

from re_common.baselibrary.tools.all_requests.mrequest import MRequest
from re_common.baselibrary.utils.baseurl import BaseUrl
from re_common.baselibrary.utils.core.mdeprecated import aiohttp_try_except
from re_common.baselibrary.utils.core.mlamada import html_strip
from re_common.baselibrary.utils.core.requests_core import set_proxy_aio


class AioHttpRequest(MRequest):

    def __init__(self, logger=None):
        if logger is None:
            from re_common.baselibrary import MLogger
            logger = MLogger().streamlogger
        super().__init__(logger=logger)
        self.kwargs = {}

    def builder(self):
        if self.refer:
            self.header["refer"] = self.refer
        self.kwargs["headers"] = self.header
        self.kwargs["proxy"] = set_proxy_aio(self.proxy)
        if BaseUrl.urlScheme(self.url) == "https":
            self.kwargs["verify_ssl"] = False
        self.kwargs["timeout"] = self.timeout
        self.kwargs["allow_redirects"] = self.allow_redirects
        self.kwargs["params"] = self.params
        return self

    async def set_resp(self, resp):
        self.resp = resp
        self.set_status_code(resp.status)
        self.html = await resp.text()
        self.html = html_strip(self.html)

    @aiohttp_try_except
    async def get(self):
        if self.sn is None:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=self.url, **self.kwargs) as resp:
                    await self.set_resp(resp)
        else:
            async with self.sn.get(url=self.url, **self.kwargs) as resp:
                await self.set_resp(resp)
        return True, {"code": self.status_code, "msg": ""}

    @aiohttp_try_except
    async def post(self):
        if self.sn is None:
            async with aiohttp.ClientSession() as session:
                async with session.post(url=self.url, data=self.data, **self.kwargs) as resp:
                    await self.set_resp(resp)
        else:
            async with self.sn.post(url=self.url, data=self.data, **self.kwargs) as resp:
                await self.set_resp(resp)
        return True, {"code": self.status_code, "msg": ""}

    def all_middlerwares(self):
        bools, dicts = True, {}
        for item in self.middler_list:
            bools, dicts = item()
            if not bools:
                return bools, dicts
        return bools, dicts

    async def run(self, moths="get"):
        self.builder()
        self.on_request_start()
        if moths == MRequest.GET:
            bools, dicts = await self.get()
        elif moths == MRequest.POST:
            bools, dicts = await self.post()
        else:
            bools, dicts = False, {}
        self.on_request_end()
        if bools:
            return self.all_middlerwares()
        return bools, dicts
