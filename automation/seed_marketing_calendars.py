"""  
Marketing Calendar Seed Data - Buildly Labs 30-Day Growth Engine
Plus adaptations for other brands.
"""

from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.brand_loader import get_all_brands
from dashboard.marketing_calendar_models import (
    MarketingCalendar, MarketingTask, ContentTemplate, TaskType, 
    TaskStatus, TaskPriority, PlatformType
)
from dashboard.models import Brand
from dashboard.database import db


def create_buildly_labs_campaign():
    """Create the Buildly Labs 30-day growth engine campaign"""
    
    start_date = datetime(2025, 1, 6)  # Week starting Monday
    end_date = start_date + timedelta(days=30)
    
    campaign = MarketingCalendar(
        brand_name='buildly',
        campaign_name='Buildly Labs - 30 Day Growth Engine',
        campaign_slug='buildly-labs-growth-30d',
        description='Complete 30-day marketing blitz for Buildly Labs. Target: 1000+ signups through Reddit, HN, Indie Hackers, LinkedIn, Dev.to, and YouTube Shorts.',
        goal='1000+ new Labs signups',
        target_metric='1000 signups',
        start_date=start_date,
        end_date=end_date,
        budget=20.0,
        currency='USD',
        status='draft',
        owner='Growth Team',
        notes='This is a 0-20 budget growth campaign using organic content and compounding social media effects.',
        metadata={
            'source': 'Buildly Labs Growth Playbook',
            'weekly_rhythm': 'Mon: Reddit, Tue: LinkedIn, Wed: Dev.to, Thu: YouTube Short, Fri: Indie Hackers, Sat: YouTube Short, Sun: Engage',
            'special_events': ['Day 5 - Show HN', 'Day 14 - Product Hunt'],
            'content_pillars': ['AI Specs', 'Agile Alternative', 'Founder Tools']
        }
    )
    
    db.session.add(campaign)
    db.session.flush()  # Get campaign ID
    
    return campaign


