from datetime import datetime, timedelta
import config

DEFAULT_CONFIGURE_REQUEST = config.DEFAULT_CONFIGURE_REQUEST
DEFAULT_CONFIGURE_INTERVAL = config.DEFAULT_CONFIGURE_INTERVAL

class Bucket:
    def __init__(self, url_name, maximum_request, interval_time):
        self.url_name = url_name
        self.maximum_request = maximum_request
        self.interval_time = interval_time

        self.start_time = datetime.now()
        self.token = maximum_request
        self.callable = True

    def set_maximum_request(self, new_maximum_request = DEFAULT_CONFIGURE_REQUEST):
        self.maximum_request = new_maximum_request

    def set_interval_time(self, new_interval_time = DEFAULT_CONFIGURE_INTERVAL):
        self.interval_time = new_interval_time

    def reset_bucket(self):
        self.token = self.maximum_request
        self.start_time = datetime.now()
        self.callable = True

    def get_bucket_status(self):
        return self.callable

    def reduce_token(self):
        self.token = self.token - 1

    def get_token(self):
        return self.token

    def get_url_name(self):
        return self.url_name

    def get_interval_time(self):
        return self.interval_time

    def bucket_timeout(self):
        self.callable = False
        self.start_time = datetime.now()

class Rate_limiter:
    def __init__(self):
        self.bucket_list = self.setup_bucket()
    
    def setup_bucket(self):
        BUCKET_LIST = config.BUCKET_LIST
        temp = []
        for bucket in BUCKET_LIST:
            temp.append(Bucket(bucket[0], bucket[1], bucket[2]))
        return temp
        
    def call(self, url_name):
        for bucket in self.bucket_list:
            if(bucket.get_url_name() == url_name):
                interval_time = bucket.get_interval_time()
                if(datetime.now() > bucket.start_time + timedelta(seconds = interval_time) or
                (not bucket.get_bucket_status() and datetime.now() > bucket.start_time + timedelta(seconds = 5))):
                    bucket.reset_bucket()

                if(bucket.get_token() > 0 and bucket.get_bucket_status()):
                    bucket.reduce_token()
                    return 200

                elif(bucket.get_token() == 0 and bucket.get_bucket_status()):
                    bucket.bucket_timeout()
                    return 429
                
                else:
                    return 429

    def configure(self, url_name, number_request = DEFAULT_CONFIGURE_REQUEST, interval_time = DEFAULT_CONFIGURE_INTERVAL):
        for bucket in self.bucket_list:
            if(bucket.get_url_name() == url_name):
                bucket.set_maximum_request(number_request)
                bucket.set_interval_time(interval_time)
                bucket.reset_bucket()

    def reset(self):
        for bucket in self.bucket_list:
            bucket.reset_bucket()