
## 🔧 **Email System Architecture**

### **Working Systems (DO NOT BREAK):**
- `marketing/buildly_user_outreach.py` - MailerSend integration
- Individual brand automation scripts
- Brand-specific .env configurations

### **Integration Layer:**
- `dashboard/app.py` - Central dashboard
- Should route to existing working systems, not replace them

## 📋 **Session Startup Checklist**

**Before making ANY changes:**
1. ✅ Check if original marketing tools still work
2. ✅ Verify each brand's email configuration
3. ✅ Test individual components before integration
4. ✅ Document current working state

**When Debugging Email Issues:**
1. ✅ Check the correct .env file for the brand
2. ✅ Verify email service routing (Buildly=MailerSend, Others=Brevo)
3. ✅ Test the original marketing tools first
4. ✅ Don't assume configuration - always verify

## 🚨 **Common Pitfalls to Avoid**

1. **Configuration Mixing**: Don't use foundry .env for Buildly campaigns
2. **Service Confusion**: Remember Buildly ≠ Brevo (uses MailerSend)
3. **Integration Breaking**: Don't replace working tools, wrap them
4. **Repeated "Fixes"**: If you've "fixed" something 3+ times, the approach is wrong

## 🎯 **Brand-Specific Details**

### **Buildly** (buildly.io):
- **Email Service**: MailerSend API
- **Config Location**: `websites/buildly-website/.env` or `marketing/` folder
- **Test Email**: greg@buildly.io (primary contact)
- **Working Tool**: `marketing/buildly_user_outreach.py`

### **Foundry** (firstcityfoundry.com):
- **Email Service**: Brevo SMTP 
- **Config Location**: `websites/foundry-website/.env`
- **Working Tools**: Foundry automation scripts

### **Open Build** (open.build):
- **Email Service**: Brevo SMTP
- **Verified Sender**: team@open.build

## 🔄 **Systematic Debugging Process**

1. **Isolate**: Test individual brand tools separately
2. **Verify**: Confirm email service routing is correct
3. **Integrate**: Only after individual components work
4. **Document**: Record what works/breaks at each step

## 💡 **Key Lessons Learned**

- **Email delivery issues**: Usually configuration routing, not credentials
- **Dashboard integration**: Should enhance, not replace working tools  
- **Multi-brand systems**: Each brand needs its own email service respect
- **Testing approach**: Bottom-up (individual → integrated)

---

**REMINDER**: Read this document at the start of each session before making changes!