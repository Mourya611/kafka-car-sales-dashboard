import requests
from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.json_schema import JSONDeserializer

# Kafka & Schema Registry Config
API_KEY = 'CNRXSNKA7C634ZNJ'
ENDPOINT_SCHEMA_URL = 'https://psrc-4yovk.us-east-2.aws.confluent.cloud'
API_SECRET_KEY = 'Hm6qkU4xni3Lh5EMPhPKPH20/enns5WSf4Q+oUtDkjDsgM6iuziW5R9HHqGPJgry'
BOOTSTRAP_SERVER = 'pkc-921jm.us-east-2.aws.confluent.cloud:9092'
SECURITY_PROTOCOL = 'SASL_SSL'
SSL_MACHENISM = 'PLAIN'
SCHEMA_REGISTRY_API_KEY = 'C5365OASJEYNM7R6'
SCHEMA_REGISTRY_API_SECRET = 'Mc8uvXkjd5JJ/RRBvJgWVt2t5eBJvQW8AfWLKrq3w3NVcJTA60sGYcjOGWC+W3n3'

def sasl_conf():
    return {
        'sasl.mechanism': SSL_MACHENISM,
        'bootstrap.servers': BOOTSTRAP_SERVER,
        'security.protocol': SECURITY_PROTOCOL,
        'sasl.username': API_KEY,
        'sasl.password': API_SECRET_KEY
    }

def schema_config():
    return {
        'url': ENDPOINT_SCHEMA_URL,
        'basic.auth.user.info': f"{SCHEMA_REGISTRY_API_KEY}:{SCHEMA_REGISTRY_API_SECRET}"
    }

class Car:
    def __init__(self, record: dict):
        for k, v in record.items():
            setattr(self, k, v)
        self.record = record

    @staticmethod
    def dict_to_car(data: dict, ctx):
        return Car(record=data)

    def __str__(self):
        return f"{self.record}"

def send_to_flask(car_data):
    try:
        res = requests.post("http://127.0.0.1:5000/new_car", json=car_data)
        if res.status_code == 200:
            print("✅ Order received and sent to Flask.")
        else:
            print(f"⚠️ Flask error: {res.status_code}")
    except Exception as e:
        print("❌ Error sending to Flask:", e)

def main(topic):
    schema_str = """
    {
      "$id": "http://example.com/myURI.schema.json",
      "$schema": "http://json-schema.org/draft-07/schema#",
      "additionalProperties": false,
      "description": "Sample schema to help you get started.",
      "properties": {
        "brand": {"type": "string"},
        "car_name": {"type": "string"},
        "engine": {"type": "number"},
        "fuel_type": {"type": "string"},
        "km_driven": {"type": "number"},
        "max_power": {"type": "number"},
        "mileage": {"type": "number"},
        "model": {"type": "string"},
        "seats": {"type": "number"},
        "seller_type": {"type": "string"},
        "selling_price": {"type": "number"},
        "transmission_type": {"type": "string"},
        "vehicle_age": {"type": "number"}
      },
      "title": "SampleRecord",
      "type": "object"
    }
    """
    json_deserializer = JSONDeserializer(schema_str, from_dict=Car.dict_to_car)

    consumer_conf = sasl_conf()
    consumer_conf.update({
        'group.id': 'car-sales-group',
        'auto.offset.reset': "latest"
    })

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    print(f"🎧 Listening to Kafka topic: {topic}")

    while True:
        try:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            car = json_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))

            if car is not None:
                print("🚗 New car sold:", car.record)
                send_to_flask(car.record)

        except KeyboardInterrupt:
            print("🛑 Stopping consumer...")
            break
        except Exception as e:
            print("❌ Error in consumer:", e)

    consumer.close()

# Run it
main("text-topic-1")
