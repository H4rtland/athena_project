import pprint

from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter

import numpy as np

from execute_query import execute_query_by_id


query_id = "c6b2d559-02a7-4836-986d-5231746c99da"
database = "apfhistorylong"
output_location = "aws-athena-query-results-lancs"

result = execute_query_by_id(query_id, database, output_location)

bytes_scanned = result.query_metadata["QueryExecution"]["Statistics"]["DataScannedInBytes"]
execution_duration = result.query_metadata["QueryExecution"]["Statistics"]["EngineExecutionTimeInMillis"]


times = [datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f") for time in result.job_time]
total_jobs = np.array(list(map(int, result.total_jobs)))
short_jobs = np.array(list(map(int, result.short_jobs)))


long_jobs = total_jobs-short_jobs

fig, ax = plt.subplots()

ax.bar(times, short_jobs, color="red", width=1/24, align="edge", label="Short jobs")
ax.bar(times, long_jobs, color="blue", width=1/24, align="edge", bottom=short_jobs, label="Long jobs")

# Borders are only being drawn on the first bar because of a bug in matplotlib 2.1.0, waiting for next minor release to fix it
# https://github.com/matplotlib/matplotlib/issues/9351

#ax.bar(times, short_jobs, width=1/24, align="edge", edgecolor="black", linewidth=1, facecolor="None", ls="solid")
#ax.bar(times, long_jobs,  width=1/24, align="edge", edgecolor="black", linewidth=1, facecolor="None", bottom=short_jobs, ls="solid")

ax.set_xlabel("Time")
ax.set_ylabel("Jobs")

ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))

ax.legend()
plt.show()
