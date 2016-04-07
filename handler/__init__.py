from tornado.options import options
from tortik.page import RequestHandler

try:
    import urlparse  # py2
except ImportError:
    import urllib.parse as urlparse  # py3


class PageHandler(RequestHandler):
    """Base handler"""
    preprocessors = []
    postprocessors = []

    def make_request(self, *args, **kwargs):
        kwargs['validate_cert'] = False

        return RequestHandler.make_request(self, *args, **kwargs)


class ProxyHandler(PageHandler):
    """Proxy handler"""
    postprocessors = []

    proxy_request_name = 'proxy-request'
    exclude_headers = {'Connection', 'Keep-Alive', 'Content-Length', 'Content-Encoding', 'Proxy-Authenticate',
                       'Proxy-Authorization', 'TE', 'Trailers', 'Transfer-Encoding', 'Upgrade'}

    def check_xsrf_cookie(self):
        return

    def _get_proxy_headers(self):
        """Getting headers to pass to proxy

        By default, proxies all headers from request
        """
        headers = self.request.headers
        parsed_url = urlparse.urlsplit(self._get_proxy_url())
        headers['Host'] = parsed_url.netloc
        return headers

    def _get_proxy_url(self):
        """Getting base url part (``http://example.com``) for proxy request.

        By default takes value from ``options.proxy_url``
        """
        return options.proxy_url

    def _get_proxy_uri(self):
        """Get request uri and parameters (``/some/path?a=1``) for proxy request.

        By default, takes data from ``request.uri``
        """
        return self.request.uri

    def proxy(self, method='GET', callback=None, data=''):
        """Method for request proxy

        :param method: HTTP-method of proxyed request
        :param callback: function to be called after proxy request would be finished
        :param data: request parameters or body
        """
        self.fetch_requests(self.make_request(
            name=self.proxy_request_name,
            method=method,
            full_url=self._get_proxy_url() + self._get_proxy_uri(),
            headers=self._get_proxy_headers(),
            follow_redirects=False,
            data=data if (data or method in ['GET', 'DELETE']) else self.request.body,
            connect_timeout=options.proxy_timeout,
            request_timeout=options.proxy_timeout
        ), callback=callback if callback is not None else self.handle_response)

    def handle_response(self):
        response = self.responses.get(self.proxy_request_name)
        redirected = self.handle_redirects(response)
        if not redirected:
            self.set_status(response.code)
            self.complete(response.body)

    def handle_redirects(self, response):
        for header in response.headers:
            if header == 'Set-Cookie':  # cookies could come in multiple headers
                values = response.headers.get_list(header)
                for value in values:
                    self.add_header(header, value)
                continue
            if header not in self.exclude_headers:
                self.set_header(header, response.headers.get(header))

        if response.code in (301, 302, 303, 307):
            self.redirect(response.headers.get('Location') or '/')
            return True
        elif response.code == 304:
            self.set_status(response.code)
            self.complete()
            return True
        elif response.code in (504, 599) and not options.debug:
            self.set_status(500)
            self.complete()
            return True

        return False

    def get(self, *args, **kwargs):
        self.proxy()

    def post(self, *args, **kwargs):
        self.proxy(method='POST')

    def put(self, *args, **kwargs):
        self.proxy(method='PUT')

    def delete(self, *args, **kwargs):
        self.proxy(method='DELETE')