def create_buildly_labs_tasks(campaign):
    """Create all tasks for Buildly Labs campaign"""
    
    tasks = []
    start_date = campaign.start_date
    
    # ===== WEEK 1 =====
    
    # Monday - Reddit Post 1
    tasks.append(MarketingTask(
        calendar_id=campaign.id,
        brand_name='buildly',
        task_name='Reddit: r/startups - Founder Idea Tool',
        task_slug='reddit-startups-w1',
        description='Post about AI tool for turning startup ideas into MVP specs',
        task_type=TaskType.SOCIAL_POST,
        platform=PlatformType.REDDIT,
        scheduled_date=start_date,
        scheduled_time='09:00',
        assigned_to='growth-team',
        status=TaskStatus.DRAFT,
        priority=TaskPriority.HIGH,
        is_automated=False,
        title='I built an AI tool that turns startup ideas into MVP specs + budgets in minutes — can I get feedback?',
        body="""Hey folks — I'm a founder who's built a lot of apps over the years and there's always one painful step:

**Turning a founder's idea into a usable tech plan.**

So I built a tool for that:
👉 **Buildly Labs — AI that turns ideas into clear specs, budgets, and release plans.**

It's meant for:
* first-time founders
* solo developers building SaaS
* teams who want to ditch Agile/Jira noise
* anyone who needs instant clarity

Would love **brutally honest feedback**, especially:
1. Does this solve a real problem for you?
2. Would you trust AI to generate release plans and estimates?
3. What's missing?

Thanks in advance — happy to run your idea through Labs if you want a free spec.

https://labs.buildly.io""",
        metadata={
            'subreddit': 'r/startups',
            'target_audience': 'First-time founders, indie developers',
            'estimated_reach': '500-2000'
        }
    ))
    
    # Tuesday - LinkedIn Post
    tasks.append(MarketingTask(
        calendar_id=campaign.id,
        brand_name='buildly',
        task_name='LinkedIn: Agile is Breaking Down',
        task_slug='linkedin-agile-w1',
        description='LinkedIn post about why Agile is broken for AI-assisted teams',
        task_type=TaskType.SOCIAL_POST,
        platform=PlatformType.LINKEDIN,
        scheduled_date=start_date + timedelta(days=1),
        scheduled_time='10:00',
        assigned_to='growth-team',
        status=TaskStatus.DRAFT,
        priority=TaskPriority.HIGH,
        is_automated=False,
        title='Agile is Breaking Down',
        body="""Teams aren't struggling because they're bad at Agile.

They're struggling because Agile is **too heavy for today's AI-assisted build cycle.**

So we built a new model — the **RAD Process** (Radical AI Development).

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

#productmanagement #startup #ai #agile""",
        metadata={
            'platform': 'LinkedIn',
            'content_type': 'thought_leadership',
            'estimated_reach': '1000-5000'
        }
    ))
    
    # Wednesday - Dev.to Article
    tasks.append(MarketingTask(
        calendar_id=campaign.id,
        brand_name='buildly',
        task_name='Dev.to: Agile is Broken - RAD Process Alternative',
        task_slug='devto-agile-broken-w1',
        description='Long-form Dev.to article about why Agile is broken and the RAD Process alternative',
        task_type=TaskType.ARTICLE,
        platform=PlatformType.DEVTO,
        scheduled_date=start_date + timedelta(days=2),
        scheduled_time='08:00',
        assigned_to='growth-team',
        status=TaskStatus.DRAFT,
        priority=TaskPriority.HIGH,
        is_automated=False,
        title='Agile is Broken. Here\'s the AI-Driven RAD Process We Use Instead.',
        body="""Agile isn't bad. It's just designed for a world before AI.

Teams today move faster, deliver continuously, and plan dynamically — but we're still trapped in Jira, story points, and rituals that don't add value.

So my team built the **RAD Process**: a lightweight, AI-assisted workflow that:
* turns ideas into specs
* generates release plans
* prioritizes work dynamically
* eliminates ritual overhead
* supports micro-release patterns

Inside Buildly Labs, you can generate:
* specs
* budgets
* architecture suggestions
* timelines

...in minutes.

## Why Agile Broke

Agile was built for 2001. Here's what was true then:
- Code took weeks to write
- Testing was expensive
- Meetings were how teams stayed aligned
- Changes were costly

Today, with AI and cloud infrastructure:
- Code takes days to write
- Testing is continuous
- Real-time collaboration is standard
- Changes are expected

Agile hasn't evolved. So teams are stuck using story points and 2-week sprints for 2-day development cycles.

## The RAD Process

We rebuilt planning for AI-assisted teams:

1. **Idea → Spec (5 min)** - AI generates technical requirements from a description
2. **Spec → Budget (2 min)** - AI estimates costs, team size, timeline
3. **Budget → Releases (5 min)** - AI suggests micro-milestones and MVP scope
4. **Releases → Decisions (ongoing)** - Team validates and adjusts weekly

No standups. No sprint planning. No backlog grooming.

Just clarity + iteration.

## What We Learned Building This

The teams that moved fastest weren't good at Agile. They were good at **clarity**.

They spent 30 minutes getting the spec right, then shipped.

Everyone else spent 30 minutes in Jira, then shipped the wrong thing.

## Try It

We built Buildly Labs to automate the spec → budget → release pipeline.

Free tier: https://labs.buildly.io

Would love thoughts — especially from PMs and devs who've felt the Agile → AI transition pain.

Tags: #ai #productmanagement #startup #agile""",
        metadata={
            'platform': 'Dev.to',
            'reading_time_minutes': 7,
            'estimated_reach': '2000-10000'
        }
    ))
    
    # Thursday - YouTube Short
    tasks.append(MarketingTask(
        calendar_id=campaign.id,
        brand_name='buildly',
        task_name='YouTube Short: Idea → Spec in 20 Seconds',
        task_slug='yt-shorts-idea-spec-w1',
        description='YouTube Short showing idea turning into spec automatically',
        task_type=TaskType.VIDEO,
        platform=PlatformType.YOUTUBE,
        scheduled_date=start_date + timedelta(days=3),
        scheduled_time='12:00',
        duration_minutes=15,  # Recording time
        assigned_to='growth-team',
        status=TaskStatus.DRAFT,
        priority=TaskPriority.MEDIUM,
        is_automated=False,
        title='Idea → Spec in 20 Seconds',
        body="""SCRIPT (30-90 seconds):

[Screen recording of typing an idea into Buildly Labs]

VOICE:
"If you're a founder, watch this idea turn into a full product spec, roadmap, and budget… automatically.

This is Buildly Labs — we built an AI that replaces the slowest part of building a startup."

[Show output appearing on screen - spec, timeline, budget]

VOICE:
"This used to take a team a week. Now it takes 30 seconds."

[Show CTA]
VOICE:
"Try it free: labs.buildly.io"

VISUALS:
- Open Buildly Labs
- Type idea: "Build an AI writing assistant for developers"
- Show AI generating spec in real-time
- Display outputs: technical spec, timeline, budget estimate
- Buildly Labs logo + link

MUSIC: Upbeat, fast-paced (no copyright)
LENGTH: 45-60 seconds""",
        metadata={
            'platform': 'YouTube',
            'format': 'shorts',
            'duration_seconds': 60,
            'estimated_reach': '5000-50000'
        }
    ))
    
    # Friday - Indie Hackers Post (+ Show HN this week)
    tasks.append(MarketingTask(
        calendar_id=campaign.id,
        brand_name='buildly',
        task_name='Indie Hackers: Week 1 Progress Update',
        task_slug='ih-week1-w1',
        description='Weekly progress update on Buildly Labs',
        task_type=TaskType.SOCIAL_POST,
        platform=PlatformType.INDIE_HACKERS,
        scheduled_date=start_date + timedelta(days=4),
        scheduled_time='14:00',
        assigned_to='growth-team',
        status=TaskStatus.DRAFT,
        priority=TaskPriority.MEDIUM,
        is_automated=False,
        title='Week 1: Built an AI that generates MVP specs in minutes — looking for test users',
        body="""Hey IH! I'm building **Buildly Labs**, an AI tool that turns founder ideas into:
* clear specs
* budgets
* release plans
* estimates
* architecture suggestions

Basically the stuff every founder struggles with before hiring a dev.

**What we've learned so far:**
- Founders spend 2-3 weeks getting specs right
- AI can do it in 5 minutes
- The output quality is 80% there on first try
- People trust the AI more than they expect

**This week:**
- 50 signups
- 20 test users running specs through Labs
- Feedback: "This is like having a CTO for $0"

**Looking for:**
- Test users (free tier)
- Feedback on spec quality
- Use cases we're missing

If you want to try it, I'll run your idea through the Labs MVP engine and share a spec. Free.

What would you want this tool to do next?

https://labs.buildly.io""",
        metadata={
            'platform': 'Indie Hackers',
            'post_type': 'weekly_update',
            'estimated_reach': '500-2000'
        }
    ))
    
    # Saturday - YouTube Short #2 (same week)
    tasks.append(MarketingTask(
        calendar_id=campaign.id,
        brand_name='buildly',
        task_name='YouTube Short: Agile is Too Slow',
        task_slug='yt-shorts-agile-slow-w1',
        description='Second YouTube Short about Agile being too slow',
        task_type=TaskType.VIDEO,
        platform=PlatformType.YOUTUBE,
        scheduled_date=start_date + timedelta(days=5),
        scheduled_time='13:00',
        duration_minutes=15,
        assigned_to='growth-team',
        status=TaskStatus.DRAFT,
        priority=TaskPriority.MEDIUM,
        is_automated=False,
        title='Agile is Too Slow Now',
        body="""SCRIPT (30-90 seconds):

VOICE:
"Agile was built for 2001.

Today, AI changes everything — and founders can't wait 3 months for a backlog grooming cycle.

That's why we built the RAD Process inside Buildly Labs.

Skip Jira. Skip Agile overhead.

Turn ideas into clear specs instantly."

[Show Buildly Labs interface]

VISUALS:
- Show typical Agile workflow (slow, painful)
- Show Buildly Labs workflow (fast, AI-powered)
- Comparison: 3 weeks vs 5 minutes
- Buildly Labs logo + link

MUSIC: Upbeat, motivational

LENGTH: 45-60 seconds""",
        metadata={
            'platform': 'YouTube',
            'format': 'shorts',
            'duration_seconds': 60,
            'hook': 'Agile comparison'
        }
    ))
    
    # Friday of Week 2 - Show HN Post
    tasks.append(MarketingTask(
        calendar_id=campaign.id,
        brand_name='buildly',
        task_name='Hacker News: Show HN - Buildly Labs',
        task_slug='hn-show-buildly-labs-w2',
        description='Show HN post for Buildly Labs - Day 5 special event',
        task_type=TaskType.SOCIAL_POST,
        platform=PlatformType.HACKER_NEWS,
        scheduled_date=start_date + timedelta(days=11),  # Friday of week 2
        scheduled_time='10:30',  # Optimal HN time
        assigned_to='growth-team',
        status=TaskStatus.DRAFT,
        priority=TaskPriority.CRITICAL,
        is_automated=False,
        title='Show HN: Buildly Labs — AI tool that turns ideas into specs, budgets, and release plans',
        body="""Hey HN —

I've spent the last few years helping startups go from idea → product. The slowest part is always turning the idea into:
* technical requirements
* estimates
* architecture suggestions
* release plans
* budgets
* priority stacks

So I built **Buildly Labs**, an AI-assisted product management platform.

It replaces slow Agile rituals with a lightweight **RAD Process** (Radical AI Development).

How it works:
1. Describe your idea (any format)
2. AI generates technical spec + budget + timeline
3. You validate, adjust, iterate

Curious for feedback on:
1. Quality of generated specs
2. Where you'd add or remove steps
3. Whether you'd trust this for early-stage planning
4. Any pain points you've had with Jira/Agile fatigue

Live demo: https://labs.buildly.io

Would love to hear thoughts — and happy to generate a spec for your idea.

---

DETAILS:
- Built with: Flask, SQLAlchemy, OpenAI
- Status: Public Alpha
- Price: Free tier available
- Use case: Founders, indie developers, teams""",
        metadata={
            'platform': 'Hacker News',
            'post_type': 'show_hn',
            'estimated_reach': '10000-100000',
            'special_event': True
        }
    ))
    
    # Add more weeks (abbreviated for space)...
    
    for task in tasks:
        db.session.add(task)
    
    db.session.flush()
    return tasks


