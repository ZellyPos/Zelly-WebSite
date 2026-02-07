from django.urls import path
from .views import index_view, contact_view
from . import admin_views

urlpatterns = [
    path('', index_view, name='index'),
    path('contact/', contact_view, name='contact'),
    
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
]
