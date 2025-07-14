// Stock Analyzer Application
class StockAnalyzer {
    constructor() {
        this.stocks = {
            'AAPL': { name: 'Apple Inc.', price: 150.00, volatility: 0.02, trend: 0.001, change: 2.50, changePercent: 1.67 },
            'AMZN': { name: 'Amazon.com', price: 3200.00, volatility: 0.025, trend: 0.002, change: -15.20, changePercent: -0.47 },
            'GOOGL': { name: 'Alphabet Inc.', price: 2800.00, volatility: 0.018, trend: 0.0015, change: 8.40, changePercent: 0.30 },
            'TSLA': { name: 'Tesla Inc.', price: 800.00, volatility: 0.04, trend: 0.003, change: 25.60, changePercent: 3.20 },
            'MSFT': { name: 'Microsoft Corp.', price: 300.00, volatility: 0.015, trend: 0.001, change: 3.75, changePercent: 1.25 },
            'BTC': { name: 'Bitcoin', price: 45000.00, volatility: 0.06, trend: 0.005, change: 1200.00, changePercent: 2.67 },
            'ETH': { name: 'Ethereum', price: 3000.00, volatility: 0.07, trend: 0.006, change: -45.00, changePercent: -1.50 },
            'GOLD': { name: 'Gold', price: 1800.00, volatility: 0.01, trend: 0.0005, change: 5.40, changePercent: 0.30 },
            'SILVER': { name: 'Silver', price: 25.00, volatility: 0.015, trend: 0.001, change: -0.15, changePercent: -0.60 },
            'OIL': { name: 'Crude Oil', price: 75.00, volatility: 0.03, trend: 0.002, change: 1.20, changePercent: 1.60 }
        };

        this.selectedStock = 'AAPL';
        this.money = 100000;
        this.portfolio = {};
        this.chartData = {};
        this.chart = null;
        this.isDarkMode = true;
        this.tradeType = 'buy';
        this.tradeAmount = 1000;
        this.timeframe = '1D';
        this.chartType = 'candlestick';

        this.init();
    }

    init() {
        this.initializeChartData();
        this.setupEventListeners();
        this.renderStockList();
        this.renderPortfolio();
        this.updateChart();
        this.updateBalances();
        this.startPriceUpdates();
    }

    initializeChartData() {
        Object.keys(this.stocks).forEach(symbol => {
            this.chartData[symbol] = this.generateHistoricalData(symbol);
        });
    }

    generateHistoricalData(symbol) {
        const data = [];
        const basePrice = this.stocks[symbol].price;
        const now = new Date();
        
        for (let i = 100; i >= 0; i--) {
            const time = new Date(now.getTime() - i * 60000); // 1 minute intervals
            const volatility = this.stocks[symbol].volatility;
            const trend = this.stocks[symbol].trend;
            
            // Generate realistic price movement
            const randomChange = (Math.random() - 0.5) * 2 * volatility;
            const trendChange = trend;
            const totalChange = randomChange + trendChange;
            
            const price = basePrice * (1 + totalChange * i / 100);
            
            // Generate OHLC data
            const open = price;
            const high = price * (1 + Math.random() * 0.02);
            const low = price * (1 - Math.random() * 0.02);
            const close = price * (1 + (Math.random() - 0.5) * 0.01);
            
            data.push({
                time: time,
                open: open,
                high: high,
                low: low,
                close: close,
                volume: Math.floor(Math.random() * 1000000) + 100000
            });
        }
        
        return data;
    }

