# Template-Driven Marketing Automation Architecture

## 🎯 **CORE PRINCIPLES**

1. **Eliminate Redundancies** - One codebase, multiple brand configurations
2. **Template-Driven** - Brand-specific templates, unified execution engine
3. **AI-Powered Content** - Ollama integration for dynamic content generation
4. **Parameterized Systems** - Configure don't duplicate

---

## 🧠 **OLLAMA AI INTEGRATION**

### **AI Configuration**
```yaml
# config/ai_config.yaml
ollama:
  base_url: "http://pop-os2.local:11434"
  models:
    content_generation: "llama3.1"      # Primary content model
    copywriting: "llama3.1"            # Marketing copy
    technical_writing: "codellama"      # Technical blog posts
    social_media: "llama3.1"           # Social media posts
    outreach: "llama3.1"               # Email outreach

  generation_settings:
    temperature: 0.7                    # Balance creativity vs consistency
    max_tokens: 2000                    # Reasonable content length
    top_p: 0.9                         # Nucleus sampling
    frequency_penalty: 0.1             # Reduce repetition
    
  fine_tuning:
    brand_voice_training: true          # Train on existing brand content
    domain_specific: true               # Technical/startup domain knowledge
    style_consistency: true             # Maintain brand voice consistency
```

### **AI Content Types**
```python
class ContentType(Enum):
    BLOG_POST = "blog_post"           # Technical articles, tutorials
    SOCIAL_POST = "social_post"       # Twitter, LinkedIn posts  
    OUTREACH_EMAIL = "outreach_email" # Cold outreach messages
    MARKETING_COPY = "marketing_copy" # Website copy, ads
    PRESS_RELEASE = "press_release"   # Announcements, news
    NEWSLETTER = "newsletter"         # Email newsletters
```

---

## 🎨 **TEMPLATE-DRIVEN SYSTEM ARCHITECTURE**

### **Brand Template Structure**
```
templates/
├── brands/
│   ├── buildly/
│   │   ├── brand_config.yaml         # Voice, tone, key messages
│   │   ├── blog_templates/           # Blog post templates
│   │   ├── social_templates/         # Social media templates  
│   │   ├── outreach_templates/       # Email templates
│   │   └── marketing_templates/      # Marketing copy templates
│   ├── foundry/
│   │   ├── brand_config.yaml         # Startup incubator voice
│   │   ├── outreach_templates/       # Proven foundry templates
│   │   └── content_templates/        # Startup-focused content
│   ├── open_build/
│   │   ├── brand_config.yaml         # Community-focused voice
│   │   ├── blog_templates/           # Developer tutorials
│   │   └── social_templates/         # Community content
│   └── radical_therapy/
│       ├── brand_config.yaml         # Methodology voice
│       ├── humor_templates/          # Programming jokes
│       └── content_templates/        # Development methodology
└── shared/
    ├── base_templates/               # Common template structures
    ├── ai_prompts/                   # Ollama prompt engineering
    └── style_guides/                 # Cross-brand consistency
```

### **Brand Configuration Example**
```yaml
# templates/brands/buildly/brand_config.yaml
brand:
  name: "Buildly"
  tagline: "AI-powered product development platform"
  
voice:
  tone: ["professional", "innovative", "developer-focused"]
  style: ["clear", "technical", "solution-oriented"]
  avoid: ["overly salesy", "buzzword-heavy", "non-technical"]

key_messages:
  primary: "Superior alternative to vibe coding with AI automation"
  secondary: 
    - "AI-driven project management & expert development community"
    - "Streamline software projects with AI insights"
    - "Connect with expert agencies through our marketplace"
  
target_audience:
  primary: ["developers", "product managers", "startup founders"]
  secondary: ["development agencies", "enterprise teams"]

content_themes:
  - "AI automation in development"
  - "Developer productivity"
  - "Project management innovation"
  - "Expert marketplace benefits"

social_media:
  hashtags: ["#Buildly", "#AIAutomation", "#DevTools", "#ProductDevelopment"]
  posting_times: ["09:00", "15:00"]  # Business hours
  content_mix:
    educational: 40%
    product_updates: 30% 
    community: 20%
    promotional: 10%

outreach:
  email_signature: |
    Best regards,
    The Buildly Team
    https://www.buildly.io
  
  pain_points:
    - "Inefficient development workflows"
    - "Lack of AI integration in development"
    - "Difficulty finding expert developers"
    - "Project management complexity"
```

---

## 🤖 **UNIFIED AUTOMATION ENGINES**

