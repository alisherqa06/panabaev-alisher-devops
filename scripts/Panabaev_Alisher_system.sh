#!/bin/bash

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
INFO_FILE="$PROJECT_DIR/Panabaev_Alisher_info.txt"

echo "=============================="
echo "Student Information"
echo "=============================="
echo "Name: Alisher"
echo "Surname: Panabaev"
echo "Group: It2-2308"
echo "Student ID: 37332"

echo
echo "=============================="
echo "System Information"
echo "=============================="
echo "Username: $(whoami)"
echo "Hostname: $(hostname)"
echo "Current Date: $(date)"
echo -n "Operating System: "
. /etc/os-release
echo "$PRETTY_NAME"
echo "Disk Usage:"
df -h "$PROJECT_DIR"
echo "Memory Usage:"
free -h

echo
if [ -f "$INFO_FILE" ]; then
    echo "Student information file exists."
else
    echo "Student information file does not exist."
fi
