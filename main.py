import os
import sys
from argparse import ArgumentParser

import pychromecast
from zeroconf import Zeroconf

from resources.chromecast import ChromecastMonitor
from resources.log import getLogger
from resources.server import getPlexServer
from resources.settings import Settings
from resources.skipper import Skipper

if __name__ == '__main__':
    log = getLogger(__name__)

    parser = ArgumentParser(description="Plex Autoskip")
    parser.add_argument('-c', '--config', help='Specify an alternate configuration file location')
    args = vars(parser.parse_args())

    if args['config'] and os.path.exists(args['config']):
        settings = Settings(args['config'], logger=log)
    elif args['config'] and os.path.exists(os.path.join(os.path.dirname(sys.argv[0]), args['config'])):
        settings = Settings(os.path.join(os.path.dirname(sys.argv[0]), args['config']), logger=log)
    else:
        settings = Settings(logger=log)

    plex, sslopt = getPlexServer(settings, log)

    if plex:
        zconf = Zeroconf()
        cc_monitor = ChromecastMonitor(zconf, log)
        cc_listener = pychromecast.discovery.SimpleCastListener(
            add_callback=cc_monitor.add_callback,
            remove_callback=cc_monitor.remove_callback,
            update_callback=cc_monitor.update_callback,
        )
        cc_browser = pychromecast.discovery.CastBrowser(cc_listener, zconf)
        cc_monitor.add_browser(browser=cc_browser)
        cc_browser.start_discovery()
        skipper = Skipper(plex, settings, cc_monitor, log)
        skipper.start(sslopt=sslopt)
    else:
        log.error("Unable to establish Plex Server object via PlexAPI")
