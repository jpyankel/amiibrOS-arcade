#!/bin/bash

# this is the amiibrOS boot/initialization script
# this should run automatically after the Raspberry Pi boots
# it will check for a first-time setup, which if completed successfully,
#   will not be run again

# check for first-run file
echo "Checking for amiibrOS install state..."

if [[ -e "first-run" ]]; then
  # initial setup
  echo -e "first-run found!\nStarting first time setup..."
  #raspi-config nonint do_expand_rootfs (already taken care of by raspbian)
  raspi-config nonint do_change_locale en_US.UTF-8
  raspi-config nonint do_configure_keyboard us
  raspi-config nonint do_boot_behaviour B2
  raspi-config nonint do_hostname amiibrOS-arcade
  mv first-run second-run
  reboot
elif [[ -e "second-run" ]]; then
  echo -e "second-run found!\nContinuing first time setup..."
  # install various 3rd party software
  apt-get update
  apt-get -y install python3-pygame
  apt-get -y install python3-pip
  python3 -m pip install -r usr/bin/amiibrOS/requirements.txt
  rm second-run
  reboot
else
  echo -e "No first-run found. Starting amiibrOS..."
  python3 usr/bin/amiibrOS/main.py
fi
