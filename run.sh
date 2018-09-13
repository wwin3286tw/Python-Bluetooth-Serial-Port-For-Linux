#!/bin/bash
log() {
now="`date '+%Y-%m-%d %H:%M:%S.%3N'`";
printf -v now "[%s %s]" $now 
echo "${now} ${@}"
}
cd ~/blueServer
log "複製dbus-org.bluez.service設定檔"
sudo cp dbus-org.bluez.service /etc/systemd/system/dbus-org.bluez.service
log "將時區更新為 /亞洲/台北"
sudo cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime
log "取得最新軟體清單"
sudo apt-get update;wait
log "安裝基本組件"
sudo apt-get -y install ntpdate curl
sudo ntpdate tick.stdtime.gov.tw;wait
log "快速安裝 apt-fast..."
/bin/bash -c "$(curl -sL https://git.io/vokNn)"
log "apt-fast 安裝完成"
log "開始安裝主要元件，這需費時較久，請稍後。"
sudo apt-fast -y install build-essential cmake pkg-config cmake automake autoconf autotools-dev fswebcam unzip p7zip-full locate libbluetooth-dev libopenobex* python-pip libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev bluez-tools;wait
log "主要元件安裝完成"
log "開始克隆必要的python程式庫"
cd ~/
git clone https://github.com/0-1-0/lightblue-0.4.git ~/lightblue-0.4;wait
cd ~/lightblue-0.4
sudo -H python setup.py install;wait
log "重啟藍芽服務中"
sudo systemctl daemon-reload
sudo systemctl restart bluetooth
log "重啟藍芽裝置"
sudo hciconfig hci0 up
log "藍芽重啟成功"
log "變更Service Discovery Protocol(SDP)執行權限"
sudo chmod 777 /var/run/sdp
log "開始使用pip安裝必要的python程式庫"
sudo -H python -m pip install pybluez
#sudo /usr/bin/sdptool add sp
log "設定藍芽可被偵測、配對"
cd ~/blueServer
sudo bluetoothctl <<EOF
power on
discoverable on
pairable on
agent NoInputNoOutput
default-agent 
EOF
log "可以跑該死的藍芽序列伺服器了"
