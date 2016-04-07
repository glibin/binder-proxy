import logging

from tornado.options import define


define('port', default=9999, type=int, help='Port to run on')
define('host', default='127.0.0.1', help='Host to run on')
define('resolver', default='tornado.platform.caresresolver.CaresResolver', help='DNS resolver to use')
define('proxy_url', default='http://sandbox1.agate.upwork.com:32819', help='Proxied backend (sandbox/dev) url')
define('proxy_timeout', default=240, type=int, help='Proxy timeout')

define('log_level', default=logging.DEBUG, help='Log level')
define('log_format', default='[%(process)s] %(asctime)s %(levelname)s %(name)s: %(message)s')

define('static_path', default=None, help='Path to binders web directory')

define('config', default='config/local.cfg', help='Path to configuration file')
