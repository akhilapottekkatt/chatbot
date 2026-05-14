# EMO Wellness — Frontend File Structure

## Files

| File | Route / Page | Description |
|------|-------------|-------------|
| `base.css` | Shared | All CSS variables, sidebar, topbar, button, card, and scrollbar styles |
| `dashboard.html` | `/` or `/dashboard` | Overview: mood check-in, stats, weekly chart, quick actions, insights |
| `chat.html` | `/chat` | Companion Chat (Serenity): conversation history sidebar, chat window, typing indicator |
| `refresh.html` | `/refresh` | Mental Refresh: 6 technique cards + live Box Breathing widget |
| `stress.html` | `/stress` | Stress Programs: 4 program cards with progress bars + today's exercise list |
| `journal.html` | `/journal` | Daily Journal: mood picker, write area, tag selector, AI prompt suggestions |
| `analytics.html` | `/analytics` | Mood Analytics: trend chart, mood prediction, heatmap, monthly bars, suggestions |
| `_sidebar.html` | — | Reference snippet (sidebar HTML — already embedded in each page) |

## How It Works
Each page is a **standalone HTML file** that links to `base.css` for shared styles,
then defines its own `<style>` block for page-specific styles. Navigation between
pages uses standard `<a href="...">` links, with the current page's nav-item given
the `active` class.

## Backend Integration (FastAPI)
Replace static data with API calls at these points:

### chat.html
- `sendUserMessage()` → POST `/api/chat` with `{ user_id, message, mood }`
- Load conversation history → GET `/api/chat/sessions?user_id=`

### journal.html
- `saveEntry()` → POST `/api/journal` with `{ user_id, mood, text, tags, date }`
- Load recent entries → GET `/api/journal?user_id=&limit=5`

### dashboard.html / analytics.html
- Stats row → GET `/api/stats?user_id=`
- Mood chart → GET `/api/mood/weekly?user_id=`
- Heatmap → GET `/api/mood/monthly?user_id=`

### stress.html
- Program progress → GET `/api/programs?user_id=`
- Toggle exercise done → PATCH `/api/exercises/:id` with `{ completed: true }`

### refresh.html
- Log breathing session → POST `/api/sessions` with `{ type: 'breathing', duration_s }`

## Crisis Detection
Crisis detection runs server-side in FastAPI before any AI response.
The frontend does not need to change — just ensure the `/api/chat` endpoint
returns a `crisis: true` flag and a safe message when triggered, and the
frontend will display it as a normal bot message.
