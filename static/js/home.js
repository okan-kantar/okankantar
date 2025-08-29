// Home Page Specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initHeroAnimations();
    initProjectFilters();
    initSkillBars();
    initTestimonialSlider();
    initParticleSystem();
});

// Hero section animations
function initHeroAnimations() {
    const heroText = document.querySelector('.hero-text');
    const heroImage = document.querySelector('.hero-image');
    
    if (heroText && heroImage) {
        // Stagger animation for hero elements
        const heroElements = heroText.querySelectorAll('h1, h2, p, .hero-buttons');
        
        heroElements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                element.style.transition = 'all 0.8s ease';
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, 2200 + (index * 200));
        });
        
        // Typewriter effect for name
        setTimeout(() => {
            typewriterEffect('.name-highlight', 'Okan Kantar');
        }, 2500);
    }
}

// Typewriter effect
function typewriterEffect(selector, text) {
    const element = document.querySelector(selector);
    if (!element) return;
    
    element.textContent = '';
    let i = 0;
    
    const timer = setInterval(() => {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
        } else {
            clearInterval(timer);
            element.classList.add('typing-complete');
        }
    }, 100);
}

// Project filtering
function initProjectFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const filter = button.getAttribute('data-filter');
            
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Filter projects
            projectCards.forEach(card => {
                const categories = card.getAttribute('data-category').split(' ');
                
                if (filter === 'all' || categories.includes(filter)) {
                    card.style.display = 'block';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'scale(1)';
                    }, 100);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.8)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                }
            });
        });
    });
}

// Animated skill bars
function initSkillBars() {
    const skillBars = document.querySelectorAll('.skill-progress');
    
    const skillObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const skillBar = entry.target;
                const percentage = skillBar.getAttribute('data-percentage');
                
                skillBar.style.width = percentage + '%';
                
                // Add number animation
                const numberElement = skillBar.parentElement.querySelector('.skill-percentage');
                if (numberElement) {
                    animateNumber(numberElement, 0, parseInt(percentage), 1500);
                }
                
                skillObserver.unobserve(skillBar);
            }
        });
    }, { threshold: 0.5 });
    
    skillBars.forEach(bar => {
        skillObserver.observe(bar);
    });
}

// Number animation
function animateNumber(element, start, end, duration) {
    const range = end - start;
    const startTime = performance.now();
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const easeProgress = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        const current = start + (range * easeProgress);
        
        element.textContent = Math.floor(current) + '%';
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }
    
    requestAnimationFrame(updateNumber);
}

// Testimonial slider
function initTestimonialSlider() {
    const slider = document.querySelector('.testimonial-slider');
    const slides = document.querySelectorAll('.testimonial-slide');
    const dots = document.querySelectorAll('.testimonial-dot');
    
    if (!slider || slides.length === 0) return;
    
    let currentSlide = 0;
    const slideCount = slides.length;
    
    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === index);
        });
        
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
        
        slider.style.transform = `translateX(-${index * 100}%)`;
    }
    
    function nextSlide() {
        currentSlide = (currentSlide + 1) % slideCount;
        showSlide(currentSlide);
    }
    
    function prevSlide() {
        currentSlide = (currentSlide - 1 + slideCount) % slideCount;
        showSlide(currentSlide);
    }
    
    // Dot navigation
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            showSlide(currentSlide);
        });
    });
    
    // Auto-play
    setInterval(nextSlide, 5000);
    
    // Arrow navigation
    const prevBtn = document.querySelector('.testimonial-prev');
    const nextBtn = document.querySelector('.testimonial-next');
    
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);
}

// Particle system for background
function initParticleSystem() {
    const particleContainer = document.querySelector('.particle-container');
    
    if (!particleContainer) return;
    
    const particleCount = 50;
    const particles = [];
    
    for (let i = 0; i < particleCount; i++) {
        createParticle();
    }
    
    function createParticle() {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random properties
        const size = Math.random() * 3 + 1;
        const x = Math.random() * window.innerWidth;
        const y = window.innerHeight + 10;
        const speed = Math.random() * 2 + 1;
        const opacity = Math.random() * 0.5 + 0.3;
        
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.opacity = opacity;
        
        particleContainer.appendChild(particle);
        
        // Animate particle
        animateParticle(particle, speed);
        
        particles.push(particle);
    }
    
    function animateParticle(particle, speed) {
        let y = parseInt(particle.style.top);
        
        function move() {
            y -= speed;
            particle.style.top = y + 'px';
            
            // Remove particle when it goes off screen
            if (y < -10) {
                particle.remove();
                const index = particles.indexOf(particle);
                if (index > -1) {
                    particles.splice(index, 1);
                }
                
                // Create new particle
                setTimeout(createParticle, Math.random() * 2000);
                return;
            }
            
            requestAnimationFrame(move);
        }
        
        move();
    }
}

// Scroll-triggered animations
function initScrollAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const animationType = element.getAttribute('data-animation') || 'fadeInUp';
                
                element.classList.add('animate-' + animationType);
                observer.unobserve(element);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    elements.forEach(element => {
        observer.observe(element);
    });
}

// Magnetic button effect
function initMagneticButtons() {
    const magneticButtons = document.querySelectorAll('.magnetic-btn');
    
    magneticButtons.forEach(button => {
        button.addEventListener('mousemove', (e) => {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            button.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px)`;
        });
        
        button.addEventListener('mouseleave', () => {
            button.style.transform = 'translate(0, 0)';
        });
    });
}

// Text scramble effect
function scrambleText(element, finalText, duration = 1000) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    const steps = 20;
    const stepDuration = duration / steps;
    let step = 0;
    
    const timer = setInterval(() => {
        let scrambledText = '';
        
        for (let i = 0; i < finalText.length; i++) {
            if (i < step) {
                scrambledText += finalText[i];
            } else {
                scrambledText += chars[Math.floor(Math.random() * chars.length)];
            }
        }
        
        element.textContent = scrambledText;
        step++;
        
        if (step > finalText.length) {
            clearInterval(timer);
            element.textContent = finalText;
        }
    }, stepDuration);
}

// Parallax mouse movement
function initMouseParallax() {
    const parallaxElements = document.querySelectorAll('.mouse-parallax');
    
    document.addEventListener('mousemove', (e) => {
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        parallaxElements.forEach(element => {
            const speed = element.getAttribute('data-speed') || 5;
            const x = (mouseX - 0.5) * speed;
            const y = (mouseY - 0.5) * speed;
            
            element.style.transform = `translate(${x}px, ${y}px)`;
        });
    });
}

// Initialize additional features
document.addEventListener('DOMContentLoaded', () => {
    initScrollAnimations();
    initMagneticButtons();
    initMouseParallax();
});

// Export functions for external use
window.OkanKantarHome = {
    typewriterEffect,
    animateNumber,
    scrambleText
};
