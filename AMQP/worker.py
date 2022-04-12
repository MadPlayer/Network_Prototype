import sys
import time
import pika
from pika.credentials import PlainCredentials


def callback(ch, method, properties, body, sec):
    print(f" [x] Received {body.decode()}")
    time.sleep(sec)
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    param = pika.ConnectionParameters(host="localhost",
                                      credentials=PlainCredentials(sys.argv[1],
                                                                   "test"))
    with pika.BlockingConnection(param) as conn:
        channel = conn.channel()
        channel.basic_qos(prefetch_count=1)
        channel.queue_declare('hello')
        channel.basic_consume(queue='hello', #auto_ack=True,
                              on_message_callback=lambda ch, method, properties,
                              body: callback(ch, method, properties, body,
                                             float(sys.argv[2])))
        print(f" [{sys.argv[1]}] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
