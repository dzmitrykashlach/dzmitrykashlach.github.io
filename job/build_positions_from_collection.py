#!/usr/bin/env python3
"""Analyst + writer: read job/collected_raw.json, write positions.md, skills.md, channel-checkpoints.json section data."""
from __future__ import annotations

import importlib.util
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COLLECTED = ROOT / "collected_raw.json"
CHANNELS_MD = ROOT / "job-channels.md"


def _load_parse_channel_urls():
    spec = importlib.util.spec_from_file_location(
        "collect_telegram_posts", ROOT / "collect_telegram_posts.py"
    )
    mod = importlib.util.module_from_spec(spec)
    loader = spec.loader
    assert loader is not None
    loader.exec_module(mod)
    return mod.parse_channel_urls


def channel_urls_from_markdown() -> list[str]:
    fn = _load_parse_channel_urls()
    return fn(CHANNELS_MD.read_text(encoding="utf-8"))


def _pid(url: str) -> int:
    m = re.search(r"/(\d+)(?:\?.*)?$", url)
    return int(m.group(1)) if m else 0


def analyst_accept(snippet: str) -> bool:
    t = snippet.lower()
    if not re.search(r"\b(java|kotlin)\b", t):
        return False
    if any(
        n in t
        for n in (
            "вебинар",
            "webinar",
            "tell me about yourself",
            "подборка лучших вакансий",
            "лучших вакансий за неделю",
            "фронтенд с нуля",
            "бесплатное обучение",
            "affiliate manager",
            "i can help with incidents",
            "looking for java developer role as a fresher",
            "новое резюме:",
            "как опубликовать вакансию",
            "айтишники, обратите внимание",
            "еженедельная подборка",
            "преподаватель",
            "онлайн-курса",
        )
    ):
        return False
    head = t[:240]
    if re.search(
        r"\b(senior frontend|front-?end engineer|react developer|vue\.js|angular developer)\b",
        head,
    ) and not re.search(r"(java|kotlin|jvm|spring)", head):
        return False
    if "требуются парни и девушки" in t:
        return False

    if "elixir" in t[:900] and not re.search(
        r"(spring boot|spring cloud|java developer|kotlin developer|java engineer|kotlin engineer|java-разработчик|kotlin-разработчик)",
        t,
    ):
        return False

    # Non‑JVM stacks as primary role (conservative exclusion)
    if (
        re.search(
            r"(\bc#\b|\.net\b|dotnet|php\b|python разработчик|python developer|"
            r"golang|\bgo engineer\b|middle golang|\(go\)|flutter-разработчик)",
            t,
        )
        and not re.search(
            r"(java developer|kotlin developer|java engineer|kotlin engineer|"
            r"java[- ]разработчик|kotlin[- ]разработчик|spring boot|spring cloud)",
            t,
        )
    ):
        return False

    strong = (
        "java developer",
        "java engineer",
        "kotlin developer",
        "kotlin engineer",
        "java backend",
        "kotlin backend",
        "java-разработчик",
        "kotlin-разработчик",
        "разработчик java",
        "разработчик kotlin",
        "java разработчик",
        "kotlin разработчик",
        "backend java",
        "backend kotlin",
        "spring boot",
        "spring cloud",
        "spring framework",
    )
    if any(s in t for s in strong):
        return True
    if ("java" in t or "kotlin" in t) and re.search(
        r"(backend|бэкенд|бекенд|spring|микросервис|microservice|\bjvm\b)",
        t,
    ):
        return True
    return False


RESUME_TERMS_LOWER = {
    "java",
    "kotlin",
    "spring",
    "jvm",
    "postgresql",
    "postgres",
    "mysql",
    "mariadb",
    "kafka",
    "elasticsearch",
    "kubernetes",
    "k8s",
    "docker",
    "jenkins",
    "gitlab",
    "teamcity",
    "oauth",
    "keycloak",
    "aws",
    "ktor",
    "angular",
    "hibernate",
    "liquibase",
}

SKILL_PAT = re.compile(
    r"\b(quarkus|micronaut|redis|mongodb|cassandra|graphql|grpc|drools|camunda|"
    r"openshift|rancher|terraform|ansible|datadog|prometheus|vault|nomad)\b",
    re.I,
)


