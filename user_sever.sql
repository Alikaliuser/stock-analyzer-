-- ProTrader User Server Management Database
-- Advanced user management, roles, permissions, and server monitoring

-- =====================================================
-- USER ROLES AND PERMISSIONS SYSTEM
-- =====================================================

-- User roles table
CREATE TABLE IF NOT EXISTS user_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Permissions table
CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    permission_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    module VARCHAR(50) NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Role permissions mapping
CREATE TABLE IF NOT EXISTS role_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    granted_by INTEGER,
    FOREIGN KEY (role_id) REFERENCES user_roles (id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions (id) ON DELETE CASCADE,
    FOREIGN KEY (granted_by) REFERENCES users (id),
    UNIQUE(role_id, permission_id)
);

-- User role assignments
CREATE TABLE IF NOT EXISTS user_role_assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_by INTEGER,
    expires_at TIMESTAMP,
    is_active INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES user_roles (id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users (id),
    UNIQUE(user_id, role_id)
);

-- =====================================================
-- SERVER LOGS AND MONITORING
-- =====================================================

-- Server access logs
CREATE TABLE IF NOT EXISTS server_access_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    session_token VARCHAR(255),
    ip_address VARCHAR(45),
    user_agent TEXT,
    request_method VARCHAR(10),
    request_url TEXT,
    request_params TEXT,
    response_status INTEGER,
    response_time_ms INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
);

-- Server error logs
CREATE TABLE IF NOT EXISTS server_error_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    session_token VARCHAR(255),
    ip_address VARCHAR(45),
    error_type VARCHAR(100),
    error_message TEXT,
    stack_trace TEXT,
    request_data TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved INTEGER DEFAULT 0,
    resolved_by INTEGER,
    resolved_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL,
    FOREIGN KEY (resolved_by) REFERENCES users (id)
);

-- Server performance logs
CREATE TABLE IF NOT EXISTS server_performance_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint VARCHAR(100),
    method VARCHAR(10),
    avg_response_time_ms REAL,
    min_response_time_ms INTEGER,
    max_response_time_ms INTEGER,
    request_count INTEGER,
    error_count INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- USER ACTIVITY TRACKING
-- =====================================================

-- User login history
CREATE TABLE IF NOT EXISTS user_login_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    login_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_timestamp TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    session_duration_seconds INTEGER,
    login_successful INTEGER DEFAULT 1,
    failure_reason TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- User activity logs
CREATE TABLE IF NOT EXISTS user_activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    activity_description TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT, -- JSON data for additional info
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- User security events
CREATE TABLE IF NOT EXISTS user_security_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_type VARCHAR(50) NOT NULL,
    event_description TEXT,
    ip_address VARCHAR(45),
    severity ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved INTEGER DEFAULT 0,
    resolved_by INTEGER,
    resolved_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL,
    FOREIGN KEY (resolved_by) REFERENCES users (id)
);

-- =====================================================
-- USER MANAGEMENT AND ADMINISTRATION
-- =====================================================

-- User account status history
CREATE TABLE IF NOT EXISTS user_account_status_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    old_status VARCHAR(20),
    new_status VARCHAR(20),
    reason TEXT,
    changed_by INTEGER,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users (id)
);

-- User profile changes
CREATE TABLE IF NOT EXISTS user_profile_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    field_name VARCHAR(50) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users (id)
);

-- User verification and KYC
CREATE TABLE IF NOT EXISTS user_verification (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    email_verified INTEGER DEFAULT 0,
    phone_verified INTEGER DEFAULT 0,
    identity_verified INTEGER DEFAULT 0,
    kyc_status ENUM('pending', 'approved', 'rejected', 'not_required') DEFAULT 'not_required',
    kyc_documents TEXT, -- JSON array of document info
    verification_date TIMESTAMP,
    verified_by INTEGER,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (verified_by) REFERENCES users (id)
);

-- =====================================================
-- SYSTEM CONFIGURATION AND SETTINGS
-- =====================================================

-- System configuration
CREATE TABLE IF NOT EXISTS system_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    config_type VARCHAR(20) DEFAULT 'string',
    description TEXT,
    is_public INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INTEGER,
    FOREIGN KEY (updated_by) REFERENCES users (id)
);

-- Feature flags
CREATE TABLE IF NOT EXISTS feature_flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    feature_name VARCHAR(100) UNIQUE NOT NULL,
    is_enabled INTEGER DEFAULT 0,
    enabled_for_all INTEGER DEFAULT 0,
    enabled_for_roles TEXT, -- JSON array of role IDs
    enabled_for_users TEXT, -- JSON array of user IDs
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INTEGER,
    FOREIGN KEY (updated_by) REFERENCES users (id)
);

