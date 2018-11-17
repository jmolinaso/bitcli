
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version

import json, urllib3

VERSION_BANNER = """
Show prices in the console from Bitpanda %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'Show prices in the console from Bitpanda'

        # text displayed at the bottom of --help output
        epilog = 'Usage: bitcli prices --fiat EUR'

        # controller level arguments. ex: 'bitcli --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""
        self.app.args.print_help()


    @ex(
        help='List the current prices from Bitpanda',
        arguments=[
            ( [ '-f', '--fiat' ],
              { 'help' : 'Only options [EUR|USD|CHF|GBP] defaults on EUR',
                'action'  : 'store',
                'dest' : 'fiat' } ),
        ],
    )
    def prices(self):
        """Example sub-command."""

        http = urllib3.PoolManager()

        url = 'https://api.bitpanda.com/v1/ticker'
        response = http.request('GET', url)
        self.app.log.debug('Code %s' % response.status)
        self.app.log.debug('Data got %s' % response.data)

        ret_json = json.loads(response.data)

        data = {
            'results' : ret_json.items(),
            'fiat' : '€'
        }

        options = {
            'EUR': '€',
            'USD': '$',
            'CHF': 'CHF',
            'GBP': '£',
        }        
        if self.app.pargs.fiat in options.keys():
            data['fiat'] = options[self.app.pargs.fiat]
        else:
            self.app.log.info('No FIAT or unknown, showing values in EUR')

        self.app.render(data, 'prices.jinja2')
