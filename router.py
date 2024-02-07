import pika
import json
import os 
from dotenv import load_dotenv
load_dotenv()

class rabbit_mq_data_manager():
    def __init__(self,logger):
       self.logger = logger

    def rabbit_mq_uploader(self,message):
      #declaring the credentials needed for connection like host, port, username, password, exchange etc
      cred = pika.PlainCredentials(os.environ.get("RABBIT_MQ_USER"),os.environ.get("RABBIT_MQ_PASSWORD"))
      connection= pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get("RABBIT_MQ_HOST"),
                                                      port=os.environ.get("RABBIT_PORT"),
                                                      connection_attempts=5,
                                                      credentials= cred))
      channel= connection.channel()
      channel.exchange_declare(os.environ.get("EXCHANGE"), durable=True, exchange_type="topic")
      channel.queue_declare(queue=os.environ.get("QUEUE"))
      channel.queue_bind(exchange=os.environ.get("EXCHANGE"), queue=os.environ.get("QUEUE"), routing_key=os.environ.get("ROUTING_KEY"))
      channel.basic_publish(exchange=os.environ.get("EXCHANGE"), routing_key=os.environ.get("ROUTING_KEY"), body= json.dumps(message))
      channel.close()
      print("pushed to rabbit mq success", message)
      return {"status": "pushed to rabbit mq success"}