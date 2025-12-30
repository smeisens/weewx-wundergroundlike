#-----------------------------------------------------------------
#         custom WundergroundLike uploader
#
#    Copyright (c) 2026 Sigi Meisenbichler <s.meisen@icloud.com>
#
#    Copyright (c) 2025 Vince Skahan <vinceskahan@gmail.com>
#
# This is derived almost verbatim from weewx 5.2.0 restx.py 
# which is:
#
#    Copyright (c) 2009-2024 Tom Keffer <tkeffer@gmail.com>
#
# The upstream code this is based on uses a LICENSE.txt file
# that is present here for reference.
#
#-----------------------------------------------------------------

import logging
import queue

import weewx.restx
from weeutil.config import search_up
from weeutil.weeutil import to_bool, to_sorted_string

log = logging.getLogger(__name__)

#-----------------------------------------------------------------
#         custom WundergroundLike uploader
#-----------------------------------------------------------------

class WundergroundLike(weewx.restx.StdWunderground):
    """Custom class to upload data to Weather Underground compatible servers.

    This class is designed for use with non-WU servers that use a WU-compatible API,
    such as HetWeerActueel.

    Differences from the weewx Wunderground class:
    - set default URLs to bogus values
    - supersede pws_url with mandatory 'server_url' from [[WundergroundLike]]
    - explicitly point to weewx.restx.foo for a few items
    - slightly different logging output to reflect this class's name
    - slightly different/added logging

    For additional information, see:
        https://support.wunderground.com/article/Knowledge/How-do-I-upload-data-from-my-personal-weather-station-to-Weather-Underground
        http://wiki.wunderground.com/index.php/PWS_-_Upload_Protocol
    """

    # bogus URLs to force use of mandatory 'server_url' in weewx.conf
    pws_url = 'http://please.set.server_url.in.weewx.conf'
    rf_url = 'http://please.set.server_url.in.weewx.conf'

    def __init__(self, engine, config_dict):
        super(WundergroundLike, self).__init__(engine, config_dict)

        # this uploader requires 'station', 'password' and 'server_url'
        _ambient_dict = weewx.restx.get_site_dict(
            config_dict, 'WundergroundLike', 'station', 'password', 'server_url')
        if _ambient_dict is None:
            log.error("WundergroundLike: Missing required configuration. "
                      "Please ensure [StdRESTful][[WundergroundLike]] is properly configured "
                      "with 'station', 'password', and 'server_url' in weewx.conf")
            return

        log.info("WundergroundLike: Configuration loaded: %s", _ambient_dict)

        # force rapidfire false
        _ambient_dict['rapidfire'] = False

        # server_url is already in _ambient_dict from get_site_dict
        log.debug("WundergroundLike server_url: %s", _ambient_dict.get('server_url'))

        # Get the manager dictionary:
        _manager_dict = weewx.manager.get_manager_dict_from_config(
            config_dict, 'wx_binding')

        # The default is to not do an archive post if a rapidfire post
        # has been specified, but this can be overridden
        do_rapidfire_post = to_bool(_ambient_dict.pop('rapidfire', False))
        do_archive_post = to_bool(_ambient_dict.pop('archive_post',
                                                     not do_rapidfire_post))
        if do_archive_post:
            # Don't use setdefault - server_url is already set from config
            self.archive_queue = queue.Queue()
            self.archive_thread = weewx.restx.AmbientThread(
                self.archive_queue,
                _manager_dict,
                protocol_name="WundergroundLike",
                **_ambient_dict)
            self.archive_thread.start()
            self.bind(weewx.NEW_ARCHIVE_RECORD, self.new_archive_record)
            log.info("WundergroundLike: Data for station %s will be posted",
                     _ambient_dict.get('station', 'UNKNOWN'))

        if do_rapidfire_post:
            _ambient_dict.setdefault('server_url', weewx.restx.StdWunderground.rf_url)
            _ambient_dict.setdefault('log_success', False)
            _ambient_dict.setdefault('log_failure', False)
            _ambient_dict.setdefault('max_backlog', 0)
            _ambient_dict.setdefault('max_tries', 1)
            _ambient_dict.setdefault('rtfreq', 2.5)
            self.cached_values = weewx.restx.CachedValues()
            self.loop_queue = queue.Queue()
            self.loop_thread = weewx.restx.AmbientLoopThread(
                self.loop_queue,
                _manager_dict,
                protocol_name="WundergroundLike-RF",
                **_ambient_dict)
            self.loop_thread.start()
            self.bind(weewx.NEW_LOOP_PACKET, self.new_loop_packet)
            log.info("WundergroundLike-RF: Data for station %s will be posted",
                     _ambient_dict.get('station', 'UNKNOWN'))

    def new_loop_packet(self, event):
        """Puts new LOOP packets in the loop queue"""
        # Because a packet is emitted before the archive record, it may be
        # this packet is a duplicate of the data sent with an archive record.
        # This filter will hold it back until the archive record has been sent.
        if self.cached_values.hit(event.packet):
            self.loop_queue.put(event.packet)

    def new_archive_record(self, event):
        """Puts new archive records in the archive queue"""
        self.archive_queue.put(event.record)
