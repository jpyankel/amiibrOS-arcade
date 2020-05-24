# check for root priveledges
if [[ $EUID -ne 0 ]]; then
  echo -e "No root priveledge detected\nPlease run with 'sudo'"
  exit
fi

# check for base raspbian img
fcount=$(ls img/*.img 2> /dev/null | wc -l)
if [[ $fcount -ne 1 ]]; then
  echo "There must exactly 1 .img file in img/"
  exit
fi

# make sure nothing is mounted in /mnt/disk yet
mkdir -p /mnt/disk

if $(findmnt -rn -o TARGET /mnt/disk >/dev/null); then
  echo -e "There is already something mounted in /mnt/disk\
    \nPlease unmount it before re-running setup"
  exit
fi

# mount the base raspbian img
# TODO do fdisk -lo START img/2020-02-13-raspbian-buster-lite.img | tail -n 2
# TODO and generate the following commands based on that. BAD HARDCODING.
# TODO WILL ONLY WORK WITH 2020-02-13-raspbian-buster-lite.img
mount -t ext4 -o loop,offset=$((532480*512)) img/2020-02-13-raspbian-buster-lite.img /mnt/disk
mount -t vfat -o loop,offset=$((8192*512)),sizelimit=$((524288*512)) img/2020-02-13-raspbian-buster-lite.img /mnt/disk/boot

# install amiibrOS system software
#TODO

# copy various user configurations and apps
#TODO

# unmount raspbian img
umount /mnt/disk/boot
umount /mnt/disk
