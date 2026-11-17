#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""장윤이 게임 아케이드 — 아침 자동 발행 파이프라인 (morning_publish.py)

왜 이 스크립트가 필요한가
------------------------------------------------------------------
기존 아침 자동화는 아래 순서로 움직였다.
    (1) 게임 폴더 작성 → (2) 게임 폴더만 먼저 커밋·푸시 → (3) games.json/menu.json 등록·7대 문서 동기화
    → (4) 다시 커밋·푸시
그래서 (2) 단계 푸시에서 CI 'Game Arcade Integrity Check'가 먼저 돌고,
  - 2449f7d(2026-11-18 07:43 KST): "미등록 게임 폴더 발견"(consonant-acorn-bakery, ten-make-starlight-train)
  - 92076f2(2026-11-17 13:03 KST): README 배지·상단 설명·히어로 링크·summary·github-about·index.html·
    portfolio-hero.svg·CHANGES.md 카운터 8곳이 옛 수치
로 실패했다. 즉 "폴더가 메타데이터보다 먼저 원격에 올라가는 순서"가 원인이다.

이 스크립트는 그 순서를 코드로 강제한다. 동기화와 검증이 끝나기 전에는
git add / commit / push 를 단 한 줄도 실행하지 않는다.

순서
------------------------------------------------------------------
  1) 사전 점검   : games.json에 등록되지 않은 게임 폴더, index.html 없는 폴더 확인
  2) 메타 동기화 : scripts/sync_metadata.py (7대 문서·카운터 원자적 동기화 + 한국어 지시문 검증)
  3) 유닛 테스트 : python -m unittest discover -s scripts -p 'test_*.py'
  4) 무결성 검증 : python scripts/verify_integrity.py (기본 --skip-live)
  5) 커밋 1회    : 게임 폴더 + 동기화된 메타데이터를 한 커밋으로 묶는다
  6) 푸시·확인   : main/master 동시 푸시 후 원격 SHA 일치 확인(선택: CI 완료까지 대기)

사용법
------------------------------------------------------------------
  python scripts/morning_publish.py --message "feat(morning): add <slug> ..."
  python scripts/morning_publish.py --message "..." --wait-ci        # 푸시 후 CI 완료까지 확인
  python scripts/morning_publish.py --dry-run                        # 검증만, 커밋·푸시 없음
  python scripts/morning_publish.py --message "..." --no-push        # 커밋까지만

종료 코드: 0 성공 / 1 검증·푸시 실패(커밋 전 중단 시 작업 트리는 그대로 보존)
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GAMES_JSON = REPO_ROOT / "games.json"
SCRIPTS = REPO_ROOT / "scripts"
SYNC_SCRIPT = SCRIPTS / "sync_metadata.py"
VERIFY_SCRIPT = SCRIPTS / "verify_integrity.py"
HOOKS_DIR = ".githooks"

sys.path.insert(0, str(SCRIPTS))
from verify_integrity import EXCLUDED_DIRS  # noqa: E402  (검증기와 동일한 제외 규칙 공유)


def line(char="=", n=62):
    print(char * n)


def step(title):
    print()
    line("-")
    print(f" {title}")
    line("-")


def run(cmd, cwd=REPO_ROOT, check=False):
    """명령 실행 후 (returncode, stdout+stderr) 반환."""
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0 and check:
        raise SystemExit(f"[FAIL] 명령 실패: {' '.join(cmd)}\n{out}")
    return proc.returncode, out


def git(*args):
    return run(["git", *args])


def fail(msg, detail=""):
    print()
    line("=")
    print(f" ❌ {msg}")
    line("=")
    if detail:
        print(detail)
    print("\n[중단] 커밋·푸시는 실행되지 않았습니다. 원격에는 아무것도 올라가지 않았습니다.")
    print("[다음] 위 문제를 고친 뒤 같은 명령을 다시 실행하세요:")
    print("       python scripts/morning_publish.py --message \"...\"")
    sys.exit(1)


def ensure_hooks_path():
    """pre-push 훅이 실제로 걸리도록 core.hooksPath를 .githooks로 맞춘다."""
    if not (REPO_ROOT / HOOKS_DIR / "pre-push").exists():
        return
    rc, current = git("config", "--local", "core.hooksPath")
    current = current.strip()
    if rc == 0 and current == HOOKS_DIR:
        return
    git("config", "--local", "core.hooksPath", HOOKS_DIR)
    print(f"[*] git 훅 경로 설정: core.hooksPath={HOOKS_DIR} (pre-push 무결성 가드 활성)")


def load_catalog():
    if not GAMES_JSON.exists():
        fail("games.json 파일이 없습니다.", str(GAMES_JSON))
    try:
        return json.loads(GAMES_JSON.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"games.json 파싱 실패: {exc}")


