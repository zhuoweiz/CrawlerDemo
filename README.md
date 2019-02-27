## python dev environemtn
```bash
sudo apt update
sudo apt install python python-dev python3 python3-dev

wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py

sudo pip install --upgrade virtualenv
```

## setup the virtual engironment
```bash
rm -rf demo
mkdir demo
cd demo
virtualenv --python python3 demo_venv
mv [path_to_files_in_demo_folder] demo_venv
cd demo_venv
```

## scrapy framework setup
```bash
sudo apt-get install python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
pip install scrapy
```

## activate the virtual environment for running the crawler
```bash
source bin/activate
```

## dependencies if missing any
```bash
sudo apt-get install mysql-server

pip install scrapy
pip install mysql-connector-python # for mysql
pip install pymongo #for mongoDB
```

## now can run the crawler spider
```bash
scrapy crawl demo -o feed.csv
```
result will be in feed.csv