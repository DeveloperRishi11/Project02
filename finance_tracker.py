#!/usr/bin/env python3
"""
Interactive Web-based Finance Tracker
A small, self-contained web server that creates an interactive finance dashboard.

No external dependencies - uses only Python built-in libraries!
Run and open http://localhost:8000 in your browser.
"""

import http.server
import socketserver
import json
import urllib.parse
import os
from datetime import datetime, date
import threading
import webbrowser
import json

class FinanceData:
    def __init__(self):
        self.file_path = 'finance_data.json'
        self.transactions = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.transactions, f)
    
    def add_transaction(self, amount, category, description, trans_type):
        transaction = {
            'id': len(self.transactions) + 1,
            'date': date.today().isoformat(),
            'amount': float(amount),
            'category': category,
            'description': description,
            'type': trans_type
        }
        self.transactions.append(transaction)
        self.save_data()
        return transaction
    
    def get_summary(self):
        income = sum(t['amount'] for t in self.transactions if t['type'] == 'income')
        expenses = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
        return {
            'income': income,
            'expenses': expenses,
            'balance': income - expenses,
            'total_transactions': len(self.transactions)
        }
    
    def get_categories_data(self):
        expense_categories = {}
        for t in self.transactions:
            if t['type'] == 'expense':
                cat = t['category']
                expense_categories[cat] = expense_categories.get(cat, 0) + t['amount']
        return expense_categories

# Global data instance
finance_data = FinanceData()

