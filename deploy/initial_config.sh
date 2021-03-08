#! /bin/bash

# for staging environment
fab initial_config:host=ubuntu@ubuntu.local

echo "next step - run your first deployment"

# for production environment
#ssh-add LinkboxesIO.pem 
#fab initial_config:host=ubuntu@54.219.168.81

