# this is a first-time initialization script
# this should run automatically after the Raspberry Pi boots for the first time
# if it completes successfully, then it will not run again

# check for first-run file
echo "Checking for first-run..."

if [[ -e "first-run" ]]; then
  echo -e "first-run found!\nStarting first time setup..."
else
  echo -e "No first-run found. Continuing with boot process..."
  exit
fi

# perform first-time setup
# sudo raspi-config nonint do_change_locale en_US.UTF-8
# sudo raspi-config nonint do_configure_keyboard us
# sudo raspi-config nonint do_hostname amiibrOS-arcade
# TODO
# pip install requirements.txt stuff
# Install retroarch
# Configure retroarch

# setup complete, delete first-run
rm first-run

# reboot
reboot
