-- ProTrader Database Initialization Script
-- Run this script to set up the basic database structure

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active INTEGER DEFAULT 1
);

-- Create user sessions table
CREATE TABLE IF NOT EXISTS user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    session_token TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create user portfolios table
CREATE TABLE IF NOT EXISTS user_portfolios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    symbol TEXT NOT NULL,
    shares REAL NOT NULL,
    average_price REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create trading history table
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
);

-- Create user balances table
CREATE TABLE IF NOT EXISTS user_balances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    cash_balance REAL DEFAULT 100000.0,
    total_value REAL DEFAULT 100000.0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create user preferences table
CREATE TABLE IF NOT EXISTS user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    dark_mode INTEGER DEFAULT 1,
    default_timeframe TEXT DEFAULT '1D',
    default_chart_type TEXT DEFAULT 'candlestick',
    notifications_enabled INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create stock price history table
CREATE TABLE IF NOT EXISTS stock_price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    open_price REAL NOT NULL,
    high_price REAL NOT NULL,
    low_price REAL NOT NULL,
    close_price REAL NOT NULL,
    volume INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert demo user
INSERT OR IGNORE INTO users (username, email, password_hash, first_name, last_name) VALUES 
('demo', 'demo@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Demo', 'User');

-- Insert demo user balance
INSERT OR IGNORE INTO user_balances (user_id, cash_balance, total_value) VALUES 
(1, 100000.0, 100000.0);

-- Insert demo user preferences
INSERT OR IGNORE INTO user_preferences (user_id, dark_mode, default_timeframe, default_chart_type) VALUES 
(1, 1, '1D', 'candlestick');

-- Insert sample portfolio for demo user
INSERT OR IGNORE INTO user_portfolios (user_id, symbol, shares, average_price) VALUES 
(1, 'AAPL', 10.5, 145.00),
(1, 'TSLA', 2.0, 750.00);

-- Insert sample trading history
INSERT OR IGNORE INTO trading_history (user_id, symbol, trade_type, shares, price, total_amount) VALUES 
(1, 'AAPL', 'buy', 5.0, 140.00, 700.00),
(1, 'AAPL', 'buy', 5.5, 150.00, 825.00),
(1, 'TSLA', 'buy', 2.0, 750.00, 1500.00);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_portfolios_user_symbol ON user_portfolios(user_id, symbol);
CREATE INDEX IF NOT EXISTS idx_trading_user_timestamp ON trading_history(user_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_price_history_symbol_timestamp ON stock_price_history(symbol, timestamp);

PRAGMA foreign_keys = ON; 