class InteractiveFinanceHandler(http.server.SimpleHTTPRequestHandler):
    
    def generate_html_page(self):
        """Generate the complete interactive HTML page"""
        summary = finance_data.get_summary()
        categories = finance_data.get_categories_data()
        recent_transactions = finance_data.transactions[-10:] if finance_data.transactions else []
        
        # Create category chart data
        chart_data = []
        colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
        for i, (cat, amount) in enumerate(categories.items()):
            chart_data.append({
                'label': cat,
                'value': amount,
                'color': colors[i % len(colors)]
            })
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <title>💰 Interactive Finance Tracker</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; padding: 20px; color: white;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ 
            background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; 
            backdrop-filter: blur(10px); text-align: center; transition: transform 0.3s;
        }}
        .stat-card:hover {{ transform: translateY(-5px); }}
        .stat-value {{ font-size: 2em; font-weight: bold; margin-bottom: 5px; }}
        .stat-label {{ opacity: 0.8; }}
        .positive {{ color: #4ade80; }}
        .negative {{ color: #f87171; }}
        
        .main-content {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
        
        .section {{ 
            background: rgba(255,255,255,0.1); padding: 25px; border-radius: 15px; 
            backdrop-filter: blur(10px); margin-bottom: 20px;
        }}
        .section h3 {{ margin-bottom: 20px; font-size: 1.3em; }}
        
        .form-group {{ margin-bottom: 15px; }}
        .form-group label {{ display: block; margin-bottom: 5px; font-weight: 500; }}
        .form-group input, .form-group select {{ 
            width: 100%; padding: 10px; border: none; border-radius: 8px; 
            background: rgba(255,255,255,0.2); color: white; font-size: 14px;
        }}
        .form-group input::placeholder {{ color: rgba(255,255,255,0.7); }}
        
        .btn-group {{ display: flex; gap: 10px; margin-top: 20px; }}
        .btn {{ 
            flex: 1; padding: 12px; border: none; border-radius: 8px; cursor: pointer; 
            font-weight: bold; font-size: 14px; transition: all 0.3s;
        }}
        .btn-income {{ background: #4ade80; color: white; }}
        .btn-expense {{ background: #f87171; color: white; }}
        .btn:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.3); }}
        
        .transaction-list {{ max-height: 300px; overflow-y: auto; }}
        .transaction-item {{ 
            display: flex; justify-content: space-between; align-items: center;
            padding: 10px; margin-bottom: 8px; background: rgba(255,255,255,0.1); 
            border-radius: 8px; font-size: 14px;
        }}
        .transaction-income {{ border-left: 4px solid #4ade80; }}
        .transaction-expense {{ border-left: 4px solid #f87171; }}
        
        .chart-container {{ position: relative; height: 300px; display: flex; align-items: center; justify-content: center; }}
        .pie-chart {{ width: 200px; height: 200px; }}
        .chart-legend {{ margin-left: 20px; }}
        .legend-item {{ display: flex; align-items: center; margin-bottom: 8px; font-size: 14px; }}
        .legend-color {{ width: 15px; height: 15px; border-radius: 3px; margin-right: 8px; }}
        
        .auto-refresh {{ text-align: center; margin-top: 20px; opacity: 0.7; font-size: 12px; }}
        
        @media (max-width: 768px) {{
            .main-content {{ grid-template-columns: 1fr; }}
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💰 Interactive Finance Tracker</h1>
            <p>Real-time financial dashboard • Auto-refreshing</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value positive">${summary['income']:.2f}</div>
                <div class="stat-label">💰 Total Income</div>
            </div>
            <div class="stat-card">
                <div class="stat-value negative">${summary['expenses']:.2f}</div>
                <div class="stat-label">💸 Total Expenses</div>
            </div>
            <div class="stat-card">
                <div class="stat-value {'positive' if summary['balance'] >= 0 else 'negative'}">${summary['balance']:.2f}</div>
                <div class="stat-label">📊 Net Balance</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary['total_transactions']}</div>
                <div class="stat-label">📋 Transactions</div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="left-panel">
                <div class="section">
                    <h3>➕ Add Transaction</h3>
                    <form id="transactionForm">
                        <div class="form-group">
                            <label>💵 Amount</label>
                            <input type="number" step="0.01" name="amount" placeholder="Enter amount" required>
                        </div>
                        <div class="form-group">
                            <label>📁 Category</label>
                            <select name="category" required>
                                <option value="">Select category</option>
                                <option value="Salary">💼 Salary</option>
                                <option value="Freelance">💻 Freelance</option>
                                <option value="Investment">📈 Investment</option>
                                <option value="Rent">🏠 Rent</option>
                                <option value="Groceries">🛒 Groceries</option>
                                <option value="Utilities">⚡ Utilities</option>
                                <option value="Transportation">🚗 Transportation</option>
                                <option value="Entertainment">🎬 Entertainment</option>
                                <option value="Healthcare">🏥 Healthcare</option>
                                <option value="Other">📌 Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>📝 Description</label>
                            <input type="text" name="description" placeholder="Enter description" required>
                        </div>
                        <div class="btn-group">
                            <button type="button" class="btn btn-income" onclick="addTransaction('income')">💰 Add Income</button>
                            <button type="button" class="btn btn-expense" onclick="addTransaction('expense')">💸 Add Expense</button>
                        </div>
                    </form>
                </div>
                
                <div class="section">
                    <h3>📊 Expense Categories</h3>
                    <div class="chart-container">'''
        
        if chart_data:
            # Generate SVG pie chart
            total = sum(item['value'] for item in chart_data)
            current_angle = 0
            
            html += '<svg class="pie-chart" viewBox="0 0 200 200">'
            
            for item in chart_data:
                angle = (item['value'] / total) * 360
                large_arc = 1 if angle > 180 else 0
                
                x1 = 100 + 80 * __import__('math').cos(__import__('math').radians(current_angle))
                y1 = 100 + 80 * __import__('math').sin(__import__('math').radians(current_angle))
                
                current_angle += angle
                
                x2 = 100 + 80 * __import__('math').cos(__import__('math').radians(current_angle))
                y2 = 100 + 80 * __import__('math').sin(__import__('math').radians(current_angle))
                
                html += f'''<path d="M 100 100 L {x1} {y1} A 80 80 0 {large_arc} 1 {x2} {y2} Z" 
                           fill="{item['color']}" stroke="white" stroke-width="2"/>'''
            
            html += '</svg><div class="chart-legend">'
            
            for item in chart_data:
                html += f'''<div class="legend-item">
                           <div class="legend-color" style="background: {item['color']}"></div>
                           <div>{item['label']}: ${item['value']:.2f}</div>
                           </div>'''
            
            html += '</div>'
        else:
            html += '<p style="text-align:center; opacity:0.7;">No expense data yet</p>'
        
        html += '''</div>
                </div>
            </div>
            
            <div class="right-panel">
                <div class="section">
                    <h3>📋 Recent Transactions</h3>
                    <div class="transaction-list">'''
        
        for transaction in reversed(recent_transactions):
            trans_class = f"transaction-{transaction['type']}"
            emoji = "💰" if transaction['type'] == 'income' else "💸"
            html += f'''<div class="transaction-item {trans_class}">
                       <div>
                           <div style="font-weight: bold;">{emoji} {transaction['category']}</div>
                           <div style="opacity: 0.8; font-size: 12px;">{transaction['description']}</div>
                       </div>
                       <div style="text-align: right;">
                           <div style="font-weight: bold;">${transaction['amount']:.2f}</div>
                           <div style="opacity: 0.7; font-size: 12px;">{transaction['date']}</div>
                       </div>
                       </div>'''
        
        if not recent_transactions:
            html += '<p style="text-align:center; opacity:0.7; padding:20px;">No transactions yet</p>'
        
        html += '''</div>
                </div>
            </div>
        </div>
        
        <div class="auto-refresh">
            🔄 Page auto-refreshes every 5 seconds • Last updated: <span id="timestamp"></span>
        </div>
    </div>
    
    <script>
        function addTransaction(type) {
            const form = document.getElementById('transactionForm');
            const formData = new FormData(form);
            formData.append('type', type);
            
            fetch('/add_transaction', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    form.reset();
                    setTimeout(() => location.reload(), 500);
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to add transaction');
            });
        }
        
        // Auto-refresh every 5 seconds
        setInterval(() => {
            location.reload();
        }, 5000);
        
        // Update timestamp
        document.getElementById('timestamp').textContent = new Date().toLocaleTimeString();
        
        // Add some interactive animations
        document.querySelectorAll('.stat-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-5px) scale(1.02)';
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0) scale(1)';
            });
        });
    </script>
</body>
</html>'''
        return html
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.generate_html_page().encode())
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/add_transaction':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse form data
                data = urllib.parse.parse_qs(post_data.decode('utf-8'))
                
                amount = float(data['amount'][0])
                category = data['category'][0]
                description = data['description'][0]
                trans_type = data['type'][0]
                
                # Add transaction
                transaction = finance_data.add_transaction(amount, category, description, trans_type)
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = {'success': True, 'transaction': transaction}
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                # Send error response
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = {'success': False, 'message': str(e)}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404)

def start_server():
    """Start the web server"""
    PORT = 8000
    
    # Add some sample data if none exists
    if not finance_data.transactions:
        sample_data = [
            (2500, 'Salary', 'Monthly salary', 'income'),
            (300, 'Freelance', 'Web project', 'income'),
            (800, 'Rent', 'Monthly rent', 'expense'),
            (150, 'Groceries', 'Food shopping', 'expense'),
            (60, 'Utilities', 'Electric bill', 'expense'),
        ]
        
        for amount, category, description, trans_type in sample_data:
            finance_data.add_transaction(amount, category, description, trans_type)
        
        print("✅ Added sample data to get you started!")
    
    with socketserver.TCPServer(("", PORT), InteractiveFinanceHandler) as httpd:
        print(f"🚀 Interactive Finance Tracker started!")
        print(f"📊 Open your browser and go to: http://localhost:{PORT}")
        print(f"💡 The page auto-refreshes every 5 seconds")
        print(f"⚡ Add transactions and watch the dashboard update in real-time!")
        print(f"🔥 Press Ctrl+C to stop the server")
        
        # Auto-open browser
        def open_browser():
            import time
            time.sleep(1)
            try:
                webbrowser.open(f'http://localhost:{PORT}')
            except:
                pass
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped! Your data has been saved.")

if __name__ == "__main__":
    start_server()
