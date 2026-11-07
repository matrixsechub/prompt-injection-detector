# Claude Code GitHub Actions — inactive, approval-gated preparation

**Status: TEMPLATE / HOLD. No action is installed or activated.**

Scope: `matrixsechub/prompt-injection-detector`, with initial target PR #3. This preparation is on branch `spec/claude-manual-review-gate`, separated from PR #3's code repairs.

## Why the review-only Base Action?

Anthropic documents `anthropics/claude-code-base-action@beta` and the `claude_code_oauth_token` input for Claude Pro/Max setup tokens. The Base Action does not need write access to GitHub to analyze a supplied PR diff. The normal full `claude-code-action@v1` + GitHub App is more suitable for automatic PR conversations and code edits; those powers are unnecessary here.

Sources (verify again before activation):
- https://github.com/anthropics/claude-code-action/blob/main/base-action/README.md
- https://github.com/anthropics/claude-code-action/blob/main/docs/setup.md
- https://github.com/anthropics/claude-code-action/blob/main/docs/security.md

## Activation checklist — requires separate Operator approval

1. Operator reviews this template and confirms no unexpected permissions, triggers, billing risk or third-party dependencies.
2. On an authorized local machine, sign in to Claude Code with the operator's **Pro/Max** account; run `claude setup-token` according to current Anthropic instructions. NEVER paste the token into ChatGPT, ClickUp, a commit or a PR.
3. Operator adds token to GitHub repository **Settings → Secrets and variables → Actions → New repository secret** named `CLAUDE_CODE_OAUTH_TOKEN`. Do not add `ANTHROPIC_API_KEY` or enable Console extra/API spending unless separately authorized.
4. Operator checks Claude subscription **usage credits / extra usage** settings and disables pay-as-you-go overages if unwilling to incur additional charges. GitHub Actions runner usage may be separately metered. `--max-turns` and `timeout-minutes` limit work, NOT dollars, and are not a guaranteed spending cap.
5. Base Action is pinned to immutable commit `1ba86a1578bc4350db6af753284bc09734ca18bf` (verified to support `prompt_file`, `claude_args`, and `claude_code_oauth_token`). Independently audit the pinned action and its transitive downloads before activation. Re-review upstream interface before any later upgrade.
6. Operator approves creating a **separate activation PR** that copies `manual-pr-review.yml.template` to `.github/workflows/claude-pr-review.yml`. Merge to `main` only by the Operator. This is the activation step and is NOT authorized by preparing this template.
7. No run occurs automatically. For each paid/usage-consuming run, Operator explicitly opens GitHub Actions → Claude Code — Operator-Approved Manual PR Review → Run workflow, enters PR number, complete exact head SHA, and selects `APPROVE_ONE_REVIEW`. Default is `DENY`.
8. Record the resulting Claude verdict, reviewed exact SHA, CI link, cost/usage observation and operator disposition in ClickUp. No auto-merge.

## Initial target

- PR: https://github.com/matrixsechub/prompt-injection-detector/pull/3
- Head as verified on 2026-11-06 America/Denver: `18f6b097ab39a3bc871859479122385d3b3dcbed`.
- Successful CI for exact head: https://github.com/matrixsechub/prompt-injection-detector/actions/runs/42328897746 (11 pytest tests passed).
- PR #3 is a **draft**, unmerged; ensure exact commit has not changed before approving any run.

## Execution safeguards in the template

- Only `workflow_dispatch` can trigger; there is no PR, push, comment, or schedule trigger.
- Manual dispatch restricted to GitHub actor `matrixsechub`, plus explicit one-run approval input.
- Every run verifies that the PR is open, targets `main`, originates from the same repository, and exactly matches the approved full head SHA. It refuses to run Claude if a successful `ci` check is not found for that SHA.
- Diff size cap 100 KB; GH CLI gets PR diff as text. Does **not checkout the PR's potentially untrusted head**.
- Only `contents: read`, `pull-requests: read`, `actions: read`; no `write` or `id-token` permissions. Claude allowed tools: `Read,Glob,Grep`. No shell/edit tools.
- No GitHub issue/PR comments are posted; result is reviewed through the GitHub Actions run log. Do not enable full raw output debugging; public repository logs may be public.
- `timeout-minutes: 12` and `--max-turns 8` are bounded work controls, but are **not a financial hard cap**.

## Known constraints / unresolved before activation

- A `claude setup-token` credential is still a sensitive long-lived secret. The operator owns its local creation, storage, rotation, and revocation.
- Pro/Max subscription usage limits and overage arrangements must be checked in the operator's Anthropic account. The preparer cannot inspect them.
- GitHub's `claude-code-base-action@beta` upstream tag is mutable; pinning is recommended before activation.
- Base Action is a thin wrapper and does not enforce security boundaries independently; this workflow supplies the manual authorization, same-repo/sha checks and minimal permissions.
- A GitHub Action review is **not** the managed Team/Enterprise Claude Code Review product. A model's PASS verdict is evidence for operator assessment, not a GitHub approval or merge permission.
- The current GitHub workflow folder has only `ci.yml`. This spec does not alter it.
- Pinned Base Action source: https://github.com/anthropics/claude-code-base-action/tree/1ba86a1578bc4350db6af753284bc09734ca18bf. It is pinned for integrity; a pin is not a security audit.

## MSH-OPS governance

Follow https://app.clickup.com/9017787639/docs/8cr117q-3237. PR/CI/Claude findings are reviewed first; only the operator may merge, deploy, or expand capabilities. Keep sensitive data out of GitHub Actions logs.
