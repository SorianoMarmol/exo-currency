from categories.models import Category

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save  # , pre_save
from django.dispatch import receiver


class Provider(Category):
    adapter = models.CharField(max_length=10, choices=getattr(settings, "PROVIDER_ADAPTERS"), unique=True)

    class Meta(Category.Meta):
        verbose_name_plural = 'Providers'
        unique_together = ()  # avoid error due to fields are not local to model

    class MPTTMeta:
        order_insertion_by = ('order', 'name')

    def __str__(self):
        return self.name

    @property
    def get_adapter_path(self):
        """Get adapter backend class path"""
        return dict(getattr(settings, "PROVIDER_ADAPTERS")).get(self.adapter)


@receiver(post_save, sender=Provider)
def set_order(sender, instance, *args, **kwargs):
    if not instance.order:
        instance.order = instance.id
        instance.save()


# @receiver(pre_save, sender=Provider)
# def rebuild_tree(sender, instance, *args, **kwargs):
#     Provider.tree.rebuild()


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(Currency, related_name='exchanges', on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency, related_name='inversed_exchanges', on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)  # created is a datetime field, but we could use it as valuation_date
    rate_value = models.DecimalField(db_index=True, decimal_places=6, max_digits=18)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def parsed_data(self):
        # settings mapping?
        data = {
            'source_currency': self.source_currency.code,
            'exchanged_currency': self.exchanged_currency.code,
            'rate_value': str(self.rate_value),
            'valuation_date': str(self.valuation_date),
        }
        if getattr(settings, "SHOW_PROVIDER") and self.provider:
            data["provider"] = self.provider.name
        return data
