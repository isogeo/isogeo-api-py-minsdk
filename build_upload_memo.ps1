<#dependencies#>
pip install twine --upgrade

<#metadata#>
python setup.py egg_info

<#build#>
python setup.py sdist
python setup.py bdist_wheel

<#upload#>
twine upload dist/* --config-file .\.pypirc
