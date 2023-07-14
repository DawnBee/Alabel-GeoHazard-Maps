from django.contrib import admin
from .models import Post, GuestPost

class PostAdmin(admin.ModelAdmin):
    fields = (
	 	'author',
	 	'location',
	 	'post_img',
	 	'content',
	 	'upvote_react',
	 	'flag_react',
	 	'is_approved',
	 	'date_posted'
	 	) 

admin.site.register(Post, PostAdmin)


class GuestPostAdmin(admin.ModelAdmin):
    fields = (
	 	'email',
	 	'phone_number',
	 	'location',
	 	'post_img',
	 	'content',
	 	'upvote_react',
	 	'flag_react',
	 	'is_approved',
	 	'date_posted'
	 	)

admin.site.register(GuestPost, GuestPostAdmin)