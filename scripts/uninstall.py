#!/usr/bin/env python3
"""
pylumo Uninstallation Script

Removes pylumo and its dependencies including proton-client.

Usage:
    python3 uninstall.py              # Uninstall everything
    python3 uninstall.py --keep-deps  # Keep dependencies, only remove pylumo

Alternative (using uv directly):
    uv pip uninstall pylumo proton-client

For more information, see INSTALL.md
"""
import argparse
import subprocess
import sys

def uninstall_pylumo():
    """Uninstall pylumo package"""
    print("=" * 60)
    print("Uninstalling pylumo...")
    print("=" * 60)
    
    result = subprocess.run([
        "uv", "pip", "uninstall", "pylumo"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error uninstalling pylumo: {result.stderr}")
        return False
    
    print("✓ pylumo uninstalled successfully\n")
    return True

def uninstall_proton_client():
    """Uninstall proton-client package"""
    print("=" * 60)
    print("Uninstalling proton-client...")
    print("=" * 60)
    
    result = subprocess.run([
        "uv", "pip", "uninstall", "proton-client"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        # It's okay if proton-client isn't installed
        if "not installed" in result.stderr.lower():
            print("proton-client was not installed\n")
            return True
        print(f"Error uninstalling proton-client: {result.stderr}")
        return False
    
    print("✓ proton-client uninstalled successfully\n")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Uninstall pylumo and its dependencies"
    )
    parser.add_argument(
        "--keep-deps",
        action="store_true",
        help="Keep dependencies (only uninstall pylumo)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("pylumo Uninstallation Script")
    print("=" * 60 + "\n")
    
    success = True
    
    # Always uninstall pylumo
    if not uninstall_pylumo():
        success = False
    
    # Uninstall proton-client unless --keep-deps is specified
    if not args.keep_deps:
        if not uninstall_proton_client():
            success = False
    else:
        print("Keeping dependencies as requested\n")
    
    print("=" * 60)
    if success:
        print("Uninstallation Complete!")
        print("=" * 60)
        print("\nTo reinstall, run:")
        print("  make install-tui\nor")
        print("  python3 scripts/install.py --tui")
    else:
        print("Uninstallation completed with errors")
        print("=" * 60)
        sys.exit(1)
    
    print("\n")

if __name__ == "__main__":
    main()