-- =====================================================
-- NOTIFICATIONS AND MESSAGING
-- =====================================================

-- System notifications
CREATE TABLE IF NOT EXISTS system_notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    notification_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    priority ENUM('low', 'normal', 'high', 'urgent') DEFAULT 'normal',
    is_read INTEGER DEFAULT 0,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    action_url TEXT,
    metadata TEXT, -- JSON data
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Email templates
CREATE TABLE IF NOT EXISTS email_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_name VARCHAR(100) UNIQUE NOT NULL,
    subject VARCHAR(200) NOT NULL,
    body_html TEXT NOT NULL,
    body_text TEXT,
    variables TEXT, -- JSON array of variable names
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Email logs
CREATE TABLE IF NOT EXISTS email_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    template_name VARCHAR(100),
    recipient_email VARCHAR(255) NOT NULL,
    subject VARCHAR(200),
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('sent', 'delivered', 'failed', 'bounced') DEFAULT 'sent',
    error_message TEXT,
    metadata TEXT, -- JSON data
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
);

-- =====================================================
-- BACKUP AND MAINTENANCE
-- =====================================================

-- Database backup logs
CREATE TABLE IF NOT EXISTS backup_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    backup_type VARCHAR(50) NOT NULL,
    backup_path TEXT,
    backup_size_bytes INTEGER,
    backup_duration_seconds INTEGER,
    status ENUM('success', 'failed', 'in_progress') DEFAULT 'in_progress',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    initiated_by INTEGER,
    FOREIGN KEY (initiated_by) REFERENCES users (id)
);

-- System maintenance logs
CREATE TABLE IF NOT EXISTS maintenance_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maintenance_type VARCHAR(50) NOT NULL,
    description TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    status ENUM('scheduled', 'in_progress', 'completed', 'failed') DEFAULT 'scheduled',
    affected_tables TEXT, -- JSON array
    duration_seconds INTEGER,
    initiated_by INTEGER,
    notes TEXT,
    FOREIGN KEY (initiated_by) REFERENCES users (id)
);

-- =====================================================
-- SAMPLE DATA INSERTION
-- =====================================================

-- Insert default roles
INSERT OR IGNORE INTO user_roles (role_name, description) VALUES
('admin', 'System Administrator with full access'),
('moderator', 'Moderator with limited administrative access'),
('premium_user', 'Premium user with advanced features'),
('standard_user', 'Standard user with basic features'),
('demo_user', 'Demo user with limited access');

-- Insert default permissions
INSERT OR IGNORE INTO permissions (permission_name, description, module) VALUES
-- User management permissions
('user.create', 'Create new users', 'user_management'),
('user.read', 'View user information', 'user_management'),
('user.update', 'Update user information', 'user_management'),
('user.delete', 'Delete users', 'user_management'),
('user.activate', 'Activate/deactivate users', 'user_management'),

-- Trading permissions
('trade.execute', 'Execute trades', 'trading'),
('trade.view', 'View trading history', 'trading'),
('trade.cancel', 'Cancel pending trades', 'trading'),
('trade.advanced', 'Access advanced trading features', 'trading'),

-- Portfolio permissions
('portfolio.view', 'View portfolio', 'portfolio'),
('portfolio.export', 'Export portfolio data', 'portfolio'),
('portfolio.advanced', 'Access advanced portfolio features', 'portfolio'),

-- System permissions
('system.config', 'Modify system configuration', 'system'),
('system.logs', 'View system logs', 'system'),
('system.backup', 'Perform system backups', 'system'),
('system.maintenance', 'Perform system maintenance', 'system');

-- Assign permissions to roles
INSERT OR IGNORE INTO role_permissions (role_id, permission_id) 
SELECT r.id, p.id FROM user_roles r, permissions p 
WHERE r.role_name = 'admin';

INSERT OR IGNORE INTO role_permissions (role_id, permission_id) 
SELECT r.id, p.id FROM user_roles r, permissions p 
WHERE r.role_name = 'moderator' AND p.permission_name IN (
    'user.read', 'user.update', 'trade.view', 'portfolio.view', 'system.logs'
);

INSERT OR IGNORE INTO role_permissions (role_id, permission_id) 
SELECT r.id, p.id FROM user_roles r, permissions p 
WHERE r.role_name = 'premium_user' AND p.permission_name IN (
    'trade.execute', 'trade.view', 'trade.advanced', 'portfolio.view', 'portfolio.export', 'portfolio.advanced'
);

INSERT OR IGNORE INTO role_permissions (role_id, permission_id) 
SELECT r.id, p.id FROM user_roles r, permissions p 
WHERE r.role_name = 'standard_user' AND p.permission_name IN (
    'trade.execute', 'trade.view', 'portfolio.view'
);

