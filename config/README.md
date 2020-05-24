# config
This subfolder contains various configuration files for customizing your
amiibrOS setup.

## wpa_supplicant.conf
This file is very important to the setup: In order for the amiibrOS first time
setup scripts to work, an internet connection is necessary. wpa_supplicant.conf
allows you to preconfigure your wireless connection.

1. Open wpa_supplicant.conf.example with a text editor.
2. Replace `SSID HERE` with your WIFI access point's name.
3. Replace `PASSWORD HERE` with your WIFI password (needed for the Raspberry Pi
to auto-connect to your WIFI).

Make sure to leave quotation marks `""` surrounding your replacement SSID and
PSK.

4. Save As wpa_supplicant.conf. Or save your changes and rename the file to
wpa_supplicant.conf
