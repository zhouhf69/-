# Colorectal 2026 - 医疗大数据

Medical Big Data Analytics Platform

## Features

- Next.js 15 with App Router
- TypeScript
- Tailwind CSS
- Vercel Speed Insights

## Getting Started

First, install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Speed Insights

This project uses Vercel Speed Insights to track performance metrics. The integration is implemented following the official Vercel documentation.

### Implementation

Speed Insights is enabled through the `@vercel/speed-insights` package with the `<SpeedInsights />` component added to the root layout (`app/layout.tsx`).

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new).

Check out the [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
