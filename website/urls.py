from django.urls import path
from .views import index_view, contact_view, about_view, team_view, careers_view, blog_view
from . import admin_views

urlpatterns = [
    path('', index_view, name='index'),
    path('contact/', contact_view, name='contact'),
    path('about/', about_view, name='about'),
    path('team/', team_view, name='team'),
    path('careers/', careers_view, name='careers'),
    path('blog/', blog_view, name='blog'),
    
    # Custom Admin Panel
    path('admin-panel/login/', admin_views.admin_login, name='admin_login'),
    path('admin-panel/logout/', admin_views.admin_logout, name='admin_logout'),
    path('admin-panel/', admin_views.admin_dashboard, name='admin_dashboard'),
    
    # Partners CRUD
    path('admin-panel/partners/', admin_views.partners_list, name='partners_list'),
    path('admin-panel/partners/create/', admin_views.partner_create, name='partner_create'),
    path('admin-panel/partners/<int:pk>/edit/', admin_views.partner_edit, name='partner_edit'),
    path('admin-panel/partners/<int:pk>/delete/', admin_views.partner_delete, name='partner_delete'),
    
    # Testimonials CRUD
    path('admin-panel/testimonials/', admin_views.testimonials_list, name='testimonials_list'),
    path('admin-panel/testimonials/create/', admin_views.testimonial_create, name='testimonial_create'),
    path('admin-panel/testimonials/<int:pk>/edit/', admin_views.testimonial_edit, name='testimonial_edit'),
    path('admin-panel/testimonials/<int:pk>/delete/', admin_views.testimonial_delete, name='testimonial_delete'),
    
    # Pricing CRUD
    path('admin-panel/pricing/', admin_views.pricing_list, name='pricing_list'),
    path('admin-panel/pricing/create/', admin_views.pricing_create, name='pricing_create'),
    path('admin-panel/pricing/<int:pk>/edit/', admin_views.pricing_edit, name='pricing_edit'),
    path('admin-panel/pricing/<int:pk>/delete/', admin_views.pricing_delete, name='pricing_delete'),
    
    # Contacts
    path('admin-panel/contacts/', admin_views.contacts_list, name='contacts_list'),
    path('admin-panel/contacts/<int:pk>/delete/', admin_views.contact_delete, name='contact_delete'),
    
    # About Stats CRUD
    path('admin-panel/stats/', admin_views.admin_stats_list, name='admin_stats_list'),
    path('admin-panel/stats/create/', admin_views.admin_stat_create, name='admin_stat_create'),
    path('admin-panel/stats/<int:pk>/edit/', admin_views.admin_stat_edit, name='admin_stat_edit'),
    path('admin-panel/stats/<int:pk>/delete/', admin_views.admin_stat_delete, name='admin_stat_delete'),
    
    # Team CRUD
    path('admin-panel/team/', admin_views.admin_team_list, name='admin_team_list'),
    path('admin-panel/team/create/', admin_views.admin_team_create, name='admin_team_create'),
    path('admin-panel/team/<int:pk>/edit/', admin_views.admin_team_edit, name='admin_team_edit'),
    path('admin-panel/team/<int:pk>/delete/', admin_views.admin_team_delete, name='admin_team_delete'),
    
    # Jobs CRUD
    path('admin-panel/jobs/', admin_views.admin_jobs_list, name='admin_jobs_list'),
    path('admin-panel/jobs/create/', admin_views.admin_job_create, name='admin_job_create'),
    path('admin-panel/jobs/<int:pk>/edit/', admin_views.admin_job_edit, name='admin_job_edit'),
    path('admin-panel/jobs/<int:pk>/delete/', admin_views.admin_job_delete, name='admin_job_delete'),
    
    # Blog CRUD
    path('admin-panel/blog/', admin_views.admin_blog_list, name='admin_blog_list'),
    path('admin-panel/blog/create/', admin_views.admin_blog_create, name='admin_blog_create'),
    path('admin-panel/blog/<int:pk>/edit/', admin_views.admin_blog_edit, name='admin_blog_edit'),
    path('admin-panel/blog/<int:pk>/delete/', admin_views.admin_blog_delete, name='admin_blog_delete'),
    
    # Settings CRUD
    path('admin-panel/settings/', admin_views.admin_settings_list, name='admin_settings_list'),
]
