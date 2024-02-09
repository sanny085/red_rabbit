from flask import Flask,request,jsonify
from router import rabbit_mq_data_manager
from db_manager import db_manager
from dotenv import load_dotenv
from feature import seg_main
import os 
import pika 
import json  
import logging
from logging.handlers import TimedRotatingFileHandler 
load_dotenv()

app = Flask(__name__)
@app.route("/route_payload_to_rabbitmq", methods=['POST','GET'])
def route_payload_to_rabbitmq():
    if request.method == 'POST': 
        logger.info("Sucess POST api call....")
        logger.info("Received POST request:")
        logger.info("Request JSON data: %s", request.json)
        print("new", request.json)
        print("processing the route_payload_to_rabbitmq")
        '''this function will consume and post the payload from  UI to rabbit_mq:'''
        rabbit_mq_uploader_status = rabbit_mq_data_manager_obj.rabbit_mq_uploader(request.json)
        logger.info("Rabbit MQ Response - ", rabbit_mq_uploader_status)
        print("Rabbit MQ Response - ", rabbit_mq_uploader_status)
        print("Sucessfully pushed to rabbit-mq")
        # seg_main_result = seg_main_obj.main()
        logger.info("end processing")
        
        return rabbit_mq_uploader_status #seg_main_result

    elif request.method == 'GET' : # true for get response "GET"
        logger.info("processing GET api call....")
        column_name =  "_id"# To do : need to update "column_name" before deployment 
        search_id = request.json["_id"] # search id will be used to quey the db and fetch a record.
        db_manager_obj = db_manager({},db_name = os.environ.get("DB_NAME"),table_name = os.environ.get("TABLE_NAME"),logger = logger)
        xy_coords = db_manager_obj.search_data(column_name, search_id)
        logger.info("end processing")
        return xy_coords
   

if __name__ == '__main__':
  
    log_filename = 'checker.log'
    logging.getLogger().setLevel(logging.ERROR)
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(log_filename, when="midnight", backupCount=4)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.info("started processing")
    rabbit_mq_data_manager_obj = rabbit_mq_data_manager(logger) #this class will route the payload to rabbit mq
    seg_main_obj = seg_main(logger)
    host = "0.0.0.0"
    app.run(debug=True,host=host,port=5008)

    # app.run (host = os.environ.get("ENDPOINT_HOST") , port = os.environ.get("ENDPOINT_PORT") )