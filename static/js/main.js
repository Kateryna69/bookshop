// AJAX Add to Cart
document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('.add-to-cart-form').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const url = form.action;
            const data = new FormData(form);

            fetch(url, {
                method: 'POST',
                headers: {'X-Requested-With': 'XMLHttpRequest'},
                body: data
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    // Оновлення лічильника
                    const badge = document.getElementById('cart-count');
                    if (badge) {
                        badge.textContent = data.cart_count;
                        badge.classList.remove('d-none');
                    }
                    showToast(data.message, 'success');
                }
            })
            .catch(() => form.submit());
        });
    });


    function showToast(message, type) {
        const existing = document.getElementById('ajax-toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.id = 'ajax-toast';
        toast.innerHTML = 
            <div style="
                position:fixed; bottom:24px; right:24px;
                background:${type === 'success' ? '#28a745' : '#dc3545'};
                color:#fff; padding:12px 20px; border-radius:10px;
                box-shadow:0 4px 16px rgba(0,0,0,0.2);
                z-index:9999; font-size:0.9rem; font-weight:500;
                animation: slideIn .3s ease;
                max-width:300px;
            ">
                ✅ ${message}
            </div>
        ;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    const cartBadge = document.getElementById('cart-count');
    if (cartBadge && parseInt(cartBadge.textContent) > 0) {
        cartBadge.style.animation = 'pulse 1s ease';
    }
});