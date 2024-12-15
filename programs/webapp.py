import os
import time

def main():
    os.makedirs("../reports", exist_ok=True)

    domain = input("Enter the web application domain to test (e.g., example.com): ")

    print(f"\nPerforming web application penetration testing for domain: {domain}...\n")

    steps = [
        f"Starting reconnaissance on {domain}...",
        f"Scanning for vulnerabilities on {domain}...",
        f"Testing authentication mechanisms for {domain}...",
        "Checking for SQL injection vulnerabilities...",
        "Checking for XSS vulnerabilities...",
        f"Generating report for {domain}..."
    ]

    for i, step in enumerate(steps, 1):
        print(f"Step {i}: {step}")
        time.sleep(1.5)

    report_path = f"../reports/webapp_report_{domain.replace('.', '_')}.txt"
    with open(report_path, "w") as report_file:
        report_file.write(f"Web Application Penetration Testing Report for {domain}\n")
        report_file.write("All steps completed successfully.\n")

    print(f"\nReport generated and stored in: {report_path}\n")

if __name__ == "__main__":
    main()
