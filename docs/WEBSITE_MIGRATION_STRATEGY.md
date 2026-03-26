# Website Migration Strategy
# Plan for moving websites to separate GitHub repositories while maintaining automation integration

## 🎯 **MIGRATION OBJECTIVES**

Transform the current mixed website/automation folders into:
- **Clean separation** - Websites in dedicated GitHub repos, automation centralized
- **Zero downtime** - Seamless transition for production sites  
- **Preserved functionality** - All existing features continue working
- **Better maintainability** - Clear boundaries between concerns

---

## 📋 **MIGRATION CHECKLIST**

### **Phase 1: Create New Website Repositories (Week 1)**

#### **1.1 Buildly Website Migration**
**Source:** `buildly-website/` → **Target:** `buildly-io/website`

**Steps:**
```bash
# 1. Create new GitHub repository
# - Repository name: website
# - Organization: buildly-io (or personal account)
# - Initialize with README

# 2. Clone new repository locally
git clone https://github.com/buildly-io/website.git buildly-website-new

# 3. Copy website files (excluding automation)
cd buildly-website-new
cp -r ../buildly-website/*.html .
cp -r ../buildly-website/css .
cp -r ../buildly-website/js .
cp -r ../buildly-website/media .
cp -r ../buildly-website/includes .
cp -r ../buildly-website/articles .
cp -r ../buildly-website/demo .
cp -r ../buildly-website/docs .
cp -r ../buildly-website/templates .
cp ../buildly-website/package.json .
cp ../buildly-website/tailwind.config.js .
cp ../buildly-website/CNAME .
cp ../buildly-website/robots.txt .
cp ../buildly-website/sitemap.xml .

# 4. DO NOT COPY: google-apps-script/ (automation)

# 5. Set up GitHub Pages
# - Go to repository Settings > Pages
# - Source: Deploy from a branch  
# - Branch: main / (root)
# - Custom domain: buildly.io (if applicable)

# 6. Test deployment
# - Verify site loads at buildly-io.github.io
# - Test all pages and functionality
# - Check that all assets load correctly
```

**Verification:**
- [ ] All HTML pages load correctly
- [ ] CSS/JS assets work properly
- [ ] Images and media display correctly
- [ ] Contact forms work (if any)
- [ ] Google Analytics tracking continues
- [ ] Custom domain pointing works

#### **1.2 Foundry Website Migration**
**Source:** `foundry/*.html` → **Target:** `foundry-labs/website`

**Special Note:** Foundry is already on GitHub Pages and fully operational. Minimal changes needed.

**Steps:**
```bash
# 1. Verify current setup (already working)
# - Repository: foundry (existing)
# - Domain: firstcityfoundry.com (working)
# - Status: ✅ OPERATIONAL - DO NOT BREAK

# 2. Separate automation from website files
mkdir foundry-website-only
cp foundry/*.html foundry-website-only/
cp -r foundry/assets foundry-website-only/
cp foundry/CNAME foundry-website-only/
cp foundry/robots.txt foundry-website-only/
cp foundry/sitemap.xml foundry-website-only/
cp foundry/package.json foundry-website-only/

# 3. Keep automation in marketing automation project
# - Move foundry/scripts/ to automation/outreach/foundry/
# - Move foundry/daily_automation.py to automation/outreach/foundry/
# - Keep foundry/outreach_data/ in data/foundry/
```

**Critical:** This is the LIVE incubator site generating business results. Make changes carefully.

#### **1.3 Open Build Website Migration**
**Source:** `open-build-new-website/*.html` → **Target:** `open-build/website`