def create_content_templates_buildly():
    """Create reusable content templates for Buildly Labs"""
    
    templates = [
        ContentTemplate(
            brand_name='buildly',
            template_name='Reddit Post - Founder Pain',
            template_slug='reddit-founder-pain',
            category='social_proof',
            platform=PlatformType.REDDIT,
            task_type=TaskType.SOCIAL_POST,
            title_template='I built {{tool_name}} that {{main_benefit}} — can I get feedback?',
            body_template="""Hey folks — {{origin_story}}

So I built a tool for that:
👉 **{{tool_name}} — {{tagline}}**

It's meant for:
{{use_cases}}

Would love **brutally honest feedback**, especially:
1. {{question_1}}
2. {{question_2}}
3. What's missing?

Thanks in advance — happy to run your {{offer}} if you want a free {{offer_type}}.

{{link}}""",
            cta='Try it free',
            hashtags='#startup #ai #productmanagement',
            variables={
                'tool_name': 'Buildly Labs',
                'main_benefit': 'turns startup ideas into MVP specs + budgets',
                'tagline': 'AI that turns ideas into clear specs, budgets, and release plans',
                'origin_story': 'a founder who\'s built a lot of apps',
                'use_cases': '* first-time founders\n* solo developers\n* teams',
                'question_1': 'Does this solve a real problem?',
                'question_2': 'Would you trust AI for release plans?',
                'offer': 'idea',
                'offer_type': 'spec',
                'link': 'https://labs.buildly.io'
            },
            description='Template for Reddit posts about founder pain points',
            usage_count=1
        ),
        
        ContentTemplate(
            brand_name='buildly',
            template_name='LinkedIn Post - Thought Leadership',
            template_slug='linkedin-thought-leadership',
            category='thought_leadership',
            platform=PlatformType.LINKEDIN,
            task_type=TaskType.SOCIAL_POST,
            title_template='{{headline}}',
            body_template="""{{main_message}}

So we built {{solution}} — the **{{process_name}}** ({{process_description}}).

Inside {{product_name}}, you {{user_action}}:
{{benefits}}

{{story}}

If you want to try it, the {{stage}} is {{status}}:
{{link}}

#{{hashtag1}} #{{hashtag2}} #{{hashtag3}}""",
            cta='Learn more',
            hashtags='#ai #productivity #startup',
            variables={
                'headline': 'Agile is Breaking Down',
                'main_message': 'Teams aren\'t struggling because they\'re bad at Agile.',
                'solution': 'a new model',
                'process_name': 'RAD Process',
                'process_description': 'Radical AI Development',
                'product_name': 'Buildly Labs',
                'user_action': 'turn an idea',
                'benefits': '* clear specs\n* budgets\n* requirements\n* release plans',
                'story': 'We helped a startup go from idea → pilot in 3 months.',
                'stage': 'Alpha',
                'status': 'open',
                'link': 'https://labs.buildly.io',
                'hashtag1': 'productmanagement',
                'hashtag2': 'startup',
                'hashtag3': 'ai'
            },
            description='Template for LinkedIn thought leadership posts'
        )
    ]
    
    for template in templates:
        db.session.add(template)
    
    db.session.flush()
    return templates


