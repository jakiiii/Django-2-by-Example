from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import m2m_changed

User = settings.AUTH_USER_MODEL


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images_created')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    user_like = models.ManyToManyField(User, related_name='images_liked', blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)
    created = models.DateField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail', args=[self.id, self.slug])


# def users_like_changed(sender, instance, *args, **kwargs):
#     instance.total_likes = instance.user_like.count()
#     instance.save()
#
#
# m2m_changed.connect(users_like_changed, sender=Image)
