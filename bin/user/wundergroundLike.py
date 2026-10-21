#-----------------------------------------------------------------
#         custom WundergroundLike uploader v1.0.1
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

import weewx
import weewx.manager
import weewx.restx
from weeutil.config import search_up
from weeutil.weeutil import to_bool

log = logging.getLogger(__name__)

SECTION = 'WundergroundLike'
REQUIRED = ('station', 'password', 'server_url')

#-----------------------------------------------------------------
#         custom WundergroundLike uploader
#-----------------------------------------------------------------

class WundergroundLike(weewx.restx.StdRESTful):
    """Upload archive records to a Weather Underground compatible server.

    Intended for non-WU servers that accept the WU PWS protocol, so that
    data can be sent to such a server *in addition to* the real Weather
    Underground (handled by the stock weewx.restx.StdWunderground).

    This service is fully independent of [[Wunderground]]:
    - it derives from StdRESTful, NOT from StdWunderground, so it never
      reads the [[Wunderground]] section and never starts a second WU
      uploader (which caused duplicate posts in v1.0.0)
    - it owns its own queue and thread

    Notes:
    - 'server_url' is mandatory
    - rapidfire is not supported (archive post only)
    """

    def __init__(self, engine, config_dict):
        super().__init__(engine, config_dict)

        _ambient_dict = weewx.restx.get_site_dict(config_dict, SECTION, *REQUIRED)
        if _ambient_dict is None:
            # get_site_dict() already logged "No config info" or
            # "Posting not enabled" at INFO level. Only if the service is
            # enabled but incomplete is there something worth a warning.
            _warn_if_enabled_but_incomplete(config_dict)
            return

        _section = config_dict['StdRESTful'][SECTION]
        _essentials_dict = search_up(_section, 'Essentials', {})

        # Get the manager dictionary:
        _manager_dict = weewx.manager.get_manager_dict_from_config(
            config_dict, 'wx_binding')

        # Rapidfire is not supported; archive posting is the only mode.
        if to_bool(_ambient_dict.pop('rapidfire', False)):
            log.warning("%s: 'rapidfire' is not supported and will be ignored", SECTION)
        do_archive_post = to_bool(_ambient_dict.pop('archive_post', True))

        if not do_archive_post:
            log.info("%s: archive_post = False, nothing to do", SECTION)
            return

        self.archive_queue = queue.Queue()
        self.archive_thread = weewx.restx.AmbientThread(
            self.archive_queue,
            _manager_dict,
            protocol_name=SECTION,
            essentials=_essentials_dict,
            **_ambient_dict)
        self.archive_thread.start()
        self.bind(weewx.NEW_ARCHIVE_RECORD, self.new_archive_record)
        log.info("%s: Data for station %s will be posted to %s",
                 SECTION, _ambient_dict['station'], _ambient_dict['server_url'])

    def new_archive_record(self, event):
        """Puts new archive records in the archive queue"""
        self.archive_queue.put(event.record)


def _warn_if_enabled_but_incomplete(config_dict):
    """Log a warning if the section is enabled but a required option is
    missing or still 'replace_me'. Disabled or absent sections stay quiet."""
    try:
        section = config_dict['StdRESTful'][SECTION]
    except KeyError:
        return
    if not to_bool(section.get('enable', True)):
        return
    missing = [opt for opt in REQUIRED
               if section.get(opt) in (None, '', 'replace_me')]
    if missing:
        log.warning("%s: enabled, but required option(s) missing in "
                    "[StdRESTful][[%s]]: %s. Nothing will be posted.",
                    SECTION, SECTION, ", ".join(missing))
