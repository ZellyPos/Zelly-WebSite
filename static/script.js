// YouTube Video ID
const YOUTUBE_VIDEO_ID = 'JURF1v_7R8o';

// Slider State
let currentTestimonialSlide = 0;
let currentFeatureSlide = 0;
let cardsPerView = 3;

function getCardsPerView() {
    if (window.innerWidth <= 768) return 1;
    if (window.innerWidth <= 1024) return 2;
    return 3;
}

function updateTestimonialSlider() {
    const slider = document.querySelector('.testimonials-slider');
    const sliderWrapper = document.querySelector('.testimonials-slider-wrapper');
    if (!slider || !sliderWrapper) return;

    cardsPerView = getCardsPerView();
    const wrapperWidth = sliderWrapper.offsetWidth;
    const gap = 40;
    const cardWidth = (wrapperWidth - (gap * (cardsPerView - 1))) / cardsPerView;

    const cards = document.querySelectorAll('.testimonial-card');
    cards.forEach(card => card.style.width = `${cardWidth}px`);

    const offset = currentTestimonialSlide * (cardWidth + gap);
    slider.style.transform = `translateX(-${offset}px)`;
    updateTestimonialDots();
}

function updateFeaturesSlider() {
    const slider = document.querySelector('.features-grid');
    const sliderWrapper = document.querySelector('.features-slider-wrapper');
    if (!slider || !sliderWrapper) return;

    const cardsPerViewFeatures = getCardsPerView();
    const wrapperWidth = sliderWrapper.offsetWidth;
    const gap = 40;
    const cardWidth = (wrapperWidth - (gap * (cardsPerViewFeatures - 1))) / cardsPerViewFeatures;

    const cards = document.querySelectorAll('.feature-card');
    cards.forEach(card => card.style.width = `${cardWidth}px`);

    const offset = currentFeatureSlide * (cardWidth + gap);
    slider.style.transform = `translateX(-${offset}px)`;
}

function slideFeatures(direction) {
    const cards = document.querySelectorAll('.feature-card');
    const cpv = getCardsPerView();
    const maxSlide = cards.length - cpv;

    currentFeatureSlide += direction;
    if (currentFeatureSlide < 0) currentFeatureSlide = maxSlide;
    else if (currentFeatureSlide > maxSlide) currentFeatureSlide = 0;

    updateFeaturesSlider();
}

function slideTestimonials(direction) {
    const cards = document.querySelectorAll('.testimonial-card');
    const cpv = getCardsPerView();
    const maxSlide = cards.length - cpv;

    currentTestimonialSlide += direction;
    if (currentTestimonialSlide < 0) currentTestimonialSlide = maxSlide;
    else if (currentTestimonialSlide > maxSlide) currentTestimonialSlide = 0;

    updateTestimonialSlider();
}

function goToTestimonialSlide(index) {
    currentTestimonialSlide = index;
    updateTestimonialSlider();
}

function createTestimonialDots() {
    const dotsContainer = document.getElementById('testimonialDots');
    if (!dotsContainer) return;

    const cards = document.querySelectorAll('.testimonial-card');
    const cpv = getCardsPerView();
    const maxSlide = cards.length - cpv;

    dotsContainer.innerHTML = '';
    for (let i = 0; i <= maxSlide; i++) {
        const dot = document.createElement('span');
        dot.className = 'dot';
        dot.onclick = () => goToTestimonialSlide(i);
        dotsContainer.appendChild(dot);
    }
    updateTestimonialDots();
}

function updateTestimonialDots() {
    const dots = document.querySelectorAll('.slider-dots .dot');
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentTestimonialSlide);
    });
}

// FAQ Toggle
function toggleFAQ(button) {
    const faqItem = button.parentElement;
    if (!faqItem) return;
    const isActive = faqItem.classList.contains('active');

    // Close all FAQ items
    document.querySelectorAll('.faq-item').forEach(item => {
        item.classList.remove('active');
    });

    // Open clicked item if it wasn't active
    if (!isActive) {
        faqItem.classList.add('active');
    }
}

// Video Modal Functions
function openVideoModal(videoId = null) {
    console.log('Attempting to open video modal...');
    const modal = document.getElementById('videoModal');
    const iframe = document.getElementById('youtubeVideo');
    if (modal && iframe) {
        const vid = videoId || YOUTUBE_VIDEO_ID;
        const origin = window.location.origin;
        iframe.src = `https://www.youtube.com/embed/${vid}?autoplay=1&rel=0&enablejsapi=1&origin=${origin}`;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        console.log('Modal opened successfully with ID:', vid);
    } else {
        console.error('Video modal or iframe not found in DOM!');
        alert('Texnik nosozlik: Video modal topilmadi. Sahifani qayta yuklab ko\'ring.');
    }
}

function closeVideoModal() {
    console.log('Closing video modal...');
    const modal = document.getElementById('videoModal');
    const iframe = document.getElementById('youtubeVideo');
    if (modal && iframe) {
        iframe.src = '';
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

// Contact Modal Functions
function openContactModal(plan = '') {
    console.log('Opening contact modal for plan:', plan);
    const modal = document.getElementById('contactModal');
    const planSelect = document.getElementById('contactPlan');
    if (modal) {
        if (planSelect && plan) planSelect.value = plan;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    } else {
        console.error('Contact modal not found!');
    }
}

function closeContactModal() {
    const modal = document.getElementById('contactModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
        const form = document.querySelector('.contact-form');
        if (form) form.reset();
    }
}

function handleContactSubmit(event) {
    event.preventDefault();
    const name = document.getElementById('contactName')?.value;
    const phone = document.getElementById('contactPhone')?.value;
    const plan = document.getElementById('contactPlan')?.value;
    const message = document.getElementById('contactMessage')?.value;

    console.log('Form yuborildi:', { name, phone, plan, message });

    const modalContent = document.querySelector('.contact-modal-content');
    if (modalContent) {
        const originalContent = modalContent.innerHTML;
        modalContent.innerHTML = `
            <button class="modal-close" onclick="closeContactModal()">&times;</button>
            <div class="success-message">
                <div class="success-icon">✓</div>
                <h3>Muvaffaqiyatli yuborildi!</h3>
                <p>Rahmat, ${name}! Sizning so'rovingiz qabul qilindi.<br>Tez orada ${phone} raqamiga qo'ng'iroq qilamiz.</p>
            </div>
        `;

        setTimeout(() => {
            closeContactModal();
            // Restore content after closing so it's ready for next time
            setTimeout(() => { modalContent.innerHTML = originalContent; }, 500);
        }, 3000);
    }
}

// Global Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded. Initializing sliders...');
    createTestimonialDots();
    updateTestimonialSlider();
    updateFeaturesSlider();

    // Scroll Animations
    try {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -100px 0px' });

        document.querySelectorAll('.feature-card, .benefit-item, .testimonial-card, .pricing-card, .faq-item').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.6s ease';
            observer.observe(el);
        });
    } catch (e) {
        console.warn('IntersectionObserver not supported or failed:', e);
    }

    if (typeof AOS !== 'undefined') AOS.refresh();
});

let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        updateTestimonialSlider();
        updateFeaturesSlider();
        createTestimonialDots();
    }, 250);
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeVideoModal();
        closeContactModal();
    }
});

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href === '#') return; // Do nothing for empty hashes

        e.preventDefault();
        try {
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        } catch (err) {
            console.warn('Invalid selector for smooth scroll:', href);
        }
    });
});
