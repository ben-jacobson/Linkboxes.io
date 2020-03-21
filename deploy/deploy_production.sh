#! /bin/bash
ssh-add LinkboxesIO.pem
fab deploy:host=ubuntu@54.219.168.81

