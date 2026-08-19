// Continuous Seamless Infinite Carousel & Animations for Verolite
document.addEventListener('DOMContentLoaded', () => {
    // ==========================================================================
    // About Us Scroll Reveal & Letter Cascade from Left Side
    // ==========================================================================
    const aboutSection = document.querySelector('.about-section');
    if (aboutSection) {
        // Prepare letter splitting for headings
        const splitElements = aboutSection.querySelectorAll('.split-letters');
        
        splitElements.forEach((el, elIndex) => {
            const text = el.textContent.trim();
            el.innerHTML = '';
            
            const startDelay = 250 + (elIndex * 280); // Stagger line 1 and line 2
            
            [...text].forEach((char, charIndex) => {
                const span = document.createElement('span');
                span.className = 'char';
                if (char === ' ') {
                    span.classList.add('space');
                    span.innerHTML = '&nbsp;';
                } else {
                    span.textContent = char;
                }
                const letterDelay = startDelay + (charIndex * 32);
                span.style.transitionDelay = `${letterDelay}ms`;
                el.appendChild(span);
            });
        });

        const observerOptions = {
            threshold: 0.15,
            rootMargin: '0px 0px -40px 0px'
        };

        const aboutObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    aboutSection.classList.add('is-visible');
                    // Add staggered transition delays to elements
                    const animItems = aboutSection.querySelectorAll('.animate-item');
                    animItems.forEach(item => {
                        const delay = item.getAttribute('data-delay') || '0';
                        item.style.transitionDelay = `${delay}ms`;
                    });
                    aboutObserver.unobserve(aboutSection);
                }
            });
        }, observerOptions);

        aboutObserver.observe(aboutSection);

        // Subtle 3D Tilt & Spotlight flare interaction on About image
        const aboutWrapper = document.getElementById('aboutImageWrapper');
        if (aboutWrapper) {
            aboutWrapper.addEventListener('mousemove', (e) => {
                const rect = aboutWrapper.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const percentX = (x / rect.width) * 100;
                const percentY = (y / rect.height) * 100;
                
                aboutWrapper.style.setProperty('--mouse-x', `${percentX.toFixed(1)}%`);
                aboutWrapper.style.setProperty('--mouse-y', `${percentY.toFixed(1)}%`);
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = ((y - centerY) / centerY) * -5;
                const rotateY = ((x - centerX) / centerX) * 5;
                
                aboutWrapper.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.02, 1.02, 1.02)`;
            });

            aboutWrapper.addEventListener('mouseleave', () => {
                aboutWrapper.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
            });
        }
    }
});
