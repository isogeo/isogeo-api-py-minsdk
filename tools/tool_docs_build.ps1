#############################################################################
#
# Script to build documentation of Isogeo Python package.
#
# Prerequisites: download markupsafe and pyyaml wheels into libs subdirectory
#
#############################################################################

# make a virtualenv to perform packaging
"-- STEP -- Creating temp virtualenv to perform dependencies packaging"
py -3 -m venv .venv_docs
./.venv_tests/Scripts/activate

# dependencies
"-- STEP -- Install and display dependencies within the virtualenv"
python -m pip install -U pip
python -m pip install -U setuptools wheel
python -m pip install -U -r ./requirements_dev.txt

# remove previous builds
"-- STEP -- Clean up previous build"
Remove-Item docs/_build/* -Recurse

# build
"-- STEP -- Build docs"
sphinx-apidoc -e -f -M -o ./docs/_apidoc ./isogeo_pysdk ./isogeo_pysdk/samples
./docs/make.bat html

"-- STEP -- Get out the virtualenv"
deactivate
Invoke-Item ./docs/_build/html/index.html
Remove-Item .venv_docs -Recurse 
