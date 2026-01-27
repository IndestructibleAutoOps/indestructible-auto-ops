# Code Review Checklist

Use this checklist during code reviews to ensure code quality and consistency.

## Functionality ✅
- [ ] Code performs the intended functionality
- [ ] Edge cases are handled appropriately
- [ ] Error handling is comprehensive
- [ ] No obvious bugs or logic errors
- [ ] Requirements are met

## Code Quality 🎨
- [ ] Code follows PEP 8 guidelines
- [ ] Imports are properly ordered (standard → third-party → local)
- [ ] Variable/function names are descriptive and follow conventions
- [ ] Code is readable and maintainable
- [ ] No dead code or commented-out code
- [ ] Consistent code style with rest of project

## Security 🔒
- [ ] No hardcoded credentials or sensitive data
- [ ] No use of eval() without proper justification and comment
- [ ] MD5 is only used for non-security purposes
- [ ] Input validation is present where needed
- [ ] SQL injection prevention (if using databases)
- [ ] XSS prevention (if handling user input)
- [ ] Sensitive data is properly logged (or not logged)
- [ ] Dependencies are up to date and secure

## Performance ⚡
- [ ] No obvious performance bottlenecks
- [ ] Appropriate use of data structures
- [ ] No unnecessary computations or loops
- [ ] Efficient algorithms used
- [ ] Proper caching where applicable
- [ ] Resource management (connections, files) is proper

## Documentation 📚
- [ ] Public functions/classes have docstrings
- [ ] Complex logic has explanatory comments
- [ ] Docstrings follow Google style guide
- [ ] README is updated if needed
- [ ] API documentation is accurate
- [ ] Examples are provided for complex functions

## Testing 🧪
- [ ] Unit tests are included for new functionality
- [ ] Tests cover critical paths and edge cases
- [ ] Tests are passing locally
- [ ] Test names are descriptive
- [ ] Tests follow AAA pattern (Arrange, Act, Assert)
- [ ] Mocks are used appropriately
- [ ] Test coverage is acceptable

## Git Best Practices 📝
- [ ] Commit messages are clear and follow conventions
- [ ] Commits are atomic (one logical change per commit)
- [ ] No merge commits in feature branches
- [ ] Branch name follows convention
- [ ] Pull request description is complete
- [ ] Related issues are referenced

## Specific to Python 🐍
- [ ] Type hints are used for function signatures
- [ ] f-strings used instead of .format() or %
- [ ] Context managers used for resources (with statements)
- [ ] Exceptions are specific (not bare except)
- [ ] List/dict comprehensions used where appropriate
- [ ] __init__.py files are present in packages
- [ ] __all__ defined for module exports

## Specific to This Project 🏗️
- [ ] Follows machine-native-ops architecture guidelines
- [ ] Uses existing utility functions when possible
- [ ] Updates configuration files if needed
- [ ] Considered backward compatibility
- [ ] Documentation follows project style

## Review Process 🔄

### Before Submitting PR
1. Run pre-commit hooks: `pre-commit run --all-files`
2. Run tests: `pytest`
3. Run type checking: `mypy .`
4. Run security scan: `bandit -r .`
5. Self-review using this checklist

### During Review
1. **Constructive feedback**: Focus on code, not person
2. **Explain why**: Don't just say "change this"
3. **Suggest improvements**: Offer better alternatives
4. **Acknowledge good work**: Positive reinforcement helps
5. **Be specific**: Reference line numbers and code

### After Review
1. **Address all comments**: Either fix or discuss
2. **Update checklist**: Mark completed items
3. **Re-run checks**: Ensure fixes don't break anything
4. **Reply to comments**: Explain changes or reasoning

## Common Issues to Watch For 🚨

### Security
- Hardcoded passwords/keys
- SQL injection vulnerabilities
- eval() or exec() usage
- Unsafe deserialization
- Insufficient input validation

### Performance
- N+1 query problems
- Inefficient loops
- Memory leaks
- Blocking I/O in async code
- Unnecessary database queries

### Maintainability
- Magic numbers (use constants)
- Deeply nested code
- Long functions (>50 lines)
- Duplicate code (DRY principle)
- Poor naming

### Testing
- Missing edge case tests
- Brittle tests (testing implementation, not behavior)
- No test isolation
- Missing assertions

## Approval Criteria ✅

A PR can be approved when:
- ✅ All automated checks pass
- ✅ All functional requirements are met
- ✅ Code quality standards are followed
- ✅ Security concerns are addressed
- ✅ Tests are adequate and passing
- ✅ Documentation is complete
- ✅ Reviewer feedback is addressed

---

*Last updated: 2025-01-16*  
*Version: 1.0*