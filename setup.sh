#!/bin/bash

# Function to check if X-Plane path exists using mdfind
check_xplane_path() {
    local xplane_path=$(mdfind "kMDItemCFBundleIdentifier == 'com.laminar-research.X-Plane'" | head -n 1)
    if [ -n "$xplane_path" ]; then
        echo "$(dirname "$xplane_path")"
    else
        echo "X-Plane not found"
        exit 1
    fi
}

# Function to check if Python plugin file exists
check_python_plugin() {
    local xplane_dir="$1"
    local plugin_file="$xplane_dir/Resources/plugins/PythonPlugins/PI_cockpitdecks_helper.py"
    if [ -f "$plugin_file" ]; then
        echo "Python plugin found: $plugin_file"
    else
        echo "Python plugin not found"
        exit 1
    fi
}

# Function to check if Python 3.10 is installed
check_python_3_10() {
    if command -v python3.10 &>/dev/null; then
        echo "Python 3.10 is installed"
    else
        echo "Python 3.10 is not installed"
        exit 1
    fi
}

# Main
xplane_path=$(check_xplane_path)
check_xplane_path
check_python_plugin "$xplane_path"
check_python_3_10
