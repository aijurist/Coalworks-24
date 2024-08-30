from confluent_kafka import Consumer, KafkaException
from config import config as consumer_config  # Rename to avoid conflict

def set_consumer_configs():
    consumer_config['group.id'] = 'iot-data'
    consumer_config['auto.offset.reset'] = 'earliest'
    consumer_config['enable.auto.commit'] = False
    consumer_config['bootstrap.servers'] = '192.168.137.1:9093'

def assignment_callback(consumer, partitions):
    for p in partitions:
        print(f'Assigned to {p.topic}, partition {p.partition}')

if __name__ == '__main__':
    set_consumer_configs()
    consumer = Consumer(consumer_config)
    consumer.subscribe(['iot-data'], on_assign=assignment_callback)

    while True:
        event = consumer.poll(1.0)
        if event is None:
            continue
        if event.error():
            raise KafkaException(event.error())
        else:
            val = event.value().decode('utf8')
            partition = event.partition()
            print(f'Received: {val} from partition {partition}')
            # consumer.commit(event)
