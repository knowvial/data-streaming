# Kafka NodeJS application
Install node
```
cd ~
curl -sL https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh -o install_nvm.sh
bash install_nvm.sh
source ~/.profile
nvm ls-remote
nvm install 10.19.0
npm -v
node -v
```

Run 
```
cd kafka/consumer-producer/nodejs
npm install

node consumer.js
node producer.js
```