def check_registration(games):
    """[1] 게임 폴더 ↔ games.json 등록 정합 사전 점검."""
    step("1/6 사전 점검 — 게임 폴더 등록 상태")
    game_ids = {str(g.get("id", "")).strip() for g in games if g.get("id")}
    game_paths = {str(g.get("path", "")).replace("\\", "/") for g in games if g.get("path")}

    unregistered, no_index = [], []
    for entry in sorted(os.listdir(REPO_ROOT)):
        folder = REPO_ROOT / entry
        if not folder.is_dir() or entry in EXCLUDED_DIRS:
            continue
        if not (folder / "index.html").exists():
            no_index.append(entry)
        if entry not in game_ids and entry not in game_paths:
            unregistered.append(entry)

    if no_index:
        print(f"[WARN] index.html이 없는 루트 폴더: {', '.join(no_index)}")

    if unregistered:
        fail(
            "games.json에 등록되지 않은 게임 폴더가 있습니다: " + ", ".join(unregistered),
            "각 폴더를 games.json에 등록(id/title/title_ko/description/thumbnail/path, "
            "description은 한국어 지시문)하고 menu.json 항목까지 추가한 뒤 다시 실행하세요.\n"
            "이 상태로 커밋·푸시하면 CI 'Game Arcade Integrity Check'가 미등록 게임 폴더로 실패합니다.",
        )

    print(f"[OK] 루트 게임 폴더 {len(game_ids)}개 등록 정합 — 등록 누락 0건")


def check_sync():
    """[2] 7대 메타데이터 동기화 (+ 게임 설명 한국어 지시문 검증)."""
    step("2/6 메타데이터 동기화 — sync_metadata.py (7대 문서·카운터, 한국어 지시문)")
    rc, out = run([sys.executable, str(SYNC_SCRIPT)])
    print(out.rstrip())
    if rc != 0:
        fail("메타데이터 동기화 실패 — games.json 콘텐츠가 규약을 벗어났습니다.", out)
    print("[OK] games.json → menu.json/README/docs/index.html/portfolio-hero.svg/CHANGES.md 동기화 완료")


def check_tests():
    """[3] 유닛 테스트."""
    step("3/6 유닛 테스트 — scripts/test_*.py")
    rc, out = run([sys.executable, "-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py"])
    tail = "\n".join(out.strip().splitlines()[-6:])
    print(tail)
    if rc != 0:
        fail("유닛 테스트 실패", out)
    print("[OK] 유닛 테스트 통과")


def check_integrity(live=False):
    """[4] 무결성 검증."""
    step("4/6 무결성 검증 — verify_integrity.py")
    args = [sys.executable, str(VERIFY_SCRIPT)] + ([] if live else ["--skip-live"])
    rc, out = run(args)
    for row in out.splitlines():
        if row.startswith(("✅", "❌", " ⚠", " [-]")) or "결함" in row or "통과" in row:
            print(row)
    if rc != 0:
        fail("무결성 검증 실패", out)
    print("[OK] 무결성 검증 통과 — 이제 커밋해도 저장소 상태가 CI와 동일하게 유효합니다")


def pending_changes():
    git("add", "-A")
    rc, out = git("status", "--porcelain")
    return [r for r in out.splitlines() if r.strip()]


def commit(message):
    """[5] 검증 통과 후 1회 커밋."""
    step("5/6 커밋 — 게임 폴더 + 동기화된 메타데이터를 한 커밋으로")
    changes = pending_changes()
    if not changes:
        print("[*] 커밋할 변경이 없습니다(이미 동기화·검증된 상태).")
        return None
    print(f"[*] 변경 파일 {len(changes)}건:")
    for row in changes[:15]:
        print(f"    {row}")
    if len(changes) > 15:
        print(f"    ... 외 {len(changes) - 15}건")
    rc, out = git("commit", "-m", message)
    if rc != 0:
        fail("커밋 실패", out)
    _, sha = git("rev-parse", "HEAD")
    sha = sha.strip()
    print(f"[OK] 커밋 완료 {sha[:7]} — {message.splitlines()[0]}")
    return sha


def remote_shas():
    rc, out = git("ls-remote", "origin", "refs/heads/main", "refs/heads/master")
    if rc != 0:
        return {}
    shas = {}
    for row in out.splitlines():
        parts = row.split()
        if len(parts) == 2:
            shas[parts[1].replace("refs/heads/", "")] = parts[0]
    return shas


