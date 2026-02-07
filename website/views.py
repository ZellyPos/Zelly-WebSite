from django.shortcuts import render, redirect
from .models import Partner, Testimonial, PricingPlan, ContactRequest

def index_view(request):
    partners = Partner.objects.all()
    testimonials = Testimonial.objects.all()
    pricing_plans = PricingPlan.objects.prefetch_related('features').all()
    
    context = {
        'partners': partners,
        'testimonials': testimonials,
        'pricing_plans': pricing_plans,
    }
    return render(request, 'index.html', context)

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')
        plan = request.POST.get('plan', 'CTA Section')
        message = request.POST.get('message', '')
        
        ContactRequest.objects.create(
            name=name,
            phone=phone,
            email=email,
            plan=plan,
            message=message
        )
        return redirect('index')
    return redirect('index')
