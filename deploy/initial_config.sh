#! /bin/bash

# for staging environment
fab initial_config:host=ubuntu@ubuntuStaging.local

# for production environment
#ssh-add LinkboxesIO.pem 
#fab initial_config:host=ubuntu@54.219.168.81

