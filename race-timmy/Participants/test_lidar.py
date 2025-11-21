#!/usr/bin/env python3
"""
LIDAR Test Utility
Helps you understand the LIDAR data format
"""

def visualize_lidar(lidar_data):
    """
    Print a simple ASCII visualization of LIDAR data
    """
    print("\n" + "="*60)
    print("LIDAR VISUALIZATION")
    print("="*60)
    
    # Show key angles
    print(f"\nKey Readings:")
    print(f"  Far Right (-45°):  {lidar_data[0]:.1f}")
    print(f"  Right (-25°):      {lidar_data[20]:.1f}")
    print(f"  Straight (0°):     {lidar_data[45]:.1f}")
    print(f"  Left (+25°):       {lidar_data[70]:.1f}")
    print(f"  Far Left (+45°):   {lidar_data[90]:.1f}")
    
    # ASCII visualization
    print(f"\nASCII View (top-down):")
    print("     LEFT          FRONT         RIGHT")
    
    # Create simple bar chart
    max_range = 50
    for angle_idx in [90, 80, 70, 60, 50, 45, 40, 30, 20, 10, 0]:
        distance = lidar_data[angle_idx]
        angle = angle_idx - 45  # Convert to degrees
        
        # Create bar
        bar_length = int((distance / max_range) * 30)
        bar = "█" * bar_length
        
        print(f"  {angle:+3d}° | {bar:<30} | {distance:.1f}")
    
    print("="*60 + "\n")


def test_lidar_understanding():
    """
    Interactive test to help understand LIDAR indexing
    """
    print("\n🎯 LIDAR Understanding Test\n")
    
    # Create sample data
    sample_data = [10.0] * 91  # All walls at distance 10
    sample_data[45] = 30.0      # Except straight ahead is clear
    sample_data[70] = 5.0       # Left side is close
    sample_data[20] = 15.0      # Right side is medium
    
    visualize_lidar(sample_data)
    
    print("Questions:")
    print("1. Which direction has the most space? (Answer: Straight ahead)")
    print("2. Which side is closer to a wall? (Answer: Left)")
    print("3. What index would you use for 30° left? (Answer: 45 + 30 = 75)")
    print("\nUse this script to test your understanding of the LIDAR data!")


if __name__ == "__main__":
    test_lidar_understanding()
