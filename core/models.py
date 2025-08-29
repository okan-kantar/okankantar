from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class PersonalInfo(models.Model):
    """Kişisel bilgiler - sadece tek bir kayıt olacak"""
    name = models.CharField(max_length=100, verbose_name="Ad Soyad", default="Okan Kantar")
    title = models.CharField(max_length=200, verbose_name="Ünvan", default="Full Stack Developer")
    bio = models.TextField(verbose_name="Kısa Tanıtım", help_text="Ana sayfada görünecek kısa tanıtım")
    about_text = models.TextField(verbose_name="Hakkımda Metni", help_text="Hakkımda sayfasında görünecek detaylı metin")
    birth_year = models.IntegerField(verbose_name="Doğum Yılı", default=1989)
    location = models.CharField(max_length=100, verbose_name="Lokasyon", default="Ankara, Türkiye")
    email = models.EmailField(verbose_name="E-posta", default="okkant@gmail.com")
    phone = models.CharField(max_length=20, verbose_name="Telefon", default="0539 315 6407")
    linkedin_url = models.URLField(verbose_name="LinkedIn URL", blank=True)
    github_url = models.URLField(verbose_name="GitHub URL", blank=True)
    profile_image = models.ImageField(upload_to='profile/', verbose_name="Profil Fotoğrafı", blank=True, null=True)
    cv_file = models.FileField(upload_to='files/', verbose_name="CV Dosyası", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Kişisel Bilgi"
        verbose_name_plural = "Kişisel Bilgiler"
    
    def __str__(self):
        return self.name
    
    @property
    def age(self):
        from datetime import datetime
        return datetime.now().year - self.birth_year

class Education(models.Model):
    DEGREE_CHOICES = [
        ('lisans', 'Lisans'),
        ('yuksek_lisans', 'Yüksek Lisans'),
        ('doktora', 'Doktora'),
        ('sertifika', 'Sertifika'),
    ]
    
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES, verbose_name="Derece")
    school = models.CharField(max_length=200, verbose_name="Okul/Kurum")
    department = models.CharField(max_length=200, verbose_name="Bölüm")
    start_year = models.IntegerField(verbose_name="Başlangıç Yılı")
    end_year = models.IntegerField(verbose_name="Bitiş Yılı", null=True, blank=True)
    location = models.CharField(max_length=100, verbose_name="Şehir")
    description = models.TextField(verbose_name="Açıklama", blank=True)
    is_current = models.BooleanField(default=False, verbose_name="Devam Ediyor")
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Eğitim"
        verbose_name_plural = "Eğitimler"
        ordering = ['-start_year', '-order']
    
    def __str__(self):
        return f"{self.degree} - {self.school}"
    
    @property
    def years_display(self):
        if self.is_current:
            return f"{self.start_year} - Devam ediyor"
        return f"{self.start_year} - {self.end_year}"

