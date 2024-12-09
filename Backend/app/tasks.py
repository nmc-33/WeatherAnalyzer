import pika
import json
import os
from urllib.parse import urlparse

def get_rabbitmq_connection():
    # Get the RabbitMQ connection URL from environment variables
    rabbitmq_url = os.getenv('CLOUDAMQP_URL')

    if not rabbitmq_url:
        raise ValueError("RABBITMQ_URL environment variable is not set")

    # Parse the URL to extract connection parameters
    url_parts = urlparse(rabbitmq_url)

    # Set up connection parameters for Pika
    connection_params = pika.ConnectionParameters(
        host=url_parts.hostname,            # Extract hostname from the URL
        port=5671,                # Extract port from the URL
        virtual_host=url_parts.path[1:],    # Extract virtual host from the URL (remove the leading '/')
        credentials=pika.PlainCredentials(url_parts.username, url_parts.password),
        ssl = True  # Extract credentials
    )

    # Return the connection parameters
    return connection_params

def send_to_queue(queue_name, data):
    connection_params = get_rabbitmq_connection()
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    
    # Declare the queue with durable=True so messages are not lost if RabbitMQ crashes
    channel.queue_declare(queue=queue_name, durable=True)
    
    # Publish the message to the queue with persistent delivery mode
    channel.basic_publish(
        exchange='', 
        routing_key=queue_name, 
        body=json.dumps(data), 
        properties=pika.BasicProperties(
            delivery_mode=2  # Make message persistent
        )
    )
    connection.close()

def start_consumer(queue_name, callback):
    connection_params = get_rabbitmq_connection()
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    
    # Declare the queue with durable=True so the queue survives server restarts
    channel.queue_declare(queue=queue_name, durable=True)
    
    # Set up the consumer and start consuming messages
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
    print(f"Listening to {queue_name}...")
    channel.start_consuming()

