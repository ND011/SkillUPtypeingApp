#!/usr/bin/env python3
"""
Test script to check database contents and leaderboard
"""

from game.database_manager import DatabaseManager

def test_database():
    """Test database contents"""
    print("🔍 Testing Database Contents")
    print("=" * 40)
    
    # Create database manager
    db_manager = DatabaseManager()
    db_manager.initialize()
    
    # Get leaderboard
    print("📊 Getting leaderboard...")
    leaderboard = db_manager.get_leaderboard(limit=10)
    
    if leaderboard:
        print(f"✅ Found {len(leaderboard)} records in leaderboard:")
        print()
        print("Rank | Name       | WPM   | Accuracy | Mode           | Date")
        print("-" * 65)
        
        for i, score in enumerate(leaderboard, 1):
            print(f"{i:4} | {score.user_name:10} | {score.wpm:5.1f} | {score.accuracy:7.1f}% | {score.mode:14} | {score.date.strftime('%Y-%m-%d %H:%M')}")
    else:
        print("❌ No records found in leaderboard!")
    
    # Test direct database query
    print("\n🔍 Direct database query:")
    try:
        cursor = db_manager.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM scores")
        count = cursor.fetchone()[0]
        print(f"Total records in database: {count}")
        
        cursor.execute("SELECT user_name, wpm, accuracy, mode FROM scores ORDER BY wpm DESC LIMIT 5")
        rows = cursor.fetchall()
        print("Top 5 records:")
        for row in rows:
            print(f"  {row[0]} - {row[1]:.1f} WPM, {row[2]:.1f}% accuracy, {row[3]}")
            
    except Exception as e:
        print(f"❌ Database query error: {e}")
    
    db_manager.close()

if __name__ == "__main__":
    test_database()