# Professional Stock Analyzer & Trading Simulator

A comprehensive stock trading simulator available in both **Python (Pygame)** and **Web (HTML/CSS/JavaScript)** versions, featuring real-time price simulation, professional charts, and advanced trading interface.

## 🚀 Features

### 🎯 Core Trading Features
- **Real-time Stock Simulation**: 10 different stocks including Apple, Amazon, Google, Tesla, Bitcoin, Ethereum, Gold, Silver, and Oil
- **Live Price Updates**: Realistic price movements with volatility and trends
- **Trading System**: Buy and sell stocks with real-time portfolio tracking
- **Money Management**: Start with $100,000 and manage your investments
- **Professional Interface**: Modern, responsive design with dark/light mode

### 📊 Professional Charts
- **Candlestick Charts**: Professional OHLC (Open, High, Low, Close) visualization
- **Line Charts**: Alternative chart view for price trends
- **Real-time Updates**: Charts update automatically as prices change
- **Historical Data**: View last 100 data points for analysis
- **Multiple Timeframes**: 1D, 1W, 1M, 3M views

### 🎨 User Interface
- **Dark/Light Mode**: Toggle between professional dark and light themes
- **Fullscreen Support**: Switch between windowed and fullscreen modes
- **Responsive Design**: Professional trading interface layout
- **Interactive Panels**: Click to select stocks, adjust trade amounts, and execute trades
- **Real-time Notifications**: Get instant feedback on trades and system events

## 📁 Project Structure

```
my_website_test/
├── GAME.py              # Python/Pygame version
├── index.html           # Web version - Main HTML
├── styles.css           # Web version - CSS styles
├── script.js            # Web version - JavaScript
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🐍 Python Version (Pygame)

### Installation & Setup

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Game**:
   ```bash
   python GAME.py
   ```

### Python Features
- **Desktop Application**: Full-screen or windowed mode
- **Keyboard Controls**: Tab (theme), Space (chart type), F11 (fullscreen), Escape (quit)
- **Mouse Interaction**: Click to select stocks, adjust amounts, execute trades
- **Real-time Simulation**: Prices update every second with adjustable speed

## 🌐 Web Version (HTML/CSS/JavaScript)

### Installation & Setup

1. **No Installation Required**: Just open `index.html` in any modern web browser
2. **Or serve locally**:
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js
   npx serve .
   ```

3. **Open in browser**: Navigate to `http://localhost:8000`

### Web Features
- **Browser-based**: Works on any device with a modern browser
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Chart.js Integration**: Professional charting library
- **Real-time Updates**: Prices update every 2 seconds
- **Modern UI**: Material design-inspired interface

## 🎮 How to Play

### Getting Started
1. Launch either version and you'll see the professional trading interface
2. You start with $100,000 in cash
3. Select a stock from the watchlist to view its chart and current price
4. Use the trading panel to buy and sell stocks

### Trading Interface

#### Stock Selection (Watchlist)
- Click on any stock symbol to select it
- View current price, company name, and price change
- Selected stock is highlighted and shows detailed chart

#### Trading Panel
- **Cash Display**: Shows your available cash
- **Portfolio Value**: Total value of cash + stocks
- **Buy/Sell Tabs**: Choose trade direction
- **Amount Input**: Set trade amount manually or use quick buttons
- **Execute Trade**: Complete the transaction with one click

#### Portfolio Management
- View all stocks you own
- See number of shares and current value
- Track your investment performance
- Real-time P&L calculation

#### Chart Analysis
- **Candlestick Chart**: Green candles = price up, Red candles = price down
- **Line Chart**: Smooth price trend visualization
- **Current Price**: Large display of selected stock price
- **Market Data**: Open, High, Low, Volume information

### Keyboard Shortcuts (Python Version)
- **Tab**: Toggle dark/light mode
- **Space**: Switch between candlestick and line charts
- **F11**: Toggle fullscreen
- **Escape**: Exit fullscreen or quit game

### Keyboard Shortcuts (Web Version)
- **Tab**: Toggle dark/light mode
- **F11**: Toggle fullscreen

## 📈 Stock Information

| Symbol | Company | Base Price | Volatility | Trend |
|--------|---------|------------|------------|-------|
| AAPL | Apple Inc. | $150 | Low | Slight Up |
| AMZN | Amazon.com | $3,200 | Medium | Up |
| GOOGL | Alphabet Inc. | $2,800 | Low | Up |
| TSLA | Tesla Inc. | $800 | High | Up |
| MSFT | Microsoft Corp. | $300 | Low | Slight Up |
| BTC | Bitcoin | $45,000 | Very High | Up |
| ETH | Ethereum | $3,000 | Very High | Up |
| GOLD | Gold | $1,800 | Low | Stable |
| SILVER | Silver | $25 | Low | Slight Up |
| OIL | Crude Oil | $75 | Medium | Variable |

## 🎯 Trading Strategy Tips

- **Buy Low, Sell High**: Watch price trends and buy when prices are low
- **Diversify**: Don't put all your money in one stock
- **Monitor Volatility**: Some stocks (like Bitcoin) are more volatile than others
- **Use Charts**: Analyze candlestick patterns for trading decisions
- **Set Stop Losses**: Protect your investments from major losses
- **Track Performance**: Monitor your portfolio's P&L regularly

## 🛠 Technical Details

### Price Simulation
- Uses random walk with trend and volatility parameters
- Each stock has unique characteristics
- Realistic OHLC data generation
- Continuous price updates

### Chart Rendering
- **Python**: Custom Pygame rendering for candlestick and line charts
- **Web**: Chart.js library for professional chart visualization
- Automatic scaling based on price range
- Professional color scheme (green/red for up/down)

### Performance
- **Python**: 60 FPS smooth rendering
- **Web**: Optimized for 60 FPS with efficient DOM updates
- Efficient data management (keeps last 100 data points)
- Responsive UI with real-time updates

## 📋 Requirements

### Python Version
- Python 3.7+
- Pygame 2.0+
- NumPy (for calculations)

### Web Version
- Modern web browser (Chrome, Firefox, Safari, Edge)
- No additional dependencies required

## 🔮 Future Enhancements

- **Technical Indicators**: Moving averages, RSI, MACD, Bollinger Bands
- **News Events**: Market-moving news affecting stock prices
- **More Realistic Simulation**: Market hours, after-hours trading
- **Save/Load Functionality**: Persistent portfolio and settings
- **Multiplayer Trading**: Real-time trading with other users
- **Advanced Charting**: Drawing tools, Fibonacci retracements
- **Mobile App**: Native mobile applications
- **Real Market Data**: Integration with live market feeds

## 🎨 Design Philosophy

Both versions feature:
- **Professional Aesthetics**: Clean, modern interface inspired by real trading platforms
- **Intuitive Navigation**: Easy-to-use controls and clear information hierarchy
- **Responsive Design**: Adapts to different screen sizes and orientations
- **Accessibility**: High contrast modes and keyboard navigation
- **Performance**: Optimized for smooth, real-time updates

## 📄 License

This project is open source and available under the MIT License.

---

**Choose Your Platform:**
- 🐍 **Python Version**: For desktop users who want a full-screen trading experience
- 🌐 **Web Version**: For cross-platform accessibility and easy sharing

**Happy Trading! 📈💰** 
