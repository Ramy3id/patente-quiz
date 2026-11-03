rules_content = """# ==============================================================================
# PATENTE B PRO / DEV-WORKSPACE — STRICT DEVELOPMENT & DEVOPS RULES
# Architecture: High-Performance Mobile Web, PWA, TWA, Hybrid Mobile Apps
# Enforcement Level: STRICT / PRODUCTION GRADE
# ==============================================================================

## 1. LIQUID RESPONSIVE ARCHITECTURE & SAFE AREAS (ZERO HARDCODED PIXELS)
- **Hardcoded Dimension Ban**: Strict prohibition against locking elements into rigid pixel heights or widths (e.g., `height: 800px;`, static fixed-height modal wrappers) that assume a specific screen model.
- **Dynamic Viewport Units**:
  - Always use Dynamic Viewport Height (`100dvh`) instead of static `100vh` to eliminate mobile browser URL-bar jump and gesture-bar overflow.
  - Utilize fluid typography and spacing via CSS `clamp(min, preferred, max)`, `rem`, and container queries (`cqw`, `cqh`).
- **Safe Area Insets**:
  - All fixed, sticky, header, navigation, and floating action elements MUST incorporate notch and gesture-bar insets:
    `padding-top: max(12px, env(safe-area-inset-top));`
    `padding-bottom: max(12px, env(safe-area-inset-bottom));`
    `padding-left: max(12px, env(safe-area-inset-left));`
    `padding-right: max(12px, env(safe-area-inset-right));`
- **Zero Horizontal Overflow Policy**: `overflow-x: hidden;` must be maintained at root layout boundaries; `scrollWidth <= innerWidth` is mandatory on all mobile viewports (320px to 430px).

---

## 2. TOUCH ERGONOMICS & INTERACTION TARGETS (MINIMUM 48x48dp)
- **Minimum Tap Surface**: Every interactive element (buttons, pills, icon buttons, radio cards, checkboxes, select triggers) MUST have a physical hit target of at least **48x48dp** (Android Material / W3C WCAG 2.5.5 Level AAA) or minimum **44x44pt** (Apple HIG).
- **Visual vs. Hit Target Separation**: If an element's visual design is compact (e.g., a 24px badge or 28px pill), its interactive hit box must be extended to >= 48px via pseudo-elements (`::before` / `::after` with `position: absolute; inset: -10px;`) or explicit touch padding.
- **Fast Touch Response**:
  - Enforce `touch-action: manipulation;` on all interactive controls to eliminate the 300ms tap delay on mobile WebKit/Blink.
  - Interactive states must define clear `:active` and `:hover` transitions with `transition-duration <= 150ms`.

---

## 3. ZERO-TOLERANCE SECURITY: SECRETS & CREDENTIALS
- **Plaintext Secrets Ban**: Absolute prohibition against committing plaintext API keys, JWT tokens, OAuth client secrets, Firebase private keys, database connection strings, or cloud storage credentials in source files.
- **Automated Detection Heuristics**: Immediate build failure and alert on any matching patterns:
  - AWS keys (`AKIA[0-9A-Z]{16}`)
  - Google / Firebase keys (`AIza[0-9A-Za-z\\-_]{35}`)
  - GitHub PATs (`ghp_[0-9A-Za-z]{36}`)
  - Generic private keys (`-----BEGIN PRIVATE KEY-----`)
  - Hardcoded password assignments (`password\\s*=\\s*['\\\"][^'\\\"]+['\\\"]`)
- **Environment Isolation**: All configuration secrets must be injected strictly via environment variables (`.env`, `process.env`, or encrypted CI/CD secret vaults).

---

## 4. PERFORMANCE, CLEANUP CONTRACTS & MEMORY LEAK PREVENTION
- **Listener Cleanup Contracts**:
  - Every `addEventListener` must have an explicit, symmetrical `removeEventListener` executed during unmount / destruction / view transition.
  - Long-running timers (`setInterval`, recursive `setTimeout`) must be tracked and cleared via `clearInterval` / `clearTimeout`.
  - MutationObservers, ResizeObservers, and IntersectionObservers must explicitly call `.disconnect()`.
- **Audio & Media Life-cycle**: Web Audio API contexts (`AudioContext`) must be suspended or `.close()`'d when the app transitions to the background; media elements must be paused and detuned.
- **Zero Dead Code & Tree Shaking**:
  - Remove unused variable declarations, commented-out dead blocks, and orphaned dependencies.
  - Avoid duplicate event registrations on dynamic re-renders (use idempotent attachment guards or single event delegation at container level).

---

## 5. GOOGLE PLAY STORE & MODERN ANDROID COMPLIANCE (TARGET SDK 34 / 35+)
- **Storage Architecture (Scoped Storage)**:
  - Do NOT request or rely on legacy `READ_EXTERNAL_STORAGE` or `WRITE_EXTERNAL_STORAGE` on Android 13+ (API 33+).
  - Use MediaStore API, Storage Access Framework (SAF), or app-specific internal cache directories (`context.getCacheDir()`).
- **Granular Permissions Protocol**:
  - Never request broad phone state, location, or background permissions unless directly core to active functionality.
  - Provide runtime rationale modals before requesting any `dangerous` permission.
- **PWA & Trusted Web Activity (TWA) Standards**:
  - Manifest (`manifest.json`) must provide: valid `id`, `start_url`, `scope`, standalone `display`, theme colors matching OS dark/light states, and high-res maskable icons (192x192 and 512x512).
  - Service Worker must handle offline fallback gracefully without displaying default browser dinosaur / connection failure screens.
- **Edge-to-Edge Layout Compliance**: Apps targeting Android 15 (API level 35) must enforce transparent system bars (`WindowCompat.setDecorFitsSystemWindows(window, false)`).
"""

import os

paths = [
    r"R:\Ramy\PATENTE_PRO_APP\.cursorrules",
    r"C:\Users\Ramy Fahmy\.gemini\antigravity\scratch\dev-workspace\.cursorrules"
]

for p in paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(rules_content.strip() + "\n")
    print(f"Created .cursorrules at: {p} (size: {os.path.getsize(p)} bytes)")

print("All .cursorrules files successfully created.")
