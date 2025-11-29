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

### 2. Download & Setup
Open your terminal (Command Prompt, PowerShell, or Terminal) and run the following commands one by one:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/JyotendraPallav/CaseWork.git
    cd CaseWork
    ```

2.  **Create a Virtual Environment**:
    ```bash
    # Windows
    python -m venv venv
    
    # macOS / Linux
    python3 -m venv venv
    ```

3.  **Activate the Environment**:
    ```bash
    # Windows
    venv\Scripts\activate
    
    # macOS / Linux
    source venv/bin/activate
    ```

4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Run the App
Once the environment is active and dependencies are installed:

```bash
python app.py
```
Open the link displayed in the terminal (usually `http://127.0.0.1:7860`) in your browser.

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
