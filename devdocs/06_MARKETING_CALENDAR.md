# 📅 Marketing Calendar System

**Complete multi-brand marketing campaign management with automated and manual task orchestration.**

## Overview

The Marketing Calendar is a comprehensive system for planning, executing, and tracking marketing campaigns across multiple brands. It supports:

✅ **Campaign Management** - Create and manage 30+ day campaigns with goals and budgets
✅ **Task Scheduling** - Automated and manually-assigned marketing tasks
✅ **Content Templates** - Reusable templates for consistent messaging across platforms
✅ **Performance Tracking** - Weekly reports and metrics collection
✅ **Multi-Brand Support** - Buildly, Foundry, Open.Build, Radical, and custom brands
✅ **Platform Integration** - Reddit, HN, LinkedIn, Dev.to, YouTube, Indie Hackers, ProductHunt, and more

---

## Features

### 1. Campaign Management

**Create campaigns** for any brand with:
- Campaign name and slug
- Description and goals
- Start/end dates and budget
- Owner assignment
- Metadata and custom fields

**Example: Buildly Labs 30-Day Growth Engine**
```json
{
  "brand_name": "buildly",
  "campaign_name": "Buildly Labs - 30 Day Growth Engine",
  "goal": "1000+ new Labs signups",
  "target_metric": "1000 signups",
  "start_date": "2025-01-06",
  "end_date": "2025-02-05",
  "budget": 20.00,
  "owner": "Growth Team"
}
```

### 2. Task Management

Create tasks with full scheduling and assignment:

**Task Types:**
- `social_post` - Social media content
- `article` - Long-form articles
- `video` - YouTube, TikTok shorts
- `email` - Email campaigns
- `paid_ad` - Sponsored content
- `press_release` - Press releases
- `podcast` - Podcast episodes
- `webinar` - Live events
- `event` - In-person/virtual events
- `custom` - Custom marketing tasks

**Platforms:**
- Reddit
- Hacker News
- Indie Hackers
- LinkedIn
- Dev.to
- Twitter/X
- YouTube
- TikTok
- Email
- Website
- Product Hunt

**Task Attributes:**
- Platform and type
- Scheduled date/time
- Priority (low, medium, high, critical)
- Automated vs manual
- Assignment to team member
- Status tracking (draft, scheduled, in_progress, completed, failed, cancelled)

### 3. Content Templates

Reusable templates for consistent brand messaging:

```python
# Example template
{
    "template_name": "Reddit Post - Founder Pain",
    "platform": "reddit",
    "task_type": "social_post",
    "category": "social_proof",
    "title_template": "I built {{tool_name}} that {{main_benefit}} — can I get feedback?",
    "body_template": "...",
    "variables": {
        "tool_name": "Buildly Labs",
        "main_benefit": "turns startup ideas into MVP specs + budgets",
        ...
    }
}
```

### 4. Weekly Performance Reports

Track and analyze marketing performance:

```python
{
    "week_start": "2025-01-06",
    "week_end": "2025-01-12",
    "posts_published": 7,
    "total_reach": 5000,
    "total_engagement": 250,
    "total_conversions": 15,
    "signups": 8,
    "platform_metrics": {
        "reddit": {"reach": 2000, "engagement": 120},
        "linkedin": {"reach": 1500, "engagement": 80},
        "devto": {"reach": 1000, "engagement": 50}
    }
}
```

---

## API Reference

### Campaigns

**GET /api/marketing/campaigns**
List all campaigns, optionally filtered by brand
```bash
curl /api/marketing/campaigns?brand=buildly
```

**POST /api/marketing/campaigns**
Create a new campaign
```bash
curl -X POST /api/marketing/campaigns \
  -H "Content-Type: application/json" \
  -d '{"brand_name":"buildly","campaign_name":"Growth Engine",...}'
```

**GET /api/marketing/campaigns/<campaign_id>**
Get campaign details with all tasks

### Tasks

**GET /api/marketing/tasks**
List tasks with multiple filters
```bash
curl '/api/marketing/tasks?brand=buildly&status=scheduled&platform=reddit'
```

**POST /api/marketing/tasks**
Create a new task
```bash
curl -X POST /api/marketing/tasks \
  -H "Content-Type: application/json" \
  -d '{"calendar_id":1,"brand_name":"buildly",...}'
```

**PUT /api/marketing/tasks/<task_id>**
Update a task (status, assignment, content, metrics)

**POST /api/marketing/tasks/<task_id>/complete**
Mark a task as completed
```bash
curl -X POST /api/marketing/tasks/5/complete \
  -H "Content-Type: application/json" \
  -d '{"executed_by":"user@example.com","metrics":{"reach":1200}}'
```

### Content Templates

**GET /api/marketing/templates**
List templates by brand, platform, or category

**POST /api/marketing/templates**
Create a reusable template

