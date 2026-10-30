// Initialize GSAP ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', () => {
    // 1. Page Load Transitions (Fade In & Slide Up)
    const tl = gsap.timeline();
    
    // Animate Navbar
    tl.from('#navbar', {
        y: -50,
        opacity: 0,
        duration: 0.8,
        ease: 'power3.out'
    });

    // Animate Hero Content (if on index page)
    const heroH1 = document.querySelector('.hero h1');
    if (heroH1) {
        tl.from('.hero h1', {
            y: 30,
            opacity: 0,
            duration: 0.8,
            ease: 'power3.out'
        }, '-=0.4')
        .from('.hero p', {
            y: 20,
            opacity: 0,
            duration: 0.6,
            ease: 'power3.out'
        }, '-=0.6')
        .from('.hero .btn', {
            y: 20,
            opacity: 0,
            duration: 0.6,
            stagger: 0.1,
            ease: 'power3.out'
        }, '-=0.4')
        .from('.hero > .container > div:nth-child(2)', {
            x: 50,
            opacity: 0,
            duration: 1,
            ease: 'power3.out'
        }, '-=0.8');
    }

    // 2. Scroll Animations (AOS style using GSAP)
    const cards = gsap.utils.toArray('.card');
    cards.forEach(card => {
        // Skip animating the form card on load since it's above fold
        if (card.id === 'form-card') {
            gsap.from(card, {
                y: 40,
                opacity: 0,
                duration: 0.8,
                ease: 'power3.out',
                delay: 0.2
            });
            return;
        }
        
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 85%',
                toggleActions: 'play none none reverse'
            },
            y: 50,
            opacity: 0,
            duration: 0.7,
            ease: 'power3.out'
        });
    });

    // 3. Staggered List Items (e.g., Saved Phones grid)
    const savedGrid = document.querySelector('.section .container > div[style*="display: grid"]');
    if (savedGrid && savedGrid.children.length > 0) {
        gsap.from(savedGrid.children, {
            scrollTrigger: {
                trigger: savedGrid,
                start: 'top 80%',
            },
            y: 30,
            opacity: 0,
            duration: 0.6,
            stagger: 0.1,
            ease: 'power2.out'
        });
    }

    // Add hover-float class to cards automatically
    document.querySelectorAll('.card').forEach(el => {
        if (!el.id.includes('form') && !el.id.includes('result')) {
            el.classList.add('hover-float');
        }
    });
});

// Expose a function to animate the Result Container specifically (called from prediction.js)
window.animateResult = function() {
    gsap.from('#result-container', {
        y: 40,
        opacity: 0,
        duration: 0.8,
        ease: 'power3.out'
    });
    
    // Number counter animation for price
    const fairPrice = document.getElementById('res-fair-price');
    const currentPrice = document.getElementById('res-current-price');
    
    if (fairPrice && currentPrice) {
        // We'd parse the text to integers and animate them up, but since it's already rendered with ₹
        // simple scale pop is cleaner and safer
        gsap.from([fairPrice, currentPrice], {
            scale: 0.8,
            opacity: 0,
            duration: 0.6,
            stagger: 0.1,
            delay: 0.2,
            ease: 'back.out(1.5)'
        });
    }
};
