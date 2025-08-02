# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Setup dependencies**: `./scripts/setup.sh` or `pip3 install -r requirements.txt`
- **Format code**: `./scripts/format.sh` or `python3 -m ruff format .`
- **Run Home Assistant with this integration**: `./scripts/run.sh` (sets PYTHONPATH and runs `hass --config ./config --debug`)
- **Test configuration**: Use the config in `/config/configuration.yaml`

## Project Architecture

This is a Home Assistant custom integration for Smart Meter Gateways (SMGW) that supports multiple vendors through a pluggable gateway architecture.

### Core Components

- **Domain**: `ppc_smgw` - Main integration domain
- **Platforms**: Button and Sensor entities
- **Gateway Architecture**: Vendor-agnostic interface with specific implementations

### Gateway System

The integration uses a factory pattern with vendor-specific gateway implementations:

- **Base Gateway**: `custom_components/ppc_smgw/gateways/gateway.py` - Abstract interface
- **PPC SMGW**: `custom_components/ppc_smgw/gateways/ppc/ppc_smgw.py` - PPC implementation  
- **Theben Conexa**: `custom_components/ppc_smgw/gateways/theben/theben.py` - Theben implementation
- **Vendor Enum**: `custom_components/ppc_smgw/gateways/vendors.py` - Defines supported vendors

Gateway selection happens in `__init__.py:59-84` using pattern matching on the `Vendor` enum.

### Data Flow

1. **Coordinator**: `SMGwDataUpdateCoordinator` manages data updates using Home Assistant's DataUpdateCoordinator pattern
2. **Config Entry**: Uses `ConfigEntry[Data]` type annotation for runtime data storage
3. **Entity Creation**: Sensors and buttons are dynamically created based on gateway capabilities
4. **Migration**: Version-based config migration system (see `async_migrate_entry`)

### Configuration

- **Config Flow**: `config_flow.py` handles UI-based setup
- **Constants**: `const.py` defines sensor types, default values, and entity descriptions
- **Manifest**: `manifest.json` specifies dependencies (beautifulsoup4) and metadata

### Key Patterns

- Uses Home Assistant's modern async patterns throughout
- Implements proper device and entity registry integration
- Supports options flow for runtime configuration changes
- Uses structured logging with domain-specific logger
- SSL verification disabled for local gateway connections (`verify_ssl=False`)

### Entity Structure

- **Sensors**: Energy import/export totals (1-0:1.8.0, 1-0:2.8.0) and last update timestamp
- **Buttons**: Gateway restart functionality
- **Device Class**: Proper Home Assistant device classes for energy monitoring

### Development Notes

- Integration follows HACS compatibility standards
- Uses ruff for code formatting
- Supports debug mode via config entry options
- Custom reverse proxy available (`reverse_proxy.go`) for development/testing