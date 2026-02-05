"""
Semantic AST Builder Tests
GL Level: GL50
Namespace: /tests/kernel/semantic
"""

import pytest
from governance.kernel.semantic.ast_builder import (
    SemanticAST,
    ASTNode,
    ASTNodeType
)
from governance.kernel.semantic.tokenizer import (
    SemanticTokenizer,
    TokenType
)


class TestSemanticAST:
    """語意 AST 測試"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.tokenizer = SemanticTokenizer()
        self.ast_builder = SemanticAST()
    
    def test_simple_action_ast(self):
        """測試簡單動作 AST"""
        text = "create user alice@example.com"
        tokens = self.tokenizer.tokenize(text)
        
        ast = self.ast_builder.build(tokens)
        
        assert ast is not None
        assert ast.root is not None
        
        # Root should be ACTION node
        assert ast.root.type == ASTNodeType.ACTION
        assert ast.root.value == "create"
    
    def test_ast_with_entity(self):
        """測試包含實體的 AST"""
        text = "create user alice@example.com"
        tokens = self.tokenizer.tokenize(text)
        
        ast = self.ast_builder.build(tokens)
        
        # Check if entity node exists in children
        entity_nodes = [n for n in ast.children if n.type == ASTNodeType.ENTITY]
        assert len(entity_nodes) >= 1
        assert entity_nodes[0].canonical == "user"
    
    def test_ast_serialization(self):
        """測試 AST 序列化"""
        text = "create user alice@example.com"
        tokens = self.tokenizer.tokenize(text)
        
        ast = self.ast_builder.build(tokens)
        ast_dict = ast.to_dict()
        
        assert "type" in ast_dict
        assert "value" in ast_dict
        assert "canonical" in ast_dict
        assert "children" in ast_dict
    
    def test_ast_deserialization(self):
        """測試 AST 反序列化"""
        text = "create user alice@example.com"
        tokens = self.tokenizer.tokenize(text)
        
        ast1 = self.ast_builder.build(tokens)
        ast_dict = ast1.to_dict()
        
        ast2 = SemanticAST.from_dict(ast_dict)
        
        assert ast1.root.canonical == ast2.root.canonical
        assert len(ast1.children) == len(ast2.children)
    
    def test_empty_tokens(self):
        """測試空 tokens"""
        tokens = []
        ast = self.ast_builder.build(tokens)
        
        assert ast is None or ast.root is None
    
    def test_complex_ast(self):
        """測試複雜 AST（多個節點）"""
        text = "create user alice@example.com replicas 3"
        tokens = self.tokenizer.tokenize(text)
        
        ast = self.ast_builder.build(tokens)
        
        # Should have ACTION, ENTITY, IDENTIFIER, VALUE nodes
        node_types = [n.type for n in ast.children]
        assert ASTNodeType.ENTITY in node_types
        assert ASTNodeType.VALUE in node_types


class TestASTNode:
    """ASTNode 測試"""
    
    def test_node_creation(self):
        """測試節點創建"""
        node = ASTNode(
            type=ASTNodeType.ACTION,
            value="create",
            canonical="create"
        )
        
        assert node.type == ASTNodeType.ACTION
        assert node.value == "create"
        assert node.canonical == "create"
        assert node.children == []
    
    def test_node_with_children(self):
        """測試帶子節點的節點"""
        parent = ASTNode(
            type=ASTNodeType.ACTION,
            value="create",
            canonical="create"
        )
        
        child1 = ASTNode(
            type=ASTNodeType.ENTITY,
            value="用戶",
            canonical="user"
        )
        
        child2 = ASTNode(
            type=ASTNodeType.IDENTIFIER,
            value="alice@example.com",
            canonical="alice@example.com"
        )
        
        parent.add_child(child1)
        parent.add_child(child2)
        
        assert len(parent.children) == 2
        assert parent.children[0].canonical == "user"
        assert parent.children[1].canonical == "alice@example.com"