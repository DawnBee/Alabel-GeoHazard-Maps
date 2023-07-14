from django.db import models
from PIL import Image
import uuid

class Warning_Devices(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=50, verbose_name='Device Name',unique=True)
	location = models.CharField(max_length=50, help_text="Places/Sites (i.e., Street Name,Purok,Barangay,Land Marks)")
	latitude = models.FloatField(null=False,blank=False)
	longitude = models.FloatField(null=False,blank=False)
	info = models.TextField(verbose_name='Description')
	image = models.ImageField(default='default.jpg',upload_to='device_imgs',verbose_name='Image')

	def __str__(self):
		return self.name
	
	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)

		img = Image.open(self.image.path)

		if img.height > 200 or img.width > 200:
			output_size = (200,200)
			img.thumbnail(output_size)
			img.save(self.image.path)

	class Meta:
		verbose_name = "Warning Device"
		verbose_name_plural = "Warning Devices"


class Evac_Centers(models.Model):

	# Evacuation Centers
	CENTERS = {
		('Alabel Central Elem. School', 'Alabel Central Elem. School'),
		('Alegria Covered Court', 'Alegria Covered Court'),
		('Bagacay Gym', 'Bagacay Gym'),
		('Baluntay Gym', 'Baluntay Gym'),
		('Datal Anggas Gym', 'Datal Anggas Gym'),
		('Domolok Gym', 'Domolok Gym'),
		('Kawas Gymnasium', 'Kawas Gymnasium'),
		('Maribulan Gym','Maribulan Gym'),
		('Municipal Gym', 'Municipal Gym'),
		('Pag-Asa Gymnasium', 'Pag-Asa Gymnasium'),
		('Paraiso Gym', 'Paraiso Gym'),
		('Purok Kawayan (Bagacay)', 'Purok Kawayan (Bagacay)'),
		('Purok 1 (Baluntay)', 'Purok 1 (Baluntay)'),
		('Spring Gym', 'Spring Gym'),
		('Tokawal Gym', 'Tokawal Gym'),
	}	

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=100,choices=CENTERS,unique=True)
	location = models.CharField(max_length=50, help_text="Places/Sites (i.e., Street Name,Purok,Barangay,Land Marks)")
	latitude = models.FloatField(null=False,blank=False)
	longitude = models.FloatField(null=False,blank=False)
	image = models.ImageField(default='default.jpg',upload_to='evac_center_imgs', verbose_name='Image')

	def __str__(self):
		return self.name
	
	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)

		img = Image.open(self.image.path)

		if img.height > 200 or img.width > 200:
			output_size = (200,200)
			img.thumbnail(output_size)
			img.save(self.image.path)

	class Meta:
		verbose_name = "Evacuation Center"
		verbose_name_plural = "Evacuation Centers"


class Warning_Signs(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=50, verbose_name='Sign Name',unique=True)
	location = models.CharField(max_length=50, help_text="Places/Sites (i.e., Street Name,Purok,Barangay,Land Marks)")
	latitude = models.FloatField(null=False,blank=False)
	longitude = models.FloatField(null=False,blank=False)
	image = models.ImageField(default='default.jpg',upload_to='sign_imgs', verbose_name='Image')


	def __str__(self):
		return self.name

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)

		img = Image.open(self.image.path)

		if img.height > 200 or img.width > 200:
			output_size = (200,200)
			img.thumbnail(output_size)
			img.save(self.image.path)

	class Meta:
		verbose_name = "Warning Sign"
		verbose_name_plural = "Warning Signs"