# Changelog

## [1.0.1] - 2026-10-21

### Fixed
- WundergroundLike no longer inherits from `StdWunderground` but from `StdRESTful`.
  In 1.0.0 the parent constructor processed `[[Wunderground]]` a second time, which
  - with only WU enabled: posted every record to Weather Underground twice
  - with WU and WundergroundLike enabled: posted every record to `server_url` twice
    and left the extra WU thread idle
- Disabling the uploader (`enable = false`) no longer logs an ERROR.
  Only the regular INFO "Posting not enabled" from weewx remains.

### Added
- WARNING (instead of a generic ERROR) when the uploader is enabled but
  `station`, `password` or `server_url` is missing or still `replace_me`;
  the message names the missing options
- WARNING if `rapidfire = true` is set (not supported, ignored)
- `[[[Essentials]]]` subsection is honored, like in the stock WU uploader
- Startup log line shows the target `server_url`

## [1.0.0] - 2026-01-04

### Changed by Sigi Meisenbichler
- Removed rapidfire
- Removed unused imports
- Removed unused attributs

## [0.2.0] - 2025-12-30

### Changed by Sigi Meisenbichler
- Complete refactoring of WundergroundLike uploader
- Removed unused imports (reduced from 26+ to 4 imports)
- Removed duplicate exception classes (use weewx.restx versions)
- Added proper error logging for missing configuration
- Added safe dictionary access to prevent KeyError crashes
- Removed unnecessary `essentials_dict` (uses AmbientThread defaults)
- Fixed rf_url reference for rapidfire mode
- Improved code maintainability and readability
- Code reduction: -25 lines (-19%)

### Fixed
- Missing error logging when configuration is incomplete
- Potential KeyError when 'station' parameter is missing
- Incorrect rf_url reference in rapidfire mode
- Missing queue import

## [0.1.0] - 2024-11-16

### Added by Vince Skahan
- Initial release
- Support for Weather Underground compatible APIs
- Derived from WeeWX StdWunderground uploader
