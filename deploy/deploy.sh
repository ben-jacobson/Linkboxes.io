#! /bin/bash
ssh-add LinkboxesIO.pem
fab deploy:host=ubuntu@ec2-13-57-247-150.us-west-1.compute.amazonaws.com
