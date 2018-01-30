#!/bin/bash
# Host the YELLOWPAGIST app on Heroku


read -p "YP API Key: " apikey
echo

echo "[*] Creating Heroku app..."
heroku create
echo

echo "[*] Adding YP APIKey to the Environment Variables..."
heroku config:add YPAPIKey=$apikey 
echo

echo "[*] Pushing to Heroku Git repo..."
url=$(git push heroku master | awk '/deployed to Heroku/ {print $(NF-3)}')
echo "The URL is: "
echo $url
echo

echo "[*] Adding Redistogo addon..."
heroku addons:create redistogo:nano
echo

echo "[*] Starting the worker process..."
heroku ps:scale worker=1
echo

echo "[*] Completed."
echo "[*] You can access the web-app at: $url"
