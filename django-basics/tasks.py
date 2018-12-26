from celery import shared_task
from django.conf import settings

from apps.products.utils import OrderPusher


@shared_task
def push_callback_into_3rd_service(data):
    pusher = OrderPusher(settings.RASA_LOGIN, settings.RASA_PASSWORD)
    pusher.push_callback(data)
    return True


@shared_task
def push_application_in_3rd_service(data):
    pusher = OrderPusher(settings.RASA_LOGIN, settings.RASA_PASSWORD)
    pusher.push_application(data)
    return True


@shared_task
def push_into_3rd_service(data):
    """
    Transfer data about order in rasa board
    :param data: order data in json format
    :return:
    """
    pusher = OrderPusher(settings.RASA_LOGIN, settings.RASA_PASSWORD)
    pusher.push_data(data)
    return True
