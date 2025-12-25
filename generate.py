#!/usr/bin/env python3
"""
Receipt Generator - Generate fuel and driver salary receipts

Usage:
    python generate.py fuel      # Generate fuel receipts
    python generate.py driver    # Generate driver salary receipts
"""

import sys
from pathlib import Path

import yaml

from generators import DriverGenerator, FuelGenerator


def load_config(config_file='config.yaml'):
    """
    Load configuration from YAML file

    Args:
        config_file: Path to configuration file

    Returns:
        Dictionary containing configuration

    Raises:
        SystemExit: If config file not found
    """
    config_path = Path(config_file)

    if not config_path.exists():
        print(f"Error: {config_file} not found!")
        print("\nPlease create a config file:")
        print("  1. Copy config.example.yaml to config.yaml")
        print("  2. Update the values with your information")
        print("\n  cp config.example.yaml config.yaml")
        sys.exit(1)

    with open(config_path) as f:
        return yaml.safe_load(f)


def main():
    """Main entry point"""
    # Check command line arguments
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    receipt_type = sys.argv[1].lower()

    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)

    # Generate receipts based on type
    try:
        if receipt_type == 'fuel':
            print("=" * 60)
            print("FUEL RECEIPT GENERATOR")
            print("=" * 60)
            generator = FuelGenerator(config['fuel'])
            generator.generate()

        elif receipt_type == 'driver':
            print("=" * 60)
            print("DRIVER SALARY RECEIPT GENERATOR")
            print("=" * 60)
            generator = DriverGenerator(config['driver'])
            generator.generate()

        else:
            print(f"Error: Unknown receipt type '{receipt_type}'")
            print("\nValid options: fuel, driver")
            sys.exit(1)

    except KeyError as e:
        print(f"Error: Missing configuration key: {e}")
        print("Please check your config.yaml file")
        sys.exit(1)
    except Exception as e:
        print(f"Error generating receipts: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