def push(branch):
    """[6] main/master 동시 푸시 후 원격 SHA 확인."""
    step("6/6 푸시 — main/master 동기화 및 원격 SHA 확인")
    _, head = git("rev-parse", "HEAD")
    head = head.strip()

    targets = ["main", "master"] if branch in ("main", "master") else [branch]
    for target in targets:
        rc, out = git("push", "origin", f"HEAD:{target}")
        if rc != 0:
            fail(f"{target} 푸시 실패", out)
        print(f"[OK] {target} 푸시 완료 → {head[:7]}")

    shas = remote_shas()
    for target in targets:
        remote = shas.get(target, "")
        state = "일치" if remote == head else f"불일치(원격 {remote[:7] or '없음'})"
        print(f"[*] origin/{target}: {remote[:7] or '없음'} — {state}")
        if remote != head:
            fail(f"origin/{target} SHA가 로컬 HEAD와 다릅니다.")
    return head


def wait_ci(head, timeout_s=900, interval_s=15):
    """선택: 푸시한 커밋의 CI 완료까지 대기."""
    step("추가 확인 — CI 'Game Arcade Integrity Check' 완료 대기")
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        rc, out = run([
            "gh", "run", "list", "-R", "shinjaehyun20/jangyoon-s-game",
            "--commit", head, "--json", "databaseId,name,status,conclusion,headBranch,url",
        ])
        if rc == 0 and out.strip():
            try:
                runs = json.loads(out)
            except json.JSONDecodeError:
                runs = []
            if runs and all(r.get("status") == "completed" for r in runs):
                for r in runs:
                    print(f"[*] {r['headBranch']} / {r['name']}: {str(r.get('conclusion')).upper()} — {r['url']}")
                if any(r.get("conclusion") != "success" for r in runs):
                    print("[WARN] 성공하지 않은 워크플로가 있습니다. 로그를 확인하세요: "
                          f"gh run view --log-failed -R shinjaehyun20/jangyoon-s-game")
                return runs
        time.sleep(interval_s)
    print("[WARN] 제한 시간 안에 CI가 끝나지 않았습니다. 나중에 확인: "
          "gh run list -R shinjaehyun20/jangyoon-s-game --limit 5")
    return None


def main():
    parser = argparse.ArgumentParser(description="장윤이 게임 아케이드 아침 발행 파이프라인 (동기화·검증 선행 강제)")
    parser.add_argument("--message", "-m", default="", help="커밋 메시지 (예: 'feat(morning): add <slug> ...')")
    parser.add_argument("--dry-run", action="store_true", help="검증까지만 수행하고 커밋·푸시하지 않음")
    parser.add_argument("--no-push", action="store_true", help="커밋까지만 수행하고 푸시하지 않음")
    parser.add_argument("--live", action="store_true", help="무결성 검증에 실서버 라이브 HTTP read-back 포함")
    parser.add_argument("--wait-ci", action="store_true", help="푸시 후 CI 완료까지 대기")
    parser.add_argument("--ci-timeout", type=int, default=900, help="CI 대기 최대 초 (기본 900)")
    args = parser.parse_args()

    line("=")
    print(" 🎮 장윤이 게임 아케이드 — 아침 발행 파이프라인 (morning_publish)")
    print(" 순서 강제: 등록 점검 → 메타 동기화 → 유닛테스트 → 무결성 검증 → 커밋 → 푸시")
    line("=")

    rc, branch = git("rev-parse", "--abbrev-ref", "HEAD")
    branch = branch.strip()
    if rc != 0 or not branch:
        fail("git 저장소가 아니거나 현재 브랜치를 확인할 수 없습니다.")
    print(f"[*] 저장소: {REPO_ROOT}")
    print(f"[*] 브랜치: {branch}")
    ensure_hooks_path()

    games = load_catalog()
    print(f"[*] games.json 등록 게임 수: {len(games)}개")

    check_registration(games)   # 1
    check_sync()                # 2
    check_tests()               # 3
    check_integrity(args.live)  # 4

    if args.dry_run:
        print()
        print("[DRY-RUN] 검증까지 모두 통과했습니다. 커밋·푸시는 수행하지 않았습니다.")
        print("[DRY-RUN] 실제 발행: python scripts/morning_publish.py --message \"...\"")
        return 0

    if not args.message.strip():
        fail("커밋 메시지가 필요합니다.", "예: --message \"feat(morning): add <slug1>, <slug2> with 7-point sync\"")

    sha = commit(args.message)   # 5
    if sha is None and not args.no_push:
        _ , head = git("rev-parse", "HEAD")
        sha = head.strip()

    if args.no_push:
        print("\n[완료] 커밋까지만 수행했습니다(푸시 생략).")
        return 0

    head = push(branch)          # 6
    if args.wait_ci:
        wait_ci(head, timeout_s=args.ci_timeout)

    print()
    line("=")
    print(f" ✅ 발행 완료 — {sha[:7]} (main/master)")
    line("=")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except KeyboardInterrupt:
        print("\n[중단] 사용자 중단")
        sys.exit(130)
