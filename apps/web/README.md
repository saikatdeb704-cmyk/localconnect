# LocalConnect Web

Next.js frontend for LocalConnect.

## Setup

```bash
cd apps/web
npm install
```

## Running

```bash
npm run dev
```

Open http://localhost:3000

## Building

```bash
npm run build
npm run start
```

## Environment Variables

Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=...
CLERK_SECRET_KEY=...
```
