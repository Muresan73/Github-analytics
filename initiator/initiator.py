import json
import datetime
import logging
import pulsar

logging.basicConfig(level=logging.INFO)

def main():
    date = datetime.date(2020, 1 ,1)
    dateEnd = datetime.date(2021, 5 ,30)

    # send to pulsar all dates
    client = pulsar.Client('pulsar://pulsar:6650')
    producer = client.create_producer('dates')
    
    inDatespan = date < dateEnd
    while True:
        if date.year == 2021 and date.month == 5 and date.day == 31:
            client.close()
            break
        for pageNum in range(1, 11):
            message = {"date": date.strftime('%d-%m-%Y'),
                       "page": pageNum}
            jsonMessage = json.dumps(message)
           
            logging.info("Sending message: %s" % jsonMessage)
            producer.send((jsonMessage).encode('utf-8'))
        date = date + datetime.timedelta(days=1)
    while True:
        logging.info("Sleeping")
        time.sleep(3600)
if __name__ == "__main__":
    main()