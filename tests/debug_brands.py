#!/usr/bin/env python3
"""
Debug Brand Configuration Loading
"""

import sys
from pathlib import Path
import yaml

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def debug_brand_configs():
    """Debug brand configuration loading"""
    
    templates_dir = project_root / 'templates'
    brands_dir = templates_dir / 'brands'
    
    print("🔍 Debugging Brand Configuration Loading")
    print("=" * 50)
    
    print(f"Templates dir exists: {templates_dir.exists()}")
    print(f"Brands dir exists: {brands_dir.exists()}")
    
    if brands_dir.exists():
        print("\n📁 Brand directories found:")
        for brand_dir in brands_dir.iterdir():
            if brand_dir.is_dir():
                print(f"  - {brand_dir.name}")
                config_file = brand_dir / 'brand_config.yaml'
                print(f"    Config file exists: {config_file.exists()}")
                
                if config_file.exists():
                    try:
                        with open(config_file, 'r') as f:
                            config = yaml.safe_load(f)
                        print(f"    ✅ Config loaded successfully")
                        print(f"    Top-level keys: {list(config.keys())}")
                        
                        if 'brand' in config:
                            brand_info = config['brand']
                            print(f"    Brand info keys: {list(brand_info.keys())}")
                            print(f"    Brand name: {brand_info.get('name', 'Not found')}")
                        else:
                            print(f"    ❌ 'brand' key not found in config")
                        
                    except Exception as e:
                        print(f"    ❌ Error loading config: {e}")
    
    # Test loading with the actual method
    print("\n🧠 Testing AIContentGenerator loading...")
    try:
        from automation.ai.ollama_integration import AIContentGenerator
        
        generator = AIContentGenerator()
        print(f"Brand configs loaded: {list(generator.brand_configs.keys())}")
        
        for brand_name, config in generator.brand_configs.items():
            print(f"\n📋 {brand_name} configuration:")
            print(f"  Top-level keys: {list(config.keys())}")
            if 'brand' in config:
                brand_info = config['brand']
                print(f"  Brand name: {brand_info.get('name', 'Not found')}")
                print(f"  Brand description: {brand_info.get('description', 'Not found')}")
            
    except Exception as e:
        print(f"❌ Error testing AIContentGenerator: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_brand_configs()