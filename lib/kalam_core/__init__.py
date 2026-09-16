"""kalam_core — shared, framework-level helpers for the Kalam manuscript agent.

Import from a bundled skill script without depending on the working directory::

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "lib"))
    from kalam_core import metadata, paths

Modules
-------
``paths``     depth-agnostic root/manuscript resolution
``metadata``  the single ``metadata.yaml`` / ``current_draft`` parser
``validate``  advisory metadata-schema validator (reports, never rewrites)

See ``resources/conventions/tooling.md``.
"""

__all__ = ["paths", "metadata", "validate"]
__version__ = "0.1.0"
