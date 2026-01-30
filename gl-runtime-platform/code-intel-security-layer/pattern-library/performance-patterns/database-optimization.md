@GL-governed
# Database Query Optimization Pattern

## Category
Performance Pattern

## Description
Identifies inefficient database queries and suggests optimizations for improved performance.

## Detection Rules
1. **N+1 Query Problem**: Detect multiple queries that could be combined
2. **Missing Indexes**: Identify queries that would benefit from indexes
3. **Unnecessary Joins**: Find joins that can be eliminated
4. **Large Result Sets**: Detect queries returning excessive data

## Optimization Strategies
1. **Query Batching**: Combine multiple queries into single batched query
2. **Eager Loading**: Load related data in advance to avoid N+1 problem
3. **Index Creation**: Add appropriate database indexes
4. **Query Pagination**: Implement pagination for large result sets
5. **Caching**: Cache frequently accessed data

## Metrics
- **Precision**: 0.90
- **Recall**: 0.85
- **Performance Improvement**: 50-80% typical