// Mobile menu functionality and Hero Slider
document.addEventListener('DOMContentLoaded', function () {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navMenu = document.getElementById('navMenu');

    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', function () {
            navMenu.classList.toggle('active');
            mobileMenuBtn.innerHTML = navMenu.classList.contains('active') ?
                '<i class="fas fa-times"></i>' : '<i class="fas fa-bars"></i>';
        });
    }

    // Hero Slider
    const heroSlider = document.getElementById('heroSlider');
    if (heroSlider) {
        const slides = heroSlider.querySelectorAll('.slide');
        console.log('Hero Slider found. Slides count:', slides.length);

        if (slides.length > 0) {
            const prevBtn = document.getElementById('prevSlide');
            const nextBtn = document.getElementById('nextSlide');
            const indicators = document.getElementById('sliderIndicators') ? document.getElementById('sliderIndicators').querySelectorAll('.indicator') : [];
            let currentSlide = 0;
            const slideInterval = 5000; // 5 seconds

            function showSlide(index) {
                slides.forEach(slide => slide.classList.remove('active'));
                if (indicators.length > 0) {
                    indicators.forEach(ind => ind.classList.remove('active'));
                }

                currentSlide = (index + slides.length) % slides.length;

                slides[currentSlide].classList.add('active');
                if (indicators.length > 0) {
                    indicators[currentSlide].classList.add('active');
                }
            }

            function nextSlide() {
                showSlide(currentSlide + 1);
            }

            function prevSlide() {
                showSlide(currentSlide - 1);
            }

            // Auto slide
            let slideTimer = setInterval(nextSlide, slideInterval);

            // Reset timer on user interaction
            function resetTimer() {
                clearInterval(slideTimer);
                slideTimer = setInterval(nextSlide, slideInterval);
            }

            if (prevBtn) {
                prevBtn.addEventListener('click', () => {
                    prevSlide();
                    resetTimer();
                });
            }

            if (nextBtn) {
                nextBtn.addEventListener('click', () => {
                    nextSlide();
                    resetTimer();
                });
            }

            if (indicators.length > 0) {
                indicators.forEach((indicator, index) => {
                    indicator.addEventListener('click', () => {
                        showSlide(index);
                        resetTimer();
                    });
                });
            }
        } // End if (slides.length > 0)
    } // End if (heroSlider)

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Newsletter form handling with AJAX
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const emailInput = document.getElementById('newsletter-email');
            const submitBtn = document.getElementById('newsletter-btn');
            const messageDiv = document.getElementById('newsletter-message');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // Disable button and show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Subscribing...';
            messageDiv.style.display = 'none';
            messageDiv.classList.remove('success', 'error');

            const formData = new FormData();
            formData.append('email', emailInput.value);
            formData.append('csrfmiddlewaretoken', csrfToken);

            fetch('/subscribe/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => response.json())
                .then(data => {
                    messageDiv.style.display = 'block';
                    messageDiv.textContent = data.message;

                    if (data.status === 'success') {
                        messageDiv.style.color = 'green';
                        emailInput.value = '';
                    } else {
                        messageDiv.style.color = 'red';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    messageDiv.style.display = 'block';
                    messageDiv.textContent = 'An error occurred. Please try again.';
                    messageDiv.style.color = 'red';
                })
                .finally(() => {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Subscribe';
                });
        });
    }
}); // End of DOMContentLoaded

// Copy to clipboard functionality
function copyToClipboard(text) {
    // Create a temporary textarea element
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);

    // Select and copy the text
    textarea.select();
    textarea.setSelectionRange(0, 99999); // For mobile devices

    try {
        const successful = document.execCommand('copy');
        const msg = successful ? 'successful' : 'unsuccessful';
        console.log('Copying text command was ' + msg);

        // Show success feedback
        showCopyFeedback('Link copied to clipboard!');
    } catch (err) {
        console.error('Unable to copy to clipboard', err);

        // Fallback: Use the Clipboard API if available
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                showCopyFeedback('Link copied to clipboard!');
            }).catch(err => {
                console.error('Could not copy text: ', err);
                showCopyFeedback('Failed to copy link', false);
            });
        } else {
            showCopyFeedback('Failed to copy link', false);
        }
    }

    // Clean up
    document.body.removeChild(textarea);
}

// Show copy feedback notification
function showCopyFeedback(message, isSuccess = true) {
    // Remove existing feedback if any
    const existingFeedback = document.querySelector('.copy-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }

    // Create feedback element
    const feedback = document.createElement('div');
    feedback.className = `copy-feedback ${isSuccess ? 'success' : 'error'}`;
    feedback.innerHTML = `
        <i class="fas ${isSuccess ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
        <span>${message}</span>
    `;

    // Style the feedback
    feedback.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${isSuccess ? '#10b981' : '#ef4444'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: var(--radius);
        box-shadow: var(--shadow-lg);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        z-index: 10000;
        animation: slideInRight 0.3s ease;
    `;

    document.body.appendChild(feedback);

    // Remove after 3 seconds
    setTimeout(() => {
        feedback.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => feedback.remove(), 300);
    }, 3000);
}

// Add CSS animations for feedback
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .copy-feedback {
        font-weight: 500;
    }
    
    .copy-feedback i {
        font-size: 1.2rem;
    }
`;
document.head.appendChild(style);

// Enhanced social sharing with analytics tracking
document.addEventListener('DOMContentLoaded', function () {
    // Track social shares
    const socialLinks = document.querySelectorAll('a[href*="twitter.com"], a[href*="facebook.com"], a[href*="linkedin.com"], a[href*="reddit.com"]');

    socialLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const platform = this.href.includes('twitter') ? 'twitter' :
                this.href.includes('facebook') ? 'facebook' :
                    this.href.includes('linkedin') ? 'linkedin' :
                        this.href.includes('reddit') ? 'reddit' : 'unknown';

            // You can add analytics tracking here
            console.log(`Shared on ${platform}: ${this.href}`);

            // For external links, we don't prevent default behavior
            // The link will open in a new tab as specified by target="_blank"
        });
    });

    // Add hover effects for copy buttons
    const copyButtons = document.querySelectorAll('button[onclick*="copyToClipboard"]');
    copyButtons.forEach(button => {
        button.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-2px)';
        });

        button.addEventListener('mouseleave', function () {
            this.style.transform = '';
        });
    });
});

// Function to check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Function to add animation class when elements are in view
function animateOnScroll() {
    const cards = document.querySelectorAll('.youtube-card');
    const header = document.querySelector('.section-header');
    const cta = document.querySelector('.youtube-cta');

    if (isInViewport(header)) {
        header.classList.add('animate');
    }

    cards.forEach(card => {
        if (isInViewport(card)) {
            card.classList.add('animate');
        }
    });

    if (isInViewport(cta)) {
        cta.classList.add('animate');
    }
}

// Initial check on page load
document.addEventListener('DOMContentLoaded', animateOnScroll);

// Check on scroll
window.addEventListener('scroll', animateOnScroll);

// Check on resize
window.addEventListener('resize', animateOnScroll);

