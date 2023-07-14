from map_auxiliary.utils import FloodFileRename, MapInfo
from django.contrib.auth.models import User
from django.utils import timezone as tz
from django.db import models
from PIL import Image
import uuid
import os

class Level(models.Model):
	RESPONSE_LEVEL = (
		('N/A', 'N/A'),
		('Level 1', 'Level 1'),
		('Level 2', 'Level 2'),
		('Level 3', 'Level 3')
		)
	
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	admin = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Admin",related_name="flood_levels")
	suscep_level = models.CharField(max_length=50, unique=True,choices=RESPONSE_LEVEL, verbose_name='Response Level',default='N/A')
	suscep_info = models.TextField(verbose_name='Response Level Description')

	def __str__(self):
		return self.suscep_level

# Flood(Base)
class Base(models.Model):
	level = models.ForeignKey(Level, verbose_name="Response Levels",on_delete=models.CASCADE)

	class Meta:
		abstract = True

class Markers(models.Model):
	FLOOD_LEVELS = (
		('Low','Low'),
		('Moderate','Moderate'),
		('High','High'),
		('Very High','Very High'),
		)

	BARANGAY = (
		('Alegria','Alegria'),
		('Bagacay','Bagacay'),
		('Baluntay','Baluntay'),
		('Datal Anggas','Datal Anggas'),
		('Domolok','Domolok'),
		('Kawas','Kawas'),
		('Ladol','Ladol'),
		('Maribulan','Maribulan'),
		('Pag-Asa','Pag-Asa'),
		('Paraiso','Paraiso'),
		('Poblacion','Poblacion'),
		('Spring','Spring'),
		('Tokawal','Tokawal')
		)

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=50,default='Alegria',choices=BARANGAY, unique=True)
	level = models.CharField(max_length=50,choices=FLOOD_LEVELS, verbose_name="Risk Level")
	latitude = models.FloatField(null=False,blank=False)
	longitude = models.FloatField(null=False,blank=False)
	image = models.ImageField(default='default.jpg',upload_to='flood_marker_imgs',blank=True)
	info = models.TextField()

	def __str__(self):
		return self.name

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)
		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (200,200)
			img.thumbnail(output_size)
			img.save(self.image.path)

	class Meta:
		verbose_name = "Flood Marker"
		verbose_name_plural = 'Flood Markers'
		ordering = ['name']

class Guidelines(Base):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	alert_level = models.CharField(max_length=50, unique=True, verbose_name="Title")
	alert_level_guide = models.TextField(verbose_name="Content")
	date_published = models.DateField(default=tz.now)

	def __str__(self):
		return self.alert_level

	class Meta:
		verbose_name = "'Flood Guidelines'"
		verbose_name_plural = 'Flood Guidelines'
		ordering = ['date_published'] 

class Procedures(Base):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	procedure_name = models.CharField(max_length=50, unique=True)
	procedure_content = models.TextField()

	def __str__(self):
		return self.procedure_name

	class Meta:
		verbose_name = 'Flood Procedure'
		verbose_name_plural = 'Flood Procedures'
		ordering = ['procedure_name']

# Code for Choropleth Section
class Choropleth(models.Model, FloodFileRename, MapInfo):
	f = FloodFileRename
	m = MapInfo

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	admin = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Admin",related_name="flood_choropleths")
	low_risk_map = models.FileField(storage=m.info('low')[0],upload_to=f.rename_to_low,verbose_name=m.info('low')[1],help_text=m.info('low')[2])
	mod_risk_map = models.FileField(storage=m.info('mod')[0],upload_to=f.rename_to_mod,verbose_name=m.info('low')[1],help_text=m.info('low')[2])
	high_risk_map = models.FileField(storage=m.info('high')[0],upload_to=f.rename_to_high,verbose_name=m.info('low')[1],help_text=m.info('low')[2])
	very_high_risk_map = models.FileField(storage=m.info('very high')[0],upload_to=f.rename_to_very_high,verbose_name=m.info('low')[1],help_text=m.info('low')[2])

	confirm_map = models.BooleanField(
		default=False,
		verbose_name="Confirm Map Changes?",
		help_text="(Click on Checkbox) We recommend to 'double-check' the uploaded file first, before confirming change.")

	date_changed = models.DateTimeField(default=tz.now)

	def __str__(self):
		DATE_FORMAT = "{:%B %d, %Y (%A)}".format(self.date_changed) 
		return f"Choropleth Maps was edited by: '{self.admin}' on '{DATE_FORMAT}'"

	class Meta:
		verbose_name = "Flood Choropleth"
		verbose_name_plural = "Flood Choropleths"