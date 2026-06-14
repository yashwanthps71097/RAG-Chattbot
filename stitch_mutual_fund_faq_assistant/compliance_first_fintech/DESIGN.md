---
name: Compliance-First Fintech
colors:
  surface: '#f8f9ff'
  surface-dim: '#d7dae2'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f3fc'
  surface-container: '#ebeef6'
  surface-container-high: '#e5e8f0'
  surface-container-highest: '#e0e2ea'
  on-surface: '#181c22'
  on-surface-variant: '#404752'
  inverse-surface: '#2d3137'
  inverse-on-surface: '#eef0f9'
  outline: '#707783'
  outline-variant: '#c0c7d4'
  surface-tint: '#0060a8'
  primary: '#005ea4'
  on-primary: '#ffffff'
  primary-container: '#0077ce'
  on-primary-container: '#fdfcff'
  inverse-primary: '#a2c9ff'
  secondary: '#006a62'
  on-secondary: '#ffffff'
  secondary-container: '#81f3e5'
  on-secondary-container: '#006f66'
  tertiary: '#8f4a00'
  on-tertiary: '#ffffff'
  tertiary-container: '#b35e00'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d3e4ff'
  primary-fixed-dim: '#a2c9ff'
  on-primary-fixed: '#001c38'
  on-primary-fixed-variant: '#004881'
  secondary-fixed: '#84f5e8'
  secondary-fixed-dim: '#66d9cc'
  on-secondary-fixed: '#00201d'
  on-secondary-fixed-variant: '#005049'
  tertiary-fixed: '#ffdcc4'
  tertiary-fixed-dim: '#ffb780'
  on-tertiary-fixed: '#2f1400'
  on-tertiary-fixed-variant: '#6f3800'
  background: '#f8f9ff'
  on-background: '#181c22'
  surface-variant: '#e0e2ea'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.01em
  code-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  max-width-desktop: 1200px
  gutter: 24px
  margin-mobile: 16px
---

## Brand & Style
The design system is engineered for a compliance-focused fintech environment where clarity and authority are paramount. The brand personality is fact-based, transparent, and neutral, avoiding promotional language in favor of structured information delivery. 

The aesthetic is **Modern Corporate Minimalism**, heavily influenced by the functional logic of Material Design but refined with a lighter, airier touch. It prioritizes high legibility and a sense of "digital safety" to ensure users feel the information provided is vetted and secure. The UI focuses on utility over ornamentation, using whitespace to reduce cognitive load during complex financial research.

## Colors
The palette is rooted in a professional blue-and-teal foundation. The primary blue represents stability and trust, while the secondary teal provides a subtle accent for success states and secondary actions. 

- **Primary & Secondary:** Use for main actions, active states, and branding elements.
- **Semantic Colors:** Success (Green) and Warning (Orange) are used strictly for compliance status and data verification alerts.
- **Surface & Background:** The background uses a cool-toned off-white (`#F8FAFC`) to separate content layers cleanly without the harshness of pure white. Text is set in a deep slate blue-gray to maintain high contrast while appearing more sophisticated than pure black.

## Typography
This design system utilizes **Inter** for its systematic, utilitarian nature. The typeface's tall x-height and clear letterforms ensure maximum readability for financial disclosures and dense FAQ content.

- **Headlines:** Use semi-bold weights with slightly tighter letter spacing for a modern, grounded feel.
- **Body Text:** The standard reading size is 16px. For longer compliance documents or detailed answers, 18px (`body-lg`) should be used to improve focus.
- **Labels:** Used for buttons, tags, and small metadata. These are always semi-bold to distinguish them from surrounding body text.

## Layout & Spacing
The layout follows a **Fluid Grid** model with a maximum content width of 1200px for desktop to prevent line lengths from becoming unreadable.

- **Desktop:** 12-column grid with 24px gutters.
- **Tablet:** 8-column grid with 24px gutters.
- **Mobile:** 4-column grid with 16px gutters and 16px side margins.

A strict 4px/8px baseline grid is used for all internal component spacing. Vertical rhythm should be generous, especially between unrelated content blocks (using `2xl` or `3xl` spacing) to maintain a minimalist, uncluttered appearance.

## Elevation & Depth
Elevation is expressed through **Tonal Layers** and subtle, functional shadows. 

1.  **Level 0 (Flat):** Used for the main page background.
2.  **Level 1 (Low Elevation):** Used for standard FAQ cards. These feature a 1px border in a light neutral tint (`#E2E8F0`) rather than a shadow, keeping the UI clean.
3.  **Level 2 (Active/Hover):** Used for interactive elements. Employs a soft, diffused shadow with a 10% opacity blue-gray tint to suggest lift.
4.  **Level 3 (Overlays):** Used for compliance alerts or source verification popovers. These use a slightly more pronounced shadow and a 4px backdrop blur on the layer beneath to focus the user’s attention on the critical information.

## Shapes
The design system uses a **Rounded** shape language to balance the "serious" nature of fintech with an approachable user experience.

- **Standard (8px / 0.5rem):** Buttons, input fields, and standard cards.
- **Large (16px / 1rem):** Main containers and featured result cards.
- **Extra Large (24px / 1.5rem):** Search bars and floating action buttons.

Avoid sharp 0px corners, as they can feel overly aggressive for a "helpful assistant" persona.

## Components

- **Conversational Search Bar:** A prominent, high-radius (rounded-xl) input field. It features an "active" blue border on focus and a subtle inner shadow to imply depth.
- **FAQ Cards:** Use a Level 1 elevation (border-based). On hover, they transition to Level 2 with a 2px primary-colored left border to indicate focus.
- **Citation Cards:** Small, recessed containers within answers. They use a slightly darker background (`#F1F5F9`) and a monospaced-style font for source numbers to emphasize data integrity.
- **Compliance Alerts:** Full-width banners or boxed cards using a light orange background with the Warning color for the icon. These must be visually distinct but not alarming.
- **Information Badges:** Small, pill-shaped tags used for "Verified," "SEC Filing," or "Mutual Fund." Use high-contrast text on low-saturation backgrounds (e.g., light teal background with dark teal text).
- **Source Verification Indicators:** A checkmark icon inside a small circle, placed next to citations. When clicked, it should trigger a Level 3 popover showing the raw source text or PDF link.
- **Buttons:** Primary buttons use the `#1E88E5` background with white text. Secondary buttons use a ghost style (border only) or a light teal tint.