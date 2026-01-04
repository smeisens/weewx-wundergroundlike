
# installer derived from the weewx Belchertown skin installer
# https://raw.githubusercontent.com/poblabs/weewx-belchertown/master/install.py
# which was Copyright Pat O'Brien, with re-fomatting from a PR by Vince Skahan 

import configobj
from setup import ExtensionInstaller

# Python 3
from io import StringIO

#-------- extension info -----------

VERSION      = "1.0.0"
NAME         = 'wundergroundLike'
DESCRIPTION  = 'Post to a custom server_url that uses Weather Underground formatting'
AUTHOR       = "Sigi Meisenbichler"
AUTHOR_EMAIL = "s.meisen@icloud.com"

#-------- main loader -----------

def loader():
    return WundergroundLikeInstaller()

class WundergroundLikeInstaller(ExtensionInstaller):
    def __init__(self):
        super(WundergroundLikeInstaller, self).__init__(
            version=VERSION,
            name=NAME,
            description=DESCRIPTION,
            author=AUTHOR,
            author_email=AUTHOR_EMAIL,
            config=config_dict,
            files=files_dict,
            restful_services=restful_dict
        )

#----------------------------------
#         config stanza
#----------------------------------

extension_config = """

[StdRESTful]

    [[WundergroundLike]]
        # This section is for configuring posts to a site that expects
        # Weather Underground formatted data. This typically is only
        # needed if you post to the actual Weather Underground 'and'
        # you 'also' want to post similarly to a different site.

        # Note - the WU "Rapidfire" protocol is 'disabled' in this extension
        # but other optional parameters supported by weewx-5.2.0 'should' work.
        # Please consult the weewx documentation for details.

        # To enable this uploader, set enable = True below and specify your
        # appropriate values for station, password, and server_url

        enable = false
        station = replace_me
        password = replace_me
        server_url = replace_me

"""
config_dict = configobj.ConfigObj(StringIO(extension_config))

#----------------------------------
#  files and services stanzas
#----------------------------------
files=[('bin/user', ['bin/user/wundergroundLike.py'])]
files_dict = files

restful_services = ['user.wundergroundLike.WundergroundLike']
restful_dict = restful_services

#---------------------------------
#          done
#---------------------------------
