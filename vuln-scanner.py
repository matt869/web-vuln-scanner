#!/usr/bin/env python3
"""
Web Vulnerability Scanner CLI Tool
Detects: SQL injection, XSS, missing security headers, outdated libraries, and more.
Usage: python3 vuln-scanner.py <url> [options]
"""

import requests
import re
import json
import sys
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import argparse
from datetime import datetime

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

def print_section(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}➤ {text}{Colors.RESET}")
    print(f"{Colors.BLUE}{'-'*70}{Colors.RESET}")

def print_critical(title, description, recommendation):
    print(f"{Colors.RED}{Colors.BOLD}[CRITICAL]{Colors.RESET} {title}")
    print(f"  └─ {description}")
    print(f"  └─ {Colors.GREEN}✓ Fix: {recommendation}{Colors.RESET}\n")

def print_warning(title, description, recommendation):
    print(f"{Colors.YELLOW}{Colors.BOLD}[WARNING]{Colors.RESET} {title}")
    print(f"  └─ {description}")
    print(f"  └─ {Colors.GREEN}✓ Fix: {recommendation}{Colors.RESET}\n")

def print_info(title, description):
    print(f"{Colors.CYAN}{Colors.BOLD}[INFO]{Colors.RESET} {title}")
    print(f"  └─ {description}\n")

def print_score(score):
    if score >= 80:
        color = Colors.GREEN
        status = "GOOD"
    elif score >= 60:
        color = Colors.YELLOW
        status = "FAIR"
    elif score >= 40:
        color = Colors.YELLOW
        status = "POOR"
    else:
        color = Colors.RED
        status = "CRITICAL"
    
    print(f"\n{Colors.BOLD}Security Score: {color}{score}/100 ({status}){Colors.RESET}\n")

# SQL Injection patterns
SQL_PATTERNS = [
    r"(\d+\s*=\s*\d+)",
    r"('.*?'.*?or.*?'.*?')",
    r"(union.*?select)",
    r"(order\s+by\s+\d+)",
]

# XSS patterns
XSS_PATTERNS = [
    r"(\?.*?=.*?[<>\"'])",
    r"(javascript:)",
    r"(on\w+\s*=)",
]

# Outdated libraries
OUTDATED_LIBRARIES = {
    "jquery": ["1.", "2."],
    "bootstrap": ["2.", "3."],
    "angular": ["1."],
}

# Security headers
REQUIRED_HEADERS = {
    "strict-transport-security": "HSTS - Force HTTPS",
    "x-content-type-options": "X-Content-Type-Options - Prevent MIME sniffing",
    "x-frame-options": "X-Frame-Options - Clickjacking protection",
    "content-security-policy": "CSP - Prevent XSS",
    "x-xss-protection": "X-XSS-Protection - XSS filter",
}

