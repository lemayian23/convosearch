// Filter state management
let currentFilters = {
    category: 'all',
    date: 'all',
    startDate: null,
    endDate: null
};

// Initialize filters
document.addEventListener('DOMContentLoaded', function() {
    loadCategories();
    setupFilterListeners();
});

// Load categories from backend
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const data = await response.json();
        
        if (data.success) {
            const categorySelect = document.getElementById('categoryFilter');
            data.categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                categorySelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Setup filter event listeners
function setupFilterListeners() {
    const categoryFilter = document.getElementById('categoryFilter');
    const dateFilter = document.getElementById('dateFilter');
    const customDateRange = document.getElementById('customDateRange');
    
    categoryFilter.addEventListener('change', function() {
        currentFilters.category = this.value;
        applyFilters();
    });
    
    dateFilter.addEventListener('change', function() {
        currentFilters.date = this.value;
        
        // Show/hide custom date range
        if (this.value === 'custom') {
            customDateRange.style.display = 'flex';
        } else {
            customDateRange.style.display = 'none';
            currentFilters.startDate = null;
            currentFilters.endDate = null;
            applyFilters();
        }
    });
    
    // Custom date range listeners
    document.getElementById('startDate').addEventListener('change', updateCustomDate);
    document.getElementById('endDate').addEventListener('change', updateCustomDate);
}

function updateCustomDate() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    
    if (startDate && endDate) {
        currentFilters.startDate = startDate;
        currentFilters.endDate = endDate;
        applyFilters();
    }
}

// Apply filters to current search or perform new search
function applyFilters() {
    // If there's a current search query, re-search with filters
    const currentQuery = document.getElementById('searchInput').value;
    if (currentQuery.trim()) {
        performSearch(currentQuery);
    }
    
    // Update UI to show active filters
    updateFilterUI();
}

// Update UI to reflect active filters
function updateFilterUI() {
    const hasActiveFilters = currentFilters.category !== 'all' || 
                            currentFilters.date !== 'all' ||
                            currentFilters.startDate !== null;
    
    const filterContainer = document.querySelector('.search-filters');
    if (hasActiveFilters) {
        filterContainer.classList.add('filter-active');
    } else {
        filterContainer.classList.remove('filter-active');
    }
}

// Modify your existing search function to include filters
async function performSearch(query) {
    try {
        showLoading(true);
        
        const searchData = {
            query: query,
            category_filter: currentFilters.category,
            date_filter: currentFilters.date
        };
        
        // Add custom date range if applicable
        if (currentFilters.date === 'custom' && currentFilters.startDate && currentFilters.endDate) {
            searchData.start_date = currentFilters.startDate;
            searchData.end_date = currentFilters.endDate;
        }
        
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(searchData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.results, data.filters);
        } else {
            displayError(data.error || 'Search failed');
        }
        
    } catch (error) {
        console.error('Search error:', error);
        displayError('Network error occurred');
    } finally {
        showLoading(false);
    }
}

// Update the displayResults function
function displayResults(results, filters) {
    const resultsContainer = document.getElementById('resultsContainer');
    
    // Create results info header
    const resultsInfo = createResultsInfo(results, filters);
    
    resultsContainer.innerHTML = resultsInfo + formatResults(results);
}

// Create results information header
function createResultsInfo(results, filters) {
    const resultsCount = results.length;
    const hasActiveFilters = filters.category !== 'all' || filters.date !== 'all';
    
    let infoHTML = `<div class="results-info">
        <span class="results-count">${resultsCount} result${resultsCount !== 1 ? 's' : ''} found</span>`;
    
    // Show active filters if any
    if (hasActiveFilters) {
        let filterText = [];
        if (filters.category !== 'all') {
            filterText.push(`Category: ${filters.category}`);
        }
        if (filters.date !== 'all') {
            filterText.push(`Date: ${filters.date}`);
        }
        
        infoHTML += `<span class="filter-indicator">(Filtered by: ${filterText.join(', ')})</span>`;
        infoHTML += `<button onclick="clearFilters()" class="clear-filters-btn">Clear Filters</button>`;
    }
    
    infoHTML += `</div>`;
    return infoHTML;
}

// Keep your existing clearFilters function
function clearFilters() {
    document.getElementById('categoryFilter').value = 'all';
    document.getElementById('dateFilter').value = 'all';
    document.getElementById('customDateRange').style.display = 'none';
    document.getElementById('startDate').value = '';
    document.getElementById('endDate').value = '';
    
    currentFilters = {
        category: 'all',
        date: 'all',
        startDate: null,
        endDate: null
    };
    
    // Re-run search if there's a current query
    const currentQuery = document.getElementById('searchInput').value;
    if (currentQuery.trim()) {
        performSearch(currentQuery);
    }
    
    updateFilterUI();
}
function createFilterSummary(filters) {
    let summary = '';
    
    if (filters.category !== 'all' || filters.date !== 'all') {
        summary = `<div class="filter-summary">
            <strong>Active Filters:</strong> 
            ${filters.category !== 'all' ? `Category: ${filters.category}` : ''}
            ${filters.date !== 'all' ? `Date: ${filters.date}` : ''}
            <button onclick="clearFilters()" class="clear-filters-btn">Clear All</button>
        </div>`;
    }
    
    return summary;
}

// Clear all filters
function clearFilters() {
    document.getElementById('categoryFilter').value = 'all';
    document.getElementById('dateFilter').value = 'all';
    document.getElementById('customDateRange').style.display = 'none';
    document.getElementById('startDate').value = '';
    document.getElementById('endDate').value = '';
    
    currentFilters = {
        category: 'all',
        date: 'all',
        startDate: null,
        endDate: null
    };
    
    applyFilters();
    updateFilterUI();
}