#! /bin/bash
ssh-add LinkboxesIO.pem 
fab initial_config:host=ubuntu@ec2-13-57-247-150.us-west-1.compute.amazonaws.com
