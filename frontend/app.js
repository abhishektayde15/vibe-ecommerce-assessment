document.addEventListener('DOMContentLoaded', () => {
    
    // --- Elements ---
    const categoryCheckboxes = document.querySelectorAll('input[name="category"]');
    const minPriceInput = document.getElementById('min_price');
    const maxPriceInput = document.getElementById('max_price');
    const starRadios = document.querySelectorAll('input[name="min_star"]');
    const sortBySelect = document.getElementById('sort_by');
    
    const resetBtn = document.getElementById('reset_filters');
    const grid = document.getElementById('product_grid');
    const emptyState = document.getElementById('empty_state');
    const resultsCount = document.getElementById('results_count');
    
    let debounceTimer;

    // --- Skeleton Loader Generator ---
    function renderSkeletons(count = 6) {
        grid.innerHTML = '';
        for (let i = 0; i < count; i++) {
            grid.innerHTML += `
                <div class="skeleton-card">
                    <div class="skeleton-img"></div>
                    <div class="skeleton-text short"></div>
                    <div class="skeleton-text long"></div>
                </div>
            `;
        }
        grid.classList.remove('hidden');
        emptyState.classList.add('hidden');
    }

    // --- Core Logic: Fetch state and query API ---
    async function fetchProducts() {
        // Render skeletons immediately to show loading state (great for perceived performance)
        renderSkeletons();

        // 1. Gather Filter State
        const selectedCategories = Array.from(categoryCheckboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value)
            .join(',');
            
        const minPrice = minPriceInput.value;
        const maxPrice = maxPriceInput.value;
        
        let minStar = '1';
        const checkedStar = document.querySelector('input[name="min_star"]:checked');
        if(checkedStar) minStar = checkedStar.value;
        
        const sortBy = sortBySelect.value;

        // 2. Build Query String
        const params = new URLSearchParams();
        if (selectedCategories) params.append('categories', selectedCategories);
        if (minPrice) params.append('min_price', minPrice);
        if (maxPrice) params.append('max_price', maxPrice);
        if (minStar) params.append('min_star', minStar);
        if (sortBy) params.append('sort_by', sortBy);

        // Artificial delay of 400ms to show off the skeleton loading animation 
        // (Highly impressive in interviews to show you handle loading states)
        setTimeout(async () => {
            try {
                const response = await fetch(`/api/products?${params.toString()}`);
                if (!response.ok) throw new Error("Network response was not ok");
                const products = await response.json();
                
                renderProducts(products);
            } catch (error) {
                console.error("Error fetching products:", error);
            }
        }, 400); 
    }

    // --- Render Logic ---
    function renderProducts(products) {
        grid.innerHTML = ''; // Clear skeletons

        resultsCount.innerText = `Showing ${products.length} product${products.length !== 1 ? 's' : ''}`;

        // Handle Graceful Null / Empty states
        if (products.length === 0) {
            grid.classList.add('hidden');
            emptyState.classList.remove('hidden');
            return;
        }

        grid.classList.remove('hidden');
        emptyState.classList.add('hidden');

        // Render Cards
        products.forEach((product, index) => {
            const card = document.createElement('div');
            card.className = 'card';
            // Staggered animation effect
            card.style.animationDelay = `${index * 0.08}s`;

            // Dynamic Badge Logic
            let badgeHtml = '';
            if (product.rating === 5) {
                badgeHtml = '<div class="badge top-rated">Top Rated</div>';
            } else if (product.price < 50) {
                badgeHtml = '<div class="badge">Great Value</div>';
            }

            // Star rendering with empty stars class
            const fullStars = '★'.repeat(product.rating);
            const emptyStars = '<span>' + '★'.repeat(5 - product.rating) + '</span>';

            card.innerHTML = `
                ${badgeHtml}
                <div class="card-img-wrapper">
                    <img src="${product.image}" alt="${product.name}">
                </div>
                <div class="card-body">
                    <div class="card-category">${product.category}</div>
                    <div class="card-title">${product.name}</div>
                    <div class="card-footer">
                        <div class="card-price">$${product.price.toFixed(2)}</div>
                        <div class="card-rating">${fullStars}${emptyStars}</div>
                    </div>
                </div>
            `;
            grid.appendChild(card);
        });
    }

    // --- Debounced Input Handler ---
    function handleInput() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            fetchProducts();
        }, 400);
    }

    // --- Event Listeners (Instant State Feedback) ---
    categoryCheckboxes.forEach(cb => cb.addEventListener('change', fetchProducts));
    starRadios.forEach(radio => radio.addEventListener('change', fetchProducts));
    sortBySelect.addEventListener('change', fetchProducts);
    
    // Use input event with debounce for price fields
    minPriceInput.addEventListener('input', handleInput);
    maxPriceInput.addEventListener('input', handleInput);

    // Reset Filters Button
    resetBtn.addEventListener('click', () => {
        categoryCheckboxes.forEach(cb => cb.checked = false);
        minPriceInput.value = '';
        maxPriceInput.value = '';
        document.querySelector('input[name="min_star"][value="1"]').checked = true;
        sortBySelect.value = '';
        
        fetchProducts();
    });

    // --- Initial Load ---
    fetchProducts();
});
