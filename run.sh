sudo cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime
sudo apt-get update;wait
sudo apt-get -y install software-properties-common ntpdate
sudo ntpdate tick.stdtime.gov.tw;wait
sudo add-apt-repository ppa:apt-fast/stable -y;wait
sudo apt-get update
sudo apt-get -y install apt-fast;wait
sudo apt-fast -y install build-essential cmake pkg-config cmake automake autoconf autotools-dev fswebcam unzip p7zip-full locate libbluetooth-dev libopenobex* python-pip libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev bluez-tools;wait
#sudo apt-fast install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
git clone https://github.com/0-1-0/lightblue-0.4.git ~/lightblue-0.4;wait
cd ~/lightblue-0.4
sudo -H python setup.py install;wait
sudo cp dbus-org.bluez.service /etc/systemd/system/dbus-org.bluez.service 
sudo chmod 777 /var/run/sdp
sudo systemctl daemon-reload
sudo systemctl restart bluetooth
sudo hciconfig hci0 up
sudo -H python -m pip install pybluez
#sudo /usr/bin/sdptool add sp
sdptool add --channel=0 SP
sudo bluetoothctl <<EOF
power on
discoverable on
pairable on
agent NoInputNoOutput
default-agent 
EOF
echo "可以跑該死的藍芽序列伺服器了"