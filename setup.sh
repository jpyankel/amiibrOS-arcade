echo "Running image setup..."

# === check for arguments ===
echo "Checking user arguments..."
if [ -z "$1" ]; then
  echo -e "Error: SD card not specified!\nPlease include /dev/YOUR-SD as arg"
  exit
fi

# === check for root priveledges ===
echo "Checking for root priveledges..."
if [[ $EUID -ne 0 ]]; then
  echo -e "Error: No root priveledge detected!\nPlease run with 'sudo'"
  exit
fi

# === check to make sure raspbian img exists ===
echo "Checking for image in img/..."
fcount=$(ls img/*.img 2> /dev/null | wc -l)
if [[ $fcount -ne 1 ]]; then
  echo "Error: There must exactly 1 .img file in img/"
  exit
fi
img=$(ls img/*.img)
echo "Image found: $img"

# === make sure nothing is mounted in /mnt/rpi yet ===
echo -e "Checking /mnt/rpi for previous mounts..."
mkdir -p /mnt/rpi
if $(findmnt -rn -o TARGET /mnt/rpi >/dev/null); then
  echo -e "Error: There is already something mounted in /mnt/rpi\
    \nPlease unmount it before re-running setup"
  exit
fi

# === preparing for copy by checking if sd card exists ===
echo -e "Checking SD card (1st arg)..."
if [ ! -e $1 ]; then
  echo -e "Error: SD card $1 doesn't exist!"
  exit
fi

# === copy the base raspbian img ===
echo -e "Copying base raspbian img to SD card..."
dd bs=4M if=$img of=$1 oflag=direct conv=fsync status=progress

# === mount the SD card ===
echo -e "Preparing mount..."
sectorsize=$(fdisk -l $1\
  | grep -o "Sector size (logical/physical): [0-9]* bytes / [0-9]* bytes"\
  | grep -o "[0-9]*"\
  | head -1)
echo "- Image sector size: $sectorsize B"

bootstart=$(fdisk -lo START,TYPE $1\
  | sed -n "s/W95 FAT32 (LBA)$//p"\
  | grep -o "[0-9]*")
echo "- Boot partition start: $bootstart"

bootsectors=$(fdisk -lo SECTORS,TYPE $1\
  | sed -n "s/W95 FAT32 (LBA)$//p"\
  | grep -o "[0-9]*")
echo "- Boot partition sector count: $bootsectors"

linuxstart=$(fdisk -lo START,TYPE $1\
  | sed -n "s/Linux$//p"\
  | grep -o "[0-9]*")
echo "- Linux partition start: $linuxstart"

bootoffset=$((bootstart * sectorsize))
echo "- Boot partition offset: $bootoffset B"

bootsize=$((bootsectors * sectorsize))
echo "- Boot partition size: $bootsize B"

linuxoffset=$((linuxstart * sectorsize))
echo "- Linux partition offset: $linuxstart B"

echo "Mounting linux partition..."
mount -t ext4 -o loop,offset=$linuxoffset $1 /mnt/rpi

echo "Mounting boot partition..."
mount -t vfat -o loop,offset=$bootoffset,sizelimit=$bootsize $1 /mnt/rpi/boot

# === install amiibrOS system software ===
echo "Transfering amiibrOS system software..."

mkdir -p /mnt/rpi/usr/bin/amiibrOS
cp src/requirements.txt /mnt/rpi/usr/bin/amiibrOS/
cp src/amiibrOS.sh /mnt/rpi/usr/bin/amiibrOS/
cp src/main.py /mnt/rpi/usr/bin/amiibrOS/
cp -r src/resources /mnt/rpi/usr/bin/amiibrOS/

# enable console output of systemd service messages
cp src/system.conf /mnt/rpi/etc/systemd/

# install amiibrOS systemd service
cp src/amiibrOS.service /mnt/rpi/etc/systemd/system/
# ensure amiibrOS systemd service is enabled by default
mkdir -p /mnt/rpi/etc/systemd/system/multi-user.target.wants
ln -s /etc/systemd/system/amiibrOS.service \
  /mnt/rpi/etc/systemd/system/multi-user.target.wants/

# === copy various user configurations and apps ===
echo "Transfering user config&apps..."
cp config/config.txt /mnt/rpi/boot/
cp config/wpa_supplicant.conf /mnt/rpi/boot/

# === create the first-time init file ===
touch /mnt/rpi/first-run

# unmount SD card
echo "Unmounting..."
umount /mnt/rpi/boot
umount /mnt/rpi

echo "setup.sh completed successfully!"
