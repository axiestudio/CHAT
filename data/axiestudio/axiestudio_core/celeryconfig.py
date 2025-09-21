# celeryconfig.py
import os

axiestudio_redis_host = os.environ.get("AXIESTUDIO_REDIS_HOST")
axiestudio_redis_port = os.environ.get("AXIESTUDIO_REDIS_PORT")
# broker default user

if axiestudio_redis_host and axiestudio_redis_port:
    broker_url = f"redis://{axiestudio_redis_host}:{axiestudio_redis_port}/0"
    result_backend = f"redis://{axiestudio_redis_host}:{axiestudio_redis_port}/0"
else:
    # RabbitMQ
    mq_user = os.environ.get("RABBITMQ_DEFAULT_USER", "axiestudio")
    mq_password = os.environ.get("RABBITMQ_DEFAULT_PASS", "axiestudio")
    broker_url = os.environ.get("BROKER_URL", f"amqp://{mq_user}:{mq_password}@localhost:5672//")
    result_backend = os.environ.get("RESULT_BACKEND", "redis://localhost:6379/0")
# tasks should be json or pickle
accept_content = ["json", "pickle"]
