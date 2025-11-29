import gradio as gr
import pandas as pd
from datetime import datetime
from logic import process_scheduling

# --- Helper Functions ---

def load_manager_config(file_obj):
    """
    Parses an uploaded manager configuration file.
    """
    if file_obj is None:
        return None
        
    try:
        # Determine file type
        file_path = file_obj.name if hasattr(file_obj, 'name') else file_obj
        
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            # Assume Excel
            df = pd.read_excel(file_path, engine='openpyxl')
            
        # Validate columns
        required_cols = ["Name", "Max Load", "Ratio"]
        # Normalize headers
        df.columns = [c.strip() for c in df.columns]
        
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"File must contain columns: {', '.join(required_cols)}")
            
        # Return relevant columns only
        return df[required_cols]
        
    except Exception as e:
        # In Gradio, returning None or raising error might not show nicely in Dataframe
        # We'll return a dummy DF with error as a row or just let Gradio handle exception
        print(f"Error loading config: {e}")
        return pd.DataFrame({"Error": [str(e)]})

# --- Gradio UI ---

def create_app():
    with gr.Blocks(title="Casework Scheduler") as app:
        gr.Markdown("# 📅 Casework Scheduler & Optimizer")
        gr.Markdown("Upload your casework Excel file and configure managers to generate an optimized schedule.")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 1. Upload Casework")
                file_input = gr.File(label="Upload Excel (Columns: 'Case Code', 'Billing Amount')")
                
                gr.Markdown("### 2. Configure Managers")
                
                with gr.Accordion("Upload Manager Config (Optional)", open=False):
                    manager_file_input = gr.File(label="Upload Config (Excel/CSV)")
                
                # Default managers
                default_managers = pd.DataFrame({
                    "Name": ["Manager A", "Manager B", "Manager C"],
                    "Max Load": [150, 200, 250],
                    "Ratio": [2, 3, 5]
                })
                managers_input = gr.Dataframe(
                    value=default_managers,
                    headers=["Name", "Max Load", "Ratio"],
                    datatype=["str", "number", "number"],
                    row_count=(1, "dynamic"),
                    col_count=(3, "fixed"),
                    label="Manager Configuration (Editable)"
                )
                
                # Wire upload event
                manager_file_input.upload(fn=load_manager_config, inputs=manager_file_input, outputs=managers_input)
                
                gr.Markdown("### 3. Calendar Configuration")
                with gr.Accordion("Working Days & Holidays", open=False):
                    start_date = gr.Textbox(
                        label="Start Date (YYYY-MM-DD)", 
                        value=datetime.now().strftime("%Y-%m-%d")
                    )
                    working_days = gr.CheckboxGroup(
                        label="Working Days",
                        choices=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                        value=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                    )
                    holidays = gr.Textbox(
                        label="Holidays (YYYY-MM-DD, one per line)",
                        lines=3,
                        placeholder="2023-12-25\n2024-01-01"
                    )
                
                submit_btn = gr.Button("🚀 Generate Schedule", variant="primary")
                
            with gr.Column():
                gr.Markdown("### 4. Download Results")
                output_file = gr.File(label="Download Schedule")
                output_preview = gr.Dataframe(label="Preview", interactive=False)

        gr.Markdown("---")
        gr.Markdown("## 📊 QC Dashboard")
        
        qc_validation = gr.Markdown("Run generation to see validation results.")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Manager Summary")
                manager_summary = gr.Dataframe(label="Target vs Actual", interactive=False)
            with gr.Column():
                gr.Markdown("### Daily Summary")
                daily_summary = gr.Dataframe(label="Daily Load", interactive=False)

        submit_btn.click(
            fn=process_scheduling,
            inputs=[file_input, managers_input, start_date, working_days, holidays],
            outputs=[output_file, output_preview, qc_validation, manager_summary, daily_summary]
        )
        
    return app

if __name__ == "__main__":
    app = create_app()
    app.launch(server_name="0.0.0.0", server_port=7860)