class VulnerabilityScanner:
    def __init__(self, url, timeout=10, verbose=False):
        self.url = self.validate_url(url)
        self.timeout = timeout
        self.verbose = verbose
        self.results = {
            "url": self.url,
            "timestamp": datetime.now().isoformat(),
            "vulnerabilities": [],
            "warnings": [],
            "info": [],
            "score": 100,
        }

    def validate_url(self, url):
        """Ensure URL has protocol"""
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        parsed = urlparse(url)
        if not parsed.netloc:
            raise ValueError(f"Invalid URL: {url}")
        return url

    def scan(self):
        """Run full vulnerability scan"""
        print_header(f"Scanning {self.url}")
        
        try:
            headers = {"User-Agent": "VulnScanner/1.0 (Security Scanner)"}
            response = requests.get(self.url, headers=headers, timeout=self.timeout, allow_redirects=True)
            
            parsed = urlparse(self.url)
            
            # Check HTTP vs HTTPS
            if parsed.scheme == "http":
                self.results["vulnerabilities"].append({
                    "type": "CRITICAL",
                    "title": "Unencrypted Connection",
                    "description": "Site uses HTTP instead of HTTPS",
                    "recommendation": "Implement SSL/TLS certificate"
                })
                self.results["score"] -= 20
            
            # Check security headers
            self.check_security_headers(response.headers)
            
            # Analyze HTML content
            if "text/html" in response.headers.get("content-type", ""):
                soup = BeautifulSoup(response.content, "html.parser")
                
                self.check_xss(self.url, soup, response.text)
                self.check_outdated_libs(response.text)
                self.check_sql_injection(soup)
                self.check_info_disclosure(response.text)
                self.check_forms(soup)
            
            self.results["score"] = max(0, min(100, self.results["score"]))
            self.print_results()
            
        except requests.exceptions.Timeout:
            print(f"{Colors.RED}[ERROR] Request timed out{Colors.RESET}")
            sys.exit(1)
        except requests.exceptions.ConnectionError:
            print(f"{Colors.RED}[ERROR] Connection failed - host unreachable{Colors.RESET}")
            sys.exit(1)
        except Exception as e:
            print(f"{Colors.RED}[ERROR] {str(e)}{Colors.RESET}")
            sys.exit(1)

    def check_security_headers(self, headers):
        """Check for missing security headers"""
        headers_lower = {k.lower(): v for k, v in headers.items()}
        
        print_section("Security Headers Analysis")
        found_missing = False
        
        for header, description in REQUIRED_HEADERS.items():
            if header not in headers_lower:
                print_warning(
                    f"Missing: {description.split(' - ')[0]}",
                    description,
                    f"Add {header} header to HTTP responses"
                )
                self.results["warnings"].append({
                    "type": "HEADER_MISSING",
                    "title": description,
                })
                self.results["score"] -= 5
                found_missing = True
        
        if not found_missing:
            print(f"{Colors.GREEN}✓ All critical security headers present{Colors.RESET}\n")

    def check_xss(self, url, soup, content):
        """Check for XSS vulnerabilities"""
        print_section("XSS (Cross-Site Scripting) Analysis")
        issues_found = False
        
        forms = soup.find_all("form")
        if forms:
            print_warning(
                f"Found {len(forms)} Form(s)",
                "Forms detected - ensure input validation and output encoding",
                "Implement input validation and use parameterized queries"
            )
            self.results["warnings"].append({"type": "FORMS_DETECTED"})
            self.results["score"] -= 3
            issues_found = True
        
        if "eval(" in content or "innerHTML" in content:
            print_critical(
                "Dangerous Functions Found",
                "JavaScript uses eval() or direct innerHTML manipulation",
                "Avoid eval() and use textContent instead of innerHTML"
            )
            self.results["vulnerabilities"].append({"type": "DANGEROUS_FUNCTIONS"})
            self.results["score"] -= 10
            issues_found = True
        
        for pattern in XSS_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                print_warning(
                    "Potential XSS Vector Detected",
                    f"Detected suspicious pattern: {pattern}",
                    "Review code for proper input sanitization"
                )
                self.results["warnings"].append({"type": "XSS_PATTERN"})
                self.results["score"] -= 5
                issues_found = True
                break
        
        if not issues_found:
            print(f"{Colors.GREEN}✓ No obvious XSS vulnerabilities detected{Colors.RESET}\n")

    def check_sql_injection(self, soup):
        """Check for SQL injection vectors"""
        print_section("SQL Injection Analysis")
        issues_found = False
        
        inputs = soup.find_all("input")
        if inputs:
            print_warning(
                f"Found {len(inputs)} Input Field(s)",
                "Input fields detected - vulnerable to SQL injection if not protected",
                "Use prepared statements and parameterized queries"
            )
            self.results["warnings"].append({"type": "INPUTS_FOUND"})
            self.results["score"] -= 4
            issues_found = True
        
        forms = soup.find_all("form")
        for form in forms:
            method = form.get("method", "GET").upper()
            if method == "GET":
                print_info(
                    "Form with GET Method",
                    "Parameters passed in URL - ensure validation and use HTTPS"
                )
        
        if not issues_found:
            print(f"{Colors.GREEN}✓ No obvious SQL injection vectors found{Colors.RESET}\n")

    def check_outdated_libs(self, content):
        """Check for outdated libraries"""
        print_section("Outdated Libraries Analysis")
        issues_found = False
        
        for lib, old_versions in OUTDATED_LIBRARIES.items():
            for version in old_versions:
                pattern = rf"{lib}['\"]?\s*:\s*['\"]?{re.escape(version)}"
                if re.search(pattern, content, re.IGNORECASE):
                    print_warning(
                        f"Outdated Library: {lib}",
                        f"Using potentially outdated version of {lib}",
                        f"Update {lib} to the latest stable version"
                    )
                    self.results["warnings"].append({"type": f"OUTDATED_{lib.upper()}"})
                    self.results["score"] -= 3
                    issues_found = True
        
        if not issues_found:
            print(f"{Colors.GREEN}✓ No obvious outdated libraries detected{Colors.RESET}\n")

    def check_info_disclosure(self, content):
        """Check for information disclosure"""
        print_section("Information Disclosure Analysis")
        issues_found = False
        
        if re.search(r"(error|exception|stack trace)", content, re.IGNORECASE):
            print_warning(
                "Error Information Disclosure",
                "Page may display detailed error messages",
                "Disable detailed error messages in production"
            )
            self.results["warnings"].append({"type": "ERROR_DISCLOSURE"})
            self.results["score"] -= 2
            issues_found = True
        
        if re.search(r"(powered by|built with|version)", content, re.IGNORECASE):
            print_info(
                "Technology Stack Disclosure",
                "Page reveals technology/version information"
            )
            self.results["info"].append({"type": "TECH_DISCLOSURE"})
        
        if not issues_found and not self.results.get("info"):
            print(f"{Colors.GREEN}✓ No obvious information disclosure{Colors.RESET}\n")

    def check_forms(self, soup):
        """Check form security"""
        print_section("Form Security Analysis")
        forms = soup.find_all("form")
        
        if not forms:
            print(f"{Colors.GREEN}✓ No forms detected{Colors.RESET}\n")
            return
        
        for idx, form in enumerate(forms, 1):
            method = form.get("method", "GET").upper()
            action = form.get("action", "")
            
            print(f"Form #{idx}: {method} to {action if action else '(same page)'}")
            
            if method == "GET":
                print(f"  {Colors.YELLOW}⚠ Uses GET method - parameters visible in URL{Colors.RESET}")
            
            inputs = form.find_all("input")
            for inp in inputs:
                inp_type = inp.get("type", "text")
                inp_name = inp.get("name", "unknown")
                if inp_type == "password":
                    print(f"  {Colors.CYAN}ℹ Has password field: {inp_name}{Colors.RESET}")
        
        print()

    def print_results(self):
        """Print scan results"""
        print_header("Scan Results")
        
        # Print score
        print_score(self.results["score"])
        
        # Summary
        vuln_count = len(self.results["vulnerabilities"])
        warn_count = len(self.results["warnings"])
        info_count = len(self.results["info"])
        
        print(f"{Colors.BOLD}Summary:{Colors.RESET}")
        print(f"  {Colors.RED}Critical Issues: {vuln_count}{Colors.RESET}")
        print(f"  {Colors.YELLOW}Warnings: {warn_count}{Colors.RESET}")
        print(f"  {Colors.CYAN}Info: {info_count}{Colors.RESET}\n")
        
        if vuln_count == 0 and warn_count == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}No critical issues found!{Colors.RESET}\n")
        
        # Export option
        if self.verbose:
            print(f"{Colors.BOLD}Detailed Results:{Colors.RESET}")
            print(json.dumps(self.results, indent=2))

def main():
    parser = argparse.ArgumentParser(
        description='Web Vulnerability Scanner',
        epilog='Example: python3 vuln-scanner.py example.com -t 15'
    )
    parser.add_argument('url', help='Target URL to scan')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Request timeout in seconds (default: 10)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print detailed JSON results')
    parser.add_argument('-o', '--output', help='Save results to JSON file')
    
    args = parser.parse_args()
    
    try:
        scanner = VulnerabilityScanner(args.url, timeout=args.timeout, verbose=args.verbose)
        scanner.scan()
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(scanner.results, f, indent=2)
            print(f"\n{Colors.GREEN}Results saved to {args.output}{Colors.RESET}\n")
    
    except ValueError as e:
        print(f"{Colors.RED}[ERROR] {str(e)}{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
