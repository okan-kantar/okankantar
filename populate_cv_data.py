#!/usr/bin/env python
"""
Okan Kantar CV verilerini veritabanına ekleyen script
"""
import os
import sys
import django
from datetime import date

# Django settings yapılandırması
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'okankantar.settings')
django.setup()

from core.models import PersonalInfo, Education, Experience, Skill, Project, Certificate, SiteSettings

def create_personal_info():
    """Kişisel bilgileri oluştur"""
    personal_info, created = PersonalInfo.objects.get_or_create(
        name="Okan Kantar",
        defaults={
            'title': "Yazılım Takım Lideri",
            'bio': "Modern teknolojilerle yaratıcı çözümler üreten, C#, Python, JavaScript ve Django, React teknolojilerinde uzman yazılım geliştirici",
            'about_text': """Merhaba! Ben Okan Kantar, teknoloji tutkunu bir Full Stack Developer'ım. 2006 yılında Gazi Üniversitesi İktisat bölümünden mezun olduktan sonra, finans alanında yüksek lisans yaparak Hacettepe Üniversitesi'nden mezun oldum.

Kariyerime kamu sektöründe bütçe ve muhasebe uzmanı olarak başladım. Ancak teknolojiye olan tutkum beni yazılım geliştirme dünyasına yönlendirdi. Bu alanda kendimi geliştirerek, şu anda yazılım takım lideri olarak çalışıyorum.

Özellikle C# .NET, Python Django, JavaScript ve modern web teknolojilerinde uzmanlaştım. Hem finans hem de teknoloji deneyimim sayesinde, karmaşık iş süreçlerini anlamak ve bunları etkili çözümlere dönüştürmek konusunda güçlüyüm.""",
            'birth_year': 1989,
            'location': "Ankara, Türkiye",
            'email': "okkant@gmail.com",
            'phone': "0539 315 6407",
            'linkedin_url': "https://www.linkedin.com/in/okan-kantar/",
            'github_url': "https://github.com/okan-kantar"
        }
    )
    print(f"✅ Kişisel bilgiler {'oluşturuldu' if created else 'zaten mevcut'}")
    return personal_info

def create_site_settings():
    """Site ayarlarını oluştur"""
    site_settings, created = SiteSettings.objects.get_or_create(
        defaults={
            'site_title': "Okan Kantar - Full Stack Developer",
            'site_description': "Modern teknolojilerle yaratıcı çözümler üreten, C#, Python, JavaScript ve Django, React teknolojilerinde uzman yazılım geliştirici",
            'meta_keywords': "Okan Kantar, Full Stack Developer, C#, Python, Django, React, JavaScript, Yazılım Geliştirici, Ankara",
            'footer_text': "© 2024 Okan Kantar. Tüm hakları saklıdır.",
            'hero_title': "Merhaba, Ben Okan Kantar",
            'hero_subtitle': "Yazılım Takım Lideri & Full Stack Developer",
            'hero_description': "Modern teknolojilerle yaratıcı çözümler üreten, C#, Python, JavaScript ve Django, React teknolojilerinde uzman yazılım geliştirici"
        }
    )
    print(f"✅ Site ayarları {'oluşturuldu' if created else 'zaten mevcut'}")
    return site_settings

def create_education():
    """Eğitim bilgilerini oluştur"""
    educations = [
        {
            'degree': 'yuksek_lisans',
            'school': 'Hacettepe Üniversitesi',
            'department': 'Finans/Finance',
            'start_year': 2019,
            'end_year': 2021,
            'location': 'Ankara',
            'order': 1
        },
        {
            'degree': 'lisans',
            'school': 'Gazi Üniversitesi',
            'department': 'İktisat/Economics',
            'start_year': 2006,
            'end_year': 2011,
            'location': 'Ankara',
            'order': 2
        }
    ]
    
    for edu_data in educations:
        education, created = Education.objects.get_or_create(
            school=edu_data['school'],
            department=edu_data['department'],
            defaults=edu_data
        )
        print(f"✅ Eğitim: {education.school} - {education.department} {'oluşturuldu' if created else 'zaten mevcut'}")

