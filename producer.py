import json
import pika

params = pika.URLParameters('amqps://uqjzsryb:DrMIPPrtXTFsVZmGjdMYDRYItLt0yK0h@rattlesnake.rmq.cloudamqp.com/uqjzsryb')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='adminMS', body=json.dumps(body), properties=properties)
