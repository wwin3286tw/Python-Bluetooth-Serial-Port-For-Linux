# <font color="Green">Python Bluetooth Classic Serial Port Communication</font>
# Copyright © 2018-09 by Yi,Jia-Ye Partition Rights Reserved
# 程式碼包含使用第三方著作(https://github.com/0-1-0/lightblue-0.4)
1. 必須公布原始碼，不得作為專有軟體
2. 僅能收取傳送與提供上必要的工本費用
3. 不能阻止他人針對軟體做任何逆向工程
4. 可執行程式必須附帶原始碼
5. 不得作為專有軟體及任何商業用途
## <font color="orange">WARNING: DEPRECATED, THIS GIST WILL NO LONGER ABLE TO MAINTAIN.</font>
## <font color="orange">警告：腳本已經廢棄，不再做任何維護！</font>
### <font color="orange">THIS SCRIPTS COMES WITH ABSOLUTELY NO WARRANTY, USE AT YOUR OWN RISK.</font>
### <font color="orange">這些腳本並沒有任何承諾，使用者風險自負！</font>

## 版本更新記錄
1. 將資料格式化
2. 字串和二進位資料使用不同通道
3. 增加Wifi模式
4. 考慮統一function命名風格

## 專案議題(Project issue)
1. 都寫在程式的開頭(Code Summary)了，請前往查看
## 建議的機台平台與軟體相依性
1. Linux(Ubuntu 16.04 tested)
2. Python2 only
3. Lightblue module(only on python2)
## 機台硬體需求
1. Single Board Computer(Ex: Raspberry)
2. Linux Base PC with WIFI and BT
## 客戶端硬體需求
1. Android Phone(tested)
2. Support bluetooth classic Serial Port Profile(SPP) Devices
## 描述
1. Can communication With Bluetooth Device(PC、RaspberryPI) using Android or support SPP device.
1. 能夠用Android與藍芽裝置(單板電腦、電腦)
2. Built-in File Transport Protocol.
2. 內建檔案傳輸功能
3. Camera Control, Take picture.
3. 相機控制，拍張照吧！
4. Waiting you to add more function.
4. 等你加入更多功能
5. WIFI file trasnfer
5. WIFI檔案傳輸功能
# 專案參考
### 1. [開機開啟藍芽](https://unix.stackexchange.com/questions/92036/enabling-bluetooth-discoverability-upon-start-up)
### 2. [資源檔JSON編輯器](https://jsoneditoronline.org/)
# 專案
1. A_BT-ftp-server.py 伺服器核心檔案
2. BlueServerLib.py 伺服器支援函數庫
3. UserMode_flowchart.xml 連線流程圖 [draw.io](https://draw.io/)
4. resource.json 伺服器資源檔 [jsoneditoronline](https://jsoneditoronline.org/)
5. 其他檔案，不做解釋。
# 安裝
## 手動安裝參考
```bash=
#sudo nmcli dev wifi connect ? password ? ifname wlan0
sudo nmcli dev wifi connect Kaiwood password 0660006000 ifname wlan0;wait
sudo cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime
sudo apt-get update;wait
sudo apt-get -y install software-properties-common ntpdate
sudo ntpdate tick.stdtime.gov.tw
sudo add-apt-repository ppa:apt-fast/stable -y;wait
sudo apt-get update
sudo apt-get -y install apt-fast;wait
sudo apt-fast -y install build-essential cmake pkg-config cmake automake autoconf autotools-dev fswebcam unzip p7zip-full locate libbluetooth-dev libopenobex* python-pip libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev;wait
#sudo apt-fast install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
git clone https://github.com/0-1-0/lightblue-0.4.git
cd lightblue-0.4
sudo -H python setup.py install
cd ~
#sudo nano /etc/systemd/system/dbus-org.bluez.service
#ExecStart=/usr/lib/bluetooth/bluetoothd -C
#add ExecStartPost=/usr/bin/sdptool add sp
#sudo sed -i '9s/.*/ExecStart=\/usr\/lib\/bluetooth\/bluetoothd -C/' /etc/systemd/system/dbus-org.bluez.service #replace string and save in one-line(已廢棄，複製比較快，幹)
###!!!RUN THE NORMAL SCRIPT!!!###
sudo cp dbus-org.bluez.service /etc/systemd/system/dbus-org.bluez.service # 如果你很不幸的rekt了bluez的設定檔，請再次執行本行、以及以下兩行 ##
sudo systemctl daemon-reload
sudo systemctl restart bluetooth
sudo -H python -m pip install pybluez
bluetoothctl
power on
scan on
pair ?
#remove ?
sudo hciconfig hci up #<class 'lightblue._lightbluecommon.BluetoothError'>, A_BT-ftp-server.py, 102, Cannot access local device: no available bluetoot devices
#sudo /usr/bin/sdptool add sp
sdptool add --channel=0 SP
sudo chmod 777 /var/run/sdp

sudo nano /etc/systemd/system/bluetooth.target.wants/bluetooth.service
#應該可以跑伺服器了 #Now, you can run the BT server.
sudo ./A_BT-ftp-server.py
#sudo apt-get install -y bluez-tools 
#sudo btmon #監聽藍芽封包

```
## 手動
```bash=
sudo nmcli dev wifi connect Kaiwood password 0660006000 ifname wlan0;wait
git config --global http.sslverify false
cd ~;
git clone https://gist.github.com/wwin3286tw/ae7ef8149e474475b14fde89b7c8783c ~/blueServer;
cd blueServer;
chmod 755 *.py;
chmod 755 *.sh;
./run.sh;

```
## 快速安裝
```bash=
sudo nmcli dev wifi connect Kaiwood password 0660006000 ifname wlan0;wait;
bash <(wget -qO- https://raw.githubusercontent.com/wwin3286tw/Python-Bluetooth-Serial-Port-For-Linux/master/quick.sh);
cd ~/blueServer
```
## 解除安裝
```bash
cd ~
rm -rf blueServer/
```

## Debugging Reinstall(如果你更新了程式，只是想重新安裝，請執行以下命令)
```bash
cd ~
rm -rf blueServer/
git clone https://github.com/wwin3286tw/Python-Bluetooth-Serial-Port-For-Linux.git ~/blueServer;
cd blueServer;
chmod 755 *.py;
chmod 755 *.sh;
```
