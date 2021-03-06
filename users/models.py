from django.db import models
from django.contrib.auth.models import User

# pillow lib is imported as PIL
from PIL import Image

# Create your models here.

class Profile (models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	image = models.ImageField(default = 'default.png', upload_to = 'profile_pics')

	# overriding the save method of base class
	def save(self, *args, **kwargs):
		super().save()
		
		img = Image.open(self.image.path)

		if img.height > 400 or img.width > 400:
			size = (400, 400)
			img.thumbnail(size) # specifyin the size
			img.save(self.image.path) #saving the resized image to original image location


	def __str__(self):
		return f'{self.user.username} Profile'
