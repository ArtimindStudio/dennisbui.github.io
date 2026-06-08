---
name: design-intelligence
description: High-fidelity visual design system, UI/UX audits, brand DNA mappings, and premium presentation slide packaging rules.
---

# Design Intelligence Skill

This skill governs the visual design, spatial layouts, brand DNA mappings, UI/UX audits, and slide presentation packaging used to create premium deliverables. It integrates the guidelines from industry-leading design systems (Stripe, Linear, Shopify), UI/UX Pro Max optimization frameworks, and strategic presentation layout patterns.

---

## 1. Brand DNA Mappings (Aesthetic Benchmarks)

### A. Stripe-Inspired: "The Financial Editorial"
*   **Colors**: Primary Electric Indigo (`#533afd`), Deep Navy Ink (`#0d253d`), cool grey secondary (`#64748d`), canvas-soft background (`#f6f9fc`).
*   **Typography**: Proprietary Sohne (fallback: **Inter** or **SF Pro Display**).
    *   *Display sizes*: 32px to 56px, rendered at thin weight (300) with aggressive negative letter-spacing (`-1.4px` to `-0.64px`) and `ss01` stylistic set enabled.
    *   *Data/Numerics*: Always render money, conversion rates, and transaction metrics using tabular figures (`font-feature-settings: "tnum"`) with `-0.4px` letter-spacing.
*   **Shape & Depth**: Pill buttons (`9999px` radius) with tight `8px 16px` padding. Subtle shadows (e.g., `rgba(0, 55, 112, 0.08) 0 8px 24px`) for card elevation.
*   **Hero Element**: Large, horizontally-washed atmospheric gradient mesh occupying the upper third of the page (cream/sherbet orange/lavender/indigo/ruby).

### B. Linear-Inspired: "The Dense Software Craft"
*   **Colors**: Deepest near-black canvas (`#010102`), four-step dark surface ladder (Surface-1: `#0f1011`, Surface-2: `#141516`, Surface-3: `#18191a`, Surface-4: `#191a1b`), light grey text (`#f7f8f8`), single accent lavender-blue (`#5e6ad2`).
*   **Typography**: Custom Display & Text sans (fallback: **Inter**). Display set at weight 500–600 with heavy negative tracking (`-3.0px` at 80px). Eyebrows use positive letter-spacing (`+0.4px`) in all-caps.
*   **Shape & Depth**: Cards use `{rounded.lg}` 12px corners with 1px hairline borders (`#23252a`). No drop shadows on dark surfaces; depth is carried entirely by the surface-level hierarchy.
*   **Visual Rhythm**: Marketing pages are structured around dark-framed product UI screenshots (`{rounded.xl}` 16px corners) with subtle white top-edge reflections.

### C. Shopify-Inspired: "The Cinematic Dual-Track"
*   **Colors**: Dual-canvas polarity. Marketing lives on pure black (`#000000`) with white-stroked outline buttons; transactional pages (pricing/signup) live on warm cream-mint (`#fbfbf5`) with solid black pills and aloe-green accents (`#c1fbd4`).
*   **Typography**: Neue Haas Grotesk Display (fallback: **Inter Display**) at thin 330 weight for headlines; Inter Variable at 420–550 for body and labels. Stylistic set `ss03` enabled globally.
*   **Shape & Depth**: Pill buttons (`9999px` radius) are non-negotiable. Light-mode cards use a soft, layered shadow halo (4 stacked tiny shadows with Y offsets from 1px to 8px at 10% black opacity) to look paper-like.
*   **Visual Rhythm**: Giant, thin-weight typography layered over full-bleed merchant photography, utilizing heavy vertical whitespace (128px+ gaps) on marketing heroes.

---

## 2. Presentation Slide Structures (Storyboarding & Layout)

### A. Duarte Sparkline Pattern (The Narrative Wave)
Structure the sequence of insights to fluctuate between the current negative state and the future positive state, building engagement toward a resolution:
```
What Is (Pain) ──> What Could Be (Hope) ──> What Is (Cost of Inaction) ──> What Could Be (Proposed Lift) ──> New Bliss (Goal Achieved)
```
*   *Position 1/3 & 2/3 Pattern Breaks*: Break layout consistency (e.g., using a full-bleed dark slide or a massive metric hero) to re-engage attention at these transition peaks.

### B. Standard Pitch/Audit Slide Flow
1.  **Personalized Cover**: High-end brand alignment showing the client's asset styled professionally.
2.  **The Core Problem**: Current conversion blocker or friction mapping.
3.  **Cost of Inaction**: Logical and financial impact if left unaddressed.
4.  **The Proposed Solution**: Visually clean wireframe or layout redesign.
5.  **Implementation Checklist**: Clear impact/effort matrix outlining immediate next steps.

### C. CSS Layout Patterns for Decks
*   **Two-Column Split**: Grid of two columns (`1fr 1fr`), gap of `48px`. Ideal for Before/After comparisons or screen-side breakdowns.
*   **Feature Grid**: Grid of three columns (`repeat(3, 1fr)`), gap of `24px` with accent-bar cards.
*   **Metrics Dashboard**: Grid of four columns (`repeat(4, 1fr)`), gap of `16px` with oversized numbers (`120px+`) and micro sparklines.

---

## 3. UI/UX Optimization Checklist (Quality Control)

*   **Accessibility (WCAG AA)**: Color contrast ratio of at least 4.5:1 for normal text (3:1 for large display text). Focus rings must be visible on all interactive elements. No emojis used as structural UI icons (always use SVG/Lucide).
*   **Touch & Interaction**: Minimum touch targets of `44x44px` on mobile. Tap states must provide feedback (opacity or color shift) within 100ms. Micro-interactions must complete in `150-300ms` with easing curves.
*   **Spacing Rhythm**: Adhere to an 8dp spacing scale for section layouts, margins, and card padding. Respect notch/gesture safe areas for fixed elements.
*   **Light/Dark Contrast**: Modal/drawer overlays must use a dark scrim of at least 40-60% black to preserve foreground legibility.

---

## 4. Project Blueprint: MUD\WTR Mobile PDP Audit

This spec defines the design system we will use to package the MUD\WTR deliverable:

*   **Aesthetic Style**: **Organic Biophilic Dark Mode** (Earthy, premium, sustainable feel combined with structured agency-grade presentation lines).
*   **Colors**:
    *   *Canvas/Background*: `#1e1e1a` (A deep, warm organic charcoal-mud background).
    *   *Primary Text*: `#f4f3ee` (A soft, warm off-white).
    *   *Accent/Highlights*: `#e26a36` (A warm energy orange representing their masala chai/spiced blends).
    *   *Secondary/CTA*: `#52796f` (A calm, earthy forest green representing wellness and natural ingredients).
    *   *Muted Borders*: `#33332f` (A subtle warm hairline).
*   **Typography**:
    *   *Headings*: **Lora** (Serif font; conveys organic trust, editorial quality, and calm).
    *   *Body/UI*: **Raleway** or **Inter** (Sans-serif; clean, readable, professional).
*   **Key Visual Effects**:
    *   Rounded corners of `12px` to `16px` on cards to mimic organic shapes.
    *   Subtle warm glassmorphism overlays (`backdrop-filter: blur(12px)`) with thin borders to isolate findings.
