#!/usr/bin/env python3
"""
Receipt Generator - Generate various types of receipts

Usage:
    python generate.py <type>

Available types:
    fuel       - Generate fuel receipts
    driver     - Generate driver salary receipts
    internet   - Generate internet receipt
    education  - Generate education receipts (dynamic multi-page PDF)
"""

import sys
from pathlib import Path

import yaml

from generators import GENERATOR_REGISTRY


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

    # Get generator class from registry
    generator_class = GENERATOR_REGISTRY.get(receipt_type)

    if not generator_class:
        print(f"Error: Unknown receipt type '{receipt_type}'")
        print(f"\nValid options: {', '.join(sorted(GENERATOR_REGISTRY.keys()))}")
        sys.exit(1)

    # Generate receipts
    try:
        generator_class.print_header()
        generator = generator_class(config[receipt_type])
        generator.generate()

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
