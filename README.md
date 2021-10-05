# social_feed
## setup a virtual env before installing dependencies
### installing virtualenv
`pip install virtualenv`
### creating virtual env
`virtualenv venv`
### activating venv
`venv\Scripts\activate`
### deactivating venv
`venv\Scripts\deactivate.bat`
## To install dependencies run the below command while venv is activated
`pip install -r requirements.txt`
## run the app
`python manage.py runserver`

PS: before running pls create u r own mongodb collection and facebook app and use it by updating settings.py
