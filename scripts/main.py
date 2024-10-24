import os
import subprocess

def run_script(script_name):
    """Execute a Python script."""
    try:
        subprocess.run(['python', script_name], check=True)
        print(f"Successfully executed {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}: {e}")

def main():
    # Define the order of script execution
    scripts_to_run = [
        'scripts/script_duckdb.py',  # Ingestion in DuckDB
        'scripts/scrape_agenda.py',  # Scrape agenda
        'scripts/scrape_details.py',  # Scrape details
        # Add other scripts as needed
    ]

    # Execute each script
    for script in scripts_to_run:
        run_script(script)

if __name__ == "__main__":
    main()