def create_experience():
    """Deneyim bilgilerini oluştur"""
    experiences = [
        {
            'position': 'Yazılım Takım Lideri',
            'company': 'Tarım ve Kırsal Kalkınmayı Destekleme Kurumu',
            'location': 'Ankara, Türkiye',
            'start_date': date(2024, 12, 1),
            'end_date': None,
            'is_current': True,
            'description': 'Yazılım geliştirme takımının liderliğini yapıyorum. Proje yönetimi, kod kalitesi ve takım koordinasyonu sorumluluklarım bulunuyor.',
            'order': 1
        },
        {
            'position': 'Yazılım Geliştirme Uzmanı',
            'company': 'Tarım ve Kırsal Kalkınmayı Destekleme Kurumu',
            'location': 'Ankara, Türkiye',
            'start_date': date(2022, 12, 1),
            'end_date': date(2024, 12, 1),
            'is_current': False,
            'description': 'Full stack web uygulamaları geliştirdim. C# .NET, Python Django ve modern JavaScript teknolojileri kullandım.',
            'order': 2
        },
        {
            'position': '.Net Yazılım Uzmanlığı Eğitmenliği',
            'company': 'Vektörel Academy',
            'location': 'Ankara, Türkiye',
            'start_date': date(2021, 6, 1),
            'end_date': date(2022, 11, 30),
            'is_current': False,
            'description': 'C# .NET teknolojileri konusunda eğitmenlik yaptım. MVC, Entity Framework ve modern web development konularında eğitimler verdim.',
            'order': 3
        }
    ]
    
    for exp_data in experiences:
        experience, created = Experience.objects.get_or_create(
            position=exp_data['position'],
            company=exp_data['company'],
            defaults=exp_data
        )
        print(f"✅ Deneyim: {experience.position} - {experience.company} {'oluşturuldu' if created else 'zaten mevcut'}")

def create_skills():
    """Yetenekleri oluştur"""
    skills = [
        # Programlama Dilleri
        {'name': 'C#', 'category': 'programming', 'level': 90, 'icon_class': 'fas fa-code', 'is_featured': True, 'order': 1},
        {'name': 'Python', 'category': 'programming', 'level': 85, 'icon_class': 'fab fa-python', 'is_featured': True, 'order': 2},
        {'name': 'JavaScript', 'category': 'programming', 'level': 80, 'icon_class': 'fab fa-js', 'is_featured': True, 'order': 3},
        {'name': 'TypeScript', 'category': 'programming', 'level': 75, 'icon_class': 'fab fa-js', 'is_featured': False, 'order': 4},
        {'name': 'SQL', 'category': 'programming', 'level': 85, 'icon_class': 'fas fa-database', 'is_featured': True, 'order': 5},
        
        # Framework ve Kütüphaneler
        {'name': 'Django', 'category': 'framework', 'level': 85, 'icon_class': 'fab fa-python', 'is_featured': True, 'order': 1},
        {'name': '.NET Framework', 'category': 'framework', 'level': 90, 'icon_class': 'fas fa-code', 'is_featured': True, 'order': 2},
        {'name': 'React', 'category': 'framework', 'level': 75, 'icon_class': 'fab fa-react', 'is_featured': True, 'order': 3},
        {'name': 'ASP.NET MVC', 'category': 'framework', 'level': 88, 'icon_class': 'fas fa-code', 'is_featured': False, 'order': 4},
        {'name': 'Entity Framework', 'category': 'framework', 'level': 85, 'icon_class': 'fas fa-database', 'is_featured': False, 'order': 5},
        
        # Veritabanları
        {'name': 'Microsoft SQL Server', 'category': 'database', 'level': 85, 'icon_class': 'fas fa-database', 'is_featured': False, 'order': 1},
        {'name': 'PostgreSQL', 'category': 'database', 'level': 80, 'icon_class': 'fas fa-database', 'is_featured': False, 'order': 2},
        {'name': 'SQLite', 'category': 'database', 'level': 75, 'icon_class': 'fas fa-database', 'is_featured': False, 'order': 3},
        
        # Araçlar ve Teknolojiler
        {'name': 'Git', 'category': 'tool', 'level': 85, 'icon_class': 'fab fa-git-alt', 'is_featured': False, 'order': 1},
        {'name': 'Visual Studio', 'category': 'tool', 'level': 90, 'icon_class': 'fas fa-code', 'is_featured': False, 'order': 2},
        {'name': 'VS Code', 'category': 'tool', 'level': 88, 'icon_class': 'fas fa-code', 'is_featured': False, 'order': 3},
        {'name': 'Docker', 'category': 'tool', 'level': 70, 'icon_class': 'fab fa-docker', 'is_featured': False, 'order': 4},
        {'name': 'Linux', 'category': 'tool', 'level': 75, 'icon_class': 'fab fa-linux', 'is_featured': False, 'order': 5},
        
        # Kişisel Beceriler
        {'name': 'Takım Liderliği', 'category': 'soft', 'level': 85, 'icon_class': 'fas fa-users', 'is_featured': False, 'order': 1},
        {'name': 'Proje Yönetimi', 'category': 'soft', 'level': 80, 'icon_class': 'fas fa-project-diagram', 'is_featured': False, 'order': 2},
        {'name': 'Problem Çözme', 'category': 'soft', 'level': 90, 'icon_class': 'fas fa-lightbulb', 'is_featured': False, 'order': 3},
        {'name': 'İletişim', 'category': 'soft', 'level': 85, 'icon_class': 'fas fa-comments', 'is_featured': False, 'order': 4},
    ]
    
    for skill_data in skills:
        skill, created = Skill.objects.get_or_create(
            name=skill_data['name'],
            category=skill_data['category'],
            defaults=skill_data
        )
        print(f"✅ Yetenek: {skill.name} ({skill.category}) {'oluşturuldu' if created else 'zaten mevcut'}")

