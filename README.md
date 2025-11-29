# 📅 CaseWork Scheduler

A smart tool to distribute casework among managers while respecting daily capacities and target distribution ratios.

## 🚀 Features

-   **Automatic Scheduling**: Distributes cases to match a target ratio (e.g., 2:3:5) and fits them into daily limits.
-   **Calendar Integration**: Maps the schedule to real dates, skipping weekends and holidays.
-   **Manager Configuration**: Easily adjust team members, limits, and ratios via the UI or by uploading a file.
-   **QC Dashboard**: Built-in validation to ensure every case is accounted for.
-   **Excel Compatible**: Works directly with your existing Excel files.

## 🛠️ Installation (For Beginners)

### 1. Install Python
If you don't have Python installed:
1.  Go to [python.org/downloads](https://www.python.org/downloads/).
2.  Download and install the latest version for your system (macOS or Windows).
3.  **Important**: During installation, check the box that says **"Add Python to PATH"**.

### 2. Download this Project
Download the code (or clone this repository) to a folder on your computer.

### 3. Setup & Run
I have included a helper script to make this easy.

**On macOS / Linux:**
1.  Open your Terminal.
2.  Navigate to the folder: `cd /path/to/folder`
3.  Run the app:
    ```bash
    sh run_app.sh
    ```

**On Windows:**
1.  Double-click `run_app.bat` (if created) or run in Command Prompt:
    ```cmd
    python app.py
    ```

## 📖 How to Use

1.  **Upload Casework**: Upload your Excel file. It must have columns: `Case Code` and `Billing Amount`.
2.  **Configure Managers**:
    -   Edit the table directly to change names, max loads, or ratios.
    -   OR upload a config file (Excel/CSV) in the "Upload Manager Config" section.
3.  **Set Dates**: Open "Calendar Configuration" to pick a start date and add holidays.
4.  **Generate**: Click **🚀 Generate Schedule**.
5.  **Review & Download**:
    -   Check the **QC Dashboard** at the bottom to verify the numbers.
    -   Download the **Schedule** Excel file.

## 📂 Input File Formats

**Casework File (Excel):**
| Case Code | Billing Amount |
| :--- | :--- |
| C001 | 50 |
| C002 | 100 |

**Manager Config (Optional, Excel/CSV):**
| Name | Max Load | Ratio |
| :--- | :--- | :--- |
| Manager A | 150 | 2 |
| Manager B | 200 | 3 |

## 🤝 Support
If you encounter issues, check the terminal window for error messages.
