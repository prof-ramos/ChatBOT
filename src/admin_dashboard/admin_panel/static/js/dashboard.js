// Dashboard JavaScript

// Get CSRF token for POST requests
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
           document.querySelector('meta[name="csrf-token"]')?.content ||
           '';
}

// Show message in bot control section
function showBotMessage(message, isSuccess) {
    const messageDiv = document.getElementById('bot-message');
    if (!messageDiv) return;

    messageDiv.className = isSuccess ? 'alert alert-success' : 'alert alert-error';
    messageDiv.textContent = message;
    messageDiv.style.display = 'block';

    // Hide after 5 seconds
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

// Update button states based on bot status
function updateButtonStates(isRunning) {
    const startBtn = document.getElementById('start-bot');
    const stopBtn = document.getElementById('stop-bot');
    const restartBtn = document.getElementById('restart-bot');

    if (startBtn) startBtn.disabled = isRunning;
    if (stopBtn) stopBtn.disabled = !isRunning;
    if (restartBtn) restartBtn.disabled = !isRunning;

    // Update status indicator
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-text');
    const statusValue = document.getElementById('status-value');

    if (statusDot) {
        statusDot.className = isRunning ? 'status-dot status-online' : 'status-dot status-offline';
    }
    if (statusText) {
        statusText.textContent = isRunning ? 'Online' : 'Offline';
    }
    if (statusValue) {
        statusValue.textContent = isRunning ? '🟢 Online' : '🔴 Offline';
    }
}

// Bot control functions
async function startBot() {
    const btn = document.getElementById('start-bot');
    btn.disabled = true;
    btn.textContent = 'Iniciando...';

    try {
        const response = await fetch('/api/bot/start', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
            },
        });

        const data = await response.json();
        showBotMessage(data.message, data.success);

        if (data.success) {
            updateButtonStates(true);
            // Reload page after 2 seconds to get fresh stats
            setTimeout(() => window.location.reload(), 2000);
        }
    } catch (error) {
        showBotMessage('Erro ao conectar com o servidor: ' + error.message, false);
    } finally {
        btn.textContent = 'Ligar Bot';
    }
}

async function stopBot() {
    const btn = document.getElementById('stop-bot');
    btn.disabled = true;
    btn.textContent = 'Parando...';

    try {
        const response = await fetch('/api/bot/stop', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
            },
        });

        const data = await response.json();
        showBotMessage(data.message, data.success);

        if (data.success) {
            updateButtonStates(false);
            // Reload page after 2 seconds
            setTimeout(() => window.location.reload(), 2000);
        }
    } catch (error) {
        showBotMessage('Erro ao conectar com o servidor: ' + error.message, false);
    } finally {
        btn.textContent = 'Desligar Bot';
    }
}

async function restartBot() {
    const btn = document.getElementById('restart-bot');
    btn.disabled = true;
    btn.textContent = 'Reiniciando...';

    try {
        const response = await fetch('/api/bot/restart', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
            },
        });

        const data = await response.json();
        showBotMessage(data.message, data.success);

        if (data.success) {
            // Reload page after 3 seconds
            setTimeout(() => window.location.reload(), 3000);
        }
    } catch (error) {
        showBotMessage('Erro ao conectar com o servidor: ' + error.message, false);
    } finally {
        btn.textContent = 'Reiniciar Bot';
        btn.disabled = false;
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Bot control buttons
    const startBtn = document.getElementById('start-bot');
    const stopBtn = document.getElementById('stop-bot');
    const restartBtn = document.getElementById('restart-bot');

    if (startBtn) {
        startBtn.addEventListener('click', startBot);
    }

    if (stopBtn) {
        stopBtn.addEventListener('click', stopBot);
    }

    if (restartBtn) {
        restartBtn.addEventListener('click', restartBot);
    }

    // Check bot status periodically (every 10 seconds)
    setInterval(async () => {
        try {
            const response = await fetch('/api/bot/status');
            const data = await response.json();
            updateButtonStates(data.is_running);
        } catch (error) {
            console.error('Error checking bot status:', error);
        }
    }, 10000);
});