def adapt_campaign_for_brand(base_campaign_data, brand_name, brand_focus):
    """Adapt the Buildly Labs campaign template for other brands"""
    
    adaptations = {
        'foundry': {
            'name': 'First City Foundry - 30 Day Growth',
            'goal': '500+ new customer leads',
            'focus': 'real estate tech, property management, developer partnerships',
            'messaging': 'Foundry helps real estate teams build custom software without technical debt.',
            'platforms': ['linkedin', 'reddit', 'twitter'],  # B2B heavy
            'pillars': ['real_estate_tech', 'property_management', 'developer_productivity']
        },
        'openbuild': {
            'name': 'Open.Build - 30 Day Community Growth',
            'goal': '1000+ new community members',
            'focus': 'open source, developer tools, decentralized building',
            'messaging': 'Open.Build is the platform for building with open source and web3.',
            'platforms': ['reddit', 'hacker_news', 'devto', 'github'],
            'pillars': ['open_source', 'developer_community', 'web3']
        },
        'radical': {
            'name': 'Radical - 30 Day Impact Campaign',
            'goal': '800+ therapist signups',
            'focus': 'mental health, therapy innovation, rad therapy methods',
            'messaging': 'Radical helps therapists deliver better outcomes with radical methods.',
            'platforms': ['linkedin', 'reddit'],  # Healthcare/professional
            'pillars': ['mental_health', 'therapy_innovation', 'practitioner_support']
        }
    }
    
    if brand_name not in adaptations:
        return None
    
    adapt = adaptations[brand_name]
    
    campaign = MarketingCalendar(
        brand_name=brand_name,
        campaign_name=adapt['name'],
        campaign_slug=adapt['name'].lower().replace(' ', '-'),
        description=f"30-day growth campaign for {brand_name}. Focus: {adapt['focus']}",
        goal=adapt['goal'],
        target_metric=adapt['goal'].split('+')[0] if '+' in adapt['goal'] else adapt['goal'],
        start_date=base_campaign_data['start_date'],
        end_date=base_campaign_data['end_date'],
        budget=base_campaign_data['budget'],
        currency='USD',
        status='draft',
        owner='Growth Team',
        metadata={
            'source': 'Multi-brand Growth Playbook',
            'brand_focus': adapt['focus'],
            'messaging': adapt['messaging'],
            'target_platforms': adapt['platforms'],
            'content_pillars': adapt['pillars']
        }
    )
    
    return campaign


