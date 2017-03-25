# ENVIRONMENT:
    > https://tutorial.djangogirls.org/en/installation/
	> https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip
	> https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation
	
# REQUIREMENTS WINDOWS:
	> Install Python 2.7.12 or latest 
		https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi
		
	> Configure environment variables:
	
		PYTHONPATH=<pathPython> (Example: C:\Python27\)
		PATH=%PATH%;%PYTHONPATH%\Scripts
		
	On Linux or OS X:
	
		pip install -U pip setuptools

	On Windows:
	
		python -m pip install -U pip setuptools
		
	> Update pip:
	
		python -m pip install --upgrade pip
		
	> Install Django:
	
		python -m pip install django

	python -m pip install virtualenvwrapper
	python -m pip install Pillow

# RUN SERVER:
    > python manage.py runserver

# SERVER:

   > http://127.0.0.1:8000