### **1. Content Generation Engine**
```python
# automation/content/ai_content_generator.py

class AIContentGenerator:
    """Unified content generation using Ollama AI with brand-specific templates"""
    
    def __init__(self, ollama_url: str = "http://pop-os2.local:11434"):
        self.ollama_client = OllamaClient(ollama_url)
        self.brand_configs = self.load_brand_configs()
        
    async def generate_blog_post(self, brand: str, topic: str, target_audience: str = None) -> BlogPost:
        """Generate brand-specific blog post using AI"""
        
        brand_config = self.brand_configs[brand]
        template = self.load_template(brand, "blog_post", topic)
        
        prompt = f"""
        Write a technical blog post for {brand_config['name']}.
        
        Brand Voice: {', '.join(brand_config['voice']['tone'])}
        Target Audience: {target_audience or brand_config['target_audience']['primary']}
        Topic: {topic}
        Key Messages: {brand_config['key_messages']['primary']}
        
        Template Structure:
        {template}
        
        Requirements:
        - 800-1200 words
        - Include code examples if technical
        - Maintain {brand} voice and tone
        - Include call-to-action for {brand_config['website']}
        - Use SEO-friendly structure
        """
        
        content = await self.ollama_client.generate(
            model="llama3.1",
            prompt=prompt,
            temperature=0.7
        )
        
        return BlogPost(
            title=self.extract_title(content),
            content=content,
            brand=brand,
            topic=topic,
            generated_at=datetime.now()
        )
    
    async def generate_social_post(self, brand: str, content_type: str, platform: str = "twitter") -> SocialPost:
        """Generate brand-specific social media post"""
        
        brand_config = self.brand_configs[brand]
        template = self.load_template(brand, "social_post", content_type)
        
        char_limit = 280 if platform == "twitter" else 1000
        
        prompt = f"""
        Create a {platform} post for {brand_config['name']}.
        
        Brand Voice: {', '.join(brand_config['voice']['tone'])}
        Content Type: {content_type}
        Character Limit: {char_limit}
        Hashtags: {brand_config['social_media']['hashtags']}
        
        Requirements:
        - Engaging and {brand_config['voice']['style'][0]}
        - Include relevant hashtags
        - Call-to-action if appropriate
        - Match {brand} personality
        """
        
        content = await self.ollama_client.generate(
            model="llama3.1", 
            prompt=prompt,
            temperature=0.8,
            max_tokens=100
        )
        
        return SocialPost(
            content=content,
            platform=platform,
            brand=brand,
            hashtags=self.extract_hashtags(content),
            scheduled_time=self.calculate_optimal_time(brand, platform)
        )
        
    async def generate_outreach_email(self, brand: str, recipient_type: str, personalization: dict) -> OutreachEmail:
        """Generate personalized outreach email"""
        
        brand_config = self.brand_configs[brand]
        template = self.load_template(brand, "outreach_email", recipient_type)
        
        prompt = f"""
        Write a personalized outreach email for {brand_config['name']}.
        
        Recipient Type: {recipient_type}
        Recipient Info: {personalization}
        Brand Voice: Professional but {brand_config['voice']['tone'][0]}
        
        Pain Points to Address: {brand_config['outreach']['pain_points']}
        Key Value Proposition: {brand_config['key_messages']['primary']}
        
        Template:
        {template}
        
        Requirements:
        - Personalize with recipient information
        - Address specific pain points for {recipient_type}
        - Clear value proposition
        - Professional but friendly tone
        - Include specific call-to-action
        - 150-250 words
        """
        
        content = await self.ollama_client.generate(
            model="llama3.1",
            prompt=prompt,
            temperature=0.6  # Lower temperature for professional communication
        )
        
        return OutreachEmail(
            subject=self.extract_subject(content),
            body=content,
            brand=brand,
            recipient_type=recipient_type,
            personalization=personalization
        )
```

### **2. Unified Social Media Engine**
```python
# automation/social/unified_social_engine.py

class UnifiedSocialEngine:
    """Single engine for all brand social media automation"""
    
    def __init__(self):
        self.content_generator = AIContentGenerator()
        self.brand_configs = self.load_brand_configs()
        self.posting_scheduler = PostingScheduler()
        
    async def generate_daily_content(self):
        """Generate daily content for all brands"""
        
        for brand in ["buildly", "foundry", "open_build", "radical_therapy"]:
            brand_config = self.brand_configs[brand]
            
            # Determine content type based on brand schedule and mix
            content_type = self.select_content_type(brand)
            
            # Generate AI content
            post = await self.content_generator.generate_social_post(
                brand=brand,
                content_type=content_type,
                platform="twitter"
            )
            
            # Schedule for optimal time
            optimal_time = self.calculate_optimal_posting_time(brand)
            self.posting_scheduler.schedule_post(post, optimal_time)
    
    def select_content_type(self, brand: str) -> str:
        """Select content type based on brand mix and schedule"""
        config = self.brand_configs[brand]
        content_mix = config['social_media']['content_mix']
        
        # Weighted random selection based on content mix percentages
        return self.weighted_random_choice(content_mix)
```

