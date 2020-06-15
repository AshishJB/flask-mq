import pika
from flask import Flask, flash, request, redirect, url_for

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def hello():
    return "hello"

@app.route('/publish',methods=['GET', 'POST'])
def publish():
    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    connection.close()
    return "hello"

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

@app.route('/consume',methods=['GET', 'POST'])
def consume():   
    channel.basic_consume(
        queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    return "waiting for messages"


if __name__ == '__main__':
    app.run(host='0.0.0.0')