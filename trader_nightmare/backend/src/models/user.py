
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class TradingPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_address = db.Column(db.String(42), nullable=False)
    token_symbol = db.Column(db.String(10), nullable=False)
    entry_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    pnl = db.Column(db.Float, default=0.0)
    pnl_percentage = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='open')  # open, closed, pending
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'token_address': self.token_address,
            'token_symbol': self.token_symbol,
            'entry_price': self.entry_price,
            'current_price': self.current_price,
            'quantity': self.quantity,
            'pnl': self.pnl,
            'pnl_percentage': self.pnl_percentage,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class TradeHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_address = db.Column(db.String(42), nullable=False)
    token_symbol = db.Column(db.String(10), nullable=False)
    trade_type = db.Column(db.String(10), nullable=False)  # buy, sell
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    pnl = db.Column(db.Float, default=0.0)
    fees = db.Column(db.Float, default=0.0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'token_address': self.token_address,
            'token_symbol': self.token_symbol,
            'trade_type': self.trade_type,
            'price': self.price,
            'quantity': self.quantity,
            'total_value': self.total_value,
            'pnl': self.pnl,
            'fees': self.fees,
            'timestamp': self.timestamp.isoformat()
        }
