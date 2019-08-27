# SmartRoom

SmartRoom is a simple django-based web app used in Munich Intel IOT Lab to connect sensors
and display values in the web browser. 
Python3.6, Django2.2
## Install
### 1. Create a virtual environment
```
$ sudo apt-get update
$ sudo apt-get install python3-pip
$ python3 -m pip install virtualenv
$ virtualenv -p python3 SmartRoom
```
### 2. Clone repo in SmartRoom/src/
```
$ git clone http://github/9OP/SmartRoom SmartRoom/src/
```
### 3. Install dependencies
**It's important to activate the virutal environnment**.
You don't want your python dependencies to be messed up
with your other python project.
```
$ source SmartRoom/bin/activate
$ pip3 install -r requirements.txt
```

#### To activate the virtual env:
```
$ source ./bin/activate
```
#### To deactivate the virtual env:
```
$ deactivate
```

## Apache2 deployment
The following deployment was made on a Ubuntu18.04 server.
### 1. Install apache2
```
$ sudo apt-get install apache2
$ sudo apt-get install libapache2-mod-wsgi-py3
```
### 2. Allow hosts in SmartRoom/src/SmartRoom/setting.py
ALLOWED_HOSTS = ['127.0.0.1', any other hosts]
This application is supposed to be used in a local network.
You should add the local server IP addresse in ALLOWED_HOSTS.
To get the local IP addresse on *nix : 
```
$ ifconfig
```
### 3. Collect static files
In case static files (css, media, icon etc.) have been modified
```
python3 SmartRoom/src/manage.py collectstatic
```

### 4. Configure Apache2
This is a pain in the ass, you are welcome I wrote
the procedure here ;)
Here is the file to edit:
**sudo nano /etc/apache2/sites-available/000-default.conf**
```
<VirtualHost **>
  ServerName localhost

  Alias /static /path/to/SmartRoom/src/static
  <Directory /path/to/SmartRoom/src/static>
    Require all granted
  </Directory>

  <Directory /path/to/SmartRoom/src/SmartRoom/>
	  <Files wsgi.py>
		  Require all granted
	  </Files>
  </Directory>
  
  WSGIDaemonProcess smartroom python-home=/path/to/SmartRoom python-path=/path/to/SmartRoom/src/SmartRoom
  WSGIProcessGroup smartroom
  WSGIScriptAlias / /path/to/SmartRoom/src/SmartRoom/wsgi.py

</VirtualHost>
```
### 4.5 Add project path to SmartRoom/src/SmartRoom/wsgi.py
This is missing in default django wsgi.py generated file.
```
from settings import BASE_DIR
path = BASE_DIR
if path not in sys.path:
    sys.path.append(path)
```
### 5. Give permission to Apache2
I am not sure about the permission given. I might have given to many permission. In my case the app is not accessible from the outside.
```
sudo chown -R www-data:www-data ./SmartRoom
sudo chmod -R 755 ./SmartRoom
sudo chmod -R 775 ./SmartRoom/src/db.sqlite3
```
### 6. Allow apache2 process
```
$ sudo ufw allow 'Apache Full'
```
### 7. test Configuration
```
$ sudo apache2ctl configtest
```
### 8. start / restart apache2
```
$ sudo systemctl restart apache2
```
To manage apache2 service:
```
$ sudo service apache2 restart / stop / start
```
## Crontab : periodic task
The webapp have to ping the sensors and update data every 10 minutes. A crontab was used to automate this.
The Django command to ping sensors is:
```
$ python3 SmartRoom/src/SmartRoom/manage.py connect_sensors
```
To edit the cron tab:
```
$ crontab -e
```
Then add to this file:
```
*/1 * * * * python3 /path/to/SmartRoom/src/SmartRoom/ manage.py connect_sensors
```
You might need to use the root cron:
```
$ sudo crontab -e
```


#### Conclusion
You can connect to the web app with:
http://127.0.0.1/ConnectedChairs/
Default admin crendentials:
username: admin
password: 123

- [X] README.md
- [X] Install guide
- [ ] Cron periodic lookup for sensors data
- [ ] dev guide