INSERT OR IGNORE INTO role_permissions (role_id, permission_id) 
SELECT r.id, p.id FROM user_roles r, permissions p 
WHERE r.role_name = 'demo_user' AND p.permission_name IN (
    'trade.view', 'portfolio.view'
);

-- Assign roles to existing users
INSERT OR IGNORE INTO user_role_assignments (user_id, role_id) 
SELECT u.id, r.id FROM users u, user_roles r 
WHERE u.username = 'demo' AND r.role_name = 'demo_user';

-- Insert system configuration
INSERT OR IGNORE INTO system_config (config_key, config_value, config_type, description) VALUES
('max_login_attempts', '5', 'integer', 'Maximum failed login attempts before lockout'),
('session_timeout_minutes', '1440', 'integer', 'Session timeout in minutes (24 hours)'),
('password_min_length', '8', 'integer', 'Minimum password length'),
('require_email_verification', 'true', 'boolean', 'Require email verification for new accounts'),
('maintenance_mode', 'false', 'boolean', 'Enable maintenance mode'),
('max_portfolio_size', '1000000', 'integer', 'Maximum portfolio value in USD'),
('trading_commission', '9.99', 'decimal', 'Default trading commission'),
('support_email', 'support@protrader.com', 'string', 'Support email address');

-- Insert email templates
INSERT OR IGNORE INTO email_templates (template_name, subject, body_html, variables) VALUES
('welcome_email', 'Welcome to ProTrader!', 
'<h1>Welcome to ProTrader!</h1><p>Hello {{first_name}},</p><p>Welcome to ProTrader! Your account has been successfully created.</p>',
'["first_name", "username"]'),
('password_reset', 'Reset Your ProTrader Password',
'<h1>Password Reset Request</h1><p>Hello {{first_name}},</p><p>Click the link below to reset your password: {{reset_link}}</p>',
'["first_name", "reset_link"]'),
('trade_confirmation', 'Trade Confirmation - {{symbol}}',
'<h1>Trade Confirmation</h1><p>Your {{trade_type}} order for {{symbol}} has been executed.</p>',
'["symbol", "trade_type", "shares", "price", "total_amount"]');

-- Insert feature flags
INSERT OR IGNORE INTO feature_flags (feature_name, is_enabled, enabled_for_all, description) VALUES
('advanced_charts', 1, 1, 'Enable advanced charting features'),
('real_time_data', 1, 1, 'Enable real-time stock data'),
('social_trading', 0, 0, 'Enable social trading features'),
('ai_predictions', 0, 0, 'Enable AI-powered stock predictions'),
('mobile_app', 1, 1, 'Enable mobile app features');

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- User roles and permissions indexes
CREATE INDEX IF NOT EXISTS idx_role_permissions_role_id ON role_permissions(role_id);
CREATE INDEX IF NOT EXISTS idx_role_permissions_permission_id ON role_permissions(permission_id);
CREATE INDEX IF NOT EXISTS idx_user_role_assignments_user_id ON user_role_assignments(user_id);
CREATE INDEX IF NOT EXISTS idx_user_role_assignments_role_id ON user_role_assignments(role_id);

-- Server logs indexes
CREATE INDEX IF NOT EXISTS idx_access_logs_user_id ON server_access_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_access_logs_timestamp ON server_access_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_access_logs_ip_address ON server_access_logs(ip_address);
CREATE INDEX IF NOT EXISTS idx_error_logs_timestamp ON server_error_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_error_logs_resolved ON server_error_logs(resolved);

-- User activity indexes
CREATE INDEX IF NOT EXISTS idx_login_history_user_id ON user_login_history(user_id);
CREATE INDEX IF NOT EXISTS idx_login_history_timestamp ON user_login_history(login_timestamp);
CREATE INDEX IF NOT EXISTS idx_activity_logs_user_id ON user_activity_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_logs_timestamp ON user_activity_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_security_events_user_id ON user_security_events(user_id);
CREATE INDEX IF NOT EXISTS idx_security_events_severity ON user_security_events(severity);

-- Notifications indexes
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON system_notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_read ON system_notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_notifications_priority ON system_notifications(priority);
CREATE INDEX IF NOT EXISTS idx_email_logs_user_id ON email_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_email_logs_status ON email_logs(status);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- User permissions view
CREATE VIEW IF NOT EXISTS user_permissions AS
SELECT 
    u.id as user_id,
    u.username,
    u.first_name,
    u.last_name,
    r.role_name,
    p.permission_name,
    p.module
FROM users u
JOIN user_role_assignments ura ON u.id = ura.user_id
JOIN user_roles r ON ura.role_id = r.id
JOIN role_permissions rp ON r.id = rp.role_id
JOIN permissions p ON rp.permission_id = p.id
WHERE ura.is_active = 1 AND r.is_active = 1 AND p.is_active = 1;

