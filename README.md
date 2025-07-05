
# 🚀 Multi-Flask App Deployment on AWS EC2 with Nginx + Supervisor

This guide documents how two independent Flask projects were deployed on a single EC2 instance, served via Gunicorn, managed by Supervisor, and reverse-proxied using Nginx.

## 🧰 EC2 Setup

1. Launch an Ubuntu EC2 instance.

```bash
ssh -i <key>.pem ubuntu@<ec2-public-ip>
```
```bash
sudo apt update && sudo apt install python3-pip python3-venv nginx supervisor -y
```
## 🔧 Setting Up Flask Projects

1. Setup Python Virtual Environments

# Bangalore House Predictor Project

```bash
cd ~/Bangalore_House_Price_Predictor/server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Celebrity Classifier Project
```bash
cd ~/Celebrity_Classifier/server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# 🔧 Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/default
```
Add inside the server {} block:
```bash
# First project (root)
location / {
    root /home/ubuntu/Bangalore_House_Price_Predictor/client;
    index index.html;
    try_files $uri $uri/ /index.html;
}

location /api/ {
    rewrite ^/api(/.*)$ $1 break;
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

# Second project (at /project2/)
location /project2/ {
    alias /home/ubuntu/Celebrity_Classifier/UI/;
    index app.html;
    try_files $uri $uri/ /app.html;
}

location /project2_api/ {
    rewrite ^/project2_api(/.*)$ $1 break;
    proxy_pass http://127.0.0.1:5001;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```
Then restart Nginx:
```bash
sudo nginx -t && sudo systemctl reload nginx
```
# 🔄 Supervisor Configuration
1. Bangalore House Price Predictor App
```bash
sudo nano /etc/supervisor/conf.d/bangalore.conf
```
```bash
[program:bangalore]
directory=/home/ubuntu/Bangalore_House_Price_Predictor/server
command=/home/ubuntu/Bangalore_House_Price_Predictor/server/venv/bin/gunicorn server:app --bind 127.0.0.1:5000 --capture-output --log-level debug
autostart=true
autorestart=true
stderr_logfile=/var/log/bangalore.err.log
stdout_logfile=/var/log/bangalore.out.log
user=ubuntu
environment=PATH="/home/ubuntu/Bangalore_House_Price_Predictor/server/venv/bin"
```
2. Celebrity Classifier App
```bash
sudo nano /etc/supervisor/conf.d/celebapp.conf
```
```bash
[program:celebapp]
directory=/home/ubuntu/Celebrity_Classifier/server
command=/home/ubuntu/Celebrity_Classifier/server/venv/bin/gunicorn server:app --bind 127.0.0.1:5001 --capture-output --log-level debug
autostart=true
autorestart=true
stderr_logfile=/var/log/celebapp.err.log
stdout_logfile=/var/log/celebapp.out.log
user=ubuntu
environment=PATH="/home/ubuntu/Celebrity_Classifier/server/venv/bin"
```
🔄 Reload and Start
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start bangalore
sudo supervisorctl start celebapp
```
📅 Test in Browser

First Project UI:
```bash
http://ec2-13-60-97-207.eu-north-1.compute.amazonaws.com/
```

Second Project UI:

```bash
http://ec2-13-60-97-207.eu-north-1.compute.amazonaws.com/project2/app.html
```

