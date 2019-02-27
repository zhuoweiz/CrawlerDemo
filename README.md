## python dev environemtn
```bash
sudo apt update
sudo apt install python python-dev python3 python3-dev

wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py

sudo pip install --upgrade virtualenv
```

## setup the virtual engironment
```
rm -rf demo
mkdir demo
cd demo
virtualenv --python python3 demo_venv
mv [path to demo folder] demo_venv
cd demo_venv
```

```
## setup third party packages needed
sudo apt-get install python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
pip install scrapy
```

## activate the virtual environment for running the crawler
source bin/activate

## dependencies if missing any
```
sudo apt-get install mysql-server

pip install scrapy
pip install mysql-connector-python # for mysql
pip install pymongo #for mongoDB
```

## now can run the crawler spider
```
scrapy crawl demo -o feed.csv
```
result will be in feed.csv