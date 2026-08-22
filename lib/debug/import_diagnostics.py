import importlib.util
import sys
from pathlib import Path


class ImportDiagnostics:
    def __init__(self, report_file: str | None):
        self.report_file = Path(report_file) if report_file else None

    @property
    def enabled(self) -> bool:
        return self.report_file is not None

    def _write(self, message: str) -> None:
        if sys.stderr is not None:
            print(message, file=sys.stderr)
        if self.report_file:
            with self.report_file.open("a", encoding="utf-8") as report:
                print(message, file=report)

    def before_reorder(self) -> None:
        inkex_spec = importlib.util.find_spec("inkex")
        self._write("INKEX IMPORT DEBUG: before reorder")
        self._write(f"  sys.frozen={getattr(sys, 'frozen', False)}")
        self._write(f"  spec.origin={inkex_spec.origin if inkex_spec else None}")
        self._write(f"  sys.modules.loaded={'inkex' in sys.modules}")
        self._write("  sys.path:")
        for path in sys.path:
            self._write(f"    {path}")

    def after_reorder(self) -> None:
        import inkex

        self._write("INKEX IMPORT DEBUG: after reorder")
        self._write(f"  sys.frozen={getattr(sys, 'frozen', False)}")
        self._write(f"  inkex.__file__={inkex.__file__}")
        self._write(f"  sys.modules.loaded={'inkex' in sys.modules}")
        self._write("  sys.path:")
        for path in sys.path:
            self._write(f"    {path}")
