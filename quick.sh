git config --global http.sslverify false
cd ~;
git clone https://gist.github.com/wwin3286tw/ae7ef8149e474475b14fde89b7c8783c ~/blueServer;
cd blueServer;
chmod 755 *.py;
chmod 755 *.sh;
./run.sh;