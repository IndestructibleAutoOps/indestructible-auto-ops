@GL-governed
# XSS Prevention Pattern

## Category
Security Pattern

## Description
Detects and prevents Cross-Site Scripting (XSS) vulnerabilities by identifying unsafe HTML/JavaScript rendering and recommending proper output encoding.

## Detection Rules
1. **Unsanitized User Input**: Detect user input rendered without sanitization
2. **Dangerous DOM Methods**: Identify use of innerHTML, outerHTML with user data
3. **Missing Content Security Policy**: Find pages without CSP headers

## Prevention Strategies
1. **Output Encoding**: Encode all user-controlled data before rendering
2. **Content Security Policy**: Implement CSP headers
3. **Safe DOM Methods**: Use textContent instead of innerHTML
4. **Input Sanitization**: Sanitize HTML with libraries like DOMPurify

## Metrics
- **Precision**: 0.93
- **Recall**: 0.88
- **False Positive Rate**: < 7%