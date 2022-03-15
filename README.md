# IoT-Project
Load ino file in arduino folder to ESP32CAM device.

User need to set up a local mosquitto broker to connect system components (link download: https://mosquitto.org/download/).

Then change the broker address in fake_cam.py and webcam/videobase.py

Run python manage.py migrate

Run python manage.py createsuperuser, then create your admin account.

Run python manage.py runserver, the system will be operated.

Run python fake_cam.py, the emulator camera will be operated.





