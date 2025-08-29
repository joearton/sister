#!/usr/bin/env python3
"""
Test script to verify bug fixes in Sister API client
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(__file__))

def test_bearer_auth_fix():
    """Test BearerAuth header fix"""
    print("Testing BearerAuth header fix...")
    from library.connector import BearerAuth
    import requests
    
    # Create a mock request
    req = requests.Request('GET', 'http://example.com')
    req = req.prepare()
    
    # Apply BearerAuth
    auth = BearerAuth("test_token")
    auth(req)
    
    # Check headers
    assert req.headers["Accept"] == "application/json"
    assert req.headers["Authorization"] == "Bearer test_token"
    print("✅ BearerAuth header fix: PASSED")

def test_template_fixes():
    """Test template.py fixes"""
    print("Testing template.py fixes...")
    from library.template import SisterTemplate
    
    template = SisterTemplate()
    
    # Test get_now_datetime with isoformat
    dt_iso = template.get_now_datetime(isoformat=True)
    assert isinstance(dt_iso, str)
    assert 'T' in dt_iso or '-' in dt_iso
    
    # Test get_expired_datetime with isoformat
    expired_iso = template.get_expired_datetime(isoformat=True, days=1)
    assert isinstance(expired_iso, str)
    
    # Test is_json with specific exceptions
    assert template.is_json('{"test": "value"}') == {"test": "value"}
    assert template.is_json('invalid json') == {}
    print("✅ Template fixes: PASSED")

def test_io_fixes():
    """Test io.py fixes"""
    print("Testing io.py fixes...")
    from library.io import SisterIO
    
    io = SisterIO()
    
    # Test parse_path_url with invalid input
    try:
        io.parse_path_url("")
        assert False, "Should raise ValueError for empty path"
    except ValueError:
        pass
    
    try:
        io.parse_path_url(None)
        assert False, "Should raise ValueError for None path"
    except ValueError:
        pass
    
    print("✅ IO fixes: PASSED")

def test_api_spec_fixes():
    """Test api_spec.py fixes"""
    print("Testing api_spec.py fixes...")
    from library.api_spec import SisterSpec
    
    spec = SisterSpec()
    
    # Test get_path_method_and_attr with invalid path
    try:
        spec.get_path_method_and_attr("/invalid/path")
        assert False, "Should raise ValueError for invalid path"
    except ValueError:
        pass
    
    print("✅ API spec fixes: PASSED")

def test_webservice_fixes():
    """Test webservice.py fixes"""
    print("Testing webservice.py fixes...")
    from library.webservice import WebService
    
    # Test input validation
    ws = WebService()
    
    # Test with invalid path
    response = ws.get_data("")
    assert response['message'] == 'Invalid path parameter'
    assert not response['status']
    
    response = ws.get_data(None)
    assert response['message'] == 'Invalid path parameter'
    assert not response['status']
    
    print("✅ WebService fixes: PASSED")

def test_cache_fixes():
    """Test cache.py fixes"""
    print("Testing cache.py fixes...")
    from library.cache import CacheAsJson
    
    cache = CacheAsJson()
    
    # Test basic operations
    test_data = {
        'id': 'test_id',
        'data': {'test': 'value'},
        'accessed_at': datetime.now().isoformat(),
        'expired_at': datetime.now().isoformat()
    }
    
    # Test save and get
    cache.save(test_data)
    retrieved = cache.get('test_id')
    assert retrieved['data'] == test_data['data']
    
    # Test delete
    cache.delete('test_id')
    deleted = cache.get('test_id')
    assert not deleted
    
    print("✅ Cache fixes: PASSED")

def main():
    """Run all tests"""
    print("🧪 Running Sister API Client Bug Fix Tests...\n")
    
    try:
        test_bearer_auth_fix()
        test_template_fixes()
        test_io_fixes()
        test_api_spec_fixes()
        test_webservice_fixes()
        test_cache_fixes()
        
        print("\n🎉 All tests PASSED! All bugs have been fixed successfully.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
