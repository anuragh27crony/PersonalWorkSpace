import random


def get_data():
    """Return 3 random integers between 0 and 9"""
    sample = random.sample(range(10), 3)
    print("Get_Data: Sample is " + str(sample))
    return sample


def consume():
    """Displays a running average across lists of integers sent to it"""
    print("consume: Starting")
    running_sum = 0
    data_items_seen = 0
    print("consume: Now entering While Loop")
    while True:
        print("consume: Hitting Yeild now")
        data = yield
        print("consume: Data is printed " + str(data))
        # print(data)
        data_items_seen += len(data)
        running_sum += sum(data)
        print('The running average is {}'.format(running_sum / float(data_items_seen)))


def produce(consumer):
    """Produces a set of values and forwards them to the pre-defined consumer
    function"""
    print("Produce: Before While Loop")
    while True:
        print("Produce: Start of the Loop")
        data = get_data()
        print('Produce : Produced {}'.format(data))
        consumer.send(data)
        print('Produce : Hitting Yield')
        yield


if __name__ == '__main__':
    consumer = consume()
    print("Main Loop: Sending None now")
    consumer.send(None)
    producer = produce(consumer)
    print("Main Loop: Producer is Initialized")
    for _ in range(2):
        print('Main Loop: Producing...')
        next(producer)
