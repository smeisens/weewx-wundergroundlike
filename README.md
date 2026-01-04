## WundergroundLike extension for weewx
This extension uploads archive data (only) in Weather Underground format to a specified remote server_url.   This is intended to permit users to send WU-like data to a custom server 'as well as' to the actual Weather Underground.   You only need this extension if you want to do both.

## Maintainer

This extension is maintained by **Sigi Meisenbichler** (@smeisens).

Originally created by Vince Skahan (@vinceskahan), derived from the WeeWX 
Weather Underground uploader by Tom Keffer.

Notes:
* Weather Underground 'rapidfire' to a custom url is 'not' supported here, and is actually disabled in this code
* this extension requires python3

#### For users who only want to upload to Weather Underground
You do not need this extension.  Use the [[Wunderground]] section in weewx.conf to use the uploader that comes with weewx.

#### For users who only want to upload to a custom WeatherUnderground-like site
You do not need this extension.  Add a custom server_url definition to the [[Wunderground] section in weewx.conf to use the uploader that comes with weewx.

#### For users who want to upload to Weather Underground 'and' also a site using the same kind of expected data
You need this extension.  See below for how to install and configure.

----

### Install via the extension installer

* if you are running a pip install, activate your venv first
* use the weewx extension installer to install this extension
   * For weewx v5 users - see [weectl](https://www.weewx.com/docs/5.2/utilities/weectl-extension/) for detailed instructions
   * For weewx v4 users - see [wee_extension](https://www.weewx.com/docs/4.10/utilities.htm\#wee_extension_utility) for detailed instructions
* edit the WundergroundLike stanza in weewx.conf to set your parameters
* restart weewx
* check your syslogs to make sure things are working

### Example installation

````
# weectl extension install https://github.com/smeisens/weewx-wundergroundlike/archive/refs/heads/main.zip
# weectl extension list
Using configuration file /etc/weewx/weewx.conf
Extension Name    Version   Description
wundergroundLike  1.0.0     Post to a custom server_url that uses Weather Underground formatting
# sudo systemctl restart weewx
````

### Configuration Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| enable | Yes | false | Enable/disable the uploader |
| station | Yes | - | Your station ID |
| password | Yes | - | Your station password |
| server_url | Yes | - | API endpoint URL |
| archive_post | No | true | Upload archive records |
| log_success | No | true | Log successful uploads |
| log_failure | No | true | Log failed uploads |

## Requirements

- WeeWX 4.0+ or 5.0+
- Python 3.7+

### Uninstall
Again, use the extension installer. For weewx v5 `weectl extension uninstall wundergroundLike`

## Support

- Issues: https://github.com/smeisens/weewx-wundergroundlike/issues
- WeeWX Forum: https://groups.google.com/g/weewx-user

## Credits

- **Current Maintainer:** Sigi Meisenbichler
- **Original Author:** Vince Skahan
- **Upstream:** Based on WeeWX restx.py by Tom Keffer

## License

GPL-3.0 - See LICENSE.txt
