# Home-Test-Agoda
This project is a part of the my interview process with Agoda. THis project was made by Sirapop Issariyodom.
To look this project on Github, please use this given link https://github.com/tigerSI/Home-Test-Agoda

Requirements:
1.) Python version 3.6+, you can download it from https://www.python.org/
2.) Open the cmd in windows or terminal in macos, and open the directory of this project.
    Then, use this command:
        pip install -r requirements.txt
    To install required library for this project.

Run Project:
1.) Open the directory of this project in cmd or terminal.
2.) use this command: 
        python server.py
    To start the server, run the server.py to start the server.

3.) open google chrome or others and using url http://localhost:8080/
    - there are 4 types of endpoints with params
        - 2 GET http requests
        - /city with 2 params city_name and ordering_type Ex. /city?city_name=Bangkok&ordering_type=ASC
        - /room with 2 params room_type and ordering_type Ex. /room?room_type=Deluxe&ordering_type=ASC

        - 2 POST http requests
        - /city/configure with 2 params interval_time and number_requests Ex. /room/configure?interval_time=10&number_requests=2
        - /room/configure with 2 params interval_time and number_requests Ex. /city/configure?interval_time=10&number_requests=2

Description:
In this section, I explain how each file works and including my decision for each point.

Server.py - I decided to use Flask as a server of this project because I familiar with this library. I implemented server and endpoints in this file.

Rate_limiter.py - It is the main point of this project. This rate limiter has to read the data from config file to know the endpoint in the project.
    I separate each endpoint in to be a bucket which consists of endpoint name, interval time, and maximum request. Moreover, in the bucket, it has status(it shows is it timeout or not) and start time(keep the time when it gets first request from each interval or when it timeout) which I use these variables to calculate what each endpoint should return.

Hoteldb.py - It is similar with the database, I use the given hoteldb.csv as a database of this project.
Test.py - It is the integration test of this project which I implemented to cover the code coverage as much as I can to prevent the wrong output.