-- User activity summary view
CREATE VIEW IF NOT EXISTS user_activity_summary AS
SELECT 
    u.id as user_id,
    u.username,
    u.first_name,
    u.last_name,
    COUNT(ual.id) as total_activities,
    COUNT(ulh.id) as total_logins,
    MAX(ulh.login_timestamp) as last_login,
    COUNT(use.id) as security_events,
    u.created_at as account_created
FROM users u
LEFT JOIN user_activity_logs ual ON u.id = ual.user_id
LEFT JOIN user_login_history ulh ON u.id = ulh.user_id
LEFT JOIN user_security_events use ON u.id = use.user_id
GROUP BY u.id, u.username, u.first_name, u.last_name;

-- Server performance summary view
CREATE VIEW IF NOT EXISTS server_performance_summary AS
SELECT 
    endpoint,
    method,
    AVG(avg_response_time_ms) as avg_response_time,
    SUM(request_count) as total_requests,
    SUM(error_count) as total_errors,
    (SUM(error_count) * 100.0 / SUM(request_count)) as error_rate_percent,
    MAX(timestamp) as last_activity
FROM server_performance_logs
GROUP BY endpoint, method;

-- =====================================================
-- TRIGGERS FOR AUTOMATIC UPDATES
-- =====================================================

-- Trigger to update user account status history
CREATE TRIGGER IF NOT EXISTS update_user_status_history
AFTER UPDATE OF is_active ON users
BEGIN
    INSERT INTO user_account_status_history (user_id, old_status, new_status, reason)
    VALUES (NEW.id, 
            CASE WHEN OLD.is_active = 1 THEN 'active' ELSE 'inactive' END,
            CASE WHEN NEW.is_active = 1 THEN 'active' ELSE 'inactive' END,
            'System update');
END;

-- Trigger to log user profile changes
CREATE TRIGGER IF NOT EXISTS log_profile_changes
AFTER UPDATE ON users
BEGIN
    -- Log username changes
    IF OLD.username != NEW.username THEN
        INSERT INTO user_profile_changes (user_id, field_name, old_value, new_value)
        VALUES (NEW.id, 'username', OLD.username, NEW.username);
    END IF;
    
    -- Log email changes
    IF OLD.email != NEW.email THEN
        INSERT INTO user_profile_changes (user_id, field_name, old_value, new_value)
        VALUES (NEW.id, 'email', OLD.email, NEW.email);
    END IF;
    
    -- Log name changes
    IF OLD.first_name != NEW.first_name THEN
        INSERT INTO user_profile_changes (user_id, field_name, old_value, new_value)
        VALUES (NEW.id, 'first_name', OLD.first_name, NEW.first_name);
    END IF;
    
    IF OLD.last_name != NEW.last_name THEN
        INSERT INTO user_profile_changes (user_id, field_name, old_value, new_value)
        VALUES (NEW.id, 'last_name', OLD.last_name, NEW.last_name);
    END IF;
END;

-- Trigger to update session duration on logout
CREATE TRIGGER IF NOT EXISTS update_session_duration
AFTER UPDATE OF logout_timestamp ON user_login_history
BEGIN
    UPDATE user_login_history 
    SET session_duration_seconds = 
        CASE 
            WHEN NEW.logout_timestamp IS NOT NULL 
            THEN (julianday(NEW.logout_timestamp) - julianday(NEW.login_timestamp)) * 86400
            ELSE NULL 
        END
    WHERE id = NEW.id;
END;

-- =====================================================
-- COMMENTS AND DOCUMENTATION
-- =====================================================

/*
ProTrader User Server Management Database

This database provides comprehensive user management, server monitoring, and administrative features:

Key Features:
1. Role-based access control (RBAC)
2. Comprehensive logging and monitoring
3. User activity tracking
4. Security event management
5. System configuration management
6. Notification system
7. Email template management
8. Backup and maintenance tracking

Security Features:
- Role-based permissions
- Session management
- Security event logging
- User activity monitoring
- IP address tracking

Monitoring Features:
- Server access logs
- Error tracking
- Performance monitoring
- User activity analytics
- Security event management

Administrative Features:
- User management
- Role assignment
- System configuration
- Feature flags
- Email templates
- Backup management

Usage:
1. Run this SQL file to create the user server management schema
2. Use the Python database.py module for programmatic access
3. Integrate with the Flask server.py for API endpoints
4. Monitor user activity and system performance

Performance Notes:
- Indexes created for common query patterns
- Views provided for complex aggregations
- Triggers maintain data consistency
- Consider partitioning for large datasets
- Regular maintenance recommended for log tables
*/
