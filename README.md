# safe-t

1. Activate Virtual environment
2. Run - pip3 install -r requirements.txt
3. Change gunicorn path to virtual env gunicorn path in supervisord.conf
4. Run  
    supervisorctl -c supervisord.conf
    supervisorctl reread
5. Run
    supervisorctl update
6. Check if its running by running
    supervisorctl status safet
