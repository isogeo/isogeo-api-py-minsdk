#################################################################
#
# Script to package and upload Isogeo Python package.
#
# PREREQUITES : fill the .pypirc file with your pypi credentials
#
#################################################################

# make a virtualenv to perform packaging
"-- STEP -- Creating temp virtualenv to perform dependencies packaging"
py -3 -m venv .venv_packaging
./.venv_packaging/Scripts/activate


# dependencies
"-- STEP -- Install and display dependencies within the virtualenv"
python -m pip install -U pip
python -m pip install --upgrade -r ./requirements.txt
python -m pip install --upgrade black twine

# apply black linter
python -m black --target-version=py37 .\isogeo_pysdk
python -m black --target-version=py37 .\tests

# remove previous builds
"-- STEP -- Clean up the previous builds"
rm -r build
rm -r dist
rm -r isogeo_pysdk.egg-info

# metadata
"-- STEP -- Prepare package's metadata"
python setup.py egg_info

# build
"-- STEP -- Build package: tar.gz and universal wheel"
python setup.py sdist
python setup.py bdist_wheel

# upload
"-- STEP -- Upload it to pypi"
# twine upload dist/* --config-file .\.pypirc

# remove virtualenv
"-- STEP -- Get out the virtualenv then remove it"
deactivate
#rm -r .venv_packaging