def main() -> None:
    if not COLLECTED.is_file():
        raise SystemExit(
            "Missing job/collected_raw.json — run: python3 job/collect_telegram_posts.py job/job-channels.md > job/collected_raw.json"
        )
    data = json.loads(COLLECTED.read_text(encoding="utf-8"))
    cands = [r for r in data if r.get("post_url") and not r.get("error")]
    accepted = [r for r in cands if analyst_accept(r.get("snippet", ""))]
    accepted.sort(key=lambda r: _pid(r["post_url"]), reverse=True)

    cap: dict[str, int] = defaultdict(int)
    picked: list[dict] = []
    for r in accepted:
        ch = r["channel_page"]
        if cap[ch] >= 3:
            continue
        cap[ch] += 1
        picked.append(r)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    sk_counter: Counter[str] = Counter()
    for r in picked:
        for m in SKILL_PAT.finditer(r["snippet"]):
            term = m.group(1).lower()
            if term not in RESUME_TERMS_LOWER:
                sk_counter[term] += 1

    seen_max: dict[str, int] = defaultdict(int)
    for r in cands:
        seen_max[r["channel_page"]] = max(seen_max[r["channel_page"]], _pid(r["post_url"]))

    match_best: dict[str, str] = {}
    for r in picked:
        ch = r["channel_page"]
        u = r["post_url"]
        if ch not in match_best or _pid(u) > _pid(match_best[ch]):
            match_best[ch] = u

    # --- positions.md ---
    lines = [
        "# Matching vacancies (Java/Kotlin backend)",
        "",
        "Baseline: [Resume (EN)](https://dzmitrykashlach.github.io/resume/en).",
        f"**Analyzed at (UTC):** {now}",
        "",
        "Selection is conservative: Java/Kotlin backend signals in the rendered post body; noise posts (webinars, digests, unrelated roles) removed. Up to three posts per source channel in this pass.",
        "",
        "## Matching posts",
        "",
        "| Role (from post) | Post | Source channel |",
        "|:-----------------|:-----|:---------------|",
    ]
    for r in sorted(picked, key=lambda x: (x["channel_page"], -_pid(x["post_url"]))):
        sn = re.sub(r"\s+", " ", r["snippet"].replace("|", "\\|"))[:120]
        if len(r["snippet"]) > 120:
            sn += "…"
        post = r["post_url"]
        post_md = f"[open]({post})"
        ch = r["channel_page"]
        lines.append(f"| {sn} | {post_md} | {ch} |")

    lines += [
        "",
        "---",
        "",
        "## Collector coverage",
        "",
        f"**Collected at (UTC):** {now}",
        "",
        f"Parsed {len(cands)} Telegram / RSS posts with concrete message links using `job/collect_telegram_posts.py` (writes `job/collected_raw.json`). "
        f"Analyst accepted {len(accepted)} posts before per-channel caps; **{len(picked)}** rows listed above.",
        "",
    ]

    (ROOT / "positions.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # --- skills.md ---
    skill_lines = [
        "# Skills",
        "",
        "Generated from accepted rows in `job/positions.md` (regex surface terms not clearly covered in the EN resume). "
        f"**Last analyzed:** {now}.",
        "",
        "| Skill | Mentions | Example posts |",
        "| --- | ---: | --- |",
    ]
    if not sk_counter:
        skill_lines.append("| — | 0 | — |")
    else:
        for term, n in sk_counter.most_common():
            ex = [
                r["post_url"]
                for r in picked
                if re.search(rf"\b{re.escape(term)}\b", r["snippet"], re.I)
            ][:3]
            links = ", ".join(ex) if ex else "—"
            skill_lines.append(f"| {term} | {n} | {links} |")

    (ROOT / "skills.md").write_text("\n".join(skill_lines) + "\n", encoding="utf-8")

    # --- merge checkpoints (live state; job-channels.md is URL list only) ---
    cp_path = ROOT / "channel-checkpoints.json"
    cp = json.loads(cp_path.read_text(encoding="utf-8"))
    cp["updated_at_utc"] = now
    chmap = cp.setdefault("channels", {})
    urls_md = channel_urls_from_markdown()
    empty = {
        "last_post_id": None,
        "last_post_hash": None,
        "last_relevant_url": None,
        "status": None,
        "checked_at_utc": None,
    }
    for url in urls_md:
        if url not in chmap:
            chmap[url] = {**empty}

    all_keys = sorted(set(chmap.keys()) | set(urls_md))
    for url in all_keys:
        if url not in seen_max and url not in match_best:
            continue
        st = chmap.setdefault(url, {**empty})
        max_id = seen_max.get(url)
        if max_id:
            st["last_post_id"] = str(max_id)
        st["checked_at_utc"] = now
        if url in match_best:
            st["status"] = "Match"
            st["last_relevant_url"] = match_best[url]
        elif url in seen_max:
            st["status"] = "No match"
            st["last_relevant_url"] = None

    cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(now)
    print("picked", len(picked), "accepted_before_cap", len(accepted))


if __name__ == "__main__":
    main()
