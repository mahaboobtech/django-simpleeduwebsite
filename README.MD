# this is just simple django authentication and also google authentication and simple education website which have courses where to buy 

### i used mysql so you need to remember this 
### and gather the google auth key and secret key and also form the razorpay

## required to make changes in settings.py 
+ data bases 
+ social account providers 
    cliend_id 
    secret
+ razarpay
    key_id
    key_secret

type on cli : 
+ python manage.py makemigrations
+ python manage.py migrate


later add create super user 
python manage.py createsuperuser
and setup the password

go to social application 
+ add  social application 
+ add client id and secret id where you gather form gooel cloud 
+ add website if your working on local host then 127.0.0.1:8000 and also domain display name 
+ save 

## now add courses what you want to add
+ add courses and price 

thats it done