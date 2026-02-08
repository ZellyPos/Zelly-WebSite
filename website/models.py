from django.db import models

class Partner(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partners/')

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    author_name = models.CharField(max_length=100)
    author_position = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(default=5)
    avatar_initials = models.CharField(max_length=5, blank=True) # For when no avatar image is provided
    avatar = models.ImageField(upload_to='testimonials/', null=True, blank=True)

    def __str__(self):
        return self.author_name

class PricingPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=50) 
    period = models.CharField(max_length=20, default="/ oy", blank=True)
    is_featured = models.BooleanField(default=False)
    button_text = models.CharField(max_length=50, default="Boshlash")
    order = models.IntegerField(default=0)  # For custom ordering

    def __str__(self):
        return self.name

class PricingFeature(models.Model):
    plan = models.ForeignKey(PricingPlan, related_name='features', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.plan.name} - {self.text}"

class ContactRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    plan = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.plan or 'CTA'}"

class AboutStatistic(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50) # e.g. "2023", "500+", "24/7"
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.label

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/', null=True, blank=True)
    emoji = models.CharField(max_length=10, default="👨‍💼", blank=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class JobOpening(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=200, help_text="Comma separated tags")
    tags = models.CharField(max_length=200, help_text="Comma separated tags like Full-time, Remote")
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    date = models.DateField()
    short_description = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', null=True, blank=True)
    emoji = models.CharField(max_length=10, default="📝", blank=True)

    def __str__(self):
        return self.title

class WebsiteSetting(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.TextField()
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.key
