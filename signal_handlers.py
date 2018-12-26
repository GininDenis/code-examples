import errno
import os
import shutil

from django.conf import settings


def create_site_directory(**kwargs):
    """
    Create sie directory for synchronization with remote service using
    additional micro-service which listens RabbitMQ queue.
    """
    site_name = kwargs['instance'].title
    dir_path = os.path.join(settings.MEDIA_ROOT, site_name)
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise exc


def remove_site_directory(**kwargs):
    """
    Remove site directory if instance was deleted
    """
    site_name = kwargs['instance'].title
    dir_path = os.path.join(settings.MEDIA_ROOT, site_name)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)


def clean_preview_images(**kwargs):
    """
    Remove all previews, which were created using parsing of remote service
    for the deleting instance.
    """
    object_images = kwargs['instance'].images
    for path in object_images:
        file_path = os.path.join(settings.BASE_DIR, path)
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass
