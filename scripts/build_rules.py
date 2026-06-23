from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def collect(data: Path, category: str) -> tuple[set[str], set[str], set[str]]:
    visited: set[str] = set()
    suffixes: set[str] = set()
    exact: set[str] = set()

    def visit(name: str) -> None:
        if name in visited:
            return
        visited.add(name)
        for raw in (data / name).read_text(encoding="utf-8").splitlines():
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            value = line.split()[0]
            if value.startswith("include:"):
                visit(value.removeprefix("include:"))
            elif value.startswith("full:"):
                exact.add(value.removeprefix("full:").lower())
            elif value.startswith("regexp:"):
                raise ValueError(f"Unsupported regexp rule: {value}")
            else:
                suffixes.add(value.lower())

    visit(category)
    return suffixes, exact, visited


def write(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=Path, help="domain-list-community data directory")
    parser.add_argument("--repo", type=Path, help="domain-list-community repository")
    args = parser.parse_args()

    suffixes, exact, categories = collect(args.data, "tencent")
    commit = "unknown"
    if args.repo:
        commit = subprocess.check_output(
            ["git", "-C", str(args.repo), "rev-parse", "HEAD"], text=True
        ).strip()

    total = len(suffixes) + len(exact)
    header = [
        "# NAME: Tencent",
        "# AUTHOR: DDcat2025",
        "# REPO: https://github.com/DDcat2025/tencent-shadowrocket-rules",
        "# SOURCE: https://github.com/v2fly/domain-list-community",
        f"# SOURCE-COMMIT: {commit}",
        f"# INCLUDED: {', '.join(sorted(categories))}",
        f"# DOMAIN-SUFFIX: {len(suffixes)}",
        f"# DOMAIN: {len(exact)}",
        f"# TOTAL: {total}",
    ]

    write(
        Path("rule/Shadowrocket/Tencent/Tencent.list"),
        header
        + [f"DOMAIN-SUFFIX,{domain}" for domain in sorted(suffixes)]
        + [f"DOMAIN,{domain}" for domain in sorted(exact)],
    )
    write(
        Path("rule/Shadowrocket/Tencent/Tencent_Domain.list"),
        header + [f".{domain}" for domain in sorted(suffixes | exact)],
    )
    write(
        Path("rule/Mihomo/Tencent/Tencent.yaml"),
        header
        + ["payload:"]
        + [f"  - DOMAIN-SUFFIX,{domain}" for domain in sorted(suffixes)]
        + [f"  - DOMAIN,{domain}" for domain in sorted(exact)],
    )
    write(Path("data/tencent-domains.txt"), header + sorted(suffixes | exact))


if __name__ == "__main__":
    main()

