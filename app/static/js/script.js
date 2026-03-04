// Get elements (safely check if they exist)
const chatBody = document.getElementById("chatBody");
const userInput = document.getElementById("userInput");

// Check authentication on chat page
function checkChatAuth() {
    if (chatBody && !localStorage.getItem('accessToken')) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

// Send message when button clicked
function sendMessage() {
    if (!userInput || !chatBody) return;
    if (!localStorage.getItem('accessToken')) {
        addMessage("⚠ Please login to chat.", "bot-message");
        return;
    }
    
    const message = userInput.value.trim();

    if (message === "") return;

    // Add user message to UI
    addMessage(message, "user-message");

    // Clear input field
    userInput.value = "";
    userInput.focus();
    
    // Show loading indicator
    const loadingDiv = document.createElement("div");
    loadingDiv.className = "message bot-message loading";
    loadingDiv.innerHTML = '<span class="loading-spinner"></span> <span>Thinking...</span>';
    chatBody.appendChild(loadingDiv);
    chatBody.scrollTop = chatBody.scrollHeight;

    // Send to backend with auth token
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem('accessToken')}`
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => {
        if (response.status === 401) {
            localStorage.removeItem('accessToken');
            localStorage.removeItem('username');
            window.location.href = '/login';
            return null;
        }
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (!data) return;
        
        // Remove loading indicator
        if (loadingDiv.parentNode === chatBody) {
            loadingDiv.remove();
        }
        
        // Add bot reply with slight delay for better UX
        setTimeout(() => {
            addMessage(data.reply, "bot-message");
            
            // Display sentiment indicator
            if (data.sentiment) {
                const sentimentClass = data.sentiment === 'Positive' ? 'sentiment-positive' : 'sentiment-negative';
                const sentimentDiv = document.createElement("div");
                sentimentDiv.className = `message sentiment-display`;
                sentimentDiv.innerHTML = `<div class="sentiment-indicator ${sentimentClass}">📊 Detected Mood: ${data.sentiment}</div>`;
                chatBody.appendChild(sentimentDiv);
                chatBody.scrollTop = chatBody.scrollHeight;
            }
        }, 300);
    })
    .catch(error => {
        if (loadingDiv.parentNode === chatBody) {
            loadingDiv.remove();
        }
        addMessage("⚠ Error connecting to server. Please check your connection and try again.", "bot-message");
        console.error("Error:", error);
    });
}

// Add message to chat UI
function addMessage(text, className) {
    if (!chatBody) return;
    
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", className);
    
    const msgText = document.createElement("div");
    msgText.classList.add("msg-text");
    
    // Handle text with simple emoji support
    msgText.textContent = text;
    
    messageDiv.appendChild(msgText);
    chatBody.appendChild(messageDiv);

    // Auto-scroll to bottom
    setTimeout(() => {
        chatBody.scrollTop = chatBody.scrollHeight;
    }, 100);
}

// Send message when Enter key is pressed
if (userInput) {
    userInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
    
    // Set focus on input when page loads
    document.addEventListener("DOMContentLoaded", function() {
        userInput.focus();
    });
}

// Authentication handling
let isLogin = window.location.pathname === '/login';

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('authForm');
    
    // Skip if no form (e.g., on dashboard/home page)
    if (!form) {
        return;
    }
    
    const endpoint = isLogin ? '/login' : '/register';
    
    // Check if already logged in
    if (localStorage.getItem('accessToken')) {
        window.location.href = '/';
    }
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Validate form before submission
        if (!validateForm()) {
            return;
        }
        
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;
        const submitBtn = form.querySelector('.auth-btn');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Loading...';
        submitBtn.disabled = true;
        
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                showError(data.msg || 'Authentication failed');
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                return;
            }
            
            // Store token and username, then redirect
            localStorage.setItem('accessToken', data.access_token);
            localStorage.setItem('username', username);
            window.location.href = '/';
        } catch (error) {
            console.error('Error:', error);
            showError('Network error. Please try again.');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
});

function validateForm() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    
    if (!username || username.length < 3) {
        showError('Username must be at least 3 characters');
        return false;
    }
    
    if (!password || password.length < 6) {
        showError('Password must be at least 6 characters');
        return false;
    }
    
    return true;
}

function showError(message) {
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    const form = document.getElementById('authForm') || document.querySelector('form');
    if (form) {
        form.parentNode.insertBefore(errorDiv, form);
    } else {
        document.body.appendChild(errorDiv);
    }
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Logout function
function logout() {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('username');
        window.location.href = '/login';
    }
}
