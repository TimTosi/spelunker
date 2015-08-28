from django.contrib import admin

from .models import Blocks, Transactions, Inputs, Outputs, Ledger
# Register your models here.

class BlockAdmin(admin.ModelAdmin):
	list_display = ('real_number', 'block_hash', 'block_timestamp')

class TransactionAdmin(admin.ModelAdmin):
	list_display = ('id', 'block', 'input_count', 'output_count')

class InputAdmin(admin.ModelAdmin):
	list_display = ('id',)

class OutputAdmin(admin.ModelAdmin):
	list_display = ('id',)

class LedgerAdmin(admin.ModelAdmin):
	list_display = ('id',)

admin.site.register(Blocks, BlockAdmin)
admin.site.register(Transactions, TransactionAdmin)
admin.site.register(Inputs, InputAdmin)
admin.site.register(Outputs, OutputAdmin)
admin.site.register(Ledger, LedgerAdmin)
