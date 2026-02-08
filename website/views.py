from django.shortcuts import render, redirect
from django.conf import settings
from .models import Partner, Testimonial, PricingPlan, ContactRequest, AboutStatistic, TeamMember, JobOpening, BlogPost, WebsiteSetting
import requests

def send_telegram_message(message):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not token or not chat_id:
        return
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Error sending telegram message: {e}")

def index_view(request):
    partners = Partner.objects.all()
    testimonials = Testimonial.objects.all()
    pricing_plans = PricingPlan.objects.prefetch_related('features').all().order_by('order')
    
    return render(request, 'index.html', {
        'partners': partners,
        'testimonials': testimonials,
        'pricing_plans': pricing_plans,
    })

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
        
        # Send Telegram notification
        bot_message = (
            f"🚀 <b>Yangi Murojaat!</b>\n\n"
            f"👤 <b>Ism:</b> {name}\n"
            f"📞 <b>Telefon:</b> {phone}\n"
            f"📧 <b>Email:</b> {email}\n"
            f"📋 <b>Tarif:</b> {plan}\n"
            f"💬 <b>Xabar:</b> {message}"
        )
        send_telegram_message(bot_message)
        
        return redirect('index')
    return redirect('index')

def about_view(request):
    pricing_plans = PricingPlan.objects.prefetch_related('features').all()
    stats = AboutStatistic.objects.all().order_by('order')
    return render(request, 'about.html', {
        'pricing_plans': pricing_plans,
        'stats': stats
    })

def team_view(request):
    pricing_plans = PricingPlan.objects.prefetch_related('features').all()
    members = TeamMember.objects.all().order_by('order')
    return render(request, 'team.html', {
        'pricing_plans': pricing_plans,
        'members': members
    })

def careers_view(request):
    pricing_plans = PricingPlan.objects.prefetch_related('features').all()
    jobs = JobOpening.objects.all().order_by('order')
    return render(request, 'careers.html', {
        'pricing_plans': pricing_plans,
        'jobs': jobs
    })

def blog_view(request):
    pricing_plans = PricingPlan.objects.prefetch_related('features').all()
    posts = BlogPost.objects.all().order_by('-date')
    return render(request, 'blog.html', {
        'pricing_plans': pricing_plans,
        'posts': posts
    })
