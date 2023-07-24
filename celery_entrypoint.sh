#!/bin/sh
celery -A app.celery worker -B --loglevel=DEBUG -P solo
