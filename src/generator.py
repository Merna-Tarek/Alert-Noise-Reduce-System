import pandas as pd
import random
from datetime import datetime, timedelta
import os


def generate_realistic_siem_logs(num_logs=500, output_file='data/generated_siem_logs.csv'):
    # === Setup ===
    public_ips = [
        "45.83.123.{}", "185.191.102.{}", "198.51.100.{}", "203.0.113.{}", "103.21.244.{}"
    ]
    internal_subnets = ["192.168.{}.{}", "10.0.{}.{}", "172.16.{}.{}"]
    device_types = ["Firewall", "EDR", "SIEM", "Email Gateway", "Web Proxy"]
    alert_templates = [
        "Failed login attempt from {src} to {dst} via RDP",
        "Brute-force detected from {src} targeting {dst} SSH port",
        "Suspicious PowerShell execution on {dst} from {src}",
        "Outbound connection to known malicious IP {dst} from host {src}",
        "Large data upload from {src} to external IP {dst} ({bytes} bytes)",
        "Lateral movement attempt from {src} to {dst}",
        "Access to known phishing domain detected from {src}",
        "Unusual login time detected for user from {src} to {dst}",
        "Multiple malware signatures triggered on {dst}",
        "USB device connected to {dst} during restricted hours"
    ]

    def get_ip(internal=True):
        if internal:
            subnet = random.choice(internal_subnets)
        else:
            subnet = random.choice(public_ips)
        return subnet.format(random.randint(0, 255), random.randint(1, 254))

    logs = []
    base_time = datetime(2025, 7, 23, 8, 0, 0)

    for _ in range(num_logs):
        timestamp = base_time + timedelta(seconds=random.randint(0, 3600 * 5))
        source_internal = random.random() < 0.7
        source_ip = get_ip(internal=source_internal)
        dest_ip = get_ip(internal=True)

        device = random.choice(device_types)
        severity = random.choices(["low", "medium", "high"], weights=[0.5, 0.3, 0.2])[0]

        # Simulate event type
        bytes_sent = random.randint(200, 200000)
        template = random.choice(alert_templates)
        description = template.format(src=source_ip, dst=dest_ip, bytes=bytes_sent)

        logs.append({
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "source_ip": source_ip,
            "destination_ip": dest_ip,
            "device_type": device,
            "severity": severity,
            "bytes_sent": bytes_sent,
            "alert_description": description
        })

    df = pd.DataFrame(logs)

    # Ensure folder exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"✅ Generated {num_logs} realistic SIEM alerts in '{output_file}'")
    return output_file


if __name__ == "__main__":
    generate_realistic_siem_logs()
