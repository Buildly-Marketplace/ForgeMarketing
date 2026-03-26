#!/usr/bin/env python3
"""
Test Real Analytics Integration
==============================

Quick test to verify the real analytics system works correctly
and can be integrated into the dashboard.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_analytics_integration():
    """Test the real analytics integration"""
    print("🧪 Testing Real Analytics Integration")
    print("=" * 50)
    
    try:
        # Import the real analytics system
        from automation.real_analytics_dashboard import get_analytics_for_dashboard
        print("✅ Real analytics import successful")
        
        # Test multi-brand summary
        print("\n📊 Testing multi-brand analytics...")
        summary_data = get_analytics_for_dashboard()
        
        print(f"📈 Found {len(summary_data.get('brands', []))} brands")
        print(f"📊 Total sessions: {summary_data['summary']['total_sessions']:,}")
        print(f"📧 Total emails: {summary_data['summary']['total_emails']:,}")
        
        # Test specific brand
        print("\n🎯 Testing single brand analytics (buildly)...")
        buildly_data = get_analytics_for_dashboard('buildly')
        
        print(f"🌐 Website sessions: {buildly_data['website']['sessions']:,}")
        print(f"👥 Website users: {buildly_data['website']['users']:,}")
        print(f"📄 Page views: {buildly_data['website']['pageviews']:,}")
        print(f"⭐ Performance score: {buildly_data['performance']['score']}/10")
        print(f"📈 Performance rating: {buildly_data['performance']['rating']}")
        
        print(f"\n📑 Top pages tracked: {len(buildly_data['website']['top_pages'])}")
        for page_info in buildly_data['website']['top_pages'][:3]:
            print(f"  • {page_info['page']}: {page_info['sessions']} sessions")
        
        print(f"\n🚦 Traffic sources:")
        for source, visits in buildly_data['website']['traffic_sources'].items():
            print(f"  • {source.title()}: {visits} visits")
        
        print(f"\n💡 Recommendations:")
        for rec in buildly_data['performance']['recommendations'][:3]:
            print(f"  • {rec}")
        
        print("\n✅ All analytics tests passed!")
        print("\n🎉 Real analytics integration is working correctly!")
        print("📋 Dashboard can now show real website and email data!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == '__main__':
    success = test_analytics_integration()
    if success:
        print("\n🚀 Ready to use real analytics in dashboard!")
    else:
        print("\n⚠️  Analytics integration needs attention")