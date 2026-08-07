# Working While Traveling — Connectivity Troubleshooting

Quick-reference for getting Claude Code / Amazon internal tools working on
inflight wifi, hotel wifi, or anywhere off the normal VPN path. Written to be
readable on a phone if Claude Code itself is the thing that's broken.

**Root cause theory, established 2026-08-06 (Delta flight, AnyConnect VPN):**
Cisco AnyConnect uses split tunneling — general internet goes direct, only
corp-internal destinations (like `midway-auth.amazon.com`) route through the
VPN tunnel. High-latency/lossy satellite wifi is a known trigger for a
split-tunnel VPN to silently drop or misroute those internal-only routes
while still showing "Connected." Result: `mwinit` gets back a cert that
doesn't validate — an SSL error (curl 58/60) — even though the captive
portal was cleared and general browsing worked fine. The tell: **only the
Midway/VPN path breaks; regular HTTPS sites are unaffected.**

**⚠️ NOT YET CONFIRMED — `--aea` alone did not reproduce/fix the failure.**
Tested `mwinit --aea` on 2026-08-06 on stable ground wifi (VPN connected) —
worked fine. But mwinit's own output said *"--aea is now a default
behavior... will be removed in future versions"* — meaning plain `mwinit`
should behave identically to `--aea` on this version. That undercuts the
theory that the flag itself was the fix, since bare `mwinit` on the flight
should have hit the same AEA-style path and still failed. Two live
possibilities: (1) VPN itself — not just mwinit's auth mode — was
interfering with the connection at the network layer, or (2) something
about the ground-wifi test didn't actually reproduce the flight's failure
conditions (different network, no real proof either way). **Ground testing
success ≠ proof the flight problem is solved.** Next real test is another
flight — treat the checklist below as the best current guess, not a
verified fix.

## Pre-flight checklist (do this before losing signal / before boarding)

1. Connect to wifi, fully clear the captive portal (open a real page, confirm
   actual internet, not just "connected").
2. **Disconnect VPN first**, then run `mwinit` (or `mwinit --aea` — same
   thing on this version). The stronger candidate fix is removing VPN from
   the path entirely, not just changing mwinit's auth flag — if VPN's
   split-tunnel routing is what's actually broken, the auth mode running
   underneath doesn't matter.
   - Cert is shorter-lived off-VPN (~2 hours) — re-run mid-flight on longer
     legs.
3. Open Claude Code, send a test prompt before relying on it for real work.
4. **If it still fails with VPN disconnected too** — this rules out the VPN
   theory entirely and points at something else (see next section). Note
   what you tried and the exact error for next time; don't assume it's fixed
   until it's actually worked once on real inflight wifi mid-failure.

If it works: no VPN needed for the rest of the flight.

## If it still fails after `mwinit --aea`

Work through in order — each step narrows the cause:

1. **Check if the failure is Midway-specific or everything.** Try a normal
   HTTPS site in a browser. If that also fails/warns → it's the wifi
   provider doing broad TLS inspection (rare, but some inflight providers do
   this). If only Midway/Claude Code fails → continue below.
2. **Confirm the exact curl error, don't guess.** Run `mwinit -o -s` from a
   terminal and read the actual error text:
   - `(58)` or `(60)` "SSL certificate problem" → likely the VPN-routing
     problem above (unconfirmed — see banner at top). Disconnect VPN
     fully and retry before assuming it's the local OTP software cert;
     only chase the stale-cert angle (`~/.midway/client_cert.cfg`) if
     VPN-off doesn't help.
   - `(28)` "Timeout was reached" → the connection to
     `midway-auth.amazon.com` isn't reaching Amazon at all. Disconnect VPN
     fully, then retry (no VPN in the path).
   - `(35)` "SSL connect error" → SSL engine issue, often fixed by
     `eval "$(ssh-agent -s)"` or a simple laptop restart (documented,
     sounds silly, actually works).
3. **Verify the fix landed without printing credentials.** Don't run
   `ada credentials print` to "check" — it dumps live AWS keys to the
   screen. Instead run `aws sts get-caller-identity` — if that returns your
   identity/account, credentials are flowing correctly.
4. **Still stuck?** Fallback is `ssh.corp.amazon.com` (browser-based SSH via
   AEA) — flaky on mobile/tablet but works from a laptop as a last resort.
   Realistically: wait for landing/real wifi if this far down the list.

## Why NOT the things Gemini/generic AI suggests

- **"Route git/SSH over port 443"** — real trick, but it's for `github.com`
  specifically (`ssh.github.com:443`). Doesn't apply to Amazon's internal
  `git.amazon.com` (Midway-cert auth) or to Claude Code's Bedrock calls
  (already HTTPS/443, nothing to reroute).
- **"Rent a VPS, SSH in over 443, run Claude Code there"** — don't do this.
  Almost everything valuable (builder-mcp, Redshift/ada, SharePoint MCP,
  `git.amazon.com`) needs Midway auth + Amazon's network. Shipping your
  Midway cert or ada credentials to a third-party host to fake that access
  is a real security problem, not a workaround.
- **Generic "airline wifi blocks SSH/port 22" theory** — doesn't match what
  actually happens: Claude Code's core chat loop only needs HTTPS/443 to
  reach Bedrock. If it "started but no prompts worked," that's a broken
  Bedrock **credential**, not a blocked port. Diagnose the credential path
  (above), not the port.

## Quick mental model

Claude Code (this setup) → AWS Bedrock (HTTPS/443, public AWS endpoint) →
auth via `ada`/`credential_process` → underneath, Midway-signed cert →
Midway auth = the actual fragile link when traveling. VPN is not required
for Bedrock itself; VPN only matters for *other* internal tools (Redshift,
SharePoint, wikis) — and even those work off-VPN via `mwinit --aea` if
Midway is happy.
