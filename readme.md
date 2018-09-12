# <font color="Green">Python Bluetooth Classic Serial Port Communication<font>
## Support platform and Software Dependency
1. Linux(Ubuntu 16.04 tested)
2. Python2 only
3. Lightblue module(only on python2)
## Server Hardware Recommand
1. Single Board Computer(Ex: Raspberry)
2. Linux Base PC
## Client Hardware Recommand
1. Android Phone(tested)
2. Support bluetooth classic Serial Port Profile(SPP) Devices
## Description
1. Can communication With Bluetooth Device(PC、RaspberryPI) using Android or support SPP device.
2. Built-in File Transport Protocol.
3. Camera Control, Take picture.
4. Waiting you to add more function.
# Installation
## Friend ARM NanoPi NEO Air
```bash=
#sudo nmcli dev wifi connect ? password ? ifname wlan0
sudo nmcli dev wifi connect Kaiwood password 0660006000 ifname wlan0
sudo cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime
sudo apt-get update
sudo apt-get install software-properties-common ntpdate
sudo ntpdate tick.stdtime.gov.tw
sudo add-apt-repository ppa:apt-fast/stable
sudo apt-get update
sudo apt-get -y install apt-fast
sudo apt-fast -y install build-essential cmake pkg-config cmake automake autoconf autotools-dev fswebcam unzip p7zip-full locate libbluetooth-dev libopenobex*
git clone https://github.com/0-1-0/lightblue-0.4.git
cd lightblue-0.4
sudo -H python setup.py install
nano /etc/systemd/system/dbus-org.bluez.service
#add ExecStartPost=/usr/bin/sdptool add sp
sudo systemctl daemon-reload
sudo systemctl restart bluetooth
```
## Normal
```bash=
git clone https://gist.github.com/wwin3286tw/ae7ef8149e474475b14fde89b7c8783c blueServer
cd blueServer
```
