from django.utils.html import format_html
from django.contrib import admin
from .models import (
	Level,
	Markers,
	Guidelines,
	Procedures,
	Choropleth
)

class ChoroplethAdmin(admin.ModelAdmin):
	LOW_INFO_PATH = "/static/data/images/lands_low_img_info.png"
	MOD_INFO_PATH = "/static/data/images/lands_mod_img_info.png"
	HIGH_INFO_PATH = "/static/data/images/lands_high_img_info.png"
	VERY_HIGH_INFO_PATH = "/static/data/images/lands_very_high_img_info.png"
	CONFIRM_INFO = "Take a moment to review each changes and make sure that the information below is correct."

	def admin_info(*args, **kwargs):
		return format_html(
			' <center><img src={} height="200" width="350"/></center>'
			'<br><u><h3>REMEMBER:</h3></u>'
			'<small> • File must be "geojson". </small></br>'
			'<small> • Changes might not reflect on the map instantly.</small></br>'
			'<small> • After saving we recommend any changes done for at least 24 hrs.</small>'
			'<small> When one level is changed this will affect other levels too, so be cautious.</small></br>'.format(*args, **kwargs)
			)

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return False

	fieldsets = (
		("LOW", {'fields':('low_risk_map',),'description': admin_info(LOW_INFO_PATH)}),
		("MODERATE", {'fields':('mod_risk_map',),'description': admin_info(MOD_INFO_PATH)}),
		("HIGH", {'fields': ('high_risk_map',),'description': admin_info(HIGH_INFO_PATH)}),
		("VERY HIGH", {'fields': ('very_high_risk_map',),'description': admin_info(VERY_HIGH_INFO_PATH)}),
		("CONFIRM", {'fields': ('admin','confirm_map','date_changed',),'description': '%s' % CONFIRM_INFO}),
	)
	

# admin.site.register(Level)
admin.site.register(Markers)
admin.site.register(Guidelines)
admin.site.register(Procedures)
admin.site.register(Choropleth, ChoroplethAdmin)

