# Release Notes

## Version 1.0.0 (November 14, 2025)

**First stable release of ForgeMark - ForgeMark AI Marketing Automation.**

### Major Features

#### Multi-Brand Management
- Unified dashboard for Buildly, The Foundry, Open Build, and Radical Therapy
- Brand-specific configuration and messaging templates
- Centralized contact and campaign management

#### AI-Powered Content Generation
- Local Ollama integration for unlimited content generation
- Support for multiple LLM models (Mistral, Llama2, Neural-Chat)
- Template-driven content with brand voice consistency
- Real-time content preview and refinement

#### Email Marketing Automation
- Brevo/Sendinblue integration for reliable delivery
- Email campaign scheduling and automation
- Delivery tracking and analytics
- A/B testing support for subject lines and content

#### Social Media Publishing
- Multi-platform support (Twitter/X, Mastodon, Bluesky)
- Scheduled posting across brands
- Social media analytics and engagement tracking
- Influencer discovery and outreach workflow

#### Google Ads Integration
- Campaign creation and bidding strategy management
- Performance reporting and optimization
- Budget tracking across brands

#### Analytics Dashboard
- Real-time performance metrics
- Campaign ROI calculation
- Cross-brand performance comparison
- Customizable reports

### Technical

- **Python 3.8+** with async/await support
- **Flask** web framework for API and dashboard
- **SQLite/PostgreSQL** for data persistence
- **Docker & Kubernetes** ready for enterprise deployment
- **GitHub Actions** CI/CD pipeline

### Breaking Changes

None - this is the first stable release.

### Known Limitations

- Ollama AI generation depends on model availability and speed
- Brevo rate limits apply (300 requests/minute)
- Dashboard real-time updates limited to 30-second refresh interval
- Single-server deployments limited to ~1000 concurrent contacts

### Upgrading

Not applicable for first release.

### Fixed Issues

- Resolved email delivery tracking for Brevo webhooks
- Fixed multi-brand contact deduplication
- Corrected timezone handling in campaign scheduling

### Contributors

- Buildly Labs Engineering Team

### Support

- Community support via GitHub Issues
- Premium support available through Buildly Forge
- See **SUPPORT.md** for details

---

**For detailed release history, see CHANGELOG.md**
