import openpyxl
import pandas as pd
import tempfile
from datetime import datetime, timedelta
from scheduler import Task, Leader, solve_scheduling

def generate_date_mapping(start_date_str, num_days, working_days, holidays_str):
    """
    Generates a list of valid dates skipping non-working days and holidays.
    """
    try:
        current_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    except:
        current_date = datetime.now()

    # Parse holidays
    holidays = set()
    if holidays_str:
        for line in holidays_str.split('\n'):
            line = line.strip()
            if line:
                try:
                    holidays.add(datetime.strptime(line, "%Y-%m-%d").date())
                except:
                    pass # Ignore invalid dates

    # Map day names to weekday index (Mon=0, Sun=6)
    day_map = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, 
        "Friday": 4, "Saturday": 5, "Sunday": 6
    }
    allowed_weekdays = {day_map[d] for d in working_days if d in day_map}
    
    valid_dates = []
    while len(valid_dates) < num_days:
        if current_date.weekday() in allowed_weekdays and current_date.date() not in holidays:
            valid_dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
        
        # Safety break to prevent infinite loop if no working days
        if (current_date - datetime.now()).days > 365 * 2: 
            break
            
    return valid_dates

def process_scheduling(file_obj, managers_df, start_date, working_days, holidays_str):
    """
    Main handler for the Gradio interface.
    """
    if file_obj is None:
        return None, "Please upload an Excel file.", None, None, None
    
    # 1. Parse Excel
    try:
        # Handle both file path (string) and file object (Gradio)
        file_path = file_obj.name if hasattr(file_obj, 'name') else file_obj
        
        # Use openpyxl directly to bypass pandas/xlrd issues
        wb = openpyxl.load_workbook(file_path, data_only=True)
        sheet = wb.active
        
        data = []
        headers = [str(cell.value).strip() for cell in sheet[1]]
        
        if "Case Code" not in headers or "Billing Amount" not in headers:
            return None, "Error: Excel must contain 'Case Code' and 'Billing Amount' columns.", None, None, None
            
        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_dict = dict(zip(headers, row))
            if row_dict.get("Case Code") and row_dict.get("Billing Amount"):
                data.append(row_dict)
        
        tasks = []
        for idx, row in enumerate(data):
            tasks.append(Task(
                id=idx,
                tokens=int(row["Billing Amount"]),
                case_code=str(row["Case Code"])
            ))
            
    except Exception as e:
        return None, f"Error reading Excel file: {str(e)}", None, None, None

    # 2. Parse Managers
    leaders = []
    try:
        # managers_df is a pandas DataFrame from the Gradio component
        for _, row in managers_df.iterrows():
            name = str(row["Name"])
            limit = int(row["Max Load"])
            ratio = int(row["Ratio"])
            if name and limit > 0 and ratio > 0:
                leaders.append(Leader(name=name, daily_limit=limit, target_ratio_weight=ratio))
        
        if not leaders:
            return None, "Error: Please configure at least one valid manager.", None, None, None
            
    except Exception as e:
        return None, f"Error parsing managers: {str(e)}", None, None, None

    # 3. Solve
    try:
        schedule_data = solve_scheduling(tasks, leaders)
    except Exception as e:
        return None, f"Error during scheduling: {str(e)}", None, None, None

    # 4. Generate Output Excel
    output_df = pd.DataFrame(schedule_data)
    
    # --- Calendar Mapping ---
    if not output_df.empty:
        max_day = output_df["Day"].max()
        valid_dates = generate_date_mapping(start_date, max_day, working_days, holidays_str)
        
        # Create a map {Day Index: Date String}
        # Note: Day is 1-indexed in output_df
        date_map = {i+1: d for i, d in enumerate(valid_dates)}
        
        output_df["Date"] = output_df["Day"].map(date_map)
        
        # Reorder columns to put Date first
        cols = ["Date"] + [c for c in output_df.columns if c != "Date"]
        output_df = output_df[cols]
    
    # --- QC Calculations ---
    
    # 1. Global Validation
    total_input_cases = len(tasks)
    total_input_value = sum(t.tokens for t in tasks)
    
    total_scheduled_cases = len(output_df)
    total_scheduled_value = output_df["Billing Amount"].sum() if not output_df.empty else 0
    
    global_validation_msg = f"""
    ### ✅ Global Validation
    - **Total Cases**: Input {total_input_cases} vs Scheduled {total_scheduled_cases}
    - **Total Value**: Input {total_input_value} vs Scheduled {total_scheduled_value}
    - **Status**: {"✅ MATCH" if total_input_value == total_scheduled_value else "❌ MISMATCH"}
    """
    
    # 2. Manager Summary
    manager_stats = []
    for l in leaders:
        manager_stats.append({
            "Manager": l.name,
            "Target Tokens": l.target_tokens,
            "Actual Tokens": l.current_tokens,
            "Variance": l.current_tokens - l.target_tokens,
            "Daily Limit": l.daily_limit,
            "Utilization %": round((l.current_tokens / l.target_tokens * 100), 2) if l.target_tokens > 0 else 0
        })
    manager_summary_df = pd.DataFrame(manager_stats)

    # 3. Daily Summary
    if not output_df.empty:
        daily_summary_df = output_df.groupby("Day")["Billing Amount"].sum().reset_index()
        daily_summary_df.rename(columns={"Billing Amount": "Total Daily Load"}, inplace=True)
    else:
        daily_summary_df = pd.DataFrame(columns=["Day", "Total Daily Load"])

    # Create a temporary file for the output
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        output_path = tmp.name
        
    try:
        # We can add a summary sheet too
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            output_df.to_excel(writer, sheet_name='Schedule', index=False)
            manager_summary_df.to_excel(writer, sheet_name='Manager Summary', index=False)
            daily_summary_df.to_excel(writer, sheet_name='Daily Summary', index=False)
            
    except Exception as e:
        return None, f"Error saving output Excel: {str(e)}", None, None, None

    return output_path, output_df, global_validation_msg, manager_summary_df, daily_summary_df
