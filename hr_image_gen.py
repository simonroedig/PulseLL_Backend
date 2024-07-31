import statistics
from icecream import ic
import datetime
import matplotlib.pyplot as plt
import os
import time

class VitalThresholdLogic:
    def __init__(self):
        self.complete_heart_rate_history = []
        self.complete_timestamp_history = []

    def create_hr_image(self, user_id):
        # Check if there is data to plot
        if not self.complete_heart_rate_history or not self.complete_timestamp_history:
            print("No data to plot")
            return
        
        # Convert UNIX timestamps to human-readable time
        times = [datetime.datetime.fromtimestamp(ts) for ts in self.complete_timestamp_history]
        
        # Create the plot
        plt.figure(figsize=(10, 5))
        plt.plot(times, self.complete_heart_rate_history, marker='o')
        
        # Format the plot
        plt.xlabel('Time')
        plt.ylabel('Heart Rate')
        plt.title(f"Your Activity on Day {times[0].strftime('%Y-%m-%d')}")
        plt.grid(True)
        
        # Create directory if it doesn't exist
        output_dir = "heart_rate_images"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the plot
        output_path = os.path.join(output_dir, f"id_{user_id}_heart_rate_{times[0].strftime('%Y%m%d')}.png")
        plt.savefig(output_path)
        plt.close()
        
        print(f"Heart rate image saved to {output_path}")


# Example usage with 30 values
vtl = VitalThresholdLogic()
vtl.complete_heart_rate_history = [
    120, 122, 119, 123, 121, 125, 130, 128, 126, 127, 
    124, 129, 131, 132, 134, 135, 133, 136, 137, 138, 
    140, 139, 141, 142, 143, 145, 144, 146, 147, 148
]

# Generating 30 UNIX timestamps, one per second starting from the current time
start_time = int(time.time())
vtl.complete_timestamp_history = [start_time + i for i in range(30)]

user_id = 2374856783
vtl.create_hr_image(user_id)