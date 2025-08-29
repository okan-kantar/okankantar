// General Animation and JavaScript Functions
document.addEventListener('DOMContentLoaded', function() {
    initAnimations();
    initScrollEffects();
    initPerformanceOptimizations();
});

function initAnimations() {
    // Stagger animations for elements
    const staggerElements = document.querySelectorAll('.stagger-item');
    staggerElements.forEach((element, index) => {
        element.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Entrance animations
    const entranceElements = document.querySelectorAll('[data-entrance]');
    
    const entranceObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const animationType = element.getAttribute('data-entrance');
                element.classList.add(`animate-${animationType}`);
                entranceObserver.unobserve(element);
            }
        });
    }, { threshold: 0.1 });
    
    entranceElements.forEach(element => {
        entranceObserver.observe(element);
    });
}

function initScrollEffects() {
    // Parallax elements
    const parallaxElements = document.querySelectorAll('.parallax-element');
    
    if (parallaxElements.length > 0) {
        window.addEventListener('scroll', throttle(() => {
            const scrollTop = window.pageYOffset;
            
            parallaxElements.forEach(element => {
                const speed = element.getAttribute('data-speed') || 0.5;
                const yPos = -(scrollTop * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
        }, 16)); // ~60fps
    }
    
    // Progress indicators
    updateScrollProgress();
    window.addEventListener('scroll', throttle(updateScrollProgress, 16));
}

function updateScrollProgress() {
    const progressElements = document.querySelectorAll('.scroll-progress');
    
    progressElements.forEach(element => {
        const winHeight = window.innerHeight;
        const docHeight = document.documentElement.scrollHeight - winHeight;
        const scrollTop = window.pageYOffset;
        const scrollPercent = (scrollTop / docHeight) * 100;
        
        element.style.width = `${scrollPercent}%`;
    });
}

function initPerformanceOptimizations() {
    // Lazy load images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Preload critical resources
    preloadCriticalResources();
}

function preloadCriticalResources() {
    const criticalImages = [
        '/static/img/hero-bg.jpg',
        '/static/img/profile.jpg'
    ];
    
    criticalImages.forEach(src => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'image';
        link.href = src;
        document.head.appendChild(link);
    });
}

// Utility functions
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

function debounce(func, wait, immediate) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Export for global use
window.OkanKantarUtils = {
    throttle,
    debounce,
    updateScrollProgress
};