### Weekly Reports

**GET /api/marketing/weekly-reports**
Get weekly performance reports

**POST /api/marketing/weekly-reports**
Create a new weekly report with metrics

### Calendar View

**GET /api/marketing/calendar-view**
Get tasks grouped by date for calendar display
```bash
curl '/api/marketing/calendar-view?brand=buildly&start_date=2025-01-06&end_date=2025-01-12'
```

---

## Buildly Labs Campaign Content

The system includes a complete **30-day growth engine for Buildly Labs** with pre-populated content:

### Weekly Rhythm
- **Monday:** Reddit post (2-3 subreddits)
- **Tuesday:** LinkedIn post
- **Wednesday:** Dev.to article
- **Thursday:** YouTube Short
- **Friday:** Indie Hackers update + Show HN (Week 1)
- **Saturday:** Second YouTube Short
- **Sunday:** Engagement + replies (no new post)

### Key Tasks (Pre-configured)

**Week 1:**
1. Reddit: r/startups - "I built an AI tool for startup ideas"
2. LinkedIn: "Agile is Breaking Down"
3. Dev.to: "Agile is Broken - RAD Process Alternative"
4. YouTube Short: "Idea → Spec in 20 Seconds"
5. Indie Hackers: Week 1 Progress Update
6. YouTube Short: "Agile is Too Slow"
7. **Hacker News: "Show HN: Buildly Labs"** (Day 5 - Special Event)

**Week 2:**
- Repeat pattern with refined messaging
- Repost top-performing Reddit posts to new subreddits
- Analyze Week 1 metrics
- Create new YouTube Shorts based on performance

**Weeks 3-4:**
- Continue cadence with compounding effect
- Algorithm amplification kicks in
- Recycle best content
- Drive Product Hunt relaunch (Week 2 special event)

### Content Examples

**Reddit Post - r/startups:**
```
Title: I built an AI tool that turns startup ideas into MVP specs + budgets in minutes — can I get feedback?

Body:
Hey folks — I'm a founder who's built a lot of apps over the years and there's always one painful step:

Turning a founder's idea into a usable tech plan.

So I built a tool for that:
👉 Buildly Labs — AI that turns ideas into clear specs, budgets, and release plans.

It's meant for:
* first-time founders
* solo developers building SaaS
* teams who want to ditch Agile/Jira noise
* anyone who needs instant clarity

Would love brutally honest feedback, especially:
1. Does this solve a real problem for you?
2. Would you trust AI to generate release plans and estimates?
3. What's missing?

Thanks in advance — happy to run your idea through Labs if you want a free spec.
https://labs.buildly.io
```

**LinkedIn Post:**
```
Teams aren't struggling because they're bad at Agile.

They're struggling because Agile is too heavy for today's AI-assisted build cycle.

So we built a new model — the RAD Process (Radical AI Development).

Inside Buildly Labs, you turn an idea into:
* a clear spec
* a budget
* technical requirements
* a release plan
* micro-milestones

…all in a few minutes.

We helped a startup go from idea → pilot in 3 months using this workflow.

If you want to try it, the Alpha is open:
https://labs.buildly.io

#productmanagement #startup #ai #agile
```

**YouTube Short Script:**
```
VOICE: "If you're a founder, watch this idea turn into a full product spec, roadmap, and budget… automatically.

This is Buildly Labs — we built an AI that replaces the slowest part of building a startup."

[Show spec generating in real-time]

VOICE: "This used to take a team a week. Now it takes 30 seconds."

MUSIC: Upbeat, fast-paced
LENGTH: 45-60 seconds
```

---

## Brand Adaptations

The system automatically adapts campaigns for other brands:

### First City Foundry
- **Focus:** Real estate tech, property management
- **Platforms:** LinkedIn, Reddit (B2B heavy)
- **Goal:** 500+ customer leads
- **Messaging:** "Foundry helps real estate teams build custom software"

### Open.Build
- **Focus:** Open source, developer tools, web3
- **Platforms:** Reddit, HN, Dev.to, GitHub
- **Goal:** 1000+ community members
- **Messaging:** "Open.Build is the platform for building with open source"

### Radical
- **Focus:** Mental health, therapy innovation
- **Platforms:** LinkedIn, Reddit (professional)
- **Goal:** 800+ therapist signups
- **Messaging:** "Radical helps therapists deliver better outcomes"

---

## Database Schema

### MarketingCalendar
```python
id, brand_name, campaign_name, campaign_slug, description, goal, target_metric,
start_date, end_date, budget, currency, status, owner, notes, metadata,
created_at, updated_at
```

### MarketingTask
```python
id, calendar_id, brand_name, task_name, task_slug, description, task_type, platform,
scheduled_date, scheduled_time, duration_minutes, assigned_to, status, priority,
is_automated, title, body, metadata, completed_at, executed_by, execution_log,
error_message, metrics, created_at, updated_at
```

