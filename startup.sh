#!/bin/bash
# Redirect both stdout and stderr to log files
python3 /home/max/workspace/auto_print_file_from_email/app/print_timer.py >> /home/max/workspace/auto_print_file_from_email/app.log 2>> /home/max/workspace/auto_print_file_from_email/error.log &