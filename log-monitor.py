import sys
import signal
import re
import time

def monitor_log(log_file):
    try:
        with open(log_file, 'r') as file:
            file.seek(0, 2)  # Move to the end of the file
            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.1)  # Wait for new log entries
                    continue
                print(line.strip())  # Display the new log entry
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
        sys.exit(0)
    except FileNotFoundError:
        print("Error: Log file not found.")
        sys.exit(1)

def analyze_log(log_file, keywords):
    try:
        keyword_counts = {keyword: 0 for keyword in keywords}
        with open(log_file, 'r') as file:
            for line in file:
                for keyword in keywords:
                    if re.search(keyword, line):
                        keyword_counts[keyword] += 1
        print("Log analysis summary:")
        for keyword, count in keyword_counts.items():
            print(f"{keyword}: {count} occurrences")
    except FileNotFoundError:
        print("Error: Log file not found.")
        sys.exit(1)

def signal_handler(signal, frame):
    print("\nMonitoring stopped.")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python log_monitor.py <log_file> <keyword1> [<keyword2> ...]")
        sys.exit(1)

    log_file = sys.argv[1]
    keywords = sys.argv[2:]

    signal.signal(signal.SIGINT, signal_handler)

    print(f"Monitoring log file: {log_file}")
    monitor_log(log_file)

    # Perform log analysis once monitoring is stopped
    analyze_log(log_file, keywords)
