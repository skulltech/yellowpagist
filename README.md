# yellowpagist
Yellow pages scraper. 

You can access the web-app [here](https://yellowpagist.herokuapp.com/) - https://yellowpagist.herokuapp.com/

### Running the app from terminal

```console
$ python3 yp.py 
[*] Search term: Nail salon
[*] Location: New york
[*] Radius (in miles): 10	
[*] Minimum rating (optional): 3
[*] Maximum rating (optional): 5

[*] 228 listings scraped. Saved in listings.csv
```


## Hosting on Heroku

__Important__: You need a [__verified__](https://devcenter.heroku.com/articles/account-verification) Heroku account to host this app, as it uses _Redistogo_ worker addon.  

You can host the app on Heroku by simply running a bash script, or manually doing all the steps yourself.

### Hosting on Heroku: Using bash script

```console
$ ./heroku.sh 
[*] YP API Key: API_KEY

[*] Creating Heroku app...
[*] Adding YP APIKey to the Environment Variables...
[*] Pushing to Heroku Git repo...
[*] Adding Redistogo addon...
[*] Starting the worker process...

[*] Completed. You can access the web-app at: https://ancient-gorge-40961.herokuapp.com/
[*] Logs stored in heroku.log
```

### Hosting on Heroku: Manually

1. __Create Heroku app__.
    
	```console
	$ heroku create
	Creating app... done, ⬢ fathomless-beach-85273
	https://fathomless-beach-85273.herokuapp.com/ | https://git.heroku.com/fathomless-beach-85273.git
	```

2. __Configure Environment Variables__. We need to add the YP.com API Key to the environment variables of the Heroku app so that it can access the API.

	```console
	$ heroku config:add YPAPIKey=API_KEY 
	Setting YPAPIKey and restarting ⬢ fathomless-beach-85273... done, v3
	YPAPIKey: 9ph6j2hpcz
	```

3. __Push to Heroku Git repo__.

	```console
	$ git push heroku master
	Counting objects: 120, done.
	Delta compression using up to 4 threads.
	Compressing objects: 100% (64/64), done.
	Writing objects: 100% (120/120), 58.57 KiB | 58.57 MiB/s, done.
	Total 120 (delta 46), reused 120 (delta 46)
	remote: Compressing source files... done.
	remote: Building source:
	remote: 
	remote: -----> Python app detected
	remote: -----> Installing python-3.6.4
	remote: -----> Installing pip
	remote: -----> Installing requirements with pip
	
	[Output Truncated]
	...

	remote:        Successfully installed Jinja2-2.10 MarkupSafe-1.0 Werkzeug-0.14.1 certifi-2018.1.18 chardet-3.0.4 click-6.7 flask-0.12.2 gunicorn-19.7.1 idna-2.6 itsdangerous-0.24 pyyaml-3.12 redis-2.10.6 requests-2.18.4 rq-0.10.0 urllib3-1.22
	remote: 
	remote: -----> Discovering process types
	remote:        Procfile declares types -> web, worker
	remote: 
	remote: -----> Compressing...
	remote:        Done: 44.2M
	remote: -----> Launching...
	remote:        Released v4
	remote:        https://fathomless-beach-85273.herokuapp.com/ deployed to Heroku
	remote: 
	remote: Verifying deploy... done.
	To https://git.heroku.com/fathomless-beach-85273.git
	 * [new branch]      master -> master
	 ```


4. __Add RedisToGo addon__.

	```console
	$ heroku addons:create redistogo:nano
	Creating redistogo:nano on ⬢ fathomless-beach-85273... free
	Created redistogo-silhouetted-31890 as REDISTOGO_URL
	Use heroku addons:docs redistogo to view documentation
	```

5. __Scale the worker dyno__.

	```console
	$ heroku ps:scale worker=1
	Scaling dynos... done, now running worker at 1:Free
	```
