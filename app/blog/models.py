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
        "Professor": 10.0,
        "Associate Professor": 9.0,
        "Assistant Professor": 8.0,
        "Lecturer": 7.0,
        "Adjunct Professor": 6.0,
        "Clinical": 5.0,
        "Research Assistant": 4.0,
        "Emeritus": 9.0,
        "Senior Lecturer": 7.0,
        "Assistant Lecturer": 6.0,
        "PhD student": 3.0
    }

    def calculate_rating(self):
        non_empty_fields = [
            self.name, self.title, self.phone, self.address,
            self.introduction, self.achievements, self.city,
            self.province, self.country, self.email, self.slug,
            self.image_url, self.url, self.research_areas,
            self.university, self.department
        ]
        non_empty_fields_count = sum(field is not None for field in non_empty_fields)
        # Calculate non_empty_fields_rating between 0 and 10
        if non_empty_fields_count == 0:
            non_empty_fields_rating = 0.0
        else:
            non_empty_fields_rating = min(non_empty_fields_count / len(non_empty_fields), 1.0) * 10

        if non_empty_fields_count == 0:
            self.rating = 0.0
        else:
            title_weight = self.TITLE_WEIGHTS.get(self.title, 0)
            # Adjust world ranking weight based on ranking (lower ranking gets higher weight)
            if self.university_world_ranking == 0:
                world_ranking_factor = 1  # Handling edge case where ranking is 0
            else:
                world_ranking_factor = max(1 - (self.university_world_ranking / 1000), 0)  # Normalize ranking to a factor between 0 and 1, capping negative factors at 0

            # Calculate title score
            title_score = title_weight if self.title else 0

            # Calculate world ranking score
            world_ranking_score = 10 * world_ranking_factor  # Scale to 0-10 range

            # Calculate total score
            total_score = (non_empty_fields_rating + title_score + world_ranking_score) / 3

            # Scale the total score to a range of 0-10
            self.rating = round(total_score, 3)

            # Print total score
            print("Non Empty Fields Score",non_empty_fields_rating)
            print("Title Score:",title_score)
            print("World Ranking:",world_ranking_score)
            print("Total Rating:", self.rating)




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
def after_save(sender, instance, **kwargs):
    print("qaqa after_save icindeyem")
    instance.calculate_rating()
    # instance.save()



