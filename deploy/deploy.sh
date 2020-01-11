#! /bin/bash
ssh-add LinkboxesIO.pem
fab deploy:host=ubuntu@ec2-54-219-168-81.us-west-1.compute.amazonaws.com

