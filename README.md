# amiibrOS-arcade
TODO description

## Creating an amiibrOS-arcade Raspbian SD-Card
Prerequisites:
* Internet access and ability to download large files
* SD-card with at least ??? GB storage
* qemu-user-static installed

Steps:
1. Download Raspbian Lite and place in img/ folder
2. Make any configuration changes in config/ folder (see the README in config/)
3. Add apps for your specific Amiibo figures in app/ follder (see the README in
app/).
4. Run `chmod +x setup.sh`
5. Run `sudo setup.sh`
6. TODO

## Folder Structure
Most subfolders will have a README with more information about the folder's
purpose. A brief overview of the project's root folder layout is given here:
* app: Contains amiibrOS apps by character ID.
* src: Contains amiibrOS system software source files.
* img: Contains the .img file for Raspbian, which will be modified by the setup
scripts.
* config: Contains any configuration files you (the amiibrOS user) should check
and potentially modify.
