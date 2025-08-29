from django.contrib import admin
from django.utils.html import format_html
from .models import (
    PersonalInfo, Education, Experience, Skill, Project, 
    Certificate, ContactMessage, SiteSettings
)

@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'location', 'updated_at']
    fieldsets = (
        ('Kişisel Bilgiler', {
            'fields': ('name', 'title', 'birth_year', 'location', 'email', 'phone')
        }),
        ('İçerik', {
            'fields': ('bio', 'about_text')
        }),
        ('Sosyal Medya', {
            'fields': ('linkedin_url', 'github_url')
        }),
        ('Dosyalar', {
            'fields': ('profile_image', 'cv_file')
        }),
    )
    
    def has_add_permission(self, request):
        # Sadece bir PersonalInfo kaydı olsun
        if PersonalInfo.objects.exists():
            return False
        return True

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'school', 'department', 'years_display', 'is_current', 'order']
    list_filter = ['degree', 'is_current', 'start_year']
    list_editable = ['order', 'is_current']
    search_fields = ['school', 'department']
    ordering = ['-start_year', '-order']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('degree', 'school', 'department', 'location')
        }),
        ('Tarih Bilgileri', {
            'fields': ('start_year', 'end_year', 'is_current')
        }),
        ('Ek Bilgiler', {
            'fields': ('description', 'order')
        }),
    )

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'years_display', 'is_current', 'order']
    list_filter = ['is_current', 'start_date']
    list_editable = ['order', 'is_current']
    search_fields = ['position', 'company', 'location']
    ordering = ['-start_date', '-order']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('position', 'company', 'location')
        }),
        ('Tarih Bilgileri', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Ek Bilgiler', {
            'fields': ('description', 'order')
        }),
    )

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'level', 'level_bar', 'is_featured', 'order']
    list_filter = ['category', 'is_featured']
    list_editable = ['level', 'is_featured', 'order']
    search_fields = ['name', 'description']
    ordering = ['category', '-level', 'order']
    
    def level_bar(self, obj):
        color = '#28a745' if obj.level >= 80 else '#ffc107' if obj.level >= 60 else '#dc3545'
        return format_html(
            '<div style="background: #f0f0f0; width: 100px; height: 10px; border-radius: 5px;">'
            '<div style="background: {}; width: {}%; height: 100%; border-radius: 5px;"></div>'
            '</div>',
            color, obj.level
        )
    level_bar.short_description = 'Seviye'
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'category', 'level')
        }),
        ('Görünüm', {
            'fields': ('icon_class', 'is_featured', 'order')
        }),
        ('Açıklama', {
            'fields': ('description',)
        }),
    )

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'is_featured', 'created_date', 'order']
    list_filter = ['category', 'status', 'is_featured', 'created_date']
    list_editable = ['status', 'is_featured', 'order']
    search_fields = ['title', 'short_description', 'technologies']
    ordering = ['-created_date', '-order']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_date'
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'slug', 'category', 'status')
        }),
        ('İçerik', {
            'fields': ('short_description', 'description', 'features')
        }),
        ('Teknoloji', {
            'fields': ('technologies',)
        }),
        ('Bağlantılar', {
            'fields': ('demo_url', 'github_url')
        }),
        ('Görsel', {
            'fields': ('image',)
        }),
        ('Ayarlar', {
            'fields': ('is_featured', 'order')
        }),
    )

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'date_received', 'credential_id', 'order']
    list_filter = ['organization', 'date_received']
    list_editable = ['order']
    search_fields = ['name', 'organization', 'credential_id']
    ordering = ['-date_received', 'order']
    date_hierarchy = 'date_received'
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'organization', 'date_received')
        }),
        ('Sertifika Detayları', {
            'fields': ('description', 'credential_id', 'credential_url')
        }),
        ('Görsel', {
            'fields': ('image',)
        }),
        ('Ayarlar', {
            'fields': ('order',)
        }),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    list_editable = ['is_read']
    search_fields = ['name', 'email', 'subject', 'message']
    ordering = ['-created_at']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        # Mesajlar sadece siteden gönderilsin
        return False
    
    fieldsets = (
        ('Gönderen Bilgileri', {
            'fields': ('name', 'email', 'created_at')
        }),
        ('Mesaj İçeriği', {
            'fields': ('subject', 'message')
        }),
        ('Durum', {
            'fields': ('is_read',)
        }),
    )

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_title', 'updated_at']
    
    fieldsets = (
        ('Site Bilgileri', {
            'fields': ('site_title', 'site_description', 'meta_keywords', 'footer_text')
        }),
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_description')
        }),
        ('Analitics', {
            'fields': ('google_analytics_id',)
        }),
    )
    
    def has_add_permission(self, request):
        # Sadece bir SiteSettings kaydı olsun
        if SiteSettings.objects.exists():
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False

# Admin site başlığını değiştir
admin.site.site_header = "Okan Kantar - Admin Panel"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Yönetim Paneli"
