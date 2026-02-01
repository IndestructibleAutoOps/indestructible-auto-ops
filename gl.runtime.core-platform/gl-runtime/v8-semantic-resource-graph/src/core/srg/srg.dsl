# GL Runtime SRG DSL (Semantic Resource Graph)
# Version: 1.0.0

# Basic Semantic Node
node Task {
    type: entity;
    attributes: { semantic_type: "execution", confidence: 0.92 };
}

node Input {
    type: entity;
    attributes: { semantic_type: "io", confidence: 0.88 };
}

# Semantic Edge
edge TaskRequiresInput {
    from: Task;
    to: Input;
    relation: depends_on;
    weight: 0.95;
}

# Inference Rule
infer missing_input {
    when: ["Task depends_on Input", "Input.confidence < 0.5"];
    then: "mark Task as invalid";
    falsifiable_by: ["inject_fake_input"];
}

# Consistency Rule
consistency semantic_integrity {
    requires: ["graph.connected == true"];
    forbids: ["contradiction.weight > 0.8"];
}