### ContentTemplate
```python
id, brand_name, template_name, template_slug, category, platform, task_type,
title_template, body_template, cta, hashtags, variables, description,
usage_count, performance_metrics, created_at, updated_at
```

### MarketingWeekly
```python
id, brand_name, calendar_id, week_start, week_end, posts_published, total_reach,
total_engagement, total_clicks, total_conversions, signups, platform_metrics,
notes, top_performing_post, insights, created_at, updated_at
```

---

## Usage Examples

### Create a Campaign

```python
from dashboard.marketing_calendar_models import MarketingCalendar
from datetime import datetime, timedelta

campaign = MarketingCalendar(
    brand_name='buildly',
    campaign_name='Buildly Labs - 30 Day Growth',
    goal='1000+ signups',
    start_date=datetime(2025, 1, 6),
    end_date=datetime(2025, 2, 5),
    budget=20.0,
    owner='Growth Team'
)
db.session.add(campaign)
db.session.commit()
```

### Create a Task

```python
from dashboard.marketing_calendar_models import MarketingTask, TaskType, PlatformType

task = MarketingTask(
    calendar_id=1,
    brand_name='buildly',
    task_name='Reddit: r/startups Post',
    task_type=TaskType.SOCIAL_POST,
    platform=PlatformType.REDDIT,
    scheduled_date=datetime(2025, 1, 6, 9, 0),
    title='I built an AI tool...',
    body='Hey folks...',
    assigned_to='growth-team@buildly.io',
    priority='high'
)
db.session.add(task)
db.session.commit()
```

### Get Tasks for Today

```python
from datetime import datetime, date

today = date.today()
start = datetime.combine(today, datetime.min.time())
end = datetime.combine(today, datetime.max.time())

tasks = MarketingTask.query.filter(
    MarketingTask.scheduled_date.between(start, end),
    MarketingTask.brand_name == 'buildly'
).order_by(MarketingTask.scheduled_date).all()
```

### Update Task Status

```python
task = MarketingTask.query.get(1)
task.status = TaskStatus.COMPLETED
task.completed_at = datetime.utcnow()
task.metrics = {'reach': 1200, 'engagement': 45}
db.session.commit()
```

### Generate Weekly Report

```python
from dashboard.marketing_calendar_models import MarketingWeekly
from datetime import datetime, timedelta

week_start = datetime(2025, 1, 6)
week_end = datetime(2025, 1, 12)

report = MarketingWeekly(
    brand_name='buildly',
    week_start=week_start,
    week_end=week_end,
    posts_published=7,
    total_reach=5000,
    total_engagement=250,
    total_conversions=15,
    signups=8,
    insights='Reddit posts performing 2x better than LinkedIn'
)
db.session.add(report)
db.session.commit()
```

---

## UI Components

### Marketing Calendar Dashboard
- **View Options:** Campaigns, Calendar, Task Board
- **Filters:** Brand, Status, Date Range
- **Visualizations:** Progress bars, platform breakdowns, metrics cards
- **Actions:** Create, edit, delete campaigns; assign and complete tasks

### Campaign Cards
- Campaign name and description
- Goal and target metric
- Progress indicator
- Task count and completion status
- Action buttons (View, Edit, Delete)

### Task Board
- Kanban-style columns: Draft → In Progress → Completed
- Drag-and-drop task movement
- Task quick-view with platform and priority
- Color-coded by status and priority

### Calendar View
- Month-based grid
- Tasks displayed on scheduled dates
- Click to create new task for date
- Platform color-coding

---

## Integration with Existing Systems

The marketing calendar integrates with:

- **Brand Management** - Multi-brand support via Brand model
- **Admin Panel** - Manage campaigns alongside brand settings
- **Dashboards** - View performance metrics and reports
- **Email Notifications** - Task reminders and deadline alerts
- **Analytics** - Track metrics and ROI

---

## Future Enhancements

- [ ] Automated task execution (API integrations)
- [ ] AI-powered content generation
- [ ] Advanced analytics and ROI tracking
- [ ] Social media auto-posting
- [ ] Slack/Teams integration for reminders
- [ ] Collaborative editing with version history
- [ ] Content approval workflows
- [ ] Team member onboarding templates
- [ ] Competitive analysis tracking
- [ ] Lead source attribution

---

## Getting Started

1. **Navigate to** `/marketing-calendar` in the dashboard
2. **Create a campaign** for your brand
3. **Add tasks** for each week/platform
4. **Assign team members** to tasks
5. **Track progress** via calendar view
6. **Update metrics** as tasks complete
7. **Review weekly reports** every Friday

---

**Built for**: Multi-brand marketing automation and coordination
**Current Status**: Alpha (Buildly Labs campaign pre-configured)
**Last Updated**: November 15, 2025
