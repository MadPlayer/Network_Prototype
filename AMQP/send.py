import time
import pika
from pika.credentials import PlainCredentials

if __name__ == '__main__':
    param = pika.ConnectionParameters(host="localhost",
                                      credentials=PlainCredentials("client1", "test"))
    with pika.BlockingConnection(param) as conn:
        channel = conn.channel()
        channel.queue_declare(queue='hello')

        for i in range(100):
            channel.basic_publish(exchange='',
                                  routing_key='hello',
                                  body=f'hello world! {i}')
            time.sleep(0.5)

        print(" [x] Sent 'Hello World'")
