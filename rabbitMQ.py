import pika


credentials = pika.PlainCredentials('qujpjozv', 'wsBGUue41YakvOm342EjLb2DVt5MEk9w')
parameters = pika.ConnectionParameters('cougar-01.rmq.cloudamqp.com', 5672, 'qujpjozv', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()


def add_to_queue(num):
    channel.queue_declare(queue='requests_queue')
    channel.basic_publish(exchange='', routing_key='requests_queue', body=str(num))
    # Close the connection
    # connection.close()

def show_content_of_queue():
    channel.queue_declare(queue='requests_queue')

    def callback(ch, method, properties, body):
        print(int(body))
    # Start consuming messages
    channel.basic_consume(queue='requests_queue', on_message_callback=callback, auto_ack=True)

    print("Waiting for messages. To exit, press CTRL+C")
    channel.start_consuming()

    # Close the connection
    connection.close()


# add_to_queue(4)
# show_content_of_queue()


