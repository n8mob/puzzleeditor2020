#!/bin/bash

cp /opt/elasticbeanstalk/deployment/env /opt/elasticbeanstalk/deployment/custom_env_var

chmod 644 /opt/elasticbeanstalk/deployment/custom_env_var

rm -f /opt/elasticbeanstalk/deployment/*.bak
