@GL-governed
# SOLID Principles Compliance Pattern

## Category
Architecture Pattern

## Description
Analyzes code for compliance with SOLID principles and suggests refactoring to improve code quality and maintainability.

## Detection Rules
1. **Single Responsibility Principle**: Identify classes/functions with multiple responsibilities
2. **Open/Closed Principle**: Find code that requires modification for extensions
3. **Liskov Substitution Principle**: Detect improper inheritance hierarchies
4. **Interface Segregation Principle**: Find bloated interfaces
5. **Dependency Inversion Principle**: Identify concrete dependencies instead of abstractions

## Refactoring Strategies
1. **Extract Class**: Split classes with multiple responsibilities
2. **Strategy Pattern**: Use strategy pattern for extensibility
3. **Interface Segregation**: Split large interfaces into smaller ones
4. **Dependency Injection**: Use dependency injection for loose coupling
5. **Abstract Factory**: Create abstractions for object creation

## Metrics
- **Precision**: 0.85
- **Recall**: 0.80
- **Maintainability Score**: +20% typical