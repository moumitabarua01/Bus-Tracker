/**
 * Real-time Notifications System
 * Handles WebSocket connections, push notifications, and notification management
 */

class NotificationManager {
    constructor() {
        this.notificationContainer = null;
        this.unreadCountElement = null;
        this.notificationDropdown = null;
        this.pollInterval = null;
        
        this.init();
    }
    
    init() {
        // Initialize DOM elements
        this.notificationContainer = document.getElementById('notification-container');
        this.unreadCountElement = document.getElementById('unread-count');
        this.notificationDropdown = document.getElementById('notification-dropdown');
        
        // Initialize push notifications
        this.initializePushNotifications();
        
        // Load initial notifications
        this.loadNotifications();
        
        // Set up polling for new notifications
        this.startPolling();
        
        // Set up event listeners
        this.setupEventListeners();
    }
    
    startPolling() {
        // Poll for new notifications every 30 seconds
        this.pollInterval = setInterval(() => {
            this.updateUnreadCount();
        }, 30000);
    }
    
    stopPolling() {
        if (this.pollInterval) {
            clearInterval(this.pollInterval);
            this.pollInterval = null;
        }
    }
    
    displayNotification(notification) {
        // Create notification element
        const notificationElement = this.createNotificationElement(notification);
        
        // Add to container
        if (this.notificationContainer) {
            this.notificationContainer.insertBefore(notificationElement, this.notificationContainer.firstChild);
        }
        
        // Show browser notification if permission granted
        this.showBrowserNotification(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notificationElement.parentNode) {
                notificationElement.remove();
            }
        }, 5000);
    }
    
    createNotificationElement(notification) {
        const element = document.createElement('div');
        element.className = `notification-item ${notification.priority} ${notification.is_read ? 'read' : 'unread'}`;
        element.dataset.notificationId = notification.id;
        
        const priorityIcon = this.getPriorityIcon(notification.priority);
        const typeIcon = this.getTypeIcon(notification.notification_type);
        
        element.innerHTML = `
            <div class="notification-content">
                <div class="notification-header">
                    <span class="notification-icon">${typeIcon}</span>
                    <span class="notification-title">${notification.title}</span>
                    <span class="notification-priority">${priorityIcon}</span>
                    <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
                </div>
                <div class="notification-message">${notification.message}</div>
                <div class="notification-meta">
                    <span class="notification-time">${this.formatTime(notification.created_at)}</span>
                    ${notification.trip_id ? `<span class="notification-trip">Trip: ${notification.trip_id}</span>` : ''}
                </div>
            </div>
        `;
        
        // Add click handler to mark as read
        element.addEventListener('click', () => {
            this.markNotificationRead(notification.id);
            element.classList.remove('unread');
            element.classList.add('read');
        });
        
        return element;
    }
    
    getPriorityIcon(priority) {
        const icons = {
            'urgent': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢'
        };
        return icons[priority] || '🟡';
    }
    
    getTypeIcon(type) {
        const icons = {
            'booking_confirmed': '✅',
            'booking_cancelled': '❌',
            'bus_delay': '⏰',
            'bus_arrived': '🚌',
            'seat_available': '💺',
            'trip_update': '📢',
            'general': '📢'
        };
        return icons[type] || '📢';
    }
    
    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) { // Less than 1 minute
            return 'Just now';
        } else if (diff < 3600000) { // Less than 1 hour
            return `${Math.floor(diff / 60000)}m ago`;
        } else if (diff < 86400000) { // Less than 1 day
            return `${Math.floor(diff / 3600000)}h ago`;
        } else {
            return date.toLocaleDateString();
        }
    }
    
    showBrowserNotification(notification) {
        if (Notification.permission === 'granted') {
            const browserNotification = new Notification(notification.title, {
                body: notification.message,
                icon: '/static/bus/bus_icon.svg',
                badge: '/static/bus/bus_icon.svg',
                tag: `notification-${notification.id}`,
                data: {
                    notificationId: notification.id,
                    type: notification.notification_type
                }
            });
            
            browserNotification.onclick = () => {
                window.focus();
                browserNotification.close();
                this.markNotificationRead(notification.id);
            };
            
            // Auto-close after 5 seconds
            setTimeout(() => {
                browserNotification.close();
            }, 5000);
        }
    }
    
    async initializePushNotifications() {
        if ('Notification' in window) {
            if (Notification.permission === 'default') {
                const permission = await Notification.requestPermission();
                if (permission === 'granted') {
                    console.log('Push notifications enabled');
                    this.registerPushToken();
                }
            } else if (Notification.permission === 'granted') {
                this.registerPushToken();
            }
        }
    }
    
    async registerPushToken() {
        try {
            // In a real implementation, you would get the push token from the browser
            // For now, we'll use a simple identifier
            const token = `web_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            
            const response = await fetch('/notifications/push/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    token: token,
                    device_type: 'web'
                })
            });
            
            if (response.ok) {
                console.log('Push token registered');
            }
        } catch (error) {
            console.error('Failed to register push token:', error);
        }
    }
    
    async loadNotifications(page = 1) {
        try {
            const response = await fetch(`/notifications/?page=${page}`);
            const data = await response.json();
            
            if (data.notifications) {
                this.displayNotificationsList(data.notifications);
            }
        } catch (error) {
            console.error('Failed to load notifications:', error);
        }
    }
    
    displayNotificationsList(notifications) {
        if (this.notificationDropdown) {
            this.notificationDropdown.innerHTML = '';
            
            if (notifications.length === 0) {
                this.notificationDropdown.innerHTML = '<div class="no-notifications">No notifications</div>';
                return;
            }
            
            notifications.forEach(notification => {
                const element = this.createNotificationElement(notification);
                this.notificationDropdown.appendChild(element);
            });
        }
    }
    
    async markNotificationRead(notificationId) {
        try {
            const response = await fetch(`/notifications/${notificationId}/mark-read/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });
            
            if (response.ok) {
                this.updateUnreadCount();
            }
        } catch (error) {
            console.error('Failed to mark notification as read:', error);
        }
    }
    
    async markAllNotificationsRead() {
        try {
            const response = await fetch('/notifications/mark-all-read/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });
            
            if (response.ok) {
                this.updateUnreadCount();
                // Update all notification elements
                document.querySelectorAll('.notification-item').forEach(item => {
                    item.classList.remove('unread');
                    item.classList.add('read');
                });
            }
        } catch (error) {
            console.error('Failed to mark all notifications as read:', error);
        }
    }
    
    async updateUnreadCount() {
        try {
            const response = await fetch('/notifications/unread-count/');
            const data = await response.json();
            this.updateUnreadCountDisplay(data.unread_count);
        } catch (error) {
            console.error('Failed to get unread count:', error);
        }
    }
    
    updateUnreadCountDisplay(count) {
        if (this.unreadCountElement) {
            this.unreadCountElement.textContent = count;
            this.unreadCountElement.style.display = count > 0 ? 'block' : 'none';
        }
    }
    
    // Connection status removed for simplified version
    
    setupEventListeners() {
        // Mark all as read button
        const markAllReadBtn = document.getElementById('mark-all-read');
        if (markAllReadBtn) {
            markAllReadBtn.addEventListener('click', () => {
                this.markAllNotificationsRead();
            });
        }
        
        // Notification dropdown toggle
        const notificationToggle = document.getElementById('notification-toggle');
        if (notificationToggle) {
            notificationToggle.addEventListener('click', () => {
                this.toggleNotificationDropdown();
            });
        }
        
        // Close dropdown when clicking outside
        document.addEventListener('click', (event) => {
            if (this.notificationDropdown && 
                !this.notificationDropdown.contains(event.target) && 
                !notificationToggle.contains(event.target)) {
                this.notificationDropdown.style.display = 'none';
            }
        });
    }
    
    toggleNotificationDropdown() {
        if (this.notificationDropdown) {
            const isVisible = this.notificationDropdown.style.display === 'block';
            this.notificationDropdown.style.display = isVisible ? 'none' : 'block';
            
            if (!isVisible) {
                this.loadNotifications();
            }
        }
    }
    
    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }
    
    // Public methods for external use
    sendTestNotification() {
        // Test notification functionality
        this.loadNotifications();
    }
    
    disconnect() {
        this.stopPolling();
    }
}

// Initialize notification manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.notificationManager = new NotificationManager();
});

// Export for global access
window.NotificationManager = NotificationManager;