### **3. Unified Outreach Engine**
```python
# automation/outreach/unified_outreach_engine.py

class UnifiedOutreachEngine:
    """Single engine for all brand outreach campaigns"""
    
    def __init__(self):
        self.content_generator = AIContentGenerator()
        self.contact_manager = ContactManager()
        self.email_sender = EmailSender()
        
    async def run_daily_outreach(self):
        """Run outreach for all brands with brand-specific targeting"""
        
        # Foundry: Startup publications (preserve existing system)
        await self.run_brand_outreach("foundry", "startup_publications")
        
        # Buildly: Developer tools and agencies
        await self.run_brand_outreach("buildly", "developer_agencies")
        
        # Open Build: Open source communities  
        await self.run_brand_outreach("open_build", "open_source_communities")
        
    async def run_brand_outreach(self, brand: str, target_type: str):
        """Run outreach campaign for specific brand"""
        
        # Get brand-specific targets
        targets = await self.contact_manager.get_targets(brand, target_type)
        
        # Generate personalized emails using AI
        for target in targets[:5]:  # Rate limit
            personalization = {
                'name': target.name,
                'company': target.company, 
                'industry': target.industry,
                'pain_points': target.likely_pain_points
            }
            
            email = await self.content_generator.generate_outreach_email(
                brand=brand,
                recipient_type=target_type,
                personalization=personalization
            )
            
            # Send with brand-specific configuration
            await self.email_sender.send_email(email, target, brand)
```

---

## 📊 **OLLAMA FINE-TUNING STRATEGY**

### **Brand Voice Training**
```python
# automation/ai/brand_voice_trainer.py

class BrandVoiceTrainer:
    """Fine-tune Ollama models for brand-specific voice and style"""
    
    async def train_brand_voice(self, brand: str):
        """Train Ollama on existing brand content for voice consistency"""
        
        # Collect existing brand content
        training_data = await self.collect_brand_content(brand)
        
        # Create brand-specific training dataset
        dataset = self.create_training_dataset(brand, training_data)
        
        # Fine-tune model for brand voice
        await self.ollama_client.fine_tune(
            base_model="llama3.1",
            dataset=dataset,
            model_name=f"{brand}_voice_model",
            training_config={
                'learning_rate': 0.0001,
                'epochs': 10,
                'batch_size': 4
            }
        )
    
    async def collect_brand_content(self, brand: str) -> List[str]:
        """Collect existing content for training data"""
        content = []
        
        # Existing social media posts
        content.extend(await self.get_existing_social_posts(brand))
        
        # Blog posts and articles
        content.extend(await self.get_existing_blog_posts(brand))
        
        # Successful outreach emails
        content.extend(await self.get_successful_outreach(brand))
        
        # Marketing copy from websites
        content.extend(await self.scrape_website_copy(brand))
        
        return content
```

### **Content Quality Optimization**
```python
# automation/ai/content_optimizer.py

class ContentOptimizer:
    """Optimize AI-generated content for quality and brand consistency"""
    
    def __init__(self):
        self.quality_metrics = QualityMetrics()
        self.brand_checker = BrandConsistencyChecker()
        
    async def optimize_content(self, content: str, brand: str, content_type: str) -> str:
        """Optimize AI-generated content for quality and brand fit"""
        
        # Check brand voice consistency
        brand_score = await self.brand_checker.check_consistency(content, brand)
        
        if brand_score < 0.8:
            # Regenerate with stronger brand prompts
            content = await self.regenerate_with_brand_emphasis(content, brand)
        
        # Check content quality metrics
        quality_score = await self.quality_metrics.evaluate(content, content_type)
        
        if quality_score < 0.7:
            # Improve content quality
            content = await self.improve_content_quality(content, content_type)
        
        return content
```

---

## 🔧 **IMPLEMENTATION ROADMAP**

### **Phase 1: AI Integration (This Week)**
1. **Set up Ollama client** and test connection to pop-os2.local:11434
2. **Create brand configuration templates** for all 4 brands
3. **Build basic AI content generator** with simple prompts
4. **Test content generation** for each brand

### **Phase 2: Template System (Next Week)**  
1. **Build template engine** for brand-specific content
2. **Create unified social media engine** with AI integration
3. **Migrate existing Twitter automation** to template-driven system
4. **Test cross-brand content generation**

### **Phase 3: Outreach Integration (Week 3)**
1. **Build unified outreach engine** with AI personalization
2. **Migrate Foundry outreach system** to new architecture (carefully!)
3. **Integrate Open Build outreach** with AI enhancement
4. **Test end-to-end outreach workflows**

### **Phase 4: Fine-Tuning & Optimization (Week 4)**
1. **Train brand-specific voice models** using existing content
2. **Implement content quality optimization**
3. **Set up automated content scheduling**
4. **Launch unified dashboard with AI controls**

This architecture eliminates redundancy by having **one codebase that generates content for all brands** using **AI-powered templates** while maintaining **each brand's unique voice and message**. The Ollama integration provides unlimited, customized content generation that gets better over time as we fine-tune it on your existing successful content.

Would you like to start with setting up the Ollama integration and testing basic AI content generation?