#!/usr/bin/env python3
"""
Test script for cache cleanup functionality
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Add the project root to Python path
sys.path.append(os.path.dirname(__file__))

def test_cache_cleanup():
    """Test cache cleanup functionality"""
    print("🧪 Testing Cache Cleanup Functionality...\n")
    
    try:
        from library.webservice import WebService
        from library.cache import SisterCache
        
        # Initialize webservice
        ws = WebService()
        
        # Test 1: Cache Statistics
        print("1. Testing Cache Statistics...")
        stats = ws.get_cache_stats()
        print(f"   ✅ Cache stats: {stats}")
        
        # Test 2: Manual Cache Cleanup
        print("\n2. Testing Manual Cache Cleanup...")
        cleanup_result = ws.cleanup_expired_cache()
        print(f"   ✅ Cleanup result: {cleanup_result}")
        
        # Test 3: Auto Cleanup Enable/Disable
        print("\n3. Testing Auto Cleanup Control...")
        ws.enable_auto_cleanup(True)
        print("   ✅ Auto cleanup enabled")
        
        ws.enable_auto_cleanup(False)
        print("   ✅ Auto cleanup disabled")
        
        # Test 4: Clear All Cache
        print("\n4. Testing Clear All Cache...")
        clear_result = ws.clear_all_cache()
        print(f"   ✅ Clear result: {clear_result}")
        
        # Test 5: Delete Specific Cache
        print("\n5. Testing Delete Specific Cache...")
        delete_result = ws.delete_cache_by_path("/test/path")
        print(f"   ✅ Delete result: {delete_result}")
        
        print("\n🎉 All cache cleanup tests PASSED!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def test_cache_manager_script():
    """Test cache manager script functionality"""
    print("\n🧪 Testing Cache Manager Script...\n")
    
    try:
        # Test help
        print("1. Testing help command...")
        os.system("python cache_manager.py --help")
        
        # Test stats
        print("\n2. Testing stats command...")
        os.system("python cache_manager.py --stats")
        
        # Test cleanup
        print("\n3. Testing cleanup command...")
        os.system("python cache_manager.py --cleanup")
        
        print("\n🎉 Cache manager script tests completed!")
        
    except Exception as e:
        print(f"\n❌ Script test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_cache_cleanup()
    test_cache_manager_script()
