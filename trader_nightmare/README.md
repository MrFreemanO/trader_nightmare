
# Trader Nightmare 🚀

Professional cryptocurrency trading bot with React frontend and Python/Flask backend. Features advanced token analysis, automated trading strategies, and real-time monitoring dashboard.

## 🌟 Features

- **Advanced Token Analysis**: Multi-layered security and viability scoring
- **Automated Trading**: Smart entry/exit strategies with risk management
- **Real-time Dashboard**: Live monitoring of positions, P&L, and market data
- **Risk Management**: Stop-loss, take-profit, and position sizing controls
- **Security First**: Comprehensive token security analysis and honeypot detection
- **Scalable Architecture**: Dockerized microservices with CI/CD pipeline

## 🏗️ Architecture

```
trader_nightmare/
├── frontend/          # React + Vite frontend
│   ├── src/
│   │   ├── components/
│   │   └── utils/
│   ├── Dockerfile
│   └── package.json
├── backend/           # Python Flask API
│   ├── src/
│   │   ├── models/
│   │   ├── routes/
│   │   └── utils/
│   ├── Dockerfile
│   └── requirements.txt
├── .github/workflows/ # CI/CD pipelines
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Environment Setup

1. Copy environment variables:
```bash
cp .env.example .env
```

2. Edit `.env` with your API keys and configuration:
```bash
# Required API Keys
ALCHEMY_API_KEY=your-alchemy-key
QUICKNODE_API_KEY=your-quicknode-key
GOPLUS_API_KEY=your-goplus-key

# Security
SECRET_KEY=your-super-secret-key
```

### Docker Deployment (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
```

### Local Development

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 📊 Trading Features

### Token Analysis
- **Security Scanning**: Honeypot detection, contract analysis
- **Liquidity Analysis**: LP token locking, liquidity depth
- **Holder Analysis**: Distribution patterns, whale detection
- **Transaction Analysis**: Wash trading detection using Benford's Law

### Risk Management
- **Dynamic Position Sizing**: Based on volatility and market conditions
- **Stop Loss**: Fixed and trailing stop-loss mechanisms
- **Take Profit**: Multiple take-profit levels
- **Portfolio Limits**: Maximum concurrent positions and exposure

### Trading Strategies
- **Momentum Trading**: Trend-following algorithms
- **Mean Reversion**: Counter-trend strategies
- **Breakout Trading**: Support/resistance level breaks
- **Custom Signals**: Configurable trading signals

## 🔧 Configuration

### Trading Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `VIABILITY_THRESHOLD` | 70.0 | Minimum token viability score |
| `MAX_POSITION_SIZE` | 1000.0 | Maximum position size in USD |
| `SLIPPAGE_TOLERANCE` | 0.02 | Maximum acceptable slippage (2%) |
| `STOP_LOSS_PERCENTAGE` | 0.15 | Stop-loss threshold (15%) |
| `TAKE_PROFIT_PERCENTAGE` | 0.25 | Take-profit threshold (25%) |
| `MAX_CONCURRENT_POSITIONS` | 5 | Maximum open positions |

### API Endpoints

#### Trading API
- `GET /api/trading/status` - System status and health
- `GET /api/trading/positions` - Active positions
- `GET /api/trading/history` - Trade history
- `POST /api/trading/start` - Start trading bot
- `POST /api/trading/stop` - Stop trading bot

#### Analytics API
- `GET /api/analytics/performance` - Performance metrics
- `GET /api/analytics/signals` - Trading signals
- `GET /api/analytics/market` - Market data

## 🚀 Deployment

### Railway Deployment

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login and deploy:
```bash
railway login
railway up
```

### Render Deployment

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: trader-nightmare-backend
    env: docker
    dockerfilePath: ./backend/Dockerfile
    
  - type: web
    name: trader-nightmare-frontend
    env: docker
    dockerfilePath: ./frontend/Dockerfile
```

2. Connect your GitHub repository to Render

### VPS Deployment

```bash
# Clone repository
git clone https://github.com/yourusername/trader_nightmare.git
cd trader_nightmare

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Deploy with Docker Compose
docker-compose up -d --build
```

## 🔒 Security

- **Environment Variables**: All secrets stored in environment variables
- **CORS Protection**: Configurable CORS origins
- **Input Validation**: Comprehensive request validation
- **Rate Limiting**: API rate limiting and abuse prevention
- **Security Headers**: Comprehensive security headers
- **Container Security**: Non-root user, minimal attack surface

## 📈 Monitoring

### Health Checks
- Backend: `http://localhost:5000/health`
- Frontend: `http://localhost:3000/`

### Logging
- Application logs: `./backend/logs/`
- Trading logs: `./backend/data/`
- Error tracking: Integrated error handling

### Metrics
- Trading performance metrics
- System resource monitoring
- API response times
- Error rates and alerts

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest --cov=. --cov-report=html

# Frontend tests
cd frontend
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This trading bot is for educational and research purposes only. Cryptocurrency trading involves substantial risk of loss. Use at your own risk and never trade with money you cannot afford to lose.

## 🆘 Support

- 📧 Email: support@trader-nightmare.com
- 💬 Discord: [Join our community](https://discord.gg/trader-nightmare)
- 📖 Documentation: [Full documentation](https://docs.trader-nightmare.com)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/trader_nightmare/issues)

---

**Made with ❤️ by the Trader Nightmare Team**
