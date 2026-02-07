#!/usr/bin/env python3
import argparse
import json
import os
import sys
import datetime

try:
    import yaml
except Exception as e:
    print("missing_dependency:pyyaml", file=sys.stderr)
    sys.exit(2)

def utc():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def load_yaml_or_json(path):
    with open(path, "r", encoding="utf-8") as f:
        if path.endswith(".json"):
            return json.load(f)
        return yaml.safe_load(f)

def validate_minimal(meta, doc):
    errors = []

    for k in ["$schema", "$id", "apiVersion", "kind", "metadata", "spec"]:
        if k not in doc:
            errors.append({"path": k, "error": "required"})
    if "metadata" in doc:
        md = doc["metadata"] or {}
        name = md.get("name")
        if not isinstance(name, str):
            errors.append({"path": "metadata.name", "error": "type"})
        else:
            import re
            if not re.fullmatch(r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?$", name):
                errors.append({"path": "metadata.name", "error": "pattern"})
            if len(name) > 63:
                errors.append({"path": "metadata.name", "error": "maxLength"})
        labels = md.get("labels", {}) or {}
        ann = md.get("annotations", {}) or {}
        import re
        kpat = re.compile(r"^[a-z0-9.-]+/[a-z0-9-]+$")
        for area, obj in [("metadata.labels", labels), ("metadata.annotations", ann)]:
            if not isinstance(obj, dict):
                errors.append({"path": area, "error": "type"})
                continue
            for kk, vv in obj.items():
                if not isinstance(kk, str) or not kpat.fullmatch(kk):
                    errors.append({"path": f"{area}.{kk}", "error": "pattern"})
                if not isinstance(vv, str):
                    errors.append({"path": f"{area}.{kk}", "error": "type"})
    if "spec" in doc:
        sp = doc["spec"] or {}
        rules = sp.get("rules", [])
        if rules is not None and not isinstance(rules, list):
            errors.append({"path": "spec.rules", "error": "type"})
        if isinstance(rules, list):
            import re
            rid = re.compile(r"^[A-Z]+-[0-9]{3}$")
            for i, r in enumerate(rules):
                if not isinstance(r, dict):
                    errors.append({"path": f"spec.rules[{i}]", "error": "type"})
                    continue
                for k in ["id", "severity", "description"]:
                    if k not in r:
                        errors.append({"path": f"spec.rules[{i}].{k}", "error": "required"})
                if "id" in r and isinstance(r["id"], str) and not rid.fullmatch(r["id"]):
                    errors.append({"path": f"spec.rules[{i}].id", "error": "pattern"})
                if "severity" in r and r["severity"] not in ["critical", "high", "medium", "low", "info"]:
                    errors.append({"path": f"spec.rules[{i}].severity", "error": "enum"})
    return errors

def walk_examples(root):
    files = []
    for base, _, names in os.walk(root):
        for n in names:
            if n.endswith(".yaml") or n.endswith(".yml") or n.endswith(".json"):
                files.append(os.path.join(base, n))
    return sorted(files)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", default="indestructibleautoops/meta_schema/v1/03_engineering_patch/schemas/meta-schema.v1.json")
    ap.add_argument("--examples", default="indestructibleautoops/meta_schema/v1/03_engineering_patch/examples")
    ap.add_argument("--write-evidence", action="store_true")
    args = ap.parse_args()

    meta = load_yaml_or_json(args.schema)
    ex_files = walk_examples(args.examples)

    report = {
        "time": utc(),
        "kind": "meta_schema_validation_report",
        "schema": args.schema,
        "examples_root": args.examples,
        "counts": {"examples": len(ex_files), "pass": 0, "fail": 0},
        "results": []
    }

    for p in ex_files:
        doc = load_yaml_or_json(p)
        errs = validate_minimal(meta, doc)
        ok = (len(errs) == 0)
        report["results"].append({"file": p, "ok": ok, "errors": errs})
        if ok:
            report["counts"]["pass"] += 1
        else:
            report["counts"]["fail"] += 1

    # Expect invalid_cases to fail
    invalid_failures = []
    for r in report["results"]:
        if "/invalid_cases/" in r["file"].replace("\\", "/"):
            if r["ok"]:
                invalid_failures.append(r["file"])
    report["invalid_cases"] = {
        "expected_fail": True,
        "unexpected_pass": invalid_failures
    }

    ok_all = (report["counts"]["fail"] >= 1 and len(invalid_failures) == 0)
    report["overall_ok"] = ok_all

    if args.write_evidence:
        outdir = ".evidence/meta_schema/reports"
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, "summary.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

    if not ok_all:
        print(json.dumps(report, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
