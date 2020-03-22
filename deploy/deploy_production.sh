#! /bin/bash
ssh-add LinkboxesIO.pem
fab deploy_production:host=ubuntu@54.219.168.81

