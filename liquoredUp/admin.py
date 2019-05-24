from django.contrib import admin

# Register your models here.
from liquoredUp.models import Product, PriceList, Competitor

admin.site.register(Product)
admin.site.register(PriceList)
admin.site.register(Competitor)