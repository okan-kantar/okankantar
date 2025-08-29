from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    """Ana sayfa - dağdan düşme animasyonu ile başlayan hero section"""
    return render(request, 'core/home.html')

def about(request):
    """Hakkımda sayfası - detaylı bilgiler"""
    context = {
        'education': [
            {
                'degree': 'Yüksek Lisans',
                'school': 'Hacettepe Üniversitesi',
                'department': 'Finans/Finance',
                'years': '07.2019 - 06.2021',
                'location': 'Ankara'
            },
            {
                'degree': 'Lisans',
                'school': 'Gazi Üniversitesi',
                'department': 'İktisat/Economics',
                'years': '09.2006 - 06.2011',
                'location': 'Ankara'
            }
        ],
        'experience': [
            {
                'position': 'Yazılım Takım Lideri',
                'company': 'Tarım ve Kırsal Kalkınmayı Destekleme Kurumu',
                'years': '12.2024 - günümüz',
                'location': 'Ankara, Türkiye'
            },
            {
                'position': 'Yazılım Geliştirme Uzmanı',
                'company': 'Tarım ve Kırsal Kalkınmayı Destekleme Kurumu',
                'years': '12.2022 - 12.2024',
                'location': 'Ankara, Türkiye'
            },
            {
                'position': '.Net Yazılım Uzmanlığı Eğitmenliği',
                'company': 'Vektörel Akademi',
                'years': '01.2023',
                'location': 'Ankara, Türkiye'
            },
            {
                'position': 'Bütçe ve Muhasebe Uzmanı',
                'company': 'Tarım ve Kırsal Kalkınmayı Destekleme Kurumu',
                'years': '10.2018 - 12.2022',
                'location': 'Ankara, Türkiye'
            },
            {
                'position': 'Bütçe ve Raporlama Uzmanı',
                'company': 'Milli Savunma Bakanlığı',
                'years': '10.2014 - 10.2018',
                'location': 'Ankara, Türkiye'
            }
        ]
    }
    return render(request, 'core/about.html', context)

def projects(request):
    """Projeler sayfası"""
    return render(request, 'core/projects.html')

def skills(request):
    """Yetenekler sayfası"""
    skills_data = {
        'programming_languages': [
            {'name': 'C#', 'level': 90},
            {'name': 'Python', 'level': 85},
            {'name': 'JavaScript', 'level': 88},
            {'name': 'SQL', 'level': 85},
        ],
        'frameworks': [
            {'name': '.NET Core', 'level': 90},
            {'name': 'Django', 'level': 80},
            {'name': 'React', 'level': 75},
            {'name': 'Bootstrap', 'level': 85},
        ],
        'databases': [
            {'name': 'MSSQL', 'level': 85},
            {'name': 'SQLite', 'level': 80},
            {'name': 'MySQL', 'level': 75},
            {'name': 'PostgreSQL', 'level': 70},
        ],
        'tools': [
            {'name': 'Visual Studio', 'level': 90},
            {'name': 'VS Code', 'level': 85},
            {'name': 'Git', 'level': 80},
            {'name': 'Docker', 'level': 70},
        ]
    }
    return render(request, 'core/skills.html', {'skills': skills_data})

def contact(request):
    """İletişim sayfası"""
    if request.method == 'POST':
        # AJAX ile gelen form verilerini işle
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')
            
            # Burada e-posta gönderme veya veritabanına kaydetme işlemi yapılabilir
            # Şimdilik sadece başarılı response döndürüyoruz
            
            return JsonResponse({
                'success': True,
                'message': 'Mesajınız başarıyla gönderildi! En kısa sürede size dönüş yapacağım.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Bir hata oluştu. Lütfen tekrar deneyin.'
            })
    
    return render(request, 'core/contact.html')
