import threading

from redis import Redis

from configuration import Configuration


def deamon(id):
    with Redis(Configuration.REDIS_HOST) as redis:
        sub = redis.pubsub()
        sub.subscribe(Configuration.REDIS_SUBSCRIBE_CHANNEL)
        for item in sub.listen():
            bytes = redis.lpop(Configuration.REDIS_VOTES_KEY)
            while (bytes):
                vote = bytes.decode("utf-8").split(",")
                print("\n{} {} thread: {}\n".format(vote[0], vote[1], id))
                bytes = redis.lpop(Configuration.REDIS_VOTES_KEY)


if __name__ == '__main__':
    threading.Thread(target=deamon, args=(1,)).start()
    threading.Thread(target=deamon, args=(2,)).start()
