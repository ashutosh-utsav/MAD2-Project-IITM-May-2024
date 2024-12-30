## for the app to running both front-end and back-end
    1> create a virtual env into root directry 
    2> run # python3 init_app.python3 //this will reset the database
    3> run # python3 app.python3   //will start the backend server

    4> cd to lmsmad2
    5> run #npm install   // to load node module
    6> run # npm run serve   // start the front end



## starting Redis Server for daily and monthly reminder
    sudo redis-server start
    redis-server

# ## stopping redis -server
    sudo service redis-server stop

# ## check if redis-server active
    redis-cli ping 
    respone should be "PONG"


## start celery worker for daily reminder
    celery -A app.celery_app worker --loglevel=INFO

## start celery beat
    celery -A app.celery_app beat --loglevel=INFO