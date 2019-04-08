Isogeo Search Form - Desktop sample based on Tkinter TTK
========================================================

*DO NOT USE THIS CODE IN PRODUCTION*

## Usage

Run this sample:

1. Clone/download this [repository](https://github.com/Isogeo/isogeo-api-py-minsdk),
2. Open a prompt (bash, powershell...),
3. Move inside this directory `cd isogeo_pysdk\samples\desktop_ttk_search_form`
4. Paste your `client_secrets.json` file inside `desktop_ttk_search_form` directory. If you don't have, ask one to Isogeo!

### With your installed Python

1. Create a virtualenv (PowerShell: `py -3 -m  venv env`), then activate it

2. Install prerequisites:

	```bash
	pip install --upgrade -r requirements.txt
	```

3. Run it:

	```python
	# using autocompletion widgets and async/await
	python isogeo_tk_search_form_py3_async.py
	# using 'pure' ttk library
	python isogeo_tk_search_form_pure.py
	```
