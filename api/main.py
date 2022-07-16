import asyncio
import json

from pydantic import BaseModel, StrictStr
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer, AIOKafkaClient
from fastapi import FastAPI

app = FastAPI()
loop = asyncio.get_event_loop()

KAFKA_INSTANCE = "localhost:9092"

producer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_INSTANCE)
consumer = AIOKafkaConsumer(
    "fastapi_kafka", bootstrap_servers=KAFKA_INSTANCE, loop=loop)


async def consume():
    await consumer.start()

    try:
        async for msg in consumer:
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )
    finally:
        await consumer.stop()


@app.on_event("startup")
async def startup_event():
    await producer.start()
    loop.create_task(consume())


@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()
    await consumer.stop()


class ProducerResponse(BaseModel):
    name: StrictStr
    message_id: StrictStr
    topic: StrictStr
    timestampe: StrictStr = ""


class ProducerMessage(BaseModel):
    name: StrictStr
    message_id: StrictStr = ""
    timestamp: StrictStr = ""


@app.post("/produce/{topicname}")
async def kafka_produce(msg: ProducerMessage, topicname: str):
    await producer.send(topicname, json.dumps(msg.dict()).encode("ascii"))

    response = ProducerResponse(
        name=msg.name, message_id=msg.message_id, topic=topicname,
    )

    return response
