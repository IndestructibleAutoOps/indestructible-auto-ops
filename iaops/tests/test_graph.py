from indestructibleautoops.graph import DAG, dag_is_acyclic, topological_sort


def test_dag_acyclic_ok():
    dag = DAG.from_nodes(
        [
            {"id": "a", "kind": "step", "run": "x", "deps": []},
            {"id": "b", "kind": "step", "run": "x", "deps": ["a"]},
        ]
    )
    assert dag_is_acyclic(dag) is True


def test_dag_cycle_fail():
    dag = DAG.from_nodes(
        [
            {"id": "a", "kind": "step", "run": "x", "deps": ["b"]},
            {"id": "b", "kind": "step", "run": "x", "deps": ["a"]},
        ]
    )
    assert dag_is_acyclic(dag) is False


def test_topological_sort_linear():
    """Test topological sort on a linear dependency chain."""
    dag = DAG.from_nodes(
        [
            {"id": "a", "kind": "step", "run": "x", "deps": []},
            {"id": "b", "kind": "step", "run": "x", "deps": ["a"]},
            {"id": "c", "kind": "step", "run": "x", "deps": ["b"]},
        ]
    )
    result = topological_sort(dag)
    assert result == ["a", "b", "c"]


def test_topological_sort_diamond():
    """Test topological sort on a diamond-shaped DAG."""
    dag = DAG.from_nodes(
        [
            {"id": "a", "kind": "step", "run": "x", "deps": []},
            {"id": "b", "kind": "step", "run": "x", "deps": ["a"]},
            {"id": "c", "kind": "step", "run": "x", "deps": ["a"]},
            {"id": "d", "kind": "step", "run": "x", "deps": ["b", "c"]},
        ]
    )
    result = topological_sort(dag)
    # a must be first, d must be last, b and c can be in any order
    assert result[0] == "a"
    assert result[3] == "d"
    assert set(result[1:3]) == {"b", "c"}


def test_topological_sort_raises_on_cycle():
    """Test that topological sort raises on cyclic graphs."""
    dag = DAG.from_nodes(
        [
            {"id": "a", "kind": "step", "run": "x", "deps": ["b"]},
            {"id": "b", "kind": "step", "run": "x", "deps": ["a"]},
        ]
    )
    try:
        topological_sort(dag)
        raise AssertionError("Expected ValueError for cyclic graph")
    except ValueError as e:
        assert "cyclic" in str(e).lower()
