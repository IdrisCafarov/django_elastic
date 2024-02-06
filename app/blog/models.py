from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from account.utils import *

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=128, db_index=True, null=True)
    draft = models.BooleanField(default=True)

    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'blog'


class Reply(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, related_name='replies', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        app_label = 'blog'
        verbose_name_plural = 'Replies'


class Title(models.Model):
    name = models.CharField(max_length=2000)

    def __str__(self):
        return self.name
    

from django.db.models.signals import post_save
from django.dispatch import receiver

class Professor(models.Model):
    name = models.CharField(max_length=1000,null=True, blank=True)
    title = models.CharField(max_length=1000, null=True,blank=True)
    phone = models.CharField(max_length=1000, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    achievements = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=1000,null=True,blank=True)
    province = models.CharField(max_length=1000,null=True,blank=True)
    country = models.CharField(max_length=1000,null=True,blank=True)
    email = models.EmailField(null=True, blank=True,unique=True)
    slug = models.SlugField(unique=True,null=True)
    image_url = models.URLField(null=True, blank=True)
    url = models.URLField(null=True,blank=True)
    research_areas = models.TextField(null=True,blank=True)
    university = models.CharField(max_length=1000,null=True,blank=True)
    university_world_ranking = models.PositiveIntegerField(default=0,null=True)
    department = models.CharField(max_length=1000,null=True,blank=True)
    public = models.BooleanField(default=True)
    rating = models.FloatField(default=0)
    # draft = models.BooleanField(default=False)


    TITLE_WEIGHTS = {
        "Professor": 1.0,
        "Associate Professor": 0.9,
        "Assistant Professor": 0.8,
        "Lecturer": 0.7,
        "Adjunct Professor": 0.6,
        "Clinical": 0.5,
        "Research Assistant": 0.4,
        "Emeritus": 0.9,
        "Senior Lecturer": 0.7,
        "Assistant Lecturer": 0.6,
        "Distinguished Professor": 1.1,
        "PhD student": 0.3
    }

    def calculate_rating(self):
        # Calculate the rating based on the count of non-empty fields, university world ranking, and title
        non_empty_fields = [
            self.name, self.title, self.phone, self.address,
            self.introduction, self.achievements, self.city,
            self.province, self.country, self.email, self.slug,
            self.image_url, self.url, self.research_areas,
            self.university, self.department
        ]
        non_empty_fields_count = sum(field is not None for field in non_empty_fields)

        if non_empty_fields_count == 0:
            self.rating = 0.0
        else:
            title_weight = self.TITLE_WEIGHTS.get(self.title, 0)
            non_empty_fields_rating = non_empty_fields_count / len(non_empty_fields)
            world_ranking_factor = 0.5  # Adjust as needed
            title_score = title_weight * 0.5 if self.title else 0  # Assuming half weight for title
            world_ranking_score = self.university_world_ranking * world_ranking_factor
            self.rating = (non_empty_fields_rating + title_score + world_ranking_score) * 10  # Scale to 0-10
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug_shortcode(size=20, model_=Professor)

       
        return super(Professor, self).save(*args,**kwargs)



    class Meta:
        unique_together = ['name', 'title','research_areas','university','department']

# @receiver(post_save, sender=Professor)
# def update_professor_rating(sender, instance, **kwargs):
#     instance.calculate_rating()


@receiver(post_save, sender=Professor)
def after_save(sender, instance, created, **kwargs):
    if created:

        instance.calculate_rating()



