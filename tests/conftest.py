import json
from datetime import datetime
from pathlib import Path

import pytest


class JSONTestReporter:
    def __init__(self):
        self.results = []
        self.start_time = datetime.utcnow().isoformat()

    def add_result(self, item, call, report):
        entry = {
            "test_name": item.name,
            "nodeid": item.nodeid,
            "file": str(item.fspath),
            "outcome": report.outcome,  # passed | failed | skipped
            "when": report.when,  # setup | call | teardown
            "duration": report.duration,
        }

        if report.failed:
            entry["error"] = {
                "type": call.excinfo.type.__name__ if call.excinfo else None,
                "message": str(call.excinfo.value) if call.excinfo else None,
                "traceback": (
                    report.longreprtext if hasattr(report, "longreprtext") else None
                ),
            }

        self.results.append(entry)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config._json_reporter = JSONTestReporter()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        reporter = item.session.config._json_reporter
        reporter.add_result(item, call, report)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    reporter = session.config._json_reporter

    output = {
        "started_at": reporter.start_time,
        "finished_at": datetime.utcnow().isoformat(),
        "exit_status": exitstatus,
        "summary": {
            "total": len(reporter.results),
            "passed": len([r for r in reporter.results if r["outcome"] == "passed"]),
            "failed": len([r for r in reporter.results if r["outcome"] == "failed"]),
            "skipped": len([r for r in reporter.results if r["outcome"] == "skipped"]),
        },
        "tests": reporter.results,
    }

    Path("pytest_results.json").write_text(
        json.dumps(output, indent=2), encoding="utf-8"
    )
