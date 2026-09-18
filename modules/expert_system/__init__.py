# modules.expert_system/__init__.py
# Public API per §7.7.

from modules.expert_system.rule_engine import diagnose

__all__ = ["diagnose"]
