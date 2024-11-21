import re
import matplotlib.pyplot as plt


log_file_path = "operations.log"
with open(log_file_path, "r") as log_file:
    log_data = log_file.read()

pattern = re.compile(r"(\w+Service\.\w+)\savg\sexecution\stime:\s(\d+\.\d+)\sseconds")
matches = pattern.findall(log_data)

services, avg_execution_times = zip(*matches)
avg_execution_times = [float(time) for time in avg_execution_times]

plt.bar(services, avg_execution_times, color=["green", "navy", "green", "navy"])
plt.xlabel("Databases and Operations")
plt.ylabel("Average Execution Time (seconds)")
plt.title("Average Execution Time of Operations in MongoDB and PostgreSQL")
plt.show()
