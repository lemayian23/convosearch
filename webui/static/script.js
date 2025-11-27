// Filter state management - tracks current filter selections
let currentFilters = {
    category: 'all',
    date: 'all',
    startDate: null,
    endDate: null
};

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

async function initializeApp() {
    // Load available categories from the backend API
    await loadCategories();
    // Set up event listeners for filter interactions
    setupFilterListeners();
}

// Fetch available categories from the backend and populate the dropdown
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const data = await response.json();
        
        if (data.success) {
            const categorySelect = document.getElementById('categoryFilter');
            // Clear existing options except "All Categories"
            categorySelect.innerHTML = '<option value="all">All Categories</option>';
            // Add categories to the dropdown menu
            data.categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                categorySelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading categories:', error);
        // If categories fail to load, the filter will still work with "All Categories"
    }
}

// Set up event listeners for filter controls
function setupFilterListeners() {
    const categoryFilter = document.getElementById('categoryFilter');
    const dateFilter = document.getElementById('dateFilter');
    const customDateRange = document.getElementById('customDateRange');
    
    if (!categoryFilter || !dateFilter) {
        console.error('Filter elements not found');
        return;
    }
    
    // Category filter change handler
    categoryFilter.addEventListener('change', function() {
        currentFilters.category = this.value;
        // Apply filters immediately when they change
        applyFilters();
    });
    
    // Date filter change handler
    dateFilter.addEventListener('change', function() {
        currentFilters.date = this.value;
        
        // Show custom date range inputs only when custom is selected
        if (this.value === 'custom') {
            customDateRange.style.display = 'flex';
        } else {
            customDateRange.style.display = 'none';
            currentFilters.startDate = null;
            currentFilters.endDate = null;
            // Apply filters immediately for preset date ranges
            applyFilters();
        }
    });
    
    // Custom date range change handlers
    const startDate = document.getElementById('startDate');
    const endDate = document.getElementById('endDate');
    if (startDate) startDate.addEventListener('change', updateCustomDate);
    if (endDate) endDate.addEventListener('change', updateCustomDate);
}

// Handle custom date range selection
function updateCustomDate() {
    const startDate = document.getElementById('startDate');
    const endDate = document.getElementById('endDate');
    
    if (startDate && endDate) {
        currentFilters.startDate = startDate.value;
        currentFilters.endDate = endDate.value;
        
        // Only apply filters when both dates are selected
        if (startDate.value && endDate.value) {
            applyFilters();
        }
    }
}

// Apply current filters to any active search
function applyFilters() {
    // If there's a current question, re-run the search with filters
    const currentQuestion = document.getElementById('questionInput').value;
    if (currentQuestion && currentQuestion.trim()) {
        askQuestion();
    }
    
    // Update UI to show active filter state
    updateFilterUI();
}

// Update visual indication of active filters
function updateFilterUI() {
    const hasActiveFilters = currentFilters.category !== 'all' || 
                            currentFilters.date !== 'all' ||
                            currentFilters.startDate !== null;
    
    const filterContainer = document.querySelector('.search-filters');
    if (filterContainer) {
        if (hasActiveFilters) {
            filterContainer.classList.add('filter-active');
        } else {
            filterContainer.classList.remove('filter-active');
        }
    }
}

// Main function to ask questions with filter support - MODIFIED VERSION
async function askQuestion() {
    const input = document.getElementById('questionInput');
    const question = input.value.trim();
    if (!question) return;
    
    const chatBox = document.getElementById('chatBox');
    
    // Add user message to chat
    chatBox.innerHTML += `<div class="message user"><strong>You:</strong> ${question}</div>`;
    input.value = '';
    
    // Show loading state
    showLoading(true);
    
    try {
        // Prepare request data with current filters
        const requestData = {
            question: question,
            category_filter: currentFilters.category,
            date_filter: currentFilters.date
        };
        
        // Add custom date range if selected
        if (currentFilters.date === 'custom' && currentFilters.startDate && currentFilters.endDate) {
            requestData.start_date = currentFilters.startDate;
            requestData.end_date = currentFilters.endDate;
        }
        
        // Call the search API with filters - using /api/query endpoint for chat
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });
        
        const data = await response.json();
        
        // Add bot response with sources and confidence
        let sourcesHtml = '';
        if (data.sources && data.sources.length > 0) {
            sourcesHtml = `<div class="sources"><strong>Sources:</strong> ${data.sources.join(', ')}</div>`;
        }
        
        // Create results info showing count and active filters
        const resultsInfo = createResultsInfo(data);
        
        chatBox.innerHTML += `
            <div class="message bot">
                <strong>ConvoSearch:</strong> ${data.answer}
                ${sourcesHtml}
                <div class="sources"><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(1)}%</div>
                ${resultsInfo}
            </div>
        `;
        
    } catch (error) {
        console.error('Search error:', error);
        chatBox.innerHTML += `<div class="message bot"><strong>Error:</strong> Failed to get response</div>`;
    }
    
    // Scroll to bottom to show latest message
    chatBox.scrollTop = chatBox.scrollHeight;
    showLoading(false);
}

// Show loading state during API calls
function showLoading(show) {
    // You could add a loading spinner here if needed
    const chatBox = document.getElementById('chatBox');
    if (show) {
        // Add loading message
        chatBox.innerHTML += `<div class="message bot"><strong>ConvoSearch:</strong> Searching...</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

// Create results information display showing count and active filters
function createResultsInfo(data) {
    const hasActiveFilters = currentFilters.category !== 'all' || currentFilters.date !== 'all';
    
    // Only show filter info if filters are active
    if (!hasActiveFilters) return '';
    
    let infoHTML = `<div class="results-info">`;
    
    // Show active filters
    let filterText = [];
    if (currentFilters.category !== 'all') {
        filterText.push(`Category: ${currentFilters.category}`);
    }
    if (currentFilters.date !== 'all') {
        filterText.push(`Date: ${currentFilters.date}`);
    }
    
    infoHTML += `<span class="results-count">Filtered results</span>`;
    infoHTML += `<span class="filter-indicator">(${filterText.join(', ')})</span>`;
    infoHTML += `<button onclick="clearAllFilters()" class="clear-filters-btn">Clear Filters</button>`;
    infoHTML += `</div>`;
    
    return infoHTML;
}

// Clear all filters and reset to default state
function clearAllFilters() {
    const categoryFilter = document.getElementById('categoryFilter');
    const dateFilter = document.getElementById('dateFilter');
    const customDateRange = document.getElementById('customDateRange');
    const startDate = document.getElementById('startDate');
    const endDate = document.getElementById('endDate');
    
    if (categoryFilter) categoryFilter.value = 'all';
    if (dateFilter) dateFilter.value = 'all';
    if (customDateRange) customDateRange.style.display = 'none';
    if (startDate) startDate.value = '';
    if (endDate) endDate.value = '';
    
    // Reset filter state
    currentFilters = {
        category: 'all',
        date: 'all',
        startDate: null,
        endDate: null
    };
    
    // Re-run search if there's a current question
    const currentQuestion = document.getElementById('questionInput').value;
    if (currentQuestion && currentQuestion.trim()) {
        askQuestion();
    }
    
    updateFilterUI();
}

// Display error message (helper function)
function displayError(message) {
    const chatBox = document.getElementById('chatBox');
    if (chatBox) {
        chatBox.innerHTML += `<div class="message bot"><strong>Error:</strong> ${message}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

// Allow Enter key to submit questions for better UX
document.addEventListener('DOMContentLoaded', function() {
    const questionInput = document.getElementById('questionInput');
    if (questionInput) {
        questionInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                askQuestion();
            }
        });
    }
});