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


    PROFESSOR_TITLES_RATINGS = {
        'Associate Professor': 2.3,
        'Assistant Professor': 2.1,
        'Lecturer': 1.9,
        'Adjunct Professor': 1.7,
        'Clinical': 1.5,
        'Research Assistant': 1.3,
        'Emeritus': 2.0,
        'Senior Lecturer': 1.8,
        'Assistant Lecturer': 1.6,
        'Distinguished Professor': 2.7,
        'PhD Student': 1.0,
        'Professor': 2.5,
    }


    def get_non_empty_field_count(self):
        # Filter out fields not defined in the Professor model
        professor_fields = [field.attname for field in self._meta.fields if field.model == Professor]
    
        # Calculate the number of non-empty fields
        non_empty_field_count = sum(1 for field_name in professor_fields if getattr(self, field_name) not in [None, ''])
        
        return non_empty_field_count-1
    
    
        
    def calculate_rating(self):
        
        # Title rating
        title_rating = 0.0
        # More detailed title rating calculation
        for title, rating in self.PROFESSOR_TITLES_RATINGS.items():
            if title.lower() in self.title.lower():
                title_rating = rating
                break  # Assumes the first match determines the rating
        
        # Dummy non-empty field count - replace with actual logic
        non_empty_field_count = self.get_non_empty_field_count()  # Example: replace with the actual logic to count non-empty fields
        max_count = 17
        step = 0.5
        rating_mapping = {i: i * step for i in range(max_count + 1)}
        non_empty_fields_rating = rating_mapping.get(non_empty_field_count, 0.0)
        
        
        # University world ranking rating
        if self.university_world_ranking is not None:
            if self.university_world_ranking == 0:
                university_world_ranking_rating = 0.0
            elif self.university_world_ranking <= 10:
                university_world_ranking_rating = 2.0
            elif self.university_world_ranking <= 100:
                university_world_ranking_rating = 1.8
            elif self.university_world_ranking <= 500:
                university_world_ranking_rating = 1.5
            elif self.university_world_ranking <= 1000:
                university_world_ranking_rating = 1.2
            elif self.university_world_ranking <= 10000:
                university_world_ranking_rating = 1.0
            elif self.university_world_ranking <= 50000:
                university_world_ranking_rating = 0.8
            elif self.university_world_ranking <= 100000:
                university_world_ranking_rating = 0.5
            else:
                university_world_ranking_rating = 0.0
        else:
            university_world_ranking_rating = 0.0
        
        # Calculate the overall rating
        print(title_rating,non_empty_fields_rating,university_world_ranking_rating)
        rating = title_rating + non_empty_fields_rating + university_world_ranking_rating
        # rating = min(total_rating, 10)
        return rating

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug_shortcode(size=20, model_=Professor)

       
        return super(Professor, self).save(*args,**kwargs)



    class Meta:
        unique_together = ['name', 'title','research_areas','university','department']
 




