#!/bin/bash
if [ $(ps -ef | grep -c "WebApp.py") -lt 2 ]; then nohup python ./WebApp.py &  fi