**Steps:**
```bash
# 1. Create new repository: open-build/website

# 2. Copy website files only
cp open-build-new-website/*.html open-build-website-new/
cp -r open-build-new-website/assets open-build-website-new/
cp -r open-build-new-website/blog open-build-website-new/
cp -r open-build-new-website/portfolios open-build-website-new/
cp open-build-new-website/package.json open-build-website-new/
cp open-build-new-website/tailwind.config.js open-build-website-new/
cp open-build-new-website/sw.js open-build-website-new/

# 3. DO NOT COPY automation files:
# - scripts/ (move to automation/outreach/open_build/)
# - *.db files (move to data/databases/)
# - create_day4_article.py (move to automation/content/)
# - google-apps-script.js (move to automation/content/)
```

#### **1.4 Radical Therapy Website Migration**
**Source:** `radical/*.html` → **Target:** `radical-therapy/website`

**Steps:**
```bash
# 1. Create new repository: radical-therapy/website

# 2. Copy website files only  
cp radical/*.html radical-therapy-website-new/
cp -r radical/assets radical-therapy-website-new/
cp radical/*.pdf radical-therapy-website-new/ # Book content

# 3. DO NOT COPY:
# - joke_tweet.py (move to automation/social/)
# - jokes.csv, jokes.json (move to automation/social/content/)
```

#### **1.5 Oregon Software Migration**
**Source:** `oregonsoftware/website/` → **Target:** `oregonsoftware/website`

**Steps:**
```bash
# 1. This is already properly structured
# 2. Create repository: oregonsoftware/website
# 3. Copy entire website/ folder contents
# 4. No automation to separate
```

---

## 🔧 **Phase 2: Consolidate Automation (Week 2)**

### **2.1 Move Outreach Automation**

#### **Foundry Outreach (CRITICAL - Fully Operational)**
```bash
# Source: foundry/scripts/, foundry/daily_automation.py
# Target: automation/outreach/foundry/

mkdir -p automation/outreach/foundry
cp -r foundry/scripts/* automation/outreach/foundry/
cp foundry/daily_automation.py automation/outreach/foundry/
cp foundry/run_automation.py automation/outreach/foundry/

# Move data
mkdir -p data/foundry
cp -r foundry/outreach_data/* data/foundry/
cp foundry/config.py config/foundry_config.py
```

#### **Open Build Outreach**
```bash
# Source: open-build-new-website/scripts/
# Target: automation/outreach/open_build/

mkdir -p automation/outreach/open_build
cp -r open-build-new-website/scripts/* automation/outreach/open_build/

# Move databases
cp open-build-new-website/*.db data/databases/
```

### **2.2 Consolidate Social Media Automation**
```bash
# Sources: Ads/, marketing/, radical/ Twitter scripts
# Target: automation/social/ (already created)

# Ads folder Twitter automation
cp Ads/tweet_scheduler.py automation/social/buildly_ads_legacy.py
cp Ads/tweets.py automation/social/buildly_content_legacy.py

# Marketing folder automation  
cp marketing/the_real_tweet.py automation/social/marketing_legacy.py

# Radical Therapy humor automation
cp radical/joke_tweet.py automation/social/radical_humor_legacy.py
cp radical/jokes.* automation/social/content/
```

### **2.3 Move Content Generation**
```bash
# Blog automation from open-build-website
cp open-build-new-website/create_day4_article.py automation/content/blog_generator.py
cp open-build-new-website/google-apps-script.js automation/content/google_apps_integration.js
```

---

## 🌐 **Phase 3: Update DNS and Domains (Week 3)**

### **3.1 Domain Configuration**
```yaml
# Update DNS records to point to new GitHub Pages:

buildly.io:
  current: Points to buildly-website GitHub Pages
  new: Points to buildly-io/website GitHub Pages
  action: Update CNAME record
  
firstcityfoundry.com:
  current: ✅ Already working (foundry GitHub Pages)
  action: No change needed
  
# New GitHub Pages domains:
open-build.github.io: 
  repository: open-build/website
  
radical-therapy.github.io:
  repository: radical-therapy/website
  
oregonsoftware.github.io:
  repository: oregonsoftware/website
```

