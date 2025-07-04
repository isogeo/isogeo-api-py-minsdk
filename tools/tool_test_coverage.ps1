#################################################################
#
# Script to package and upload Isogeo Python package.
#
#################################################################

"-- STEP -- Creating virtualenv"
py -3 -m venv .venv_tests
./.venv_tests/Scripts/activate

"-- STEP -- Install and display dependencies within the virtualenv"
python -m pip install -U pip
python -m pip install --upgrade setuptools wheel
python -m pip install --upgrade -r ./requirements_dev.txt

"-- STEP -- Python code style"
python -m black --target-version=py37 ./isogeo_pysdk
python -m black --target-version=py37 ./tests

"-- STEP -- Run coverage"
# coverage run -m unittest discover -s tests/
python -m pytest --maxfail=2 --random-order --junitxml=junit/test-results.xml --cov-config=.coveragerc --cov=isogeo_pysdk --cov-report=xml --cov-report=html --cov-append tests

"-- STEP -- Build and open coverage report"
coverage html
Invoke-Item htmlcov/index.html

"-- STEP -- Exit virtualenv"
deactivate
