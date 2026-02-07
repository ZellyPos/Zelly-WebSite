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
