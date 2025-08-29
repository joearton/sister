#!/usr/bin/env python3
"""
Sister API Client - Cache Management Utility

This script provides utilities to manage the cache system:
- View cache statistics
- Clean up expired cache
- Clear all cache
- Delete specific cache entries
"""

import sys
import os
import argparse
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(__file__))

def main():
    parser = argparse.ArgumentParser(
        description='Sister API Client Cache Management Utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cache_manager.py --stats                    # Show cache statistics
  python cache_manager.py --cleanup                 # Remove expired cache
  python cache_manager.py --clear                   # Clear all cache
  python cache_manager.py --delete "/referensi/sdm" # Delete specific cache
  python cache_manager.py --auto-cleanup            # Enable auto cleanup
        """
    )
    
    parser.add_argument('--stats', action='store_true',
                       help='Show cache statistics')
    parser.add_argument('--cleanup', action='store_true',
                       help='Remove expired cache entries')
    parser.add_argument('--clear', action='store_true',
                       help='Clear all cache entries')
    parser.add_argument('--delete', type=str, metavar='PATH',
                       help='Delete cache for specific path')
    parser.add_argument('--auto-cleanup', action='store_true',
                       help='Enable automatic cache cleanup')
    parser.add_argument('--disable-auto-cleanup', action='store_true',
                       help='Disable automatic cache cleanup')
    
    args = parser.parse_args()
    
    if not any([args.stats, args.cleanup, args.clear, args.delete, 
                args.auto_cleanup, args.disable_auto_cleanup]):
        parser.print_help()
        return
    
    try:
        from library.webservice import WebService
        
        # Initialize webservice
        ws = WebService()
        
        if args.stats:
            show_cache_stats(ws)
        
        elif args.cleanup:
            cleanup_expired_cache(ws)
        
        elif args.clear:
            clear_all_cache(ws)
        
        elif args.delete:
            delete_specific_cache(ws, args.delete)
        
        elif args.auto_cleanup:
            enable_auto_cleanup(ws, True)
        
        elif args.disable_auto_cleanup:
            enable_auto_cleanup(ws, False)
            
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("Make sure you're in the correct directory and virtual environment is activated")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def show_cache_stats(ws):
    """Display cache statistics"""
    print("📊 Cache Statistics")
    print("=" * 50)
    
    stats = ws.get_cache_stats()
    
    print(f"Total Cache Entries: {stats['total_cache_entries']}")
    print(f"Total Size: {stats['total_size_mb']} MB ({stats['total_size_bytes']} bytes)")
    
    if stats['total_cache_entries'] > 0:
        print("\n📁 Cache Directory:")
        cache_dir = os.path.join(os.path.dirname(__file__), '.cache')
        if os.path.exists(cache_dir):
            print(f"   {cache_dir}")
        else:
            print("   Cache directory does not exist")


def cleanup_expired_cache(ws):
    """Clean up expired cache entries"""
    print("🧹 Cleaning up expired cache...")
    
    result = ws.cleanup_expired_cache()
    
    print(f"✅ Cleanup completed!")
    print(f"   Expired entries removed: {result['expired_count']}")
    print(f"   Files removed: {len(result['removed_files'])}")
    print(f"   Remaining cache entries: {result['remaining_cache']}")
    
    if result['removed_files']:
        print("\n🗑️  Removed files:")
        for filepath in result['removed_files']:
            print(f"   - {os.path.basename(filepath)}")


def clear_all_cache(ws):
    """Clear all cache entries"""
    print("🗑️  Clearing all cache...")
    
    # Ask for confirmation
    response = input("Are you sure you want to clear ALL cache? (y/N): ")
    if response.lower() != 'y':
        print("❌ Cache clearing cancelled")
        return
    
    result = ws.clear_all_cache()
    
    print(f"✅ All cache cleared!")
    print(f"   Files removed: {result['removed_files']}")
    print(f"   Database cleared: {result['cleared_database']}")


def delete_specific_cache(ws, path):
    """Delete cache for specific path"""
    print(f"🗑️  Deleting cache for path: {path}")
    
    success = ws.delete_cache_by_path(path)
    
    if success:
        print(f"✅ Cache deleted for: {path}")
    else:
        print(f"❌ No cache found for: {path}")


def enable_auto_cleanup(ws, status):
    """Enable or disable automatic cache cleanup"""
    ws.enable_auto_cleanup(status)
    
    if status:
        print("✅ Automatic cache cleanup enabled")
        print("   Cache will be automatically cleaned on each API call")
    else:
        print("❌ Automatic cache cleanup disabled")
        print("   Cache will not be automatically cleaned")


if __name__ == "__main__":
    main()
