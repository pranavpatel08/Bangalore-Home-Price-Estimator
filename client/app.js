// Configuration
const API_BASE_URL = 'https://bangalore-home-price.onrender.com';

// DOM Elements
const form = document.getElementById('priceForm');
const locationInput = document.getElementById('location');
const autocompleteList = document.getElementById('autocomplete-list');
const resultBox = document.getElementById('result');
const priceSpan = document.getElementById('price');

// State
let allLocations = [];
let selectedLocation = '';

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    loadLocations();
    setupEventListeners();
});

// Load all locations
async function loadLocations() {
    try {
        const response = await fetch(`${API_BASE_URL}/get_location_names`);
        const data = await response.json();
        allLocations = data.locations;
    } catch (error) {
        console.error('Error loading locations:', error);
    }
}

// Setup event listeners
function setupEventListeners() {
    // Form submission
    form.addEventListener('submit', handleSubmit);
    
    // Location autocomplete
    locationInput.addEventListener('input', handleLocationInput);
    locationInput.addEventListener('focus', function(e) {
        if (e.target.value.trim().length > 0) {
            handleLocationInput(e);
        }
    });
    
    // Close autocomplete when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.autocomplete-wrapper')) {
            autocompleteList.classList.remove('active');
        }
    });
}

// Handle location input for autocomplete
async function handleLocationInput(e) {
    const query = e.target.value.trim();
    
    // Clear selected location when user types
    selectedLocation = '';
    
    if (query.length === 0) {
        autocompleteList.classList.remove('active');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/search_locations?query=${encodeURIComponent(query)}&limit=10`);
        const data = await response.json();
        displayAutocompleteResults(data.locations);
    } catch (error) {
        console.error('Error searching locations:', error);
    }
}

// Utility function to capitalize each word
function capitalizeWords(str) {
    return str.split(' ').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(' ');
}

// Display autocomplete results
function displayAutocompleteResults(locations) {
    if (locations.length === 0) {
        autocompleteList.innerHTML = '<div class="autocomplete-item">No matches found</div>';
        autocompleteList.classList.add('active');
        return;
    }
    
    autocompleteList.innerHTML = locations.map(location => 
        `<div class="autocomplete-item" data-location="${location}">${capitalizeWords(location)}</div>`
    ).join('');
    
    autocompleteList.classList.add('active');
    
    // Add click handlers to autocomplete items
    document.querySelectorAll('.autocomplete-item').forEach(item => {
        item.addEventListener('click', function() {
            const location = this.getAttribute('data-location');
            if (location && location !== 'No matches found') {
                locationInput.value = capitalizeWords(location);
                selectedLocation = location;
                autocompleteList.classList.remove('active');
            }
        });
    });
}

// Handle form submission
async function handleSubmit(e) {
    e.preventDefault();
    
    // Get form values
    const sqft = document.getElementById('sqft').value;
    const bhk = document.querySelector('input[name="bhk"]:checked').value;
    const bath = document.querySelector('input[name="bath"]:checked').value;
    const location = selectedLocation || locationInput.value; // Use selectedLocation if available
    
    // Validate
    if (!sqft || !location) {
        alert('Please fill in all fields');
        return;
    }
    
    // Show loading state
    const submitBtn = form.querySelector('.submit-btn');
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Calculating';
    
    try {
        // Create form data
        const formData = new FormData();
        formData.append('total_sqft', parseFloat(sqft));
        formData.append('bhk', parseInt(bhk));
        formData.append('bath', parseInt(bath));
        formData.append('location', location);
        
        // Make API call
        const response = await fetch(`${API_BASE_URL}/predict_home_price`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        // Display result
        displayResult(data.estimated_price);
        
    } catch (error) {
        console.error('Error predicting price:', error);
        alert('Error calculating price. Please try again.');
    } finally {
        // Reset button state
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Estimate Price';
    }
}

// Display the result
function displayResult(price) {
    priceSpan.textContent = price.toFixed(2);
    resultBox.style.display = 'block';
    resultBox.classList.add('show');
    
    // Smooth scroll to result
    resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Remove the show class after animation completes
    setTimeout(() => {
        resultBox.classList.remove('show');
    }, 2000);
}

// Utility function for keyboard navigation (optional enhancement)
locationInput.addEventListener('keydown', function(e) {
    const items = document.querySelectorAll('.autocomplete-item');
    const selected = document.querySelector('.autocomplete-item.selected');
    let index = Array.from(items).indexOf(selected);
    
    if (e.key === 'ArrowDown') {
        e.preventDefault();
        index = index < items.length - 1 ? index + 1 : 0;
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        index = index > 0 ? index - 1 : items.length - 1;
    } else if (e.key === 'Enter' && selected) {
        e.preventDefault();
        const location = selected.getAttribute('data-location');
        if (location && location !== 'No matches found') {
            locationInput.value = capitalizeWords(location);
            selectedLocation = location;
            autocompleteList.classList.remove('active');
        }
        return;
    } else {
        return;
    }
    
    // Update selection
    items.forEach(item => item.classList.remove('selected'));
    if (items[index]) {
        items[index].classList.add('selected');
    }
});