### **3.2 Analytics Integration**
```javascript
// Ensure Google Analytics continues working across all sites
// Property ID: G-YFY5W80XQX

// Update automation/analytics/website_monitor.py with new URLs:
websites = {
    'buildly': 'https://buildly.io',  // or buildly-io.github.io
    'foundry': 'https://www.firstcityfoundry.com',  // No change
    'open_build': 'https://open-build.github.io',
    'radical_therapy': 'https://radical-therapy.github.io',
    'oregonsoftware': 'https://oregonsoftware.github.io'
}
```

---

## 🔗 **Phase 4: Integration Testing (Week 4)**

### **4.1 End-to-End Testing**
```bash
# Test website functionality
curl -I https://buildly.io  # Should return 200
curl -I https://www.firstcityfoundry.com  # Should return 200
curl -I https://open-build.github.io  # Should return 200

# Test automation integration
python automation/analytics/website_monitor.py
python automation/social/unified_twitter_manager.py --test
python dashboard/main_controller.py --status
```

### **4.2 Data Migration Verification**
```python
# Verify all data migrated correctly
import sqlite3

# Check database integrity
dbs = ['contacts.db', 'campaigns.db', 'analytics.db', 'content.db']
for db in dbs:
    conn = sqlite3.connect(f'data/databases/{db}')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"{db}: {len(tables)} tables")
    conn.close()
```

---

## ⚠️ **CRITICAL PRESERVATION REQUIREMENTS**

### **NEVER BREAK THESE:**

1. **Foundry Outreach System** 
   - Status: ✅ Fully operational, generating business results
   - Action: Move automation but preserve exact functionality
   - Test: Verify daily automation continues running after move

2. **Buildly Website**
   - Status: ✅ Production site (buildly.io)
   - Action: Seamless GitHub Pages migration
   - Test: All pages load, analytics continue, no broken links

3. **Google Analytics**
   - Property: G-YFY5W80XQX
   - Action: Ensure tracking continues across all migrated sites
   - Test: Verify events still fire after migration

### **ROLLBACK PLAN:**
If any migration fails:
```bash
# 1. Restore original folder structure
# 2. Update DNS back to original configuration  
# 3. Restart automation from original locations
# 4. Debug issues before re-attempting migration
```

---

## 📊 **SUCCESS METRICS**

### **Technical Success:**
- [ ] All websites load without errors
- [ ] Google Analytics data continues flowing  
- [ ] Automation runs without failures
- [ ] Zero downtime during migration
- [ ] All links and assets work correctly

### **Business Success:**
- [ ] Foundry outreach continues generating leads
- [ ] Social media posts maintain engagement
- [ ] Website traffic remains stable
- [ ] Contact forms continue working
- [ ] SEO rankings maintained

### **Operational Success:**
- [ ] Websites can be updated independently
- [ ] Automation runs from centralized location
- [ ] Dashboard monitors all sites successfully
- [ ] Team can manage sites efficiently
- [ ] Clear documentation for all systems

---

## 🚀 **POST-MIGRATION BENEFITS**

### **For Websites:**
- **Independent deployments** - Update sites without affecting automation
- **Focused repositories** - Clean, single-purpose repos
- **Better performance** - Optimized GitHub Pages hosting
- **Team collaboration** - Website teams work in dedicated repos

### **For Automation:**
- **Centralized control** - All automation in one place
- **Unified monitoring** - Single dashboard for all activities
- **Reduced duplication** - Consolidated Twitter/social automation
- **Better scalability** - Easy to add new brands or campaigns

### **For Development:**
- **Clear boundaries** - Website vs automation concerns separated  
- **Faster onboarding** - Developers focus on their domain
- **Better testing** - Independent CI/CD for websites and automation
- **Professional structure** - Industry-standard project organization

This migration transforms a collection of mixed-purpose folders into a professional, scalable marketing automation system with clean website deployment workflows.