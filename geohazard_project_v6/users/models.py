from django.contrib.auth.models import User
from django.db import models
from PIL import Image
import uuid


class Profile(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default="default.jpg", upload_to="profile_pics")
	description = models.TextField()

	def __str__(self):
		return self.user.username

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)
		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (200,200)
			img.thumbnail(output_size)
			img.save(self.image.path)	

	class Meta:
		verbose_name = "Profile"
		verbose_name_plural = "Profiles"
