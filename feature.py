import pika
import logging
import json 
from db_manager import db_manager
from logging.handlers import TimedRotatingFileHandler
import os
from dotenv import load_dotenv
load_dotenv()

# this file will consume the datafrom rabbitmq_que and push the required fileds to db

class seg_main():
    def __init__(self,logger):
       self.logger = logger
    def main(self):
        cred = pika.PlainCredentials(os.environ.get("RABBIT_MQ_USER"),os.environ.get("RABBIT_MQ_PASSWORD"))
        connection= pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get("RABBIT_MQ_HOST"),
                                                        port=os.environ.get("RABBIT_PORT"),
                                                        connection_attempts=5,
                                                        credentials= cred))
        channel= connection.channel()
        status = "processing...."
        print("seg_main: initial status: " + status)
        def callbackFunctionForQueueA(ch,method,properties,body):
            data = json.loads(body)
            db_manager_obj = db_manager(data,db_name = os.environ.get("DB_NAME"),table_name = os.environ.get("TABLE_NAME"),logger=self.logger)
            status = db_manager_obj.insert_data()
            channel.close()
            return status
        channel.basic_consume(queue=os.environ.get("QUEUE"), on_message_callback=callbackFunctionForQueueA, auto_ack=True)
        channel.start_consuming()
        return status
        # while True:
        #     try:
        #         channel.basic_consume(queue=os.environ.get("QUEUE"), on_message_callback=callbackFunctionForQueueA, auto_ack=True)
        #     except:
        #         continue
        #         # print("error processing --------")
        #         # channel.basic_consume(queue=os.environ.get("QUEUE"), consumer_callback=callbackFunctionForQueueA, no_ack=True)
        #     try:    
        #         channel.start_consuming()
        #     except Exception as err:
        #             continue