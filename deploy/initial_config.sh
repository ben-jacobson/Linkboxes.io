#! /bin/bash
ssh-add ../DosGamesFinderWebServer.pem 
fab initial_config:host=ubuntu@ec2-18-208-170-10.compute-1.amazonaws.com
