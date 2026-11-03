# Patente B Pro - Mobile & UI Architectural Rules (2026)

All AI agents and developers modifying this codebase MUST strictly follow these 3 Golden Standards:

## 1. Apple HIG & Google Material 3 Touch Targets
- Every interactive element (buttons, tabs, inputs, icon toggles) MUST have a minimum tap target height of **44px** on touch and mobile viewports (`min-height: 44px; min-width: 44px;`).
- All interactive controls must provide immediate tactile feedback (`:active { transform: scale(0.94); }`).

## 2. Typography & Contrast (WCAG 2.1 AA Compliant)
- Contrast ratio between text and background MUST be at least **4.5:1** for standard text and **3:1** for large headings and icons.
- **Dark Mode:** Deep slate backgrounds (`#0B0F19` / `#111827`) paired with high-contrast text (`#F8FAFC`, `#E2E8F0`, `#94A3B8`). Zero muddy dark-gray text on dark backgrounds.
- **Light Mode:** Crisp surfaces (`#FFFFFF` / `#F8FAFC`) paired with deep ink text (`#0F172A`, `#1E293B`, `#475569`). Zero washed-out gray text.

## 3. Clean Architecture & Zero-Bloat
- **Zero Heavy External Frameworks:** Pure Vanilla JS and Modern CSS without runtime bloat.
- **Hardware Acceleration:** Key floating layers (such as `.patente-mobile-bottom-bar`, `.unified-portal-nav`, and `.tools-sheet-pane`) must use GPU acceleration (`transform: translateZ(0)`).
- **Responsive Layout:** Mobile viewports ($\le 768px$) must always prioritize core user actions and eliminate desktop marketing clutter.