    setupEventListeners() {
        // Theme toggle
        document.getElementById('themeToggle').addEventListener('click', () => {
            this.toggleTheme();
        });

        // Fullscreen toggle
        document.getElementById('fullscreenToggle').addEventListener('click', () => {
            this.toggleFullscreen();
        });

        // Trading tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setTradeType(e.target.dataset.tab);
            });
        });

        // Amount buttons
        document.querySelectorAll('.amount-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.adjustTradeAmount(parseInt(e.target.dataset.amount));
            });
        });

        // Trade amount input
        document.getElementById('tradeAmount').addEventListener('input', (e) => {
            this.tradeAmount = parseFloat(e.target.value) || 0;
            this.updateTradeSummary();
        });

        // Execute trade
        document.getElementById('executeTrade').addEventListener('click', () => {
            this.executeTrade();
        });

        // Timeframe buttons
        document.querySelectorAll('.timeframe-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setTimeframe(e.target.dataset.timeframe);
            });
        });

        // Chart type buttons
        document.querySelectorAll('.chart-type-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setChartType(e.target.dataset.type);
            });
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                e.preventDefault();
                this.toggleTheme();
            } else if (e.key === 'F11') {
                e.preventDefault();
                this.toggleFullscreen();
            }
        });
    }

    toggleTheme() {
        this.isDarkMode = !this.isDarkMode;
        document.body.className = this.isDarkMode ? 'dark-mode' : 'light-mode';
        
        const icon = document.querySelector('#themeToggle i');
        icon.className = this.isDarkMode ? 'fas fa-sun' : 'fas fa-moon';
        
        this.updateChart();
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
            document.querySelector('#fullscreenToggle i').className = 'fas fa-compress';
        } else {
            document.exitFullscreen();
            document.querySelector('#fullscreenToggle i').className = 'fas fa-expand';
        }
    }

    setTradeType(type) {
        this.tradeType = type;
        
        // Update UI
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${type}"]`).classList.add('active');
        
        this.updateTradeSummary();
    }

    adjustTradeAmount(amount) {
        this.tradeAmount += amount;
        document.getElementById('tradeAmount').value = this.tradeAmount;
        this.updateTradeSummary();
    }

    updateTradeSummary() {
        const currentPrice = this.stocks[this.selectedStock].price;
        const shares = this.tradeAmount / currentPrice;
        const commission = 9.99;
        const total = this.tradeAmount + commission;
        
        document.getElementById('sharesToTrade').textContent = shares.toFixed(2);
        document.getElementById('totalTradeAmount').textContent = `$${total.toFixed(2)}`;
    }

    executeTrade() {
        const symbol = this.selectedStock;
        const currentPrice = this.stocks[symbol].price;
        const shares = this.tradeAmount / currentPrice;
        
        if (this.tradeType === 'buy') {
            if (this.tradeAmount > this.money) {
                this.showNotification('Insufficient funds!', 'error');
                return;
            }
            
            this.money -= this.tradeAmount;
            this.portfolio[symbol] = (this.portfolio[symbol] || 0) + shares;
            
            this.showNotification(`Bought ${shares.toFixed(2)} shares of ${symbol} for $${this.tradeAmount.toFixed(2)}`, 'success');
        } else {
            if (!this.portfolio[symbol] || this.portfolio[symbol] < shares) {
                this.showNotification('Insufficient shares to sell!', 'error');
                return;
            }
            
            this.money += this.tradeAmount;
            this.portfolio[symbol] -= shares;
            
            if (this.portfolio[symbol] <= 0) {
                delete this.portfolio[symbol];
            }
            
            this.showNotification(`Sold ${shares.toFixed(2)} shares of ${symbol} for $${this.tradeAmount.toFixed(2)}`, 'success');
        }
        
        this.updateBalances();
        this.renderPortfolio();
    }

    setTimeframe(timeframe) {
        this.timeframe = timeframe;
        
        document.querySelectorAll('.timeframe-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-timeframe="${timeframe}"]`).classList.add('active');
        
        this.updateChart();
    }

    setChartType(type) {
        this.chartType = type;
        
        document.querySelectorAll('.chart-type-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-type="${type}"]`).classList.add('active');
        
        this.updateChart();
    }

    renderStockList() {
        const stockList = document.getElementById('stockList');
        stockList.innerHTML = '';
        
        Object.entries(this.stocks).forEach(([symbol, stock]) => {
            const stockItem = document.createElement('div');
            stockItem.className = `stock-item ${symbol === this.selectedStock ? 'active' : ''}`;
            stockItem.innerHTML = `
                <div class="stock-item-header">
                    <span class="stock-symbol">${symbol}</span>
                    <span class="stock-price">$${stock.price.toFixed(2)}</span>
                </div>
                <div class="stock-item-details">
                    <span>${stock.name}</span>
                    <span class="price-change ${stock.change >= 0 ? 'positive' : 'negative'}">
                        ${stock.change >= 0 ? '+' : ''}$${Math.abs(stock.change).toFixed(2)} (${stock.changePercent >= 0 ? '+' : ''}${stock.changePercent.toFixed(2)}%)
                    </span>
                </div>
            `;
            
            stockItem.addEventListener('click', () => {
                this.selectStock(symbol);
            });
            
            stockList.appendChild(stockItem);
        });
    }

    selectStock(symbol) {
        this.selectedStock = symbol;
        this.renderStockList();
        this.updateStockInfo();
        this.updateChart();
        this.updateTradeSummary();
    }

    updateStockInfo() {
        const stock = this.stocks[this.selectedStock];
        
        document.getElementById('selectedStockName').textContent = stock.name;
        document.getElementById('selectedStockSymbol').textContent = this.selectedStock;
        document.getElementById('selectedStockPrice').textContent = `$${stock.price.toFixed(2)}`;
        
        const priceChangeElement = document.getElementById('priceChange');
        priceChangeElement.textContent = `${stock.change >= 0 ? '+' : ''}$${Math.abs(stock.change).toFixed(2)} (${stock.changePercent >= 0 ? '+' : ''}${stock.changePercent.toFixed(2)}%)`;
        priceChangeElement.className = `price-change ${stock.change >= 0 ? 'positive' : 'negative'}`;
        
        // Update market data
        const data = this.chartData[this.selectedStock];
        if (data && data.length > 0) {
            const latest = data[data.length - 1];
            const open = data[0].open;
            const high = Math.max(...data.map(d => d.high));
            const low = Math.min(...data.map(d => d.low));
            const volume = data.reduce((sum, d) => sum + d.volume, 0);
            
            document.getElementById('marketOpen').textContent = `$${open.toFixed(2)}`;
            document.getElementById('marketHigh').textContent = `$${high.toFixed(2)}`;
            document.getElementById('marketLow').textContent = `$${low.toFixed(2)}`;
            document.getElementById('marketVolume').textContent = `${(volume / 1000000).toFixed(1)}M`;
        }
    }

    renderPortfolio() {
        const portfolioHoldings = document.getElementById('portfolioHoldings');
        portfolioHoldings.innerHTML = '';
        
        if (Object.keys(this.portfolio).length === 0) {
            portfolioHoldings.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: var(--spacing-4);">No stocks owned</p>';
            return;
        }
        
        Object.entries(this.portfolio).forEach(([symbol, shares]) => {
            const stock = this.stocks[symbol];
            const value = shares * stock.price;
            
            const holdingItem = document.createElement('div');
            holdingItem.className = 'holding-item';
            holdingItem.innerHTML = `
                <div class="holding-header">
                    <span class="holding-symbol">${symbol}</span>
                    <span class="holding-value">$${value.toFixed(2)}</span>
                </div>
                <div class="holding-details">
                    <span>${shares.toFixed(2)} shares</span>
                    <span>$${stock.price.toFixed(2)}</span>
                </div>
            `;
            
            portfolioHoldings.appendChild(holdingItem);
        });
    }

    updateBalances() {
        let portfolioValue = this.money;
        Object.entries(this.portfolio).forEach(([symbol, shares]) => {
            portfolioValue += shares * this.stocks[symbol].price;
        });
        
        document.getElementById('totalBalance').textContent = this.money.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        document.getElementById('portfolioValue').textContent = portfolioValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        
        // Calculate P&L (simplified)
        const pnl = portfolioValue - 100000;
        const pnlElement = document.getElementById('todayPnL');
        pnlElement.textContent = `${pnl >= 0 ? '+' : ''}$${Math.abs(pnl).toFixed(2)}`;
        pnlElement.className = `pnl ${pnl >= 0 ? 'positive' : 'negative'}`;
    }

    updateChart() {
        const ctx = document.getElementById('stockChart').getContext('2d');
        
        if (this.chart) {
            this.chart.destroy();
        }
        
        const data = this.chartData[this.selectedStock];
        if (!data || data.length === 0) return;
        
        const labels = data.map(d => d.time.toLocaleTimeString());
        const prices = data.map(d => d.close);
        
        const chartData = {
            labels: labels,
            datasets: [{
                label: this.selectedStock,
                data: prices,
                borderColor: this.isDarkMode ? '#58a6ff' : '#007bff',
                backgroundColor: this.isDarkMode ? 'rgba(88, 166, 255, 0.1)' : 'rgba(0, 123, 255, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.1
            }]
        };
        
        this.chart = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        display: false
                    },
                    y: {
                        display: true,
                        grid: {
                            color: this.isDarkMode ? '#30363d' : '#e9ecef'
                        },
                        ticks: {
                            color: this.isDarkMode ? '#8b949e' : '#6c757d'
                        }
                    }
                },
                elements: {
                    point: {
                        radius: 0
                    }
                }
            }
        });
    }

    startPriceUpdates() {
        setInterval(() => {
            this.updatePrices();
        }, 2000); // Update every 2 seconds
    }

    updatePrices() {
        Object.entries(this.stocks).forEach(([symbol, stock]) => {
            // Simulate price movement
            const volatility = stock.volatility;
            const trend = stock.trend;
            const randomChange = (Math.random() - 0.5) * 2 * volatility;
            const trendChange = trend;
            const totalChange = randomChange + trendChange;
            
            const oldPrice = stock.price;
            stock.price *= (1 + totalChange);
            
            // Update change and change percent
            stock.change = stock.price - oldPrice;
            stock.changePercent = (stock.change / oldPrice) * 100;
            
            // Add new data point
            const newDataPoint = {
                time: new Date(),
                open: oldPrice,
                high: Math.max(oldPrice, stock.price),
                low: Math.min(oldPrice, stock.price),
                close: stock.price,
                volume: Math.floor(Math.random() * 1000000) + 100000
            };
            
            this.chartData[symbol].push(newDataPoint);
            
            // Keep only last 100 data points
            if (this.chartData[symbol].length > 100) {
                this.chartData[symbol].shift();
            }
        });
        
        this.renderStockList();
        this.updateStockInfo();
        this.updateChart();
        this.updateBalances();
        this.renderPortfolio();
    }

    showNotification(message, type = 'info') {
        const notifications = document.getElementById('notifications');
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        notifications.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new StockAnalyzer();
}); 
