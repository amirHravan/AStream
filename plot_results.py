import json
import os

import matplotlib.pyplot as plt
import pandas as pd

# Configuration
LOG_DIR = "dist/client/ASTREAM_LOGS"
SCENARIOS = {
    "1": {"id": "2025-12-02.19_36_47", "desc": "Scenario 1: Short, No Proxy"},
    "2": {"id": "2025-12-02.19_56_26", "desc": "Scenario 2: Short, Proxy"},
    "3": {"id": "2025-12-02.20_09_20", "desc": "Scenario 3: Long, No Proxy"},
    "4": {"id": "2025-12-02.20_22_42", "desc": "Scenario 4: Long, Proxy"},
}


def load_data(run_id):
    json_file = os.path.join(LOG_DIR, f"ASTREAM_{run_id}.json")
    csv_file = os.path.join(LOG_DIR, f"DASH_BUFFER_LOG_{run_id}.csv")

    data = {}

    # Load CSV
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        # Normalize time
        if not df.empty:
            start_time = df["EpochTime"].iloc[0]
            df["Time"] = df["EpochTime"] - start_time
        data["csv"] = df
    else:
        data["csv"] = None

    # Load JSON
    if os.path.exists(json_file):
        try:
            with open(json_file, "r") as f:
                content = f.read()
                if content.strip():
                    json_data = json.loads(content)
                    if json_data and "segment_info" in json_data:
                        data["json"] = json_data
                    else:
                        data["json"] = None
                else:
                    data["json"] = None
        except json.JSONDecodeError:
            data["json"] = None
    else:
        data["json"] = None

    return data


def plot_individual(scenario_key, data):
    run_id = SCENARIOS[scenario_key]["id"]
    desc = SCENARIOS[scenario_key]["desc"]

    df_csv = data["csv"]
    json_data = data["json"]

    if df_csv is None:
        print(f"No CSV data for {desc}")
        return

    # Determine how many subplots
    if json_data:
        fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=False)

        # Parse segments
        segment_info = json_data["segment_info"]
        # segment_info structure: [filename, bitrate, size, duration]
        df_seg = pd.DataFrame(
            segment_info, columns=["filename", "bitrate", "size", "duration"]
        )
        df_seg["segment_index"] = df_seg.index + 1
        df_seg["download_rate"] = (
            (df_seg["size"] * 8) / df_seg["duration"] / 1e6
        )  # Mbps

        # 1. Bitrate (Segments)
        axes[0].plot(df_seg["segment_index"], df_seg["bitrate"] / 1e6, marker="o")
        axes[0].set_title(f"Bitrate per Segment - {desc}")
        axes[0].set_ylabel("Bitrate (Mbps)")
        axes[0].set_xlabel("Segment Index")
        axes[0].grid(True)

        # 2. Buffer (Time)
        axes[1].plot(df_csv["Time"], df_csv["CurrentBufferSize"], color="orange")
        axes[1].set_title(f"Buffer Size - {desc}")
        axes[1].set_ylabel("Buffer (Segments)")
        axes[1].set_xlabel("Time (s)")
        axes[1].grid(True)

        # 3. Download Rate (Segments)
        axes[2].plot(
            df_seg["segment_index"], df_seg["download_rate"], color="green", marker="x"
        )
        axes[2].set_title(f"Download Rate - {desc}")
        axes[2].set_ylabel("Rate (Mbps)")
        axes[2].set_xlabel("Segment Index")
        axes[2].grid(True)

    else:
        # Fallback to CSV only
        fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        # 1. Bitrate (Time)
        axes[0].plot(df_csv["Time"], df_csv["Bitrate"] / 1e6, drawstyle="steps-post")
        axes[0].set_title(f"Bitrate over Time - {desc}")
        axes[0].set_ylabel("Bitrate (Mbps)")
        axes[0].grid(True)

        # 2. Buffer (Time)
        axes[1].plot(df_csv["Time"], df_csv["CurrentBufferSize"], color="orange")
        axes[1].set_title(f"Buffer Size - {desc}")
        axes[1].set_ylabel("Buffer (Segments)")
        axes[1].set_xlabel("Time (s)")
        axes[1].grid(True)

    plt.tight_layout()
    os.makedirs("plots", exist_ok=True)
    output_path = f"plots/scenario_{scenario_key}.png"
    plt.savefig(output_path)
    plt.close()
    print(f"Saved {output_path}")


def plot_comparison(scenario_keys, title, filename):
    plt.figure(figsize=(12, 6))

    for key in scenario_keys:
        data = load_data(SCENARIOS[key]["id"])
        df = data["csv"]
        desc = SCENARIOS[key]["desc"]
        if df is not None and not df.empty:
            plt.plot(df["Time"], df["CurrentBufferSize"], label=desc)

    plt.title(f"Buffer Size Comparison: {title}")
    plt.xlabel("Time (s)")
    plt.ylabel("Buffer Size (segments)")
    plt.legend()
    plt.grid(True)

    os.makedirs("plots", exist_ok=True)
    output_path = f"plots/{filename}"
    plt.savefig(output_path)
    plt.close()
    print(f"Saved {output_path}")


def main():
    # Load all data
    all_data = {}
    for key in SCENARIOS:
        all_data[key] = load_data(SCENARIOS[key]["id"])

    # Plot Individual
    for key, data in all_data.items():
        plot_individual(key, data)

    # Plot Comparisons
    plot_comparison(["1", "2"], "Short Video (No Proxy vs Proxy)", "compare_1_2.png")
    plot_comparison(["3", "4"], "Long Video (No Proxy vs Proxy)", "compare_3_4.png")
    plot_comparison(["1", "2", "3", "4"], "All Scenarios", "compare_all.png")


if __name__ == "__main__":
    main()
