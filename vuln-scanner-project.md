# 🔒 Web Vulnerability Scanner CLI

A powerful command-line tool to scan websites for security vulnerabilities, misconfigurations, and best practice violations.

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Scan a website
python3 vuln-scanner.py example.com

# 3. With options
python3 vuln-scanner.py https://github.com -t 15 -o results.json
```

## 📋 Features

✅ **SQL Injection Detection** - Finds vulnerable query parameters and form fields  
✅ **XSS (Cross-Site Scripting)** - Detects dangerous JavaScript patterns  
✅ **Missing Security Headers** - Checks HSTS, CSP, X-Frame-Options, etc.  
✅ **Outdated Libraries** - Warns about vulnerable jQuery, Bootstrap, Angular versions  
✅ **Information Disclosure** - Finds exposed error messages and version info  
✅ **SSL/TLS Validation** - Alerts on unencrypted HTTP connections  
✅ **Form Analysis** - Reviews form methods and security practices  
✅ **Color-Coded Output** - Easy-to-read terminal output with severity levels  

## 💻 Usage

### Basic Scan
```bash
python3 vuln-scanner.py example.com
```

### With Timeout
```bash
python3 vuln-scanner.py https://example.com -t 30
```

### Verbose (JSON Output)
```bash
python3 vuln-scanner.py example.com -v
```

### Save Results to File
```bash
python3 vuln-scanner.py example.com -o results.json
```

### Combine Options
```bash
python3 vuln-scanner.py https://github.com -t 15 -v -o scan.json
```

## 🚀 Command Options

```
positional arguments:
  url                   Target URL to scan (e.g., example.com or https://example.com)

optional arguments:
  -h, --help            Show help message
  -t, --timeout SECONDS Timeout for requests (default: 10)
  -v, --verbose         Print detailed JSON results
  -o, --output FILE     Save results to JSON file
```

## 📊 Output Example

```
======================================================================
                  Scanning https://example.com                        
======================================================================

Security Headers Analysis
----------------------------------------------------------------------
[WARNING] Missing: X-Content-Type-Options
  └─ X-Content-Type-Options - Prevent MIME sniffing
  └─ ✓ Fix: Add x-content-type-options header to HTTP responses

[WARNING] Missing: Strict-Transport-Security
  └─ HSTS - Force HTTPS
  └─ ✓ Fix: Add strict-transport-security header to HTTP responses

XSS (Cross-Site Scripting) Analysis
----------------------------------------------------------------------
✓ No obvious XSS vulnerabilities detected

SQL Injection Analysis
----------------------------------------------------------------------
[WARNING] Found 3 Input Field(s)
  └─ Input fields detected - vulnerable to SQL injection if not protected
  └─ ✓ Fix: Use prepared statements and parameterized queries

======================================================================
                        Scan Results
======================================================================

Security Score: 65/100 (FAIR)

Summary:
  Critical Issues: 0
  Warnings: 4
  Info: 2
```

## 🎯 Security Checks Explained

### 1. HTTP vs HTTPS
- **CRITICAL** if site uses unencrypted HTTP
- Switch to HTTPS immediately

### 2. Security Headers
Checks for these headers:
- `Strict-Transport-Security` - Force browser to use HTTPS
- `X-Content-Type-Options` - Prevent MIME-sniffing attacks
- `X-Frame-Options` - Protect against clickjacking
- `Content-Security-Policy` - Prevent XSS attacks
- `X-XSS-Protection` - Enable browser XSS filtering

### 3. SQL Injection
Detects:
- Forms without protection
- Query parameters with user input
- Vulnerable SQL patterns

**Fix:** Use prepared statements
```python
# ❌ VULNERABLE
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ SAFE
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### 4. XSS (Cross-Site Scripting)
Detects:
- eval() usage
- innerHTML with user data
- Event handlers
- Dangerous patterns

**Fix:** Sanitize input, use textContent
```javascript
// ❌ VULNERABLE
element.innerHTML = userInput;

// ✅ SAFE
element.textContent = userInput;
```

### 5. Outdated Libraries
Warns about:
- jQuery 1.x, 2.x
- Bootstrap 2.x, 3.x
- Angular 1.x

**Fix:** Update to latest versions

### 6. Information Disclosure
Detects:
- Stack traces in output
- Version numbers exposed
- Technology stack leaks
- Debugging information

**Fix:** Disable detailed errors in production

## 📈 Scoring System

| Score | Status | Action |
|-------|--------|--------|
| 80-100 | Good | Maintain current practices |
| 60-79 | Fair | Address medium priorities |
| 40-59 | Poor | Fix multiple issues |
| 0-39 | Critical | Urgent action needed |

## 🧪 Test Websites

Safe public websites to scan:
```bash
python3 vuln-scanner.py example.com
python3 vuln-scanner.py github.com
python3 vuln-scanner.py wikipedia.org
python3 vuln-scanner.py bbc.com
```

Intentional vulnerable apps (for learning):
```bash
python3 vuln-scanner.py dvwa.co.uk
python3 vuln-scanner.py webhacking.kr
```

## 🐛 Troubleshooting

**Connection Error:**
```
[ERROR] Connection failed - host unreachable
```
→ Check URL is correct, site might be blocking requests

**Timeout Error:**
```
[ERROR] Request timed out
```
→ Use `-t 30` to increase timeout

**Invalid URL:**
```
[ERROR] Invalid URL: ...
```
→ Use proper format: `example.com` or `https://example.com`

## ⚠️ Important Notes

**LEGAL NOTICE:**
- ✅ Scan sites you own
- ✅ Scan with explicit permission
- ✅ Use for learning and improvement
- ❌ Never scan without authorization
- ❌ Do not use for malicious purposes

**LIMITATIONS:**
- Performs static analysis only
- Does NOT execute JavaScript
- Cannot detect all vulnerabilities
- Should be used with other tools (OWASP ZAP, Burp Suite)

## 📚 Learn More

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection
- XSS: https://owasp.org/www-community/attacks/xss/
- Security Headers: https://securityheaders.com/

## 📁 Files

```
vuln-scanner.py       # Main CLI tool
requirements.txt      # Python dependencies
README.md            # This file
```

## 🔧 Installation

### Requirements
- Python 3.6+
- pip (Python package manager)

### Setup
```bash
# Clone or download files
# Install dependencies
pip install -r requirements.txt

# Make executable (Unix/Mac)
chmod +x vuln-scanner.py

# Run
python3 vuln-scanner.py example.com
```

## 📝 JSON Output Format

When using `-v` or `-o`, results are in JSON format:
```json
{
  "url": "https://example.com",
  "timestamp": "2024-03-02T14:30:00",
  "score": 65,
  "vulnerabilities": [
    {
      "type": "CRITICAL",
      "title": "...",
      "description": "...",
      "recommendation": "..."
    }
  ],
  "warnings": [...],
  "info": [...]
}
```

## 🎓 What You'll Learn

Using this scanner teaches:
- How websites are vulnerable
- Common attack vectors
- Security best practices
- Defensive coding patterns
- Security architecture

## 🙌 Tips for Best Results

1. **Test multiple sites** - See how different sites compare
2. **Fix issues systematically** - Start with Critical, then High, etc.
3. **Understand recommendations** - Don't just blindly apply fixes
4. **Use with other tools** - Combine with manual testing
5. **Stay updated** - Keep libraries and frameworks current

---

**Happy scanning! 🔐**

Made for cybersecurity professionals and learners