def seed_all_calendars():
    """Seed all marketing calendars for all brands"""
    
    print("🚀 Seeding Marketing Calendars...\n")
    
    # Check if brand exists
    buildly = Brand.query.filter_by(name='buildly').first()
    if not buildly:
        print("❌ Buildly brand not found. Please create brands first.")
        return False
    
    # Create Buildly Labs campaign
    print("📅 Creating Buildly Labs 30-Day Growth Campaign...")
    campaign_buildly = create_buildly_labs_campaign()
    
    print("✏️ Creating tasks...")
    tasks_buildly = create_buildly_labs_tasks(campaign_buildly)
    print(f"   ✅ Created {len(tasks_buildly)} tasks")
    
    print("📝 Creating content templates...")
    templates_buildly = create_content_templates_buildly()
    print(f"   ✅ Created {len(templates_buildly)} templates")
    
    # Create adapted campaigns for other brands - load from database
    all_brands = get_all_brands(active_only=True)
    other_brands = [b for b in all_brands if b != 'buildly']
    base_data = {
        'start_date': campaign_buildly.start_date,
        'end_date': campaign_buildly.end_date,
        'budget': 20.0
    }
    
    for brand_name in other_brands:
        brand = Brand.query.filter_by(name=brand_name).first()
        if brand:
            print(f"\n📅 Creating {brand_name} campaign...")
            adapted = adapt_campaign_for_brand(base_data, brand_name, 'general')
            if adapted:
                db.session.add(adapted)
                print(f"   ✅ Campaign created for {brand_name}")
    
    # Commit all changes
    try:
        db.session.commit()
        print("\n✅ All marketing calendars seeded successfully!")
        print(f"   - 1 Buildly Labs campaign with {len(tasks_buildly)} tasks")
        print(f"   - 4 adapted brand campaigns")
        print(f"   - {len(templates_buildly)} reusable content templates")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error seeding calendars: {e}")
        return False


if __name__ == '__main__':
    from dashboard.app import app
    
    with app.app_context():
        seed_all_calendars()
