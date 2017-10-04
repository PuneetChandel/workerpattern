# workerpattern  
worker pattern using rabbit MQ, celery and MongoDB  

1. Install RabbitMQ  
2. setup rabbitMQ for celery   
http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html    
- create user and set permissions for virtual host 
- create virtual host    

  abbitmqctl add_user puneet welcome1   
  rabbitmqctl add_vhost feedvhost  
  rabbitmqctl set_user_tags puneet dev  
  rabbitmqctl set_permissions -p feedvhost puneet ".*" ".*" ".*" 

- start rabbit mq server : rabbitmq-server  
- to monitor http://localhost:15672 , can create a user with monitor role to monitor queues  

3. create virtual env for your project  and install celery,pymongo,PyYAML    
virtualenv vworkpatt   
source source vworkpatt/bin/activate  
pip install celery pymongo PyYAML    

4. If you are using pyCharm use the virtual env just created  


5. run rabbit mq : rabbitmq-server  
6. rn mongodb : mongod  
7. start celery :   
  celery -A tasks.feedtask.celery worker -Q usage_queue --loglevel=info  
  
8. start flask app   
python3 app.py  

Post Feeds : http://0.0.0.0:4001/Usagefeed  

Get job status : http://0.0.0.0:4001/Usagefeed/261d6625-d18e-4945-85da-8f89ff388cf6  


9 . freeze env to generate requirements.txt    
pip freeze > requirements.txt    

10. To run celery with concurrency option  
celery -A tasks.feedtask.celery worker -Q usage_queue --loglevel=info --concurrency=20  

11. for scaling  
celery -A tasks.feedtask.celery worker -Q usage_queue --loglevel=info --autoscale=10,3  



References:  
http://flask.pocoo.org/docs/0.11/patterns/celery/  
http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html  
