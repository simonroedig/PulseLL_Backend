import statistics
from icecream import ic

class VitalThresholdLogic:
    def __init__(self, change_threshold, window_size):
        self.heart_rate_history = []
        self.complete_heart_rate_history = []
        self.change_threshold = change_threshold  
        # number of heart rate readings included in each average calculation. 
        # With heart rate data received every 5 seconds, 
        # a window size of 5 readings covers 25 seconds of data.
        self.window_size = window_size  

    def set_append_heart_rate_and_time(self, heart_rate):
        self.heart_rate_history.append(heart_rate)
        self.complete_heart_rate_history.append(heart_rate)
        
        if len(self.heart_rate_history) > 100:  # limit size to last 100 readings
            self.heart_rate_history.pop(0)
            
    def get_current_median_heartrate(self, check_last_x_heart_rates):
        # Return median of the last x heart rates
        if len(self.complete_heart_rate_history) < check_last_x_heart_rates:
            # If there are fewer than x entries, return the most recent heart rate
            return self.complete_heart_rate_history[-1]

        # Calculate the median of the last x entries
        last_x_rates = self.complete_heart_rate_history[-check_last_x_heart_rates:]
        return statistics.median(last_x_rates)
        
    def has_significant_change_occurred(self):
        """
        My Logic:
        
        Time 0s: 70 bpm
        Time 5s: 72 bpm
        Time 10s: 74 bpm
        Time 15s: 73 bpm
        Time 20s: 75 bpm
        Time 25s: 80 bpm
        Time 30s: 85 bpm
        Time 35s: 86 bpm
        Time 40s: 87 bpm
        Time 45s: 88 bpm
        
        If window_size is 5:
        
        recent_average:
        Consider the most recent 5 readings: 80, 85, 86, 87, 88 bpm.
        Average = (80 + 85 + 86 + 87 + 88) / 5 = 85.2 bpm
        
        previous_average:
        Average = (70 + 72 + 74 + 73 + 75) / 5 = 72.8 b
        Consider the readings just before the most recent window: 70, 72, 74, 73, 75 bpm.pm
        
        Change = |85.2 bpm - 72.8 bpm| = 12.4 bpm
        
        Compare Change to Threshold 
        """
        # based on moving averages
        ic(self.heart_rate_history)
        if len(self.heart_rate_history) < 2 * self.window_size:
            return False
        
        # average of the last window_size heart rates
        recent_average = sum(self.heart_rate_history[-self.window_size:]) / self.window_size
        ic(recent_average)

        # average of the previous window_size heart rates before the last
        previous_average = sum(self.heart_rate_history[-2*self.window_size:-self.window_size]) / self.window_size
        ic(previous_average)

        # change in averages
        change = abs(recent_average - previous_average)
        ic(change)

        # reset the history if a significant change is detected
        if change >= self.change_threshold:
            #self.heart_rate_history = self.heart_rate_history[-self.window_size:]
            self.heart_rate_history = []
            print("Resetting history of the heart rate:")
            ic(self.heart_rate_history)

        # return True if the change is significant    
        return change >= self.change_threshold
    
    def reset(self):
        self.heart_rate_history = []
        self.complete_heart_rate_history = []
        print("Resetting history of the heart rate.")

    def create_hr_image(self):
        return
