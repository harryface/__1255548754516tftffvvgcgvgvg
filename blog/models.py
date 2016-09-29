from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

# Create your models here.

class Post (models.Model):
	title = models.CharField(max_length=40)
	post_image = models.ImageField(upload_to='static/blog', blank=True)
	post_body = models.TextField(blank = True)
	slug = models.SlugField(max_length=200, editable = False)
	
	def get_absolute_url(self):
		return reverse('post_detail', args=[self.id, self.slug])
		
	def save(self, *args, **kwargs):
		if not self.pk:
			self.slug = slugify(self.title)
		try:
			a = Post.objects.get(pk = self.pk)
			if a.post_image != self.post_image:
				a.post_image.delete(save=False)
			self.post_image = self.post_image
		except:
			pass
		return super(Post, self).save(*args, **kwargs)

		
class Gallery (models.Model):
	title = models.CharField(max_length=40)
	image = models.ImageField(upload_to='static/gallery', blank=True)
	description = models.TextField(blank = True)
	slug = models.SlugField(max_length=200, editable = False)
	
	def get_absolute_url(self):
		return reverse('gallery_detail', args=[self.id, self.slug])
		
	def save(self, *args, **kwargs):
		if not self.pk:
			self.slug = slugify(self.title)
		try:
			a = Gallery.objects.get(pk = self.pk)
			if a.image != self.image:
				a.image.delete(save=False)
			self.image = self.image
		except:
			pass
		return super(Gallery, self).save(*args, **kwargs)
