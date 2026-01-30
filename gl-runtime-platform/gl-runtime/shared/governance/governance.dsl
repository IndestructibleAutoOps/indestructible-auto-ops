# GL Runtime Governance DSL (G-DSL)
# Version: 1.0.0

# Basic Governance Rule (V3)
rule basic_success_failure {
    applies_to: V3;
    requires: ["task.state in [SUCCESS, FAILURE]"];
    forbids: ["task.state == UNKNOWN"];
    falsifiable_by: ["inject_invalid_state"];
    evidence: ["state_logs"];
    enforce: "reject_task";
}

# Root Governance (V23)
rule anti_fabric {
    applies_to: V23;
    requires: ["decision.external_verification == true"];
    forbids: ["self_referential_validation"];
    falsifiable_by: ["inject_false_positive"];
    evidence: ["governance_logs", "verification_reports"];
    enforce: "invalidate_decision";
}

# Meta Governance (V24)
rule meta_falsification {
    applies_to: V24;
    requires: ["falsification_engine.falsifiable == true"];
    forbids: ["unfalsifiable_rules"];
    falsifiable_by: ["inject_meta_paradox"];
    evidence: ["meta_logs"];
    enforce: "reject_rule";
}
