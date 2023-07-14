from map_auxiliary.models import Warning_Devices, Evac_Centers, Warning_Signs
from .models import Markers, Procedures, Guidelines
from django.shortcuts import render, redirect
from auxiliary.models import News
from map_auxiliary.utils import set_marker
from folium import plugins, IFrame
from django.views import View
import folium
import branca
import os


class LandslideView(View):
	center_coord = [6.1726,125.3671]
	evac_centers = Evac_Centers.objects.all()
	warning_signs = Warning_Signs.objects.all()
	warning_devices = Warning_Devices.objects.all()
	guidelines = Guidelines.objects.all()
	news = News.objects.all()[:3]
	procedures = Procedures.objects.all()
	landslide_markers = Markers.objects.all()
	template_name = 'landslide/landslide.html'
	static_dir = os.path.join('landslide','static','data')
	dynamic_dir = os.path.join('choropleth_storage','dynamic','landslide_map')
	
	def post(self, request):
		return render(request,LandslideView.template_name)

	def get(self, request):
		landslide_map = folium.Map(location=self.center_coord,zoom_start=11,control_scale=True,zoom_control=True,max_bounds=True,tiles=None)
		map_size = branca.element.Figure(height="100%")
		map_size.add_child(landslide_map)

		mapBorderStyle = {'color':'#555555','weight':1,'fillColor':'rgba(0,0,0,0)'}
		veryHighStyle = {'weight':0,'fillColor':'red','fillOpacity':0.5}
		highStyle = {'weight':0,'fillColor':'orangered','fillOpacity':0.5}
		modStyle = {'weight':0,'fillColor':'green','fillOpacity':0.5}
		lowStyle = {'weight':0,'fillColor':'yellow','fillOpacity':0.5}
		
		very_high_lvl_file = os.path.join(self.dynamic_dir,"very_high_lvl.geojson")
		high_lvl_file = os.path.join(self.dynamic_dir,"high_lvl.geojson")
		mod_lvl_file = os.path.join(self.dynamic_dir,"mod_lvl.geojson")
		low_lvl_file = os.path.join(self.dynamic_dir,"low_lvl.geojson")
		map_border_file = os.path.join(self.static_dir,"Boundary.geojson")

		# "Map Border" should always be rendered first on the map (sequence is important).
		folium.GeoJson(map_border_file,name='Municipal Boundary',control=False,style_function=lambda x:mapBorderStyle).add_to(landslide_map)
		folium.GeoJson(low_lvl_file,name='Low',style_function=lambda x:lowStyle).add_to(landslide_map)
		folium.GeoJson(mod_lvl_file,name='Moderate',style_function=lambda x:modStyle).add_to(landslide_map)
		folium.GeoJson(high_lvl_file,name='High',style_function=lambda x:highStyle).add_to(landslide_map)
		folium.GeoJson(very_high_lvl_file,name='Very High',style_function=lambda x:veryHighStyle).add_to(landslide_map)
		
		# Map Layers	
		folium.raster_layers.TileLayer(tiles='Stamen Terrain',name='Auxiliary Map',min_zoom=11,overlay=True,control=False).add_to(landslide_map)		
		folium.raster_layers.TileLayer(tiles='Open Street Map',name='Landslide GeoHazard Map',min_zoom=11,overlay=False).add_to(landslide_map)
		folium.raster_layers.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
			name='Satellite View',
			attr='Esri',
			min_zoom=11,
			overlay=False).add_to(landslide_map)
		

		for marker in self.landslide_markers:
			html = set_marker(marker)
			popup = folium.Popup(html, max_width=200, max_height=300)
			barangay_markers = folium.Marker(
				location=[marker.latitude,marker.longitude],
				popup=popup,
				tooltip="Click For More",
				icon=folium.Icon(color="green",icon="glyphicon-flag")).add_to(landslide_map)

		# Emergency and Warning Systems Markers
		device_group = folium.FeatureGroup(name="Warning Systems & Evac Centers",overlay=False)
		evac_group = plugins.FeatureGroupSubGroup(device_group,control=False)
		sign_group = plugins.FeatureGroupSubGroup(device_group,control=False)

		list_devices = []
		list_centers = []
		list_signs = []

		# Warning Systems
		for device in self.warning_devices:
			html = set_marker(device)
			popup = folium.Popup(html, max_width=200, max_height=300)
			device_markers = folium.Marker(
				location=[device.latitude,device.longitude],
				popup=popup,
				icon=folium.Icon(color="red",icon="glyphicon-bullhorn"))

			list_devices.append(device_markers)

			for device in list_devices:
				device.add_to(device_group)

		# Evacuation Centers
		for building in self.evac_centers:
			html = set_marker(building)
			popup = folium.Popup(html, max_width=200, max_height=300)
			evac_markers = folium.Marker(
				location=[building.latitude,building.longitude],
				popup=popup,
				icon=folium.Icon(color="orange",icon="glyphicon-home"))

			list_centers.append(evac_markers)
				
			for building in list_centers:
				building.add_to(evac_group)

		# Warning Signs
		for sign in self.warning_signs:
			html = set_marker(sign)
			popup = folium.Popup(html, max_width=200, max_height=300)
			sign_markers = folium.Marker(
				location=[sign.latitude,sign.longitude],
				popup=popup,
				icon=folium.Icon(color="blue",icon="glyphicon-exclamation-sign"))

			list_signs.append(sign_markers)
				
			for sign in list_signs:
				sign.add_to(sign_group)

		# add marker group to map
		device_group.add_to(landslide_map)
		evac_group.add_to(landslide_map)
		sign_group.add_to(landslide_map)

		# add minimap to map
		minimap = plugins.MiniMap(toggle_display=True)
		landslide_map.add_child(minimap)

		# add full screen button to map
		plugins.Fullscreen(position='topleft').add_to(landslide_map)

		# add latitude and longitude tool to map
		landslide_map.add_child(folium.LatLngPopup())

		folium.LayerControl().add_to(landslide_map)
		landslide_map = landslide_map._repr_html_()

		context = {
			'news':self.news,
			'guidelines':self.guidelines,
			'procedures':self.procedures,
			'landslide_markers':self.landslide_markers,
			'landslide_map':landslide_map,
			'title':'Landslide Map'
			}

		return render(request,LandslideView.template_name, context)