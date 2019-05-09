from flask import Flask, request

from Hoteldb import Hotel_DB
from Rate_limiter import Rate_limiter
import config

app = Flask(__name__)
db = Hotel_DB()
rate_limiter = Rate_limiter()
LOCALHOST = config.LOCALHOST
PORT = config.PORT

DEFAULT_CONFIGURE_REQUEST = config.DEFAULT_CONFIGURE_REQUEST
DEFAULT_CONFIGURE_INTERVAL = config.DEFAULT_CONFIGURE_INTERVAL

@app.route('/')
def hello_world():
   return 'Hello World', 200

@app.route('/city', methods = ['GET'])
def get_city():
   city_name = request.args.get('city_name')
   ordering_type = request.args.get('ordering_type')

   if(ordering_type != 'ASC' and ordering_type != 'DESC'):
      return '', 400

   status_code = rate_limiter.call('city')
   if(status_code == 200):
      result = db.get_city(city_name, ordering_type)
      return result, status_code
   
   elif(status_code == 429):
      return '', status_code

@app.route('/room', methods = ['GET'])
def get_room():
   room_type = request.args.get('room_type')
   ordering_type = request.args.get('ordering_type')

   if(ordering_type != 'ASC' and ordering_type != 'DESC'):
      return '', 400

   status_code = rate_limiter.call('room')
   if(status_code == 200):
      result = db.get_room(room_type, ordering_type)
      return result, status_code
   
   elif(status_code == 429):
      return '', status_code

@app.route('/city/configure', methods = ['POST'])
def configure_city():
   interval_time = request.args.get('interval_time')
   number_requests = request.args.get('number_requests')

   
   if(interval_time != None):
      if(not interval_time.isdigit() and interval_time != None):
         return '', 400

   if(number_requests != None):
      if(not number_requests.isdigit() and number_requests != None):
         return '', 400

   if(interval_time == None):
      interval_time = DEFAULT_CONFIGURE_INTERVAL 

   if(number_requests == None):
      number_requests = DEFAULT_CONFIGURE_REQUEST

   if(type(interval_time) == str and interval_time.isdigit()):
      interval_time = int(interval_time)

   if(type(number_requests) == str and number_requests.isdigit()):
      number_requests = int(number_requests)

   rate_limiter.configure('city', number_requests, interval_time)
   return '', 200

@app.route('/room/configure', methods = ['POST'])
def configure_room():
   interval_time = request.args.get('interval_time')
   number_requests = request.args.get('number_requests')

   if(interval_time != None):
      if(not interval_time.isdigit() and interval_time != None):
         return '', 400

   if(number_requests != None):
      if(not number_requests.isdigit() and number_requests != None):
         return '', 400

   if(interval_time == None):
      interval_time = DEFAULT_CONFIGURE_INTERVAL 

   if(number_requests == None):
      number_requests = DEFAULT_CONFIGURE_REQUEST

   if(type(interval_time) == str and interval_time.isdigit()):
      interval_time = int(interval_time)

   if(type(number_requests) == str and number_requests.isdigit()):
      number_requests = int(number_requests)

   rate_limiter.configure('room', number_requests, interval_time)
   return '', 200

@app.route('/reset', methods = ['POST'])
def reset_rate_limit():
   rate_limiter.reset()
   return '', 200

if __name__ == '__main__':
   app.run(host = LOCALHOST, port = PORT, debug = True)