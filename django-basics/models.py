from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.products.models import signal_handlers


class Site(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=30)
    link = models.CharField(
        verbose_name=_('link'), max_length=50, blank=True, null=True
    )
    ip_address = models.GenericIPAddressField(
        _("IP Address"), default="0.0.0.0"
    )
    additional_info = models.OneToOneField(
        'SiteSettings', related_name='site', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('web site')
        verbose_name_plural = _('web sites')

    def __str__(self):
        return self.title


class Preview(models.Model):
    color = models.ForeignKey(
        'Color', on_delete=models.CASCADE, related_name='previews'
    )
    model = models.ForeignKey(
        'Model', on_delete=models.CASCADE, related_name='previews', null=True,
        blank=True
    )
    images = ArrayField(
        models.CharField(max_length=50), default=list
    )

    class Meta:
        verbose_name = _('Preview')
        verbose_name_plural = _('Previews')


# bind signal handlers in apps.py on ready method.

models.signals.post_delete.connect(
    signal_handlers.remove_site_directory, sender=Site
)
models.signals.post_save.connect(
    signal_handlers.create_site_directory,
    sender=Site
)
models.signals.pre_delete.connect(
    signal_handlers.clean_preview_images,
    sender=Preview
)
