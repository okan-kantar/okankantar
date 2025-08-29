// Mountain Fall Animation with Three.js
class MountainFallAnimation {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.mountains = [];
        this.animationId = null;
        this.isAnimating = true;
        this.animationProgress = 0;
        this.init();
    }

    init() {
        this.setupScene();
        this.createMountains();
        this.setupCamera();
        this.setupRenderer();
        this.setupLighting();
        this.startAnimation();
        this.handleResize();
    }

    setupScene() {
        this.scene = new THREE.Scene();
        
        // Gradient background
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = 256;
        canvas.height = 256;
        
        const gradient = context.createLinearGradient(0, 0, 0, 256);
        gradient.addColorStop(0, '#667eea');
        gradient.addColorStop(1, '#764ba2');
        
        context.fillStyle = gradient;
        context.fillRect(0, 0, 256, 256);
        
        const texture = new THREE.CanvasTexture(canvas);
        this.scene.background = texture;
    }

    createMountains() {
        const mountainCount = 5;
        const colors = [
            '#2d3748', '#4a5568', '#2c5282', '#553c9a', '#744210'
        ];

        for (let i = 0; i < mountainCount; i++) {
            const geometry = this.createMountainGeometry(i);
            const material = new THREE.MeshLambertMaterial({
                color: colors[i % colors.length],
                transparent: true,
                opacity: 0.8 - (i * 0.1)
            });
            
            const mountain = new THREE.Mesh(geometry, material);
            mountain.position.z = -i * 2;
            mountain.position.y = 10 + Math.random() * 5; // Start above viewport
            mountain.rotation.x = Math.PI * 0.1;
            
            this.mountains.push(mountain);
            this.scene.add(mountain);
        }
    }

    createMountainGeometry(index) {
        const geometry = new THREE.BufferGeometry();
        const vertices = [];
        const indices = [];
        
        const width = 20;
        const segments = 50;
        const heightVariation = 3 + index * 0.5;
        
        // Create mountain silhouette
        for (let i = 0; i <= segments; i++) {
            const x = (i / segments) * width - width / 2;
            
            // Create multiple peaks with noise
            let height = 0;
            height += Math.sin((i / segments) * Math.PI * 2) * heightVariation;
            height += Math.sin((i / segments) * Math.PI * 6) * heightVariation * 0.3;
            height += Math.sin((i / segments) * Math.PI * 14) * heightVariation * 0.1;
            height += (Math.random() - 0.5) * 0.5;
            
            // Ensure mountains have a base
            vertices.push(x, height, 0);
            vertices.push(x, -2, 0);
        }
        
        // Create triangles
        for (let i = 0; i < segments; i++) {
            const base = i * 2;
            
            // Top triangle
            indices.push(base, base + 2, base + 1);
            
            // Bottom triangle
            indices.push(base + 1, base + 2, base + 3);
        }
        
        geometry.setIndex(indices);
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        geometry.computeVertexNormals();
        
        return geometry;
    }

    setupCamera() {
        this.camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );
        
        // Start camera at high angle looking down
        this.camera.position.set(0, 15, 8);
        this.camera.lookAt(0, 0, 0);
    }

    setupRenderer() {
        const canvas = document.getElementById('mountain-canvas');
        this.renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            antialias: true,
            alpha: true
        });
        
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    }

    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x6b7280, 0.4);
        this.scene.add(ambientLight);
        
        // Directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(5, 10, 5);
        directionalLight.castShadow = true;
        this.scene.add(directionalLight);
        
        // Point light for dramatic effect
        const pointLight = new THREE.PointLight(0x667eea, 1, 100);
        pointLight.position.set(0, 5, 5);
        this.scene.add(pointLight);
    }

    startAnimation() {
        const duration = 2000; // 2 seconds
        const startTime = Date.now();
        
        const animate = () => {
            if (!this.isAnimating) return;
            
            const elapsed = Date.now() - startTime;
            this.animationProgress = Math.min(elapsed / duration, 1);
            
            // Easing function for smooth animation
            const easeProgress = this.easeOutCubic(this.animationProgress);
            
            // Animate mountains falling
            this.mountains.forEach((mountain, index) => {
                const delay = index * 0.1;
                const mountainProgress = Math.max(0, (this.animationProgress - delay) / (1 - delay));
                const easedProgress = this.easeOutBounce(mountainProgress);
                
                // Fall from above
                mountain.position.y = 10 - (easedProgress * 12);
                
                // Slight rotation during fall
                mountain.rotation.x = Math.PI * 0.1 * (1 - easedProgress);
                mountain.rotation.z = Math.sin(elapsed * 0.001 + index) * 0.02 * (1 - easedProgress);
            });
            
            // Animate camera
            const cameraProgress = this.easeOutQuart(this.animationProgress);
            this.camera.position.y = 15 - (cameraProgress * 10);
            this.camera.position.z = 8 - (cameraProgress * 3);
            this.camera.lookAt(0, -2, 0);
            
            this.renderer.render(this.scene, this.camera);
            
            if (this.animationProgress < 1) {
                this.animationId = requestAnimationFrame(animate);
            } else {
                this.completeAnimation();
            }
        };
        
        animate();
    }

    completeAnimation() {
        this.isAnimating = false;
        
        // Show hero content
        const heroContent = document.getElementById('hero-content');
        if (heroContent) {
            heroContent.style.opacity = '1';
            heroContent.style.transform = 'translateY(0)';
        }
        
        // Continue with gentle ambient animation
        this.startAmbientAnimation();
    }

    startAmbientAnimation() {
        const animate = () => {
            const time = Date.now() * 0.0005;
            
            this.mountains.forEach((mountain, index) => {
                // Gentle floating motion
                mountain.position.y = -2 + Math.sin(time + index) * 0.1;
                mountain.rotation.z = Math.sin(time * 0.5 + index) * 0.005;
            });
            
            // Gentle camera sway
            this.camera.position.x = Math.sin(time * 0.2) * 0.1;
            this.camera.position.y = 5 + Math.sin(time * 0.3) * 0.1;
            
            this.renderer.render(this.scene, this.camera);
            requestAnimationFrame(animate);
        };
        
        animate();
    }

    // Easing functions
    easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    }

    easeOutBounce(t) {
        const n1 = 7.5625;
        const d1 = 2.75;

        if (t < 1 / d1) {
            return n1 * t * t;
        } else if (t < 2 / d1) {
            return n1 * (t -= 1.5 / d1) * t + 0.75;
        } else if (t < 2.5 / d1) {
            return n1 * (t -= 2.25 / d1) * t + 0.9375;
        } else {
            return n1 * (t -= 2.625 / d1) * t + 0.984375;
        }
    }

    easeOutQuart(t) {
        return 1 - Math.pow(1 - t, 4);
    }

    handleResize() {
        window.addEventListener('resize', () => {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(window.innerWidth, window.innerHeight);
        });
    }

    destroy() {
        this.isAnimating = false;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        
        // Clean up Three.js resources
        this.mountains.forEach(mountain => {
            mountain.geometry.dispose();
            mountain.material.dispose();
        });
        
        if (this.renderer) {
            this.renderer.dispose();
        }
    }
}

// Initialize animation when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize if we're on the home page and Three.js is available
    if (document.getElementById('mountain-canvas') && typeof THREE !== 'undefined') {
        const mountainAnimation = new MountainFallAnimation();
        
        // Store reference for cleanup
        window.mountainAnimation = mountainAnimation;
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.mountainAnimation) {
        window.mountainAnimation.destroy();
    }
});
