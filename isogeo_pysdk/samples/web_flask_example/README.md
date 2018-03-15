Isogeo User oAuth2 example - Website with Flask
===============================================

*DO NOT USE THIS CODE IN PRODUCTION*

## Usage

Run this sample:

1. Clone/download this [repository](https://github.com/Guts/isogeo-api-py-minsdk),
2. Open a prompt (bash, powershell...),
3. move inside this directory `cd isogeo_pysdk\samples\web_flask_example`
4. Paste your `client_secrets.json` file inside `web_flask_example` directory. If you don't have, ask one to Isogeo!

### With your installed Python

1. Create a virtualenv (PowerShell: `py -3 -m  venv env`)

2. Install prerequisites:

	```powershell
	pip install --upgrade -r requirements.txt
	```

3. Run it:

	```python
	python runserver.py
	```

4. Open your favorite browser to [http://localhost:5000](http://localhost:5000)

### With Docker

```powershell
# build the container
docker build -t isogeo-oauth2-sample:latest .
# launch it in detached mode
docker run --name isogeo-websample -d -p 5000:5000 isogeo-oauth2-sample
```

Then, open your favorite browser to [http://localhost:5000](http://localhost:5000)
