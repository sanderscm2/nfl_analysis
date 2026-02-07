# NFL Analytics Web Dashboard

Modern, AI-powered NFL analytics platform built with Next.js, React, and TypeScript.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd web
npm install
```

### 2. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📁 Project Structure

```
web/
├── app/                    # Next.js 14 App Router
│   ├── layout.tsx         # Root layout with header/nav/footer
│   ├── page.tsx           # Home page (League Overview)
│   └── globals.css        # Global styles + Tailwind
├── components/
│   └── layout/            # Layout components
│       ├── Header.tsx     # Top header with season selector
│       └── Navigation.tsx # Main navigation tabs
├── lib/                   # Utilities and types
├── package.json          # Dependencies
├── tsconfig.json         # TypeScript config
├── tailwind.config.ts    # Tailwind config (minimalist theme)
└── next.config.js        # Next.js config
```

## 🎨 Design System

Based on Dieter Rams minimalist principles:

**Colors:**
- Primary: `#1A1A1A` (Rich Black)
- Secondary: `#4A4A4A` (Charcoal)
- Accent: `#0066CC` (NFL Blue)
- Background: `#FAFAFA` (Off-white)
- Surface: `#FFFFFF` (Pure white)

**Typography:**
- System fonts (-apple-system, Roboto)
- Font weight: 300-400 (light/normal)
- Reduced letter spacing for modern feel

## 🛠️ Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Charts:** Recharts (to be added in Phase 2)
- **Deployment:** Vercel

## 📋 Current Status

**Phase 1: Foundation** ✅
- [x] Next.js project setup
- [x] Basic layout (header, nav, footer)
- [x] League Overview page (with mock data)
- [x] Minimalist styling with Tailwind
- [ ] Install dependencies and test locally
- [ ] Deploy to Vercel

## 🔜 Next Steps

1. **Phase 2:** Add Team Analysis and Player Stats pages
2. **Phase 3:** Integrate AI features (insights, analysis)
3. **Phase 4:** Build Custom Analysis chart builder
4. **Phase 5:** Polish and launch

## 📝 Notes

- Currently using mock data - real NFL data integration coming in Phase 2
- AI features are placeholders - will be implemented in Phase 3
- Design follows the minimalist aesthetic from VISION.md

