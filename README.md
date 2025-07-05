✅ Deployment of Two Flask Projects on AWS EC2 with Nginx + Supervisor
markdown
Copy
Edit
# 🚀 Multi-Flask App Deployment on AWS EC2 with Nginx + Supervisor

This guide documents how two independent Flask projects were deployed on a single EC2 instance, served via **Gunicorn**, managed by **Supervisor**, and reverse-proxied using **Nginx**.

---

## 🗂️ Project Structure

/home/ubuntu/
├── Bangalore_House_Price_Predictor/
│ └── server/
│ ├── server.py
│ ├── util.py
│ ├── artifacts/
│ └── venv/
│
├── Celebrity_Classifier/
│ ├── server/
│ │ ├── server.py
│ │ ├── util.py
│ │ ├── artifacts/
│ │ └── venv/
│ └── UI/
│ ├── app.html
│ ├── app.js
│ └── app.css

yaml
Copy
Edit

---

## 🧰 EC2 Setup

1. Launch an Ubuntu EC2 instance.
2. SSH into the instance:

   ```bash
   ssh -i <key>.pem ubuntu@<ec2-public-ip>
Update and install required tools:

bash
Copy
Edit
sudo apt update && sudo apt install python3-pip python3-venv nginx supervisor -y
⚙️ Setup for Each Project
🔹 1. Create Python Virtual Environments
bash
Copy
Edit
cd ~/Bangalore_House_Price_Predictor/server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

cd ~/Celebrity_Classifier/server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
Make sure each requirements.txt includes:

nginx
Copy
Edit
Flask
gunicorn
opencv-python
scikit-learn
pywavelets
seaborn
🔧 Nginx Configuration
Edit the Nginx config:

bash
Copy
Edit
sudo nano /etc/nginx/sites-available/default
Add the following blocks inside server {}:

nginx
Copy
Edit
# First project (served at root)
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

# Second project (served at /project2/)
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
Restart Nginx:

bash
Copy
Edit
sudo nginx -t && sudo systemctl reload nginx
🔁 Supervisor Setup
🔹 Create config for both projects:
/etc/supervisor/conf.d/bangalore.conf
ini
Copy
Edit
[program:bangalore]
directory=/home/ubuntu/Bangalore_House_Price_Predictor/server
command=/home/ubuntu/Bangalore_House_Price_Predictor/server/venv/bin/gunicorn server:app --bind 127.0.0.1:5000 --capture-output --log-level debug
autostart=true
autorestart=true
stderr_logfile=/var/log/bangalore.err.log
stdout_logfile=/var/log/bangalore.out.log
user=ubuntu
environment=PATH="/home/ubuntu/Bangalore_House_Price_Predictor/server/venv/bin"
/etc/supervisor/conf.d/celebapp.conf
ini
Copy
Edit
[program:celebapp]
directory=/home/ubuntu/Celebrity_Classifier/server
command=/home/ubuntu/Celebrity_Classifier/server/venv/bin/gunicorn server:app --bind 127.0.0.1:5001 --capture-output --log-level debug
autostart=true
autorestart=true
stderr_logfile=/var/log/celebapp.err.log
stdout_logfile=/var/log/celebapp.out.log
user=ubuntu
environment=PATH="/home/ubuntu/Celebrity_Classifier/server/venv/bin"
🔄 Activate Supervisor
bash
Copy
Edit
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start bangalore
sudo supervisorctl start celebapp
