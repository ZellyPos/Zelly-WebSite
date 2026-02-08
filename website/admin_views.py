from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count
from .models import Partner, Testimonial, PricingPlan, ContactRequest, AboutStatistic, TeamMember, JobOpening, BlogPost, WebsiteSetting
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

# Helper function to check if user is staff
def is_staff_user(user):
    return user.is_authenticated and user.is_staff

# Login View
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Noto\'g\'ri login yoki parol, yoki sizda admin huquqi yo\'q.')
    
    return render(request, 'admin/login.html')

# Logout View
@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# Dashboard View
@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_dashboard(request):
    stats = {
        'partners_count': Partner.objects.count(),
        'testimonials_count': Testimonial.objects.count(),
        'pricing_plans_count': PricingPlan.objects.count(),
        'contact_requests_count': ContactRequest.objects.count(),
        'stats_count': AboutStatistic.objects.count(),
        'team_count': TeamMember.objects.count(),
        'jobs_count': JobOpening.objects.count(),
        'blog_count': BlogPost.objects.count(),
        'recent_contacts': ContactRequest.objects.order_by('-created_at')[:5],
    }
    return render(request, 'admin/dashboard.html', stats)

# ============= PARTNERS CRUD =============
@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def partners_list(request):
    partners = Partner.objects.all().order_by('-id')
    return render(request, 'admin/partners_list.html', {'partners': partners})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def partner_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.FILES.get('logo')
        
        Partner.objects.create(name=name, logo=logo)
        messages.success(request, 'Hamkor muvaffaqiyatli qo\'shildi!')
        return redirect('partners_list')
    
    return render(request, 'admin/partner_form.html', {'action': 'create'})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def partner_edit(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    
    if request.method == 'POST':
        partner.name = request.POST.get('name')
        if request.FILES.get('logo'):
            partner.logo = request.FILES.get('logo')
        partner.save()
        messages.success(request, 'Hamkor muvaffaqiyatli yangilandi!')
        return redirect('partners_list')
    
    return render(request, 'admin/partner_form.html', {'partner': partner, 'action': 'edit'})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def partner_delete(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    partner.delete()
    messages.success(request, 'Hamkor o\'chirildi!')
    return redirect('partners_list')

# ============= TESTIMONIALS CRUD =============
@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def testimonials_list(request):
    testimonials = Testimonial.objects.all().order_by('-id')
    return render(request, 'admin/testimonials_list.html', {'testimonials': testimonials})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def testimonial_create(request):
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        author_position = request.POST.get('author_position')
        text = request.POST.get('text')
        rating = request.POST.get('rating', 5)
        
        Testimonial.objects.create(
            author_name=author_name,
            author_position=author_position,
            text=text,
            rating=rating
        )
        messages.success(request, 'Fikr muvaffaqiyatli qo\'shildi!')
        return redirect('testimonials_list')
    
    return render(request, 'admin/testimonial_form.html', {'action': 'create'})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def testimonial_edit(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    
    if request.method == 'POST':
        testimonial.author_name = request.POST.get('author_name')
        testimonial.author_position = request.POST.get('author_position')
        testimonial.text = request.POST.get('text')
        testimonial.rating = request.POST.get('rating', 5)
        testimonial.save()
        messages.success(request, 'Fikr muvaffaqiyatli yangilandi!')
        return redirect('testimonials_list')
    
    return render(request, 'admin/testimonial_form.html', {'testimonial': testimonial, 'action': 'edit'})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def testimonial_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    messages.success(request, 'Fikr o\'chirildi!')
    return redirect('testimonials_list')

# ============= PRICING CRUD =============
@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def pricing_list(request):
    plans = PricingPlan.objects.all().order_by('order')
    return render(request, 'admin/pricing_list.html', {'plans': plans})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def pricing_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        period = request.POST.get('period')
        is_featured = request.POST.get('is_featured') == 'on'
        button_text = request.POST.get('button_text')
        order = request.POST.get('order', 0)
        
        plan = PricingPlan.objects.create(
            name=name,
            price=price,
            period=period,
            is_featured=is_featured,
            button_text=button_text,
            order=order
        )
        
        # Add features
        features = request.POST.getlist('features[]')
        for feature_text in features:
            if feature_text.strip():
                plan.features.create(text=feature_text)
        
        messages.success(request, 'Tarif muvaffaqiyatli qo\'shildi!')
        return redirect('pricing_list')
    
    return render(request, 'admin/pricing_form.html', {'action': 'create'})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def pricing_edit(request, pk):
    plan = get_object_or_404(PricingPlan, pk=pk)
    
    if request.method == 'POST':
        plan.name = request.POST.get('name')
        plan.price = request.POST.get('price')
        plan.period = request.POST.get('period')
        plan.is_featured = request.POST.get('is_featured') == 'on'
        plan.button_text = request.POST.get('button_text')
        plan.order = request.POST.get('order', 0)
        plan.save()
        
        # Update features
        plan.features.all().delete()
        features = request.POST.getlist('features[]')
        for feature_text in features:
            if feature_text.strip():
                plan.features.create(text=feature_text)
        
        messages.success(request, 'Tarif muvaffaqiyatli yangilandi!')
        return redirect('pricing_list')
    
    return render(request, 'admin/pricing_form.html', {'plan': plan, 'action': 'edit'})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def pricing_delete(request, pk):
    plan = get_object_or_404(PricingPlan, pk=pk)
    plan.delete()
    messages.success(request, 'Tarif o\'chirildi!')
    return redirect('pricing_list')

# ============= CONTACTS VIEW =============
@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def contacts_list(request):
    contacts = ContactRequest.objects.all().order_by('-created_at')
    return render(request, 'admin/contacts_list.html', {'contacts': contacts})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def contact_delete(request, pk):
    contact = get_object_or_404(ContactRequest, pk=pk)
    contact.delete()
    messages.success(request, 'So\'rov o\'chirildi!')
    return redirect('contacts_list')

# ============= STATS CRUD =============
@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_stats_list(request):
    stats = AboutStatistic.objects.all().order_by('order')
    return render(request, 'admin/stats_list.html', {'stats': stats})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_stat_create(request):
    if request.method == 'POST':
        label = request.POST.get('label')
        value = request.POST.get('value')
        order = request.POST.get('order', 0)
        AboutStatistic.objects.create(label=label, value=value, order=order)
        messages.success(request, 'Statistika muvaffaqiyatli qo\'shildi!')
        return redirect('admin_stats_list')
    return render(request, 'admin/stat_form.html', {'action': 'create'})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_stat_edit(request, pk):
    stat = get_object_or_404(AboutStatistic, pk=pk)
    if request.method == 'POST':
        stat.label = request.POST.get('label')
        stat.value = request.POST.get('value')
        stat.order = request.POST.get('order', 0)
        stat.save()
        messages.success(request, 'Statistika muvaffaqiyatli yangilandi!')
        return redirect('admin_stats_list')
    return render(request, 'admin/stat_form.html', {'stat': stat, 'action': 'edit'})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_stat_delete(request, pk):
    stat = get_object_or_404(AboutStatistic, pk=pk)
    stat.delete()
    messages.success(request, 'Statistika o\'chirildi!')
    return redirect('admin_stats_list')

# ============= TEAM CRUD =============
@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_team_list(request):
    members = TeamMember.objects.all().order_by('order')
    return render(request, 'admin/team_list.html', {'members': members})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_team_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        role = request.POST.get('role')
        emoji = request.POST.get('emoji', '👨‍💼')
        image = request.FILES.get('image')
        linkedin = request.POST.get('linkedin')
        twitter = request.POST.get('twitter')
        order = request.POST.get('order', 0)
        
        TeamMember.objects.create(
            name=name, role=role, emoji=emoji, image=image,
            linkedin=linkedin, twitter=twitter, order=order
        )
        messages.success(request, 'Jamoa azosi qo\'shildi!')
        return redirect('admin_team_list')
    return render(request, 'admin/team_form.html', {'action': 'create'})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_team_edit(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        member.name = request.POST.get('name')
        member.role = request.POST.get('role')
        member.emoji = request.POST.get('emoji')
        if request.FILES.get('image'):
            member.image = request.FILES.get('image')
        member.linkedin = request.POST.get('linkedin')
        member.twitter = request.POST.get('twitter')
        member.order = request.POST.get('order', 0)
        member.save()
        messages.success(request, 'Jamoa azosi yangilandi!')
        return redirect('admin_team_list')
    return render(request, 'admin/team_form.html', {'member': member, 'action': 'edit'})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_team_delete(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    member.delete()
    messages.success(request, 'Jamoa azosi o\'chirildi!')
    return redirect('admin_team_list')

# ============= JOBS CRUD =============
@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_jobs_list(request):
    jobs = JobOpening.objects.all().order_by('order')
    return render(request, 'admin/jobs_list.html', {'jobs': jobs})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_job_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        technologies = request.POST.get('technologies')
        tags = request.POST.get('tags')
        order = request.POST.get('order', 0)
        JobOpening.objects.create(
            title=title, description=description, 
            technologies=technologies, tags=tags, order=order
        )
        messages.success(request, 'Vakansiya qo\'shildi!')
        return redirect('admin_jobs_list')
    return render(request, 'admin/job_form.html', {'action': 'create'})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_job_edit(request, pk):
    job = get_object_or_404(JobOpening, pk=pk)
    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.description = request.POST.get('description')
        job.technologies = request.POST.get('technologies')
        job.tags = request.POST.get('tags')
        job.order = request.POST.get('order', 0)
        job.save()
        messages.success(request, 'Vakansiya yangilandi!')
        return redirect('admin_jobs_list')
    return render(request, 'admin/job_form.html', {'job': job, 'action': 'edit'})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_job_delete(request, pk):
    job = get_object_or_404(JobOpening, pk=pk)
    job.delete()
    messages.success(request, 'Vakansiya o\'chirildi!')
    return redirect('admin_jobs_list')

# ============= BLOG CRUD =============
@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_blog_list(request):
    posts = BlogPost.objects.all().order_by('-date')
    return render(request, 'admin/blog_list.html', {'posts': posts})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_blog_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        date = request.POST.get('date')
        short_description = request.POST.get('short_description')
        content = request.POST.get('content')
        emoji = request.POST.get('emoji', '📝')
        image = request.FILES.get('image')
        
        BlogPost.objects.create(
            title=title, category=category, date=date,
            short_description=short_description, content=content,
            emoji=emoji, image=image
        )
        messages.success(request, 'Blog xabari qo\'shildi!')
        return redirect('admin_blog_list')
    return render(request, 'admin/blog_form.html', {'action': 'create'})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_blog_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.category = request.POST.get('category')
        post.date = request.POST.get('date')
        post.short_description = request.POST.get('short_description')
        post.content = request.POST.get('content')
        post.emoji = request.POST.get('emoji')
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
        post.save()
        messages.success(request, 'Blog xabari yangilandi!')
        return redirect('admin_blog_list')
    return render(request, 'admin/blog_form.html', {'post': post, 'action': 'edit'})

@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    messages.success(request, 'Blog xabari o\'chirildi!')
    return redirect('admin_blog_list')

# ============= SETTINGS CRUD =============
@login_required
@user_passes_test(is_staff_user, login_url='/admin-panel/login/')
def admin_settings_list(request):
    settings = WebsiteSetting.objects.all()
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                clean_value = value.strip()
                if key == 'youtube_id':
                    # Handle full URLs like https://www.youtube.com/watch?v=XXXX
                    if 'v=' in clean_value:
                        clean_value = clean_value.split('v=')[1].split('&')[0]
                    elif 'youtu.be/' in clean_value:
                        clean_value = clean_value.split('youtu.be/')[1].split('?')[0]
                
                WebsiteSetting.objects.filter(key=key).update(value=clean_value)
        messages.success(request, 'Sozlamalar yangilandi!')
        return redirect('admin_settings_list')
    return render(request, 'admin/settings_list.html', {'settings': settings})
