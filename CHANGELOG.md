# Changelog

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
