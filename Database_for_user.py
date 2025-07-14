import sqlite3
import json
from datetime import datetime
import hashlib
import os

class StockDatabase:
    def __init__(self, db_path="stock_trader.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE,
                password_hash TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # User sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # User portfolios table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_portfolios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                symbol TEXT NOT NULL,
                shares REAL NOT NULL,
                average_price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Trading history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trading_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                symbol TEXT NOT NULL,
                trade_type TEXT NOT NULL,
                shares REAL NOT NULL,
                price REAL NOT NULL,
                total_amount REAL NOT NULL,
                commission REAL DEFAULT 9.99,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # User balances table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_balances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                cash_balance REAL DEFAULT 100000.0,
                total_value REAL DEFAULT 100000.0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                dark_mode BOOLEAN DEFAULT 1,
                default_timeframe TEXT DEFAULT '1D',
                default_chart_type TEXT DEFAULT 'candlestick',
                notifications_enabled BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Stock price history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                open_price REAL NOT NULL,
                high_price REAL NOT NULL,
                low_price REAL NOT NULL,
                close_price REAL NOT NULL,
                volume INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, username, password, email=None, first_name=None, last_name=None):
        """Create a new user account"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Hash the password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, first_name, last_name)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, first_name, last_name))
            
            user_id = cursor.lastrowid
            
            # Initialize user balance
            cursor.execute('''
                INSERT INTO user_balances (user_id, cash_balance, total_value)
                VALUES (?, 100000.0, 100000.0)
            ''', (user_id,))
            
            # Initialize user preferences
            cursor.execute('''
                INSERT INTO user_preferences (user_id, dark_mode, default_timeframe, default_chart_type)
                VALUES (?, 1, '1D', 'candlestick')
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            
            return {"success": True, "user_id": user_id, "message": "User created successfully"}
        
        except sqlite3.IntegrityError:
            return {"success": False, "message": "Username or email already exists"}
        except Exception as e:
            return {"success": False, "message": f"Error creating user: {str(e)}"}
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute('''
                SELECT id, username, first_name, last_name, email
                FROM users 
                WHERE username = ? AND password_hash = ? AND is_active = 1
            ''', (username, password_hash))
            
            user = cursor.fetchone()
            
            if user:
                user_id, username, first_name, last_name, email = user
                
                # Update last login
                cursor.execute('''
                    UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
                ''', (user_id,))
                
                # Create session token
                session_token = hashlib.sha256(f"{username}{datetime.now()}".encode()).hexdigest()
                
                # Store session
                cursor.execute('''
                    INSERT INTO user_sessions (user_id, session_token, expires_at)
                    VALUES (?, ?, datetime('now', '+24 hours'))
                ''', (user_id, session_token))
                
                conn.commit()
                conn.close()
                
                return {
                    "success": True,
                    "user_id": user_id,
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "session_token": session_token
                }
            else:
                conn.close()
                return {"success": False, "message": "Invalid username or password"}
        
        except Exception as e:
            return {"success": False, "message": f"Authentication error: {str(e)}"}
    
    def validate_session(self, session_token):
        """Validate user session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT u.id, u.username, u.first_name, u.last_name, u.email
                FROM users u
                JOIN user_sessions s ON u.id = s.user_id
                WHERE s.session_token = ? AND s.expires_at > CURRENT_TIMESTAMP AND u.is_active = 1
            ''', (session_token,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    "success": True,
                    "user_id": user[0],
                    "username": user[1],
                    "first_name": user[2],
                    "last_name": user[3],
                    "email": user[4]
                }
            else:
                return {"success": False, "message": "Invalid or expired session"}
        
        except Exception as e:
            return {"success": False, "message": f"Session validation error: {str(e)}"}
    
    def get_user_portfolio(self, user_id):
        """Get user's current portfolio"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT symbol, shares, average_price
                FROM user_portfolios
                WHERE user_id = ? AND shares > 0
            ''', (user_id,))
            
            portfolio = cursor.fetchall()
            conn.close()
            
            return {
                "success": True,
                "portfolio": [{"symbol": row[0], "shares": row[1], "average_price": row[2]} for row in portfolio]
            }
        
        except Exception as e:
            return {"success": False, "message": f"Error fetching portfolio: {str(e)}"}
    
    def get_user_balance(self, user_id):
        """Get user's current balance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT cash_balance, total_value
                FROM user_balances
                WHERE user_id = ?
            ''', (user_id,))
            
            balance = cursor.fetchone()
            conn.close()
            
            if balance:
                return {
                    "success": True,
                    "cash_balance": balance[0],
                    "total_value": balance[1]
                }
            else:
                return {"success": False, "message": "Balance not found"}
        
        except Exception as e:
            return {"success": False, "message": f"Error fetching balance: {str(e)}"}
    
    def execute_trade(self, user_id, symbol, trade_type, shares, price, total_amount):
        """Execute a trade and update portfolio"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Record the trade
            cursor.execute('''
                INSERT INTO trading_history (user_id, symbol, trade_type, shares, price, total_amount)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, symbol, trade_type, shares, price, total_amount))
            
            if trade_type == 'buy':
                # Check if user already owns this stock
                cursor.execute('''
                    SELECT shares, average_price FROM user_portfolios 
                    WHERE user_id = ? AND symbol = ?
                ''', (user_id, symbol))
                
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing position
                    current_shares, current_avg = existing
                    new_shares = current_shares + shares
                    new_avg = ((current_shares * current_avg) + (shares * price)) / new_shares
                    
                    cursor.execute('''
                        UPDATE user_portfolios 
                        SET shares = ?, average_price = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = ? AND symbol = ?
                    ''', (new_shares, new_avg, user_id, symbol))
                else:
                    # Create new position
                    cursor.execute('''
                        INSERT INTO user_portfolios (user_id, symbol, shares, average_price)
                        VALUES (?, ?, ?, ?)
                    ''', (user_id, symbol, shares, price))
                
                # Update cash balance
                cursor.execute('''
                    UPDATE user_balances 
                    SET cash_balance = cash_balance - ?, last_updated = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (total_amount, user_id))
            
            elif trade_type == 'sell':
                # Check if user has enough shares
                cursor.execute('''
                    SELECT shares FROM user_portfolios 
                    WHERE user_id = ? AND symbol = ?
                ''', (user_id, symbol))
                
                current_shares = cursor.fetchone()
                
                if current_shares and current_shares[0] >= shares:
                    new_shares = current_shares[0] - shares
                    
                    if new_shares > 0:
                        cursor.execute('''
                            UPDATE user_portfolios 
                            SET shares = ?, updated_at = CURRENT_TIMESTAMP
                            WHERE user_id = ? AND symbol = ?
                        ''', (new_shares, user_id, symbol))
                    else:
                        cursor.execute('''
                            DELETE FROM user_portfolios 
                            WHERE user_id = ? AND symbol = ?
                        ''', (user_id, symbol))
                    
                    # Update cash balance
                    cursor.execute('''
                        UPDATE user_balances 
                        SET cash_balance = cash_balance + ?, last_updated = CURRENT_TIMESTAMP
                        WHERE user_id = ?
                    ''', (total_amount, user_id))
                else:
                    conn.rollback()
                    conn.close()
                    return {"success": False, "message": "Insufficient shares to sell"}
            
            conn.commit()
            conn.close()
            
            return {"success": True, "message": f"Trade executed successfully"}
        
        except Exception as e:
            return {"success": False, "message": f"Error executing trade: {str(e)}"}
    
    def save_stock_price(self, symbol, open_price, high_price, low_price, close_price, volume):
        """Save stock price data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO stock_price_history (symbol, open_price, high_price, low_price, close_price, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (symbol, open_price, high_price, low_price, close_price, volume))
            
            conn.commit()
            conn.close()
            
            return {"success": True}
        
        except Exception as e:
            return {"success": False, "message": f"Error saving price data: {str(e)}"}
    
    def get_stock_history(self, symbol, limit=100):
        """Get stock price history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT open_price, high_price, low_price, close_price, volume, timestamp
                FROM stock_price_history
                WHERE symbol = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (symbol, limit))
            
            history = cursor.fetchall()
            conn.close()
            
            return {
                "success": True,
                "history": [
                    {
                        "open": row[0],
                        "high": row[1],
                        "low": row[2],
                        "close": row[3],
                        "volume": row[4],
                        "timestamp": row[5]
                    } for row in history
                ]
            }
        
        except Exception as e:
            return {"success": False, "message": f"Error fetching stock history: {str(e)}"}
    
    def update_user_preferences(self, user_id, dark_mode=None, default_timeframe=None, default_chart_type=None):
        """Update user preferences"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if dark_mode is not None:
                updates.append("dark_mode = ?")
                params.append(dark_mode)
            
            if default_timeframe is not None:
                updates.append("default_timeframe = ?")
                params.append(default_timeframe)
            
            if default_chart_type is not None:
                updates.append("default_chart_type = ?")
                params.append(default_chart_type)
            
            if updates:
                params.append(user_id)
                cursor.execute(f'''
                    UPDATE user_preferences 
                    SET {', '.join(updates)}
                    WHERE user_id = ?
                ''', params)
                
                conn.commit()
            
            conn.close()
            
            return {"success": True, "message": "Preferences updated"}
        
        except Exception as e:
            return {"success": False, "message": f"Error updating preferences: {str(e)}"}
    
    def get_user_preferences(self, user_id):
        """Get user preferences"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT dark_mode, default_timeframe, default_chart_type, notifications_enabled
                FROM user_preferences
                WHERE user_id = ?
            ''', (user_id,))
            
            prefs = cursor.fetchone()
            conn.close()
            
            if prefs:
                return {
                    "success": True,
                    "dark_mode": bool(prefs[0]),
                    "default_timeframe": prefs[1],
                    "default_chart_type": prefs[2],
                    "notifications_enabled": bool(prefs[3])
                }
            else:
                return {"success": False, "message": "Preferences not found"}
        
        except Exception as e:
            return {"success": False, "message": f"Error fetching preferences: {str(e)}"}
    
    def get_trading_history(self, user_id, limit=50):
        """Get user's trading history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT symbol, trade_type, shares, price, total_amount, timestamp
                FROM trading_history
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            
            history = cursor.fetchall()
            conn.close()
            
            return {
                "success": True,
                "history": [
                    {
                        "symbol": row[0],
                        "trade_type": row[1],
                        "shares": row[2],
                        "price": row[3],
                        "total_amount": row[4],
                        "timestamp": row[5]
                    } for row in history
                ]
            }
        
        except Exception as e:
            return {"success": False, "message": f"Error fetching trading history: {str(e)}"}
    
    def logout_user(self, session_token):
        """Logout user by removing session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM user_sessions WHERE session_token = ?
            ''', (session_token,))
            
            conn.commit()
            conn.close()
            
            return {"success": True, "message": "Logged out successfully"}
        
        except Exception as e:
            return {"success": False, "message": f"Error logging out: {str(e)}"}

# Example usage
if __name__ == "__main__":
    db = StockDatabase()
    
    # Create a test user
    result = db.create_user("testuser", "password123", "test@example.com", "John", "Doe")
    print("Create user:", result)
    
    # Authenticate user
    auth_result = db.authenticate_user("testuser", "password123")
    print("Authentication:", auth_result) 
