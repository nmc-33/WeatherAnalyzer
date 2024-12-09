import pika
import json

def send_to_queue(queue_name, data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange='', 
        routing_key=queue_name, 
        body=json.dumps(data), 
        properties=pika.BasicProperties(
                delivery_mode=2  # Make message persistent
            ))
    connection.close()

def start_consumer(queue_name, callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable = True)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
    print(f"Listening to {queue_name}...")
    channel.start_consuming()