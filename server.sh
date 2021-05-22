#! /bin/sh
gunicorn -w 4 -b 127.0.0.1:5000 run-server:app