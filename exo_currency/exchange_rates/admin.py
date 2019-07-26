# from categories.admin import CategoryBaseAdmin

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Register your models here.

from .models import Currency, CurrencyExchangeRate, Provider


class BaseAdmin(admin.ModelAdmin):
    save_on_top = True


class CurrencyAdmin(BaseAdmin):
    list_display = ('code', 'name', 'symbol')
    list_filter = ['code', 'name']
    search_fields = ('code', 'name', 'symbol')
    list_editable = ('name', 'symbol')


class CurrencyExchangeRateAdmin(BaseAdmin):
    list_display = ('source_currency', 'exchanged_currency', 'valuation_date', 'rate_value')
    list_filter = ['source_currency', 'exchanged_currency']
    search_fields = ('source_currency', 'exchanged_currency', 'valuation_date', 'rate_value')
    ordering = ('-valuation_date', '-rate_value')
    # list_select_related = ('source_currency', 'exchanged_currency',)


class ProviderAdmin(BaseAdmin):  # CategoryBaseAdmin bug
    list_display = ('slug', 'name', 'order', 'adapter', 'active')
    list_editable = ('name', 'order', 'adapter', 'active')
    search_fields = ('name', 'active')
    prepopulated_fields = {'slug': ('name',)}
    actions = ['activate', 'deactivate']
    ordering = ('-order', )

    fieldsets = (
        (None, {
            'fields': ('parent', 'name', 'adapter', 'order', 'active')
        }),
        (_('Meta Data'), {
            'fields': ('alternate_title', 'alternate_url', 'description',
                        'meta_keywords', 'meta_extra'),
            'classes': ('collapse',),
        }),
        (_('Advanced'), {
            'fields': ('thumbnail', 'slug'),
            'classes': ('collapse',),
        }),
    )

    def move(self, obj):
        return '<a href="#" class="move up">&uarr;</a> <a href="#" class="move down">&darr;</a>'

    move.allow_tags = True

    def get_form(self, request, obj=None, **kwargs):
        # self.exclude = ("thumbnail", "thumbnail_width", "thumbnail_height")
        # self.exclude = ("meta_extra", )
        form = super(ProviderAdmin, self).get_form(request, obj, **kwargs)
        return form

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyExchangeRate, CurrencyExchangeRateAdmin)
admin.site.register(Provider, ProviderAdmin)
