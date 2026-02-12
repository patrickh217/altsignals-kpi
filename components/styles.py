"""
CSS Styles for the application
"""

APP_STYLES = """
    body {
        margin: 0;
        padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    .login-container {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .login-box {
        background: white;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        width: 100%;
        max-width: 400px;
    }
    .login-box h1 {
        text-align: center;
        color: #333;
        margin-bottom: 30px;
    }
    .form-group {
        margin-bottom: 20px;
    }
    .form-group label {
        display: block;
        margin-bottom: 5px;
        color: #555;
        font-weight: 500;
    }
    .form-group input {
        width: 100%;
        padding: 12px;
        border: 1px solid #ddd;
        border-radius: 5px;
        font-size: 14px;
        box-sizing: border-box;
    }
    .form-group input:focus {
        outline: none;
        border-color: #667eea;
    }
    .btn-login {
        width: 100%;
        padding: 12px;
        background: #667eea;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.3s;
    }
    .btn-login:hover {
        background: #5568d3;
    }
    .error-message {
        background: #fee;
        color: #c33;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        text-align: center;
    }
    .platform-container {
        min-height: 100vh;
        background: #f5f7fa;
        padding: 40px 20px;
    }
    .platform-header {
        text-align: center;
        margin-bottom: 40px;
    }
    .platform-header h1 {
        color: #333;
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    .platform-header p {
        color: #666;
        font-size: 1.1em;
    }
    .platform-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 25px;
        max-width: 1200px;
        margin: 0 auto;
    }
    .platform-box {
        background: white;
        padding: 40px 30px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: all 0.3s;
        text-decoration: none;
        color: inherit;
        display: block;
    }
    .platform-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    .platform-box.linkedin { border-top: 4px solid #0077b5; }
    .platform-box.system-health { border-top: 4px solid #28a745; }
    .platform-box.similarweb { border-top: 4px solid #FF6B35; }
    .platform-box.trends { border-top: 4px solid #4285F4; }
    .platform-box.capterra { border-top: 4px solid #FF6D42; }
    .platform-box.twitter { border-top: 4px solid #1DA1F2; }
    .platform-box.appstore { border-top: 4px solid #0D96F6; }
    .platform-box.amazon { border-top: 4px solid #FF9900; }
    .platform-box.crunchbase { border-top: 4px solid #0288D1; }
    .platform-box.meta { border-top: 4px solid #1877F2; }
    .platform-box.glassdoor { border-top: 4px solid #0CAA41; }
    .platform-box.producthunt { border-top: 4px solid #DA552F; }
    .platform-icon {
        font-size: 3em;
        margin-bottom: 15px;
    }
    .platform-name {
        font-size: 1.3em;
        font-weight: 600;
        color: #333;
    }
    .coming-soon-container {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f5f7fa;
    }
    .coming-soon-box {
        text-align: center;
        padding: 60px 40px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        max-width: 500px;
    }
    .coming-soon-box h1 {
        font-size: 3em;
        color: #667eea;
        margin-bottom: 20px;
    }
    .coming-soon-box p {
        font-size: 1.2em;
        color: #666;
        margin-bottom: 30px;
    }
    .btn-back {
        display: inline-block;
        padding: 12px 30px;
        background: #667eea;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        font-weight: 600;
        transition: background 0.3s;
    }
    .btn-back:hover {
        background: #5568d3;
    }
    .logout-btn {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 10px 20px;
        background: #dc3545;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        font-weight: 500;
        transition: background 0.3s;
    }
    .logout-btn:hover {
        background: #c82333;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px;
        flex: 1;
    }
    .metric-value {
        font-size: 2em;
        font-weight: bold;
        color: #007bff;
    }
    .metric-label {
        color: #6c757d;
        font-size: 0.9em;
        text-transform: uppercase;
    }
    .chart-container {
        margin-top: 30px;
        margin-bottom: 30px;
        padding: 20px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .grid-row {
        display: flex;
        flex-wrap: wrap;
        margin: 0 -10px;
    }
    .col-half {
        flex: 0 0 50%;
        max-width: 50%;
        padding: 0 10px;
        box-sizing: border-box;
    }
    .col-third {
        flex: 0 0 33.333%;
        max-width: 33.333%;
        padding: 0 10px;
        box-sizing: border-box;
    }
    @media (max-width: 768px) {
        .col-half, .col-third {
            flex: 0 0 100%;
            max-width: 100%;
        }
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }
    th, td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    th {
        background-color: #f8f9fa;
    }
    tr:hover {
        background-color: #f5f5f5;
    }
    .filter-buttons {
        display: flex;
        gap: 10px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    .filter-btn {
        padding: 10px 20px;
        border: 2px solid #007bff;
        background: white;
        color: #007bff;
        border-radius: 5px;
        cursor: pointer;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s;
    }
    .filter-btn:hover {
        background: #007bff;
        color: white;
    }
    .filter-btn.active {
        background: #007bff;
        color: white;
    }
    .version-badge {
        display: inline-block;
        background: #28a745;
        color: white;
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 0.85em;
        font-weight: bold;
        margin-left: 10px;
    }
    .header-info {
        color: #666;
        margin-bottom: 20px;
    }
    .health-check-section {
        background: #f0f8ff;
        border-left: 4px solid #17a2b8;
        padding: 15px;
        margin-top: 20px;
    }
    .health-check-title {
        color: #17a2b8;
        margin-bottom: 10px;
    }
    .status-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 0.85em;
        font-weight: 600;
    }
    .status-badge.healthy {
        background: #d4edda;
        color: #155724;
    }
    .status-badge.warning {
        background: #fff3cd;
        color: #856404;
    }
    .status-badge.error {
        background: #f8d7da;
        color: #721c24;
    }
    .system-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 20px;
        font-family: sans-serif;
    }
"""
