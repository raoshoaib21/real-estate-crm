from django.urls import path
from django.contrib.auth import views as auth_views
from crm import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='crm/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('properties/', views.property_list, name='property_list'),
    path('properties/create/', views.property_create, name='property_create'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('properties/<int:pk>/edit/', views.property_edit, name='property_edit'),
    path('properties/<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('properties/<int:pk>/add-image/', views.property_add_image, name='property_add_image'),

    path('leads/', views.lead_list, name='lead_list'),
    path('leads/create/', views.lead_create, name='lead_create'),
    path('leads/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('leads/<int:pk>/edit/', views.lead_edit, name='lead_edit'),
    path('leads/<int:pk>/delete/', views.lead_delete, name='lead_delete'),
    path('leads/<int:pk>/status/', views.lead_status_update, name='lead_status_update'),

    path('deals/', views.deal_list, name='deal_list'),
    path('deals/create/', views.deal_create, name='deal_create'),
    path('deals/<int:pk>/', views.deal_detail, name='deal_detail'),
    path('deals/<int:pk>/edit/', views.deal_edit, name='deal_edit'),
    path('pipeline/', views.pipeline_board, name='pipeline_board'),
    path('api/deal-stage/', views.deal_stage_update, name='deal_stage_update'),

    path('visits/', views.visit_list, name='visit_list'),
    path('visits/create/', views.visit_create, name='visit_create'),
    path('visits/<int:pk>/', views.visit_detail, name='visit_detail'),
    path('visits/<int:pk>/cancel/', views.visit_cancel, name='visit_cancel'),

    path('commissions/', views.commission_list, name='commission_list'),
    path('commissions/create/', views.commission_create, name='commission_create'),
    path('commissions/reports/', views.commission_reports, name='commission_reports'),

    path('reports/', views.reports, name='reports'),
]
