# amiibrOS-arcade
A 2020 update to the original amiibrOS system software. This time, using Python and the Pygame
library to replace the C system software. The goal is to make amiibrOS more easy to maintain and
extend.

## Creating an amiibrOS-arcade Raspbian SD-Card
Prerequisites:
* Internet access and ability to download large files
* SD-card (8GB+ storage recommended)

Steps:
1. Download Raspbian Lite and place in img/ folder
2. Make any configuration changes in config/ folder (see the README in config/)
3. Add apps for your specific Amiibo figures in app/ follder (see the README in
app/).
4. Run `chmod +x setup.sh`
5. Run `sudo setup.sh`
6. Plug the SD card into the PI and let it boot. It will require some time for downloads and installation. It will automatically reboot a few times on its own.
7. Enjoy!

## Folder Structure
Most subfolders will have a README with more information about the folder's
purpose. A brief overview of the project's root folder layout is given here:
* install: Contains amiibrOS installation.
* img: Contains the .img file for Raspbian, which will be modified by the setup
scripts.
* boot: Contains a few boot configuration files you (the amiibrOS user) should modify.
