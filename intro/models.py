from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Enquiry(models.Model):
    eid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=150, blank=True, null=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.content

pcat = (
    ('Hong Kong', 'Hong Kong'),
    ('Taiwan', 'Taiwan'),
    ('Japan', 'Japan'),
)

class ManagePhotos(models.Model):
    pid = models.AutoField(primary_key=True)
    photo = models.ImageField()
    category = models.CharField(max_length=100, choices=pcat)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    date_token = models.DateField()

    def __str__(self):
        return self.category


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(blank=True, null=True)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['-created']

    @property
    def num_likes(self):
        return self.liked.all().count()

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)

class Poll(models.Model):
    question = models.TextField()
    option_one = models.CharField(max_length=50)
    option_two = models.CharField(max_length=50)
    option_three = models.CharField(max_length=50)
    option_four = models.CharField(max_length=50)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)
    option_four_count = models.IntegerField(default=0)

    def total(self):
        return self.option_one_count + self.option_two_count + self.option_three_count + self.option_four_count

