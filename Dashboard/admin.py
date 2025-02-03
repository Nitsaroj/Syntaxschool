from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_coins', 'spend_coins', 'reward_coins')

@admin.register(CoinHistory)
class CoinHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'coin_type', 'amount', 'timestamp')
    list_filter = ('coin_type',)