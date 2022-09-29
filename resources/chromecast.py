import logging
from uuid import UUID

import pychromecast
from pychromecast.controllers.plex import PlexController
from this import d
from zeroconf import Zeroconf


class ChromecastMonitor:
    # The callbacks are called from a thread different from the main thread.

    def __init__(self, zconf: Zeroconf, logger: logging.Logger = None):
        self.log = logger or logging.getLogger(__name__)
        self._browser = None
        self._zconf = zconf
        self._chromecasts: dict[UUID, pychromecast.Chromecast] = {}

    def add_browser(self, browser: pychromecast.CastBrowser):
        self._browser = browser

    def get_chromecast_by_ip(self, ip: str) -> pychromecast.Chromecast:
        for cc in self._chromecasts.values():
            if cc.socket_client.host == ip:
                return cc
        self.log.debug(f"Discovered Chromecasts: {self._chromecasts}")
        raise ValueError(f"could not find Chromecast with address {ip}")

    def add_callback(self, uuid: UUID, name: str):
        chromecast = pychromecast.get_chromecast_from_cast_info(
            self._browser.devices[uuid], self._zconf
        )
        chromecast.wait()
        self._chromecasts[uuid] = chromecast
        self.log.debug(f"Discovered new Chromecast: {chromecast}")

    def update_callback(self, uuid: UUID, name: str):
        # No-op.
        pass

    def remove_callback(self, uuid: UUID, name: str, service):
        chromecast = self._chromecasts.pop(uuid)
        self.log.debug(f"Removed discovered Chromecast: {chromecast}")

class ChromecastAdapter:
    def __init__(self, plex_ctrl: PlexController):
        self._plex_ctrl = plex_ctrl

    def seekTo(self, offset_ms: int):
        self._plex_ctrl.seek(offset_ms / 1000)

    def setVolume(self, volume: int):
        self._plex_ctrl.set_volume(volume)

    def playMedia(self, media):
        self._plex_ctrl.play_media(media=media)

    def skipNext(self):
        self._plex_ctrl.next()
    
    def stop(self):
        self._plex_ctrl.stop()
