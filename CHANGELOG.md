# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 25-1-2026 - Marie Borisová
### Added
- HTML file for web display
- Registry design pattern for command parsing and creation
- Client being automatically disconnected after too many frequent invalid command inputs
### Changed
- Command parser proxy method
- ```web_monitor.py``` moved to ```ui``` directory
### Fixed
- Not being able to shutdown server through the web UI

## 25-1-2026 - Lukáš Eger
### Added
- Config lib added
- Proxy added
- Web monitoring class
### Changed
- Added AW command to command parser
- Web monitor fixed

## 24-1-2026 - Marie Borisová
### Added
- Class for web monitoring logic
- Class for AW command
- Implemented the AW command in the command parser
- Class for AD command
- Implemented the AD command in the command parser

## 22-1-2026 - Marie Borisová 
### Added
- Class for AR command
- Implemented the AR command in the command parser
- CHANGELOG file
- Class for AB command
- Implemented the AB command in the command parser

## 22-1-2026 - Lukáš Eger
### Added
- AC command
- BA command
- BN command
### Fixed
- Bank persistence

## 21-1-2026 - Lukáš Eger
### Added
- Class for the bank
- The bank object

## 19-1-2026 - Marie Borisová
### Changed
- Method for getting the IP address of the local machine

## 18-1-2026 - Marie Borisová
### Added
- Basic server logic for TCP socket connection
- Command interface for implementing various commands
- Class for BC command
- Implemented the BC command in the command parser
- Class for logging
- Command parser
- Utils file for getting device IP address
- README file

### [Changed]
- Timeout duration
- Timeout error message
