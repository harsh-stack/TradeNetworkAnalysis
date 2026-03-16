import pandas as pd
import matplotlib.pyplot as plt

def parse_pidstat(file_path):
    lines = []
    with open(file_path) as f:
        for line in f:
            # Skip headers, averages, and empty lines
            if line.strip() and not line.startswith("#") and not line.startswith("Linux") \
            and not line.startswith("UID") and not line.startswith("Average:"):
                parts = line.strip().split()
                # Only keep lines with at least 10 columns and a numeric PID
                if len(parts) >= 10 and parts[2].isdigit():
                    lines.append(parts)
    columns = ["Time", "UID", "PID", "%usr", "%system", "%guest", "%wait", "%CPU", "CPU", "Command"]
    df = pd.DataFrame(lines, columns=columns)
    for col in ["%usr", "%system", "%guest", "%wait", "%CPU"]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

if __name__ == "__main__":
    df = parse_pidstat("pidstat_80_output.txt")
    if df.empty:
        print("No valid CPU usage data found. Check input file and parsing.")
    else:
        # Group by Time and sum CPU for that timestamp
        df_grouped = df.groupby("Time")["%CPU"].sum().reset_index()
        plt.plot(df_grouped["Time"], df_grouped["%CPU"])
        plt.xlabel("Time")
        plt.ylabel("Total CPU Usage (%)")
        plt.title("Total CPU Usage Over Time from pidstat")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("cpu_usage_plot_80.png")
        print("Plot saved as cpu_usage_plot_80.png")
