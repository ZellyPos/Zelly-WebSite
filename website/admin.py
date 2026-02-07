from django.contrib import admin
from .models import Partner, Testimonial, PricingPlan, PricingFeature, ContactRequest

class PricingFeatureInline(admin.TabularInline):
    model = PricingFeature
    extra = 1

@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    inlines = [PricingFeatureInline]
    list_display = ('name', 'price', 'is_featured')

admin.site.register(Partner)
admin.site.register(Testimonial)
admin.site.register(ContactRequest)
