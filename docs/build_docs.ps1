#############################################################################
#
# Script to build documentation of Isogeo Python package.
#
# Prerequisites: download markupsafe and pyyaml wheels into libs subdirectory
#
#############################################################################

# make a virtualenv to perform packaging
"-- STEP -- Creating temp virtualenv to perform dependencies packaging"
py -3 -m venv env3_docs
./env3_docs/Scripts/activate

# dependencies
"-- STEP -- Install and display dependencies within the virtualenv"
python -m pip install -U pip
pip install --upgrade setuptools wheel
pip install MarkupSafe PyYAML --find-links=libs
pip install -r ./requirements_docs.txt

# remove previous builds
"-- STEP -- Clean up previous build"
rm -r _build/*

# build
"-- STEP -- Build docs"
sphinx-apidoc -e -f -M -o .\_apidoc\ ..\isogeo_pysdk\ ..\isogeo_pysdk\samples\
./make.bat html

"-- STEP -- Get out the virtualenv"
deactivate
# rm -r env3_docs
Invoke-Item _build/html/index.html
