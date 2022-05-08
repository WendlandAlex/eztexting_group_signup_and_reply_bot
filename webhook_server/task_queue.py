import redis
import rq
import os

redis_conn = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379'))
with rq.Connection(redis_conn):
    in_queue = rq.Queue(name='in_queue')
    out_queue = rq.Queue(name='out_queue')

if __name__ == '__main__':
    worker = rq.Worker([in_queue, out_queue], connection=redis_conn)
    worker.work()