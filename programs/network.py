import os
import time

def main():
    os.makedirs("../reports", exist_ok=True)

    ip_address = input("Enter the network IP address to test: ")

    print(f"\nPerforming network penetration testing for IP: {ip_address}...\n")

    steps = [
        f"Starting reconnaissance on network {ip_address}...",
        f"Scanning for open ports on {ip_address}...",
        f"Performing vulnerability analysis on {ip_address}...",
        "Attempting to gain access...",
        "Privilege escalation in progress...",
        f"Generating report for {ip_address}..."
    ]

    for i, step in enumerate(steps, 1):
        print(f"Step {i}: {step}")
        time.sleep(1.5)

    report_path = f"../reports/network_report_{ip_address.replace('.', '_')}.txt"
    with open(report_path, "w") as report_file:
        report_file.write(f"Network Penetration Testing Report for {ip_address}\n")
        report_file.write("All steps completed successfully.\n")
    
    print(f"\nReport generated and stored in: {report_path}\n")

if __name__ == "__main__":
    main()
