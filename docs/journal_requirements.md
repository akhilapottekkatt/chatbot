# Journal Feature Requirements

## Fields
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | Integer | auto | Unique ID for each entry |
| user_id | String | auto | Identifies the user, defaults to "default" |
| title | String | No | Short summary of the entry |
| content | Text | Yes | The main journal writing |
| mood_selected | String | No | Picked from fixed list: Happy, Sad, Anxious, Stressed, Neutral, Not Sure |
| mood_note | String | No | User's own words to describe feeling in more detail |
| ai_reflection | Text | No | EMO's empathetic response to the entry |
| ai_mood_suggestion | String | No | Mood EMO suggests when "Not Sure" is selected |
| tags | String | No | Comma separated keywords eg. "work, family, sleep" |
| timestamp | DateTime | auto | When entry was created |
| updated_at | DateTime | auto | When entry was last edited |

## Mood Options
- 😊 Happy
- 😢 Sad
- 😰 Anxious
- 😤 Stressed
- 😐 Neutral
- ❓ Not Sure

## Features
- [ ] Create journal entry
- [ ] Edit journal entry
- [ ] Delete journal entry
- [ ] Filter by mood
- [ ] Filter by date range
- [ ] Search by tags
- [ ] EMO AI reflection on entry
- [ ] AI mood suggestion when "Not Sure" selected
- [ ] Journal streaks