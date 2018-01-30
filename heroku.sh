#!/bin/bash
# Host the YELLOWPAGIST app on Heroku


echo "Starting execution of heroku.sh at `date`" > heroku.log
echo >> heroku.log

read -p "[*] YP API Key: " apikey
echo

echo "[*] Creating Heroku app..."
heroku create &>> heroku.log
echo &>> heroku.log

echo "[*] Adding YP APIKey to the Environment Variables..."
heroku config:add YPAPIKey=$apikey &>> heroku.log
echo &>> heroku.log

echo "[*] Pushing to Heroku Git repo..."
git push heroku master &>> heroku.log
echo &>> heroku.log

echo "[*] Adding Redistogo addon..."
heroku addons:create redistogo:nano &>> heroku.log
echo &>> heroku.log

echo "[*] Starting the worker process..."
heroku ps:scale worker=1 &>> heroku.log
echo &>> heroku.log

HEROKUURL=$(cat heroku.log |& awk '/deployed to Heroku/ {print $(NF-3)}')
echo 
echo "[*] Completed. You can access the web-app at: $HEROKUURL"
