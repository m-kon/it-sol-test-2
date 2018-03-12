import json
from multidimensional_urlencode import urlencode
from requests import adapters, get, post, exceptions

class Bitrix24Hook(object):
    """Class for working with Bitrix24 cloud API hooks"""
    _hook_endpoint_template = 'https://{domain}/rest/1/{hook_code}/'
#    _timeout = 60

    # @property to make calculated property read-only 
    @property
    def _resolve_hook_endpoint(self):
        return self._hook_endpoint_template.format(domain=self.domain, hook_code=self.hook_code)
    
    def __init__(self, domain, hook_code, hook_endpoint=None):
        """Create Bitrix24 API hook object
        :param domain: str Bitrix24 domain
        :param auth_code: str Hook auth code
        :param method: str Method to use in url
        """
        self.domain = domain
        self.hook_code = hook_code
        self.hook_endpoint = hook_endpoint

    def _resolve_call_url(self, method, endpoint=None):
        return '{endpoint}{method}.json'.format(
            endpoint=endpoint or self._resolve_hook_endpoint,
            method=method
        )
            
    def call_method(self, method, json=None):
        """Call Bitrix24 API method
        :param method: API method name
        :param json: API parameters as json
        :return: Call result
        """
        if method is None:
            raise Exception('Empty Method')

        url = self._resolve_call_url(method)            
        r = {}

        try:
#            r = post(url, json=json, timeout=self.timeout)
            r = post(url, json=json)
        except exceptions.RequestException:
            r = None
        result = self.resolve_response(r)
        return result

    def call_batch(self, calls, halt_on_error=False):
        """Groups many single methods into request
        :param calls: dict Sub-methods with params
        :param halt_on_error: bool Halt on error
        :return: dict Decoded response text
        """
        result = self.call_method('batch', {
            'cmd': self.prepare_batch(calls),
            'halt': halt_on_error
        })
        return result
        
    def resolve_response(self, response):
        try:
            result = json.loads(response.text)
        except AttributeError:
            result = None
        except TypeError:
            result = None
        return result

    def prepare_batch(self, calls):
        """Prepare batch of calls.
        call template ~= {
        'method': dotted_method_name,
        'params': params_dict
        }
        :param calls: list List of calls
        :return: dict Batch of calls
        """
        commands = {}
        for name, call in calls.items():
            command = '{}?{}'.format(call['method'], urlencode(call['params']))
            commands[name] = command
        return commands
