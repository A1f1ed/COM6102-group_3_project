#!/bin/sh

if [ "$WAIT_FOR_DB" = "true" ]; then
    echo "Waiting for MySQL..."
    until mysqladmin ping -h mysql -u root -proot123 --silent; do
        echo "MySQL not ready, sleeping..."
        sleep 2
    done
    echo "MySQL is ready!"

    echo "Waiting for Redis..."
    until redis-cli -h redis ping; do
        echo "Redis not ready, sleeping..."
        sleep 2
    done
    echo "Redis is ready!"
fi

exec "$@"