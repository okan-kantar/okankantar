#!/usr/bin/env python
"""
Proje verilerini güncelleyen script - Demo URL ve GitHub URL ekler
"""
import os
import sys
import django

# Django settings yapılandırması
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'okankantar.settings')
django.setup()

from core.models import Project

def update_projects():
    """Proje verilerini güncelle"""
    projects_data = {
        'e-ticaret-platformu': {
            'demo_url': 'https://demo-eticaret.example.com',
            'github_url': 'https://github.com/okan-kantar/eticaret-platform'
        },
        'stok-yonetim-sistemi': {
            'demo_url': '',
            'github_url': 'https://github.com/okan-kantar/stok-yonetim'
        },
        'kisisel-portfolio-sitesi': {
            'demo_url': 'http://127.0.0.1:8000',
            'github_url': 'https://github.com/okan-kantar/portfolio'
        }
    }
    
    for slug, urls in projects_data.items():
        try:
            project = Project.objects.get(slug=slug)
            project.demo_url = urls['demo_url']
            project.github_url = urls['github_url']
            project.save()
            print(f"✅ {project.title} güncellendi")
        except Project.DoesNotExist:
            print(f"❌ {slug} projesi bulunamadı")

def main():
    """Ana fonksiyon"""
    print("🔗 Proje URL'lerini güncelliyorum...\n")
    
    try:
        update_projects()
        print("\n🎉 Proje URL'leri başarıyla güncellendi!")
        
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
        return False
    
    return True

if __name__ == '__main__':
    main()
