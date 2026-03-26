#!/usr/bin/env python3
"""
Unified Outreach Automation Runner
This script is referenced in the existing crontab and runs unified outreach campaigns across all brands
"""

import os
import sys
import subprocess
import logging
from datetime import datetime
from pathlib import Path

# Get project root directory
project_root = Path(__file__).parent.parent

# Add project root to Python path for imports
sys.path.insert(0, str(project_root))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(project_root / 'logs' / 'unified_outreach.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('UnifiedOutreach')

def run_foundry_automation():
    """Run Foundry daily automation"""
    try:
        foundry_script = project_root / 'foundry' / 'scripts' / 'daily_automation.py'
        if foundry_script.exists():
            logger.info("🚀 Running Foundry daily automation...")
            result = subprocess.run([
                sys.executable, str(foundry_script)
            ], capture_output=True, text=True, cwd=str(project_root / 'foundry'))
            
            if result.returncode == 0:
                logger.info("✅ Foundry automation completed successfully")
                return True
            else:
                logger.error(f"❌ Foundry automation failed: {result.stderr}")
                return False
        else:
            logger.warning(f"⚠️ Foundry automation script not found: {foundry_script}")
            return False
    except Exception as e:
        logger.error(f"❌ Error running Foundry automation: {e}")
        return False

def run_open_build_automation():
    """Run Open Build daily automation"""
    try:
        open_build_script = project_root / 'open-build-new-website' / 'scripts' / 'run_daily_automation.sh'
        if open_build_script.exists():
            logger.info("🚀 Running Open Build daily automation...")
            result = subprocess.run([
                'bash', str(open_build_script)
            ], capture_output=True, text=True, cwd=str(project_root / 'open-build-new-website'))
            
            if result.returncode == 0:
                logger.info("✅ Open Build automation completed successfully")
                return True
            else:
                logger.error(f"❌ Open Build automation failed: {result.stderr}")
                return False
        else:
            logger.warning(f"⚠️ Open Build automation script not found: {open_build_script}")
            return False
    except Exception as e:
        logger.error(f"❌ Error running Open Build automation: {e}")
        return False

def run_unified_outreach():
    """Run unified multi-brand outreach campaign"""
    try:
        # Import the outreach system
        from automation.multi_brand_outreach import MultiBrandOutreachCampaign
        
        logger.info("🚀 Running unified multi-brand outreach campaign...")
        
        # Initialize outreach system
        outreach = MultiBrandOutreachCampaign()
        
        # Run campaign for all configured brands
        results = outreach.run_daily_campaigns()
        
        success_count = sum(1 for result in results.values() if result.get('success', False))
        total_brands = len(results)
        
        logger.info(f"✅ Unified outreach completed: {success_count}/{total_brands} brands successful")
        
        return success_count > 0
        
    except Exception as e:
        logger.error(f"❌ Error running unified outreach: {e}")
        return False

def send_execution_report(success_results: dict):
    """Send execution report via email"""
    try:
        from automation.daily_analytics_emailer import DailyAnalyticsEmailer
        
        emailer = DailyAnalyticsEmailer()
        
        # Prepare report content
        total_automations = len(success_results)
        successful_automations = sum(success_results.values())
        
        report_content = f"""
        Daily Marketing Automation Report
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Execution Summary:
        - Total Automations: {total_automations}
        - Successful: {successful_automations}
        - Failed: {total_automations - successful_automations}
        - Success Rate: {(successful_automations/total_automations)*100:.1f}%
        
        Automation Results:
        """
        
        for automation, success in success_results.items():
            status = "✅ Success" if success else "❌ Failed"
            report_content += f"- {automation}: {status}\n"
        
        # Send report
        emailer.send_daily_report(
            subject=f"Marketing Automation Daily Report - {datetime.now().strftime('%Y-%m-%d')}",
            content=report_content,
            recipients=['greg@buildly.io']  # Configure as needed
        )
        
        logger.info("📧 Execution report sent successfully")
        
    except Exception as e:
        logger.error(f"❌ Error sending execution report: {e}")

def main():
    """Main unified outreach automation runner"""
    logger.info("🎯 Starting unified marketing automation pipeline")
    
    # Track execution results
    execution_results = {}
    
    # Run individual website automations
    execution_results['Foundry Daily'] = run_foundry_automation()
    execution_results['Open Build Daily'] = run_open_build_automation()
    
    # Run unified outreach campaign
    execution_results['Unified Outreach'] = run_unified_outreach()
    
    # Calculate overall success
    successful_count = sum(execution_results.values())
    total_count = len(execution_results)
    
    # Send execution report
    send_execution_report(execution_results)
    
    # Log final results
    if successful_count == total_count:
        logger.info(f"🎉 All automations completed successfully ({successful_count}/{total_count})")
        sys.exit(0)
    elif successful_count > 0:
        logger.warning(f"⚠️ Partial success: {successful_count}/{total_count} automations completed")
        sys.exit(1)
    else:
        logger.error(f"❌ All automations failed ({successful_count}/{total_count})")
        sys.exit(2)

if __name__ == "__main__":
    main()