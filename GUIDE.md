For rabbitmq first instal erlang 

run cmd as admin 

rabbitmqctl.bat status

https://www.rabbitmq.com/install-windows-manual.html#start-as-application

https://www.rabbitmq.com/access-control.html

celery --app django_project worker -l info --pool=solo

Add workers in tasks.py in app_modules ,
restart celery instance for changes to reflect 

