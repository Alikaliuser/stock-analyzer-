import sqlite3
import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import os
import shutil
from database import StockDatabase

class ServerManager:
    def __init__(self, db_path="stock_trader.db"):
        self.db_path = db_path
        self.db = StockDatabase(db_path)
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('server_manager.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    # =====================================================
    # USER MANAGEMENT
    # =====================================================
    
    def create_user_with_role(self, username: str, password: str, email: str, 
                             first_name: str, last_name: str, role_name: str = 'standard_user') -> Dict:
        """Create a new user with specified role"""
        try:
            # Create user
            user_result = self.db.create_user(username, password, email, first_name, last_name)
            
            if not user_result['success']:
                return user_result
            
            user_id = user_result['user_id']
            
            # Assign role
            role_result = self.assign_role_to_user(user_id, role_name)
            
            if not role_result['success']:
                self.logger.warning(f"User created but role assignment failed: {role_result['message']}")
            
            return {
                'success': True,
                'user_id': user_id,
                'message': 'User created successfully with role assignment'
            }
            
        except Exception as e:
            self.logger.error(f"Error creating user with role: {str(e)}")
            return {'success': False, 'message': f'Error creating user: {str(e)}'}
    
    def assign_role_to_user(self, user_id: int, role_name: str, assigned_by: int = None) -> Dict:
        """Assign a role to a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get role ID
            cursor.execute('SELECT id FROM user_roles WHERE role_name = ? AND is_active = 1', (role_name,))
            role = cursor.fetchone()
            
            if not role:
                return {'success': False, 'message': f'Role {role_name} not found'}
            
            role_id = role[0]
            
            # Check if user exists
            cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            
            if not user:
                return {'success': False, 'message': 'User not found'}
            
            # Assign role
            cursor.execute('''
                INSERT OR REPLACE INTO user_role_assignments (user_id, role_id, assigned_by)
                VALUES (?, ?, ?)
            ''', (user_id, role_id, assigned_by))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Role {role_name} assigned to user {user_id}")
            return {'success': True, 'message': f'Role {role_name} assigned successfully'}
            
        except Exception as e:
            self.logger.error(f"Error assigning role: {str(e)}")
            return {'success': False, 'message': f'Error assigning role: {str(e)}'}
    
    def get_user_permissions(self, user_id: int) -> Dict:
        """Get all permissions for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT p.permission_name, p.module
                FROM users u
                JOIN user_role_assignments ura ON u.id = ura.user_id
                JOIN user_roles r ON ura.role_id = r.id
                JOIN role_permissions rp ON r.id = rp.role_id
                JOIN permissions p ON rp.permission_id = p.id
                WHERE u.id = ? AND ura.is_active = 1 AND r.is_active = 1 AND p.is_active = 1
            ''', (user_id,))
            
            permissions = cursor.fetchall()
            conn.close()
            
            return {
                'success': True,
                'permissions': [{'name': p[0], 'module': p[1]} for p in permissions]
            }
            
        except Exception as e:
            self.logger.error(f"Error getting user permissions: {str(e)}")
            return {'success': False, 'message': f'Error getting permissions: {str(e)}'}
    
    def check_user_permission(self, user_id: int, permission_name: str) -> bool:
        """Check if user has a specific permission"""
        try:
            permissions = self.get_user_permissions(user_id)
            if not permissions['success']:
                return False
            
            return any(p['name'] == permission_name for p in permissions['permissions'])
            
        except Exception as e:
            self.logger.error(f"Error checking permission: {str(e)}")
            return False
    
    # =====================================================
    # SERVER MONITORING
    # =====================================================
    
    def log_server_access(self, user_id: int = None, session_token: str = None, 
                         ip_address: str = None, user_agent: str = None,
                         request_method: str = None, request_url: str = None,
                         request_params: str = None, response_status: int = None,
                         response_time_ms: int = None) -> bool:
        """Log server access"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO server_access_logs 
                (user_id, session_token, ip_address, user_agent, request_method, 
                 request_url, request_params, response_status, response_time_ms)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, session_token, ip_address, user_agent, request_method,
                  request_url, request_params, response_status, response_time_ms))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging server access: {str(e)}")
            return False
    
    def log_server_error(self, user_id: int = None, session_token: str = None,
                        ip_address: str = None, error_type: str = None,
                        error_message: str = None, stack_trace: str = None,
                        request_data: str = None) -> bool:
        """Log server error"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO server_error_logs 
                (user_id, session_token, ip_address, error_type, error_message, 
                 stack_trace, request_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, session_token, ip_address, error_type, error_message,
                  stack_trace, request_data))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging server error: {str(e)}")
            return False
    
    def log_user_activity(self, user_id: int, activity_type: str, 
                         activity_description: str, ip_address: str = None,
                         user_agent: str = None, metadata: Dict = None) -> bool:
        """Log user activity"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            metadata_json = json.dumps(metadata) if metadata else None
            
            cursor.execute('''
                INSERT INTO user_activity_logs 
                (user_id, activity_type, activity_description, ip_address, user_agent, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, activity_type, activity_description, ip_address, user_agent, metadata_json))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging user activity: {str(e)}")
            return False
    
    def log_security_event(self, user_id: int = None, event_type: str = None,
                          event_description: str = None, ip_address: str = None,
                          severity: str = 'medium') -> bool:
        """Log security event"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO user_security_events 
                (user_id, event_type, event_description, ip_address, severity)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, event_type, event_description, ip_address, severity))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging security event: {str(e)}")
            return False
    
    # =====================================================
    # SYSTEM CONFIGURATION
    # =====================================================
    
    def get_system_config(self, config_key: str) -> Optional[str]:
        """Get system configuration value"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT config_value FROM system_config WHERE config_key = ?', (config_key,))
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
            
        except Exception as e:
            self.logger.error(f"Error getting system config: {str(e)}")
            return None
    
    def set_system_config(self, config_key: str, config_value: str, 
                         updated_by: int = None) -> bool:
        """Set system configuration value"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO system_config 
                (config_key, config_value, updated_at, updated_by)
                VALUES (?, ?, CURRENT_TIMESTAMP, ?)
            ''', (config_key, config_value, updated_by))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"System config updated: {config_key} = {config_value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting system config: {str(e)}")
            return False
    
    def is_feature_enabled(self, feature_name: str, user_id: int = None) -> bool:
        """Check if a feature is enabled for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT is_enabled, enabled_for_all, enabled_for_roles, enabled_for_users
                FROM feature_flags WHERE feature_name = ?
            ''', (feature_name,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return False
            
            is_enabled, enabled_for_all, enabled_for_roles, enabled_for_users = result
            
            if not is_enabled:
                return False
            
            if enabled_for_all:
                return True
            
            if user_id and enabled_for_users:
                user_ids = json.loads(enabled_for_users)
                if user_id in user_ids:
                    return True
            
            if user_id and enabled_for_roles:
                role_ids = json.loads(enabled_for_roles)
                user_roles = self.get_user_roles(user_id)
                if any(role['id'] in role_ids for role in user_roles):
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking feature flag: {str(e)}")
            return False
    
    # =====================================================
    # USER ANALYTICS
    # =====================================================
    
    def get_user_activity_summary(self, user_id: int = None) -> Dict:
        """Get user activity summary"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute('''
                    SELECT * FROM user_activity_summary WHERE user_id = ?
                ''', (user_id,))
            else:
                cursor.execute('SELECT * FROM user_activity_summary')
            
            results = cursor.fetchall()
            conn.close()
            
            columns = ['user_id', 'username', 'first_name', 'last_name', 
                      'total_activities', 'total_logins', 'last_login', 
                      'security_events', 'account_created']
            
            return {
                'success': True,
                'data': [dict(zip(columns, row)) for row in results]
            }
            
        except Exception as e:
            self.logger.error(f"Error getting user activity summary: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def get_server_performance_summary(self) -> Dict:
        """Get server performance summary"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM server_performance_summary')
            results = cursor.fetchall()
            conn.close()
            
            columns = ['endpoint', 'method', 'avg_response_time', 'total_requests',
                      'total_errors', 'error_rate_percent', 'last_activity']
            
            return {
                'success': True,
                'data': [dict(zip(columns, row)) for row in results]
            }
            
        except Exception as e:
            self.logger.error(f"Error getting server performance summary: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    # =====================================================
    # MAINTENANCE AND BACKUP
    # =====================================================
    
    def create_backup(self, backup_type: str = 'full', initiated_by: int = None) -> Dict:
        """Create database backup"""
        try:
            backup_dir = 'backups'
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f"{backup_dir}/backup_{backup_type}_{timestamp}.db"
            
            # Copy database file
            shutil.copy2(self.db_path, backup_path)
            
            # Get file size
            file_size = os.path.getsize(backup_path)
            
            # Log backup
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO backup_logs 
                (backup_type, backup_path, backup_size_bytes, status, completed_at, initiated_by)
                VALUES (?, ?, ?, 'success', CURRENT_TIMESTAMP, ?)
            ''', (backup_type, backup_path, file_size, initiated_by))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Backup created: {backup_path}")
            return {
                'success': True,
                'backup_path': backup_path,
                'file_size': file_size
            }
            
        except Exception as e:
            self.logger.error(f"Error creating backup: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    def cleanup_old_logs(self, days_to_keep: int = 30) -> Dict:
        """Clean up old log entries"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # Clean up access logs
            cursor.execute('''
                DELETE FROM server_access_logs 
                WHERE timestamp < ?
            ''', (cutoff_date,))
            access_logs_deleted = cursor.rowcount
            
            # Clean up error logs (keep resolved ones longer)
            cursor.execute('''
                DELETE FROM server_error_logs 
                WHERE timestamp < ? AND resolved = 1
            ''', (cutoff_date,))
            error_logs_deleted = cursor.rowcount
            
            # Clean up activity logs
            cursor.execute('''
                DELETE FROM user_activity_logs 
                WHERE timestamp < ?
            ''', (cutoff_date,))
            activity_logs_deleted = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Cleaned up {access_logs_deleted} access logs, {error_logs_deleted} error logs, {activity_logs_deleted} activity logs")
            
            return {
                'success': True,
                'access_logs_deleted': access_logs_deleted,
                'error_logs_deleted': error_logs_deleted,
                'activity_logs_deleted': activity_logs_deleted
            }
            
        except Exception as e:
            self.logger.error(f"Error cleaning up logs: {str(e)}")
            return {'success': False, 'message': str(e)}
    
    # =====================================================
    # HELPER METHODS
    # =====================================================
    
    def get_user_roles(self, user_id: int) -> List[Dict]:
        """Get roles for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT r.id, r.role_name, r.description, ura.assigned_at
                FROM user_roles r
                JOIN user_role_assignments ura ON r.id = ura.role_id
                WHERE ura.user_id = ? AND ura.is_active = 1 AND r.is_active = 1
            ''', (user_id,))
            
            roles = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': role[0],
                    'name': role[1],
                    'description': role[2],
                    'assigned_at': role[3]
                }
                for role in roles
            ]
            
        except Exception as e:
            self.logger.error(f"Error getting user roles: {str(e)}")
            return []
    
    def get_all_roles(self) -> List[Dict]:
        """Get all available roles"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, role_name, description, is_active
                FROM user_roles
                ORDER BY role_name
            ''')
            
            roles = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': role[0],
                    'name': role[1],
                    'description': role[2],
                    'is_active': bool(role[3])
                }
                for role in roles
            ]
            
        except Exception as e:
            self.logger.error(f"Error getting all roles: {str(e)}")
            return []

# Example usage
if __name__ == "__main__":
    manager = ServerManager()
    
    # Create a new user with role
    result = manager.create_user_with_role(
        username="testuser",
        password="password123",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        role_name="premium_user"
    )
    print("Create user result:", result)
    
    # Check permissions
    if result['success']:
        permissions = manager.get_user_permissions(result['user_id'])
        print("User permissions:", permissions)
    
    # Create backup
    backup_result = manager.create_backup('full')
    print("Backup result:", backup_result)
    
    # Get system config
    max_login_attempts = manager.get_system_config('max_login_attempts')
    print("Max login attempts:", max_login_attempts)
