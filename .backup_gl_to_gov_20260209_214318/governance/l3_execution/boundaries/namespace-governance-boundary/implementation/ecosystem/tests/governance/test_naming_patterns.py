#!/usr/bin/env python3
"""Naming pattern coverage for NG primary prefix with GL fallback."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "enforcers"))

from complete_naming_enforcer import NamingPatterns  # noqa: E402


def test_invalid_prefix_is_rejected():
    with pytest.raises(ValueError):
        NamingPatterns(primary_prefix="ng(", legacy_prefix=None)


def test_comment_tag_accepts_ng_and_gl():
    patterns = NamingPatterns()
    assert patterns.COMMENT_TAG.match("ng:dom:cap:tag")
    assert patterns.COMMENT_TAG.match("gl:dom:cap:tag")
    assert patterns.COMMENT_BLOCK.match("ng-block:dom:cap:tag_block")
    assert patterns.COMMENT_BLOCK.match("gov-block:dom:cap:tag_block")
    assert patterns.COMMENT_TAG.match("zz:dom:cap:tag") is None


def test_core_patterns_respect_prefixes():
    patterns = NamingPatterns()
    assert patterns.GL_ANNOTATION.match("@NG-layer")
    assert patterns.API_PATH.match("/ng/runtime/exec/task")
    assert patterns.API_PATH.match("/gl/runtime/exec/task")
    assert patterns.SERVICE.match("ng-runtime-exec-svc")
    assert patterns.SERVICE.match("gov-runtime-exec-svc")
    assert patterns.ENV_VAR.match("NG_RUNTIME_EXEC_KEY")
    assert patterns.ENV_VAR.match("GL_RUNTIME_EXEC_KEY")
    assert patterns.ENV_VAR.match("ZZ_RUNTIME_EXEC_KEY") is None


def test_k8s_label_key_accepts_ng_and_gl_domains():
    patterns = NamingPatterns()
    assert patterns.K8S_LABEL_KEY.match("ng.machinenativeops.io/component")
    assert patterns.K8S_LABEL_KEY.match("gl.machinenativeops.io/component")
    assert patterns.K8S_LABEL_KEY.match("app.kubernetes.io/name")
    assert patterns.K8S_LABEL_KEY.match("zz.machinenativeops.io/component") is None
