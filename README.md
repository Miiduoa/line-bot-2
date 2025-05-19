# LINE Bot with Gemini AI

This is a LINE Bot integrated with Google's Gemini AI and multiple API services.

## Quick Deploy
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FYOUR_USERNAME%2FYOUR_REPO_NAME&env=LINE_CHANNEL_ACCESS_TOKEN,LINE_CHANNEL_SECRET,GOOGLE_GEMINI_API_KEY,NEWS_API_KEY,TMDB_API_KEY,OPENWEATHERMAP_API_KEY)

## Features
- Integration with LINE Messaging API
- Powered by Google Gemini Pro
- News searching capability
- Movie and weather information (to be implemented)

## Deployment on Vercel
This application is configured for Vercel deployment.

1. Install Vercel CLI:
```
npm i -g vercel
```

2. Login to Vercel:
```
vercel login
```

3. Deploy to Vercel:
```
vercel
```

4. Set environment variables in Vercel dashboard after deployment:
   - LINE_CHANNEL_ACCESS_TOKEN
   - LINE_CHANNEL_SECRET
   - GOOGLE_GEMINI_API_KEY
   - NEWS_API_KEY
   - TMDB_API_KEY
   - OPENWEATHERMAP_API_KEY

5. Set your LINE Bot webhook URL to `https://your-vercel-domain.vercel.app/callback`
