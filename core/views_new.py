from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    PersonalInfo, Education, Experience, Skill, Project, 
    Certificate, ContactMessage, SiteSettings
)
import json

def get_site_context():
    """Tüm sayfalarda kullanılacak ortak context"""
    try:
        personal_info = PersonalInfo.objects.first()
        site_settings = SiteSettings.objects.first()
    except:
        personal_info = None
        site_settings = None
    
    return {
        'personal_info': personal_info,
        'site_settings': site_settings,
    }

def home(request):
    """Ana sayfa - dağdan düşme animasyonu ile başlayan hero section"""
    context = get_site_context()
    
    # Featured skills
    featured_skills = Skill.objects.filter(is_featured=True)[:6]
    
    # Featured projects
    featured_projects = Project.objects.filter(is_featured=True)[:3]
    
    # Latest experience
    latest_experience = Experience.objects.first()
    
    context.update({
        'featured_skills': featured_skills,
        'featured_projects': featured_projects,
        'latest_experience': latest_experience,
    })
    
    return render(request, 'core/home.html', context)

def about(request):
    """Hakkımda sayfası - detaylı bilgiler"""
    context = get_site_context()
    
    # Eğitim bilgileri
    educations = Education.objects.all()
    
    # Deneyim bilgileri
    experiences = Experience.objects.all()
    
    # Sertifikalar
    certificates = Certificate.objects.all()[:6]  # Son 6 sertifika
    
    context.update({
        'educations': educations,
        'experiences': experiences,
        'certificates': certificates,
    })
    
    return render(request, 'core/about.html', context)

def skills(request):
    """Yetenekler sayfası"""
    context = get_site_context()
    
    # Kategorilere göre yetenekler
    programming_skills = Skill.objects.filter(category='programming')
    framework_skills = Skill.objects.filter(category='framework')
    database_skills = Skill.objects.filter(category='database')
    tool_skills = Skill.objects.filter(category='tool')
    soft_skills = Skill.objects.filter(category='soft')
    
    context.update({
        'programming_skills': programming_skills,
        'framework_skills': framework_skills,
        'database_skills': database_skills,
        'tool_skills': tool_skills,
        'soft_skills': soft_skills,
    })
    
    return render(request, 'core/skills.html', context)

def projects(request):
    """Projeler sayfası"""
    context = get_site_context()
    
    # Tüm projeler
    all_projects = Project.objects.all()
    
    # Kategorilere göre filtreleme
    category = request.GET.get('category', 'all')
    if category != 'all':
        all_projects = all_projects.filter(category=category)
    
    # Kategorileri ve sayıları al
    categories = Project.CATEGORY_CHOICES
    category_counts = {}
    for cat_code, cat_name in categories:
        category_counts[cat_code] = Project.objects.filter(category=cat_code).count()
    
    context.update({
        'projects': all_projects,
        'categories': categories,
        'category_counts': category_counts,
        'current_category': category,
    })
    
    return render(request, 'core/projects.html', context)

def project_detail(request, slug):
    """Proje detay sayfası"""
    context = get_site_context()
    project = get_object_or_404(Project, slug=slug)
    
    # Diğer projeler (öneriler)
    other_projects = Project.objects.exclude(slug=slug)[:3]
    
    context.update({
        'project': project,
        'other_projects': other_projects,
    })
    
    return render(request, 'core/project_detail.html', context)

def contact(request):
    """İletişim sayfası"""
    context = get_site_context()
    return render(request, 'core/contact.html', context)

@csrf_exempt
def contact_submit(request):
    """İletişim formu gönderimi"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Mesajı veritabanına kaydet
            message = ContactMessage.objects.create(
                name=data.get('name'),
                email=data.get('email'),
                subject=data.get('subject', ''),
                message=data.get('message')
            )
            
            # E-posta gönder (isteğe bağlı)
            try:
                personal_info = PersonalInfo.objects.first()
                if personal_info and personal_info.email:
                    send_mail(
                        subject=f"Yeni İletişim Mesajı: {data.get('subject', 'Konusuz')}",
                        message=f"""
                        Ad Soyad: {data.get('name')}
                        E-posta: {data.get('email')}
                        Konu: {data.get('subject', 'Konusuz')}
                        
                        Mesaj:
                        {data.get('message')}
                        """,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[personal_info.email],
                        fail_silently=True,
                    )
            except Exception as e:
                print(f"E-posta gönderme hatası: {e}")
            
            return JsonResponse({
                'success': True,
                'message': 'Mesajınız başarıyla gönderildi!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Mesaj gönderilirken bir hata oluştu.'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Geçersiz istek.'
    })