class Experience(models.Model):
    position = models.CharField(max_length=200, verbose_name="Pozisyon")
    company = models.CharField(max_length=200, verbose_name="Şirket")
    location = models.CharField(max_length=100, verbose_name="Şehir")
    start_date = models.DateField(verbose_name="Başlangıç Tarihi")
    end_date = models.DateField(verbose_name="Bitiş Tarihi", null=True, blank=True)
    description = models.TextField(verbose_name="Açıklama", blank=True)
    is_current = models.BooleanField(default=False, verbose_name="Mevcut Pozisyon")
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Deneyim"
        verbose_name_plural = "Deneyimler"
        ordering = ['-start_date', '-order']
    
    def __str__(self):
        return f"{self.position} - {self.company}"
    
    @property
    def years_display(self):
        start = self.start_date.strftime("%m.%Y")
        if self.is_current:
            return f"{start} - günümüz"
        end = self.end_date.strftime("%m.%Y") if self.end_date else "günümüz"
        return f"{start} - {end}"

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programlama Dilleri'),
        ('framework', 'Framework ve Kütüphaneler'),
        ('database', 'Veritabanları'),
        ('tool', 'Araçlar ve Teknolojiler'),
        ('soft', 'Kişisel Beceriler'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Yetenek Adı")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Kategori")
    level = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Seviye (%)",
        help_text="0-100 arası değer"
    )
    icon_class = models.CharField(max_length=100, verbose_name="İkon Sınıfı", blank=True, help_text="Font Awesome sınıfı (örn: fab fa-python)")
    description = models.TextField(verbose_name="Açıklama", blank=True)
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan")
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Yetenek"
        verbose_name_plural = "Yetenekler"
        ordering = ['category', '-level', 'order']
    
    def __str__(self):
        return f"{self.name} ({self.level}%)"

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web Uygulaması'),
        ('desktop', 'Masaüstü Uygulaması'),
        ('mobile', 'Mobil Uygulama'),
        ('api', 'API Projesi'),
        ('website', 'Web Sitesi'),
        ('other', 'Diğer'),
    ]
    
    STATUS_CHOICES = [
        ('completed', 'Tamamlandı'),
        ('in_progress', 'Devam Ediyor'),
        ('planned', 'Planlandı'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Proje Başlığı")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL Slug")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Kategori")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed', verbose_name="Durum")
    short_description = models.TextField(max_length=300, verbose_name="Kısa Açıklama")
    description = models.TextField(verbose_name="Detaylı Açıklama")
    technologies = models.CharField(max_length=500, verbose_name="Kullanılan Teknolojiler", help_text="Virgülle ayırın")
    features = models.TextField(verbose_name="Özellikler", help_text="Her satıra bir özellik")
    image = models.ImageField(upload_to='projects/', verbose_name="Proje Görseli", blank=True, null=True)
    demo_url = models.URLField(verbose_name="Demo URL", blank=True)
    github_url = models.URLField(verbose_name="GitHub URL", blank=True)
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan")
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    created_date = models.DateField(verbose_name="Oluşturma Tarihi", auto_now_add=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Proje"
        verbose_name_plural = "Projeler"
        ordering = ['-created_date', '-order']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('core:project_detail', kwargs={'slug': self.slug})
    
    @property
    def tech_list(self):
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]
    
    @property
    def features_list(self):
        return [feature.strip() for feature in self.features.split('\n') if feature.strip()]

class Certificate(models.Model):
    name = models.CharField(max_length=200, verbose_name="Sertifika Adı")
    organization = models.CharField(max_length=200, verbose_name="Veren Kurum")
    date_received = models.DateField(verbose_name="Alınma Tarihi")
    description = models.TextField(verbose_name="Açıklama", blank=True)
    credential_id = models.CharField(max_length=100, verbose_name="Sertifika ID", blank=True)
    credential_url = models.URLField(verbose_name="Sertifika URL", blank=True)
    image = models.ImageField(upload_to='certificates/', verbose_name="Sertifika Görseli", blank=True, null=True)
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Sertifika"
        verbose_name_plural = "Sertifikalar"
        ordering = ['-date_received', 'order']
    
    def __str__(self):
        return f"{self.name} - {self.organization}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ad Soyad")
    email = models.EmailField(verbose_name="E-posta")
    subject = models.CharField(max_length=200, verbose_name="Konu", blank=True)
    message = models.TextField(verbose_name="Mesaj")
    is_read = models.BooleanField(default=False, verbose_name="Okundu")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Gönderim Tarihi")
    
    class Meta:
        verbose_name = "İletişim Mesajı"
        verbose_name_plural = "İletişim Mesajları"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject or 'Konusuz'}"

class SiteSettings(models.Model):
    """Site genel ayarları"""
    site_title = models.CharField(max_length=100, verbose_name="Site Başlığı", default="Okan Kantar")
    site_description = models.TextField(verbose_name="Site Açıklaması")
    meta_keywords = models.CharField(max_length=500, verbose_name="Meta Anahtar Kelimeler", blank=True)
    footer_text = models.CharField(max_length=200, verbose_name="Footer Metni", default="© 2024 Okan Kantar. Tüm hakları saklıdır.")
    google_analytics_id = models.CharField(max_length=20, verbose_name="Google Analytics ID", blank=True)
    
    # Hero section settings
    hero_title = models.CharField(max_length=200, verbose_name="Hero Başlık", default="Merhaba, Ben Okan Kantar")
    hero_subtitle = models.CharField(max_length=200, verbose_name="Hero Alt Başlık", default="Full Stack Developer")
    hero_description = models.TextField(verbose_name="Hero Açıklama")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Ayarları"
        verbose_name_plural = "Site Ayarları"
    
    def __str__(self):
        return "Site Ayarları"
    
    def save(self, *args, **kwargs):
        # Sadece bir tane site ayarları olsun
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('Sadece bir Site Ayarları kaydı olabilir')
        return super().save(*args, **kwargs)
