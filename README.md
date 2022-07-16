# FastAPI Kafka Example

This is an example of how to integrate FastAPI with Kafka. 

To run this example, just clone the repo, run `docker-compose -f docker-compose.yml up` e after the Kafka & Zookeeper images were pulled e the containers were created, you must install the python dependencies. 

Then you run the app with `uvicorn api.main:app --reload`. 

After that just POST request to `localhost:8000/produce/fastapi_kafka` with the payload: 

```json
{
    "name": "some message"
}
```

Or, modify the models to suite your needs. 