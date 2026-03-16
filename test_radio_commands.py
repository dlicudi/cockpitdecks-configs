"""Test script to verify all radio datarefs and flip commands for the SR22 radio page.

Tests:
1. All datarefs used in annunciators are readable
2. All flip commands work (frequencies swap correctly)
3. Encoder tuning commands are valid

Usage:
    python test_radio_commands.py [host] [port]
    Default: host=127.0.0.1 port=8086
"""
import sys
import time

import xpwebapi

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8086

# All datarefs used in the radio page annunciators
DATAREFS = [
    # COM1
    "sim/cockpit2/radios/actuators/com1_frequency_hz_833",
    "sim/cockpit2/radios/actuators/com1_standby_frequency_hz_833",
    # COM2
    "sim/cockpit2/radios/actuators/com2_frequency_hz_833",
    "sim/cockpit2/radios/actuators/com2_standby_frequency_hz_833",
    # NAV1
    "sim/cockpit/radios/nav1_freq_hz",
    "sim/cockpit/radios/nav1_stdby_freq_hz",
    # NAV2
    "sim/cockpit/radios/nav2_freq_hz",
    "sim/cockpit/radios/nav2_stdby_freq_hz",
    # ADF
    "sim/cockpit/radios/adf1_freq_hz",
    "sim/cockpit/radios/adf1_stdby_freq_hz",
]

# Flip commands and their associated dataref pairs (active, standby)
FLIP_COMMANDS = {
    "sim/GPS/g1000n1_com_ff": (
        "sim/cockpit2/radios/actuators/com1_frequency_hz_833",
        "sim/cockpit2/radios/actuators/com1_standby_frequency_hz_833",
    ),
    "sim/radios/com2_standy_flip": (
        "sim/cockpit2/radios/actuators/com2_frequency_hz_833",
        "sim/cockpit2/radios/actuators/com2_standby_frequency_hz_833",
    ),
    "sim/GPS/g1000n3_nav_ff": (
        "sim/cockpit/radios/nav1_freq_hz",
        "sim/cockpit/radios/nav1_stdby_freq_hz",
    ),
    "sim/radios/nav2_standy_flip": (
        "sim/cockpit/radios/nav2_freq_hz",
        "sim/cockpit/radios/nav2_stdby_freq_hz",
    ),
    "sim/radios/adf1_standy_flip": (
        "sim/cockpit/radios/adf1_freq_hz",
        "sim/cockpit/radios/adf1_stdby_freq_hz",
    ),
}

# Encoder tuning commands (from encoders_radio.yaml)
ENCODER_COMMANDS = [
    # COM1 (e0)
    "sim/radios/stby_com1_coarse_down",
    "sim/radios/stby_com1_coarse_up",
    "sim/radios/stby_com1_fine_down",
    "sim/radios/stby_com1_fine_up",
    # NAV1 (e1)
    "sim/radios/stby_nav1_coarse_down",
    "sim/radios/stby_nav1_coarse_up",
    "sim/radios/stby_nav1_fine_down",
    "sim/radios/stby_nav1_fine_up",
    # ADF (e2)
    "sim/radios/stby_adf1_hundreds_thous_down",
    "sim/radios/stby_adf1_hundreds_thous_up",
    "sim/radios/stby_adf1_4dig_hundreds_down",
    "sim/radios/stby_adf1_4dig_hundreds_up",
    # COM2 (e3)
    "sim/radios/stby_com2_coarse_down",
    "sim/radios/stby_com2_coarse_up",
    "sim/radios/stby_com2_fine_down",
    "sim/radios/stby_com2_fine_up",
    # NAV2 (e4)
    "sim/radios/stby_nav2_coarse_down",
    "sim/radios/stby_nav2_coarse_up",
    "sim/radios/stby_nav2_fine_down",
    "sim/radios/stby_nav2_fine_up",
]


def main():
    api = xpwebapi.rest_api(host=HOST, port=PORT, api_version="v2")
    print(f"Connected to X-Plane at {HOST}:{PORT}")
    print(f"API capabilities: {api.capabilities}\n")

    # Test 1: Read all datarefs
    print("=" * 60)
    print("TEST 1: Dataref readability")
    print("=" * 60)
    for ref_path in DATAREFS:
        try:
            dr = api.dataref(ref_path)
            val = dr.value
            print(f"  OK   {ref_path} = {val}")
        except Exception as e:
            print(f"  FAIL {ref_path}: {e}")
    print()

    # Test 2: Flip commands
    print("=" * 60)
    print("TEST 2: Flip commands (each flipped twice to restore state)")
    print("=" * 60)
    for cmd_name, (active_ref, standby_ref) in FLIP_COMMANDS.items():
        active_before = api.dataref(active_ref).value
        standby_before = api.dataref(standby_ref).value
        print(f"\n  --- {cmd_name} ---")
        print(f"  Before: active={active_before}, standby={standby_before}")

        try:
            cmd = api.command(cmd_name)
            cmd.execute()
            print(f"  Command sent OK")
        except Exception as e:
            print(f"  FAIL to send command: {e}")
            continue

        time.sleep(0.5)

        active_after = api.dataref(active_ref).value
        standby_after = api.dataref(standby_ref).value
        print(f"  After:  active={active_after}, standby={standby_after}")

        if active_before == standby_after and standby_before == active_after:
            print(f"  PASS - frequencies swapped correctly")
        elif active_before == active_after:
            print(f"  WARN - no change detected (command may not work)")
        else:
            print(f"  INFO - values changed but not a clean swap")

        # Flip back to restore original state
        time.sleep(0.3)
        cmd.execute()
        time.sleep(0.3)

    print()

    # Test 3: Encoder commands exist
    print("=" * 60)
    print("TEST 3: Encoder command validity")
    print("=" * 60)
    for cmd_name in ENCODER_COMMANDS:
        try:
            cmd = api.command(cmd_name)
            print(f"  OK   {cmd_name}")
        except Exception as e:
            print(f"  FAIL {cmd_name}: {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()