def create_projects():
    """Projeleri oluştur"""
    projects = [
        {
            'title': 'E-Ticaret Platformu',
            'slug': 'e-ticaret-platformu',
            'category': 'web',
            'status': 'completed',
            'short_description': 'Django ve React teknolojileri kullanılarak geliştirilmiş modern e-ticaret platformu.',
            'description': '''Django REST Framework backend ve React frontend kullanılarak geliştirilmiş kapsamlı e-ticaret platformu. 
            
Proje, modern web teknolojileri kullanılarak kullanıcı dostu bir alışveriş deneyimi sunmak üzere tasarlandı. Responsive tasarım, güvenli ödeme entegrasyonu ve kapsamlı admin paneli ile donatıldı.''',
            'technologies': 'Django, React, PostgreSQL, Redis, Docker',
            'features': '''Kullanıcı kayıt ve giriş sistemi
Ürün katalog yönetimi
Sepet ve sipariş işlemleri
Ödeme entegrasyonu
Admin paneli
Responsive tasarım''',
            'is_featured': True,
            'order': 1
        },
        {
            'title': 'Stok Yönetim Sistemi',
            'slug': 'stok-yonetim-sistemi',
            'category': 'desktop',
            'status': 'completed',
            'short_description': 'C# .NET ile geliştirilmiş kapsamlı stok takip ve yönetim uygulaması.',
            'description': '''WPF kullanılarak geliştirilmiş masaüstü stok yönetim uygulaması. 
            
Küçük ve orta ölçekli işletmeler için tasarlanan bu uygulama, envanter takibi, satış süreçleri ve raporlama özelliklerini bir arada sunuyor.''',
            'technologies': 'C# .NET, WPF, MSSQL, Entity Framework',
            'features': '''Ürün tanımlama ve kategorizasyon
Stok giriş/çıkış işlemleri
Satış süreçleri
Raporlama sistemi
Kullanıcı yetkilendirme''',
            'is_featured': True,
            'order': 2
        },
        {
            'title': 'Kişisel Portfolio Sitesi',
            'slug': 'kisisel-portfolio-sitesi',
            'category': 'website',
            'status': 'completed',
            'short_description': 'Django ile geliştirilmiş dinamik portfolio sitesi.',
            'description': '''Django framework kullanılarak geliştirilmiş kişisel portfolio sitesi.
            
Admin paneli üzerinden tamamen yönetilebilen, dinamik içerik yapısına sahip modern bir web sitesi. Three.js ile geliştirilmiş özel animasyonlar içeriyor.''',
            'technologies': 'Django, Three.js, HTML5, CSS3, JavaScript',
            'features': '''Dinamik içerik yönetimi
Admin panel entegrasyonu
3D animasyonlar
Responsive tasarım
SEO optimizasyonu
İletişim formu''',
            'is_featured': True,
            'order': 3
        }
    ]
    
    for project_data in projects:
        project, created = Project.objects.get_or_create(
            slug=project_data['slug'],
            defaults=project_data
        )
        print(f"✅ Proje: {project.title} {'oluşturuldu' if created else 'zaten mevcut'}")

def create_certificates():
    """Sertifikaları oluştur"""
    certificates = [
        {
            'name': 'Vektörel Academy .Net Software Expertise Certificate',
            'organization': 'Vektörel Academy',
            'date_received': date(2021, 12, 15),
            'description': 'C#, MVC, .Net Framework, SQL, HTML, CSS, Javascript konularında kapsamlı eğitim ve sertifikasyon programı.',
            'order': 1
        },
        {
            'name': 'Python Django Certification',
            'organization': 'Online Course Platform',
            'date_received': date(2022, 6, 10),
            'description': 'Django framework ile web geliştirme konularında uzmanlaşma sertifikası.',
            'order': 2
        },
        {
            'name': 'React.js Developer Certification',
            'organization': 'Frontend Masters',
            'date_received': date(2023, 3, 20),
            'description': 'Modern React.js geliştirme teknikleri ve en iyi uygulamalar sertifikası.',
            'order': 3
        }
    ]
    
    for cert_data in certificates:
        certificate, created = Certificate.objects.get_or_create(
            name=cert_data['name'],
            organization=cert_data['organization'],
            defaults=cert_data
        )
        print(f"✅ Sertifika: {certificate.name} {'oluşturuldu' if created else 'zaten mevcut'}")

def main():
    """Ana fonksiyon"""
    print("🚀 Okan Kantar CV verilerini veritabanına ekleme işlemi başlıyor...\n")
    
    try:
        create_personal_info()
        create_site_settings()
        create_education()
        create_experience()
        create_skills()
        create_projects()
        create_certificates()
        
        print("\n🎉 Tüm veriler başarıyla veritabanına eklendi!")
        print("👉 Şimdi siteyi ziyaret ederek değişiklikleri görebilirsiniz: http://127.0.0.1:8000/")
        
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
        return False
    
    return True

if __name__ == '__main__':
    main()
