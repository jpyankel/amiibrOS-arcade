echo "Running image setup..."

# check for root priveledges
echo "Checking for root priveledges..."
if [[ $EUID -ne 0 ]]; then
  echo -e "Error: No root priveledge detected!\nPlease run with 'sudo'"
  exit
fi

# check for base raspbian img
echo "Checking for image in img/..."
fcount=$(ls img/*.img 2> /dev/null | wc -l)
if [[ $fcount -ne 1 ]]; then
  echo "Error: There must exactly 1 .img file in img/"
  exit
fi
img=$(ls img/*.img)
echo "Image found: $img"

# make sure nothing is mounted in /mnt/rpi yet
echo -e "Checking /mnt/rpi for previous mounts..."
mkdir -p /mnt/rpi
if $(findmnt -rn -o TARGET /mnt/rpi >/dev/null); then
  echo -e "Error: There is already something mounted in /mnt/rpi\
    \nPlease unmount it before re-running setup"
  exit
fi

# mount the base raspbian img
echo -e "Preparing mount..."
sectorsize=$(fdisk -l $img\
  | grep -o "Sector size (logical/physical): [0-9]* bytes / [0-9]* bytes"\
  | grep -o "[0-9]*"\
  | head -1)
echo "- Image sector size: $sectorsize B"

bootstart=$(fdisk -lo START,TYPE $img\
  | sed -n "s/W95 FAT32 (LBA)$//p"\
  | grep -o "[0-9]*")
echo "- Boot partition start: $bootstart"

bootsectors=$(fdisk -lo SECTORS,TYPE $img\
  | sed -n "s/W95 FAT32 (LBA)$//p"\
  | grep -o "[0-9]*")
echo "- Boot partition sector count: $bootsectors"

linuxstart=$(fdisk -lo START,TYPE $img\
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
mount -t ext4 -o loop,offset=$linuxoffset $img /mnt/rpi

echo "Mounting boot partition..."
mount -t vfat -o loop,offset=$bootoffset,sizelimit=$bootsize $img\
  /mnt/rpi/boot

# install amiibrOS system software
echo "Transfering amiibrOS system software..."
#TODO

# copy various user configurations and apps
echo "Transfering user config&apps..."
cp config/config.txt /mnt/rpi/boot/
cp config/wpa_supplicant.conf /mnt/rpi/boot/

# unmount raspbian img
echo "Unmounting..."
umount /mnt/rpi/boot
umount /mnt/rpi

echo "setup.sh completed successfully!"
