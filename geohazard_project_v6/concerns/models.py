from django.contrib.auth.models import User
from django.utils import timezone as tz
from django.urls import reverse
from django.db import models
import uuid


class Post(models.Model):

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
	location = models.CharField(max_length=50,default='Alegria',choices=BARANGAY)
	post_img = models.ImageField(upload_to='post_images',verbose_name='Image (Optional)',null=True,blank=True)
	date_posted = models.DateTimeField(default=tz.now)
	author = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
	content = models.TextField()
	upvote_react = models.ManyToManyField(User,related_name='concern_posts_upvoted',blank=True)
	flag_react = models.ManyToManyField(User,related_name='concern_posts_flagged',blank=True)
	is_approved = models.BooleanField(
		default=False,
		verbose_name="Approve concern?",
		help_text="Post will be displayed in the community after it's approved.")
			
	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

	def total_upvotes(self):
		return self.upvote_react.count()

	def total_flags(self):
		return self.flag_react.count()	

	@property
	def formatted_date_posted(self):
		return self.date_posted.strftime('%B %d, %Y (%I:%M %p)')

	def __str__(self):
		return f"A post created by '{self.author}' on {self.formatted_date_posted} from '{self.location}'"

	class Meta:
		verbose_name = "Post"
		verbose_name_plural = "Posts"
		ordering = ['-date_posted']


class GuestPost(models.Model):

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
	author = models.CharField(max_length=20,default="Anonymous User",blank=True,null=True)
	phone_number = models.CharField(max_length=20)
	email = models.EmailField(max_length=50,blank=True,null=True)
	location = models.CharField(max_length=50,default='Alegria',choices=BARANGAY)
	post_img = models.ImageField(upload_to='post_images',verbose_name='Image (Optional)',null=True,blank=True)
	date_posted = models.DateTimeField(default=tz.now)
	content = models.TextField()
	upvote_react = models.ManyToManyField(User,related_name='concern_guest_posts_upvoted',blank=True)
	flag_react = models.ManyToManyField(User,related_name='concern_guest_posts_flagged',blank=True)
	is_approved = models.BooleanField(
		default=False,
		verbose_name="Approve concern?",
		help_text="Post will be displayed in the community after it's approved.")
			
	def get_absolute_url(self):
		return reverse('guest-post-detail', kwargs={'pk': self.pk})

	def total_upvotes(self):
		return self.upvote_react.count()

	def total_flags(self):
		return self.flag_react.count()	

	@property
	def formatted_date_posted(self):
		return self.date_posted.strftime('%B %d, %Y (%I:%M %p)')

	def __str__(self):
		return f"A post created by an 'Anonymous User' with the phone of '{self.phone_number}' on {self.formatted_date_posted}"		

	class Meta:
		verbose_name = "Guest Post"
		verbose_name_plural = "Guest Posts"
		ordering = ['-date_posted']		


class CombinedPost(models.Model):
	post = models.OneToOneField(Post,on_delete=models.CASCADE,null=True,blank=True)
	guest_post = models.OneToOneField(GuestPost,on_delete=models.CASCADE,null=True,blank=True)

	def get_latest_date(self):
		if self.post:
			return self.post.date_posted
		elif self.guest_post:
			return self.guest_post.date_posted
		else:
			return None

	def get_absolute_url(self):
		if self.post:
			return self.post.get_absolute_url()
		elif self.guest_post:
			return self.guest_post.get_absolute_url()
		else:
			return ''

	def  __str__(self):
		if self.post:
			return str(self.post)
		elif self.guest_post:
			return str(self.guest_post)
		else:
			return ''

	# Calculate the total flags
	def total_flags(self):
		flags = 0
		if self.post:
			flags = self.post.flag_react.count()
		elif self.guest_post:
			flags = self.guest_post.flag_react.count()
		return flags

	# Calculate the total upvotes
	def total_upvotes(self):
		upvotes = 0
		if self.post:
			upvotes = self.post.upvote_react.count()
		elif self.guest_post:
			upvotes = self.guest_post.upvote_react.count()
		return upvotes