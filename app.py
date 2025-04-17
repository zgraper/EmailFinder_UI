import gradio as gr
import pandas as pd
import tempfile
from combined_email_finder import get_combined_emails

def extract_emails(domain):
    emails = get_combined_emails(domain)
    return "\n".join(emails) if emails else "⚠️ No valid emails found."

def export_csv(domain):
    emails = get_combined_emails(domain)
    if not emails:
        return None
    df = pd.DataFrame({"Email": emails})
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w', encoding='utf-8') as tmp:
        df.to_csv(tmp.name, index=False)
        return tmp.name

# Create the two interfaces
email_interface = gr.Interface(
    fn=extract_emails,
    inputs=gr.Textbox(label="Enter Domain"),
    outputs=gr.Textbox(label="Extracted Emails", lines=10),
    title="📧 Email Extractor",
    description="Scrapes and extracts emails from a domain."
)

csv_interface = gr.Interface(
    fn=export_csv,
    inputs=gr.Textbox(label="Enter Domain"),
    outputs=gr.File(label="Download CSV"),
    title="📥 CSV Exporter",
    description="Download extracted emails as a CSV file."
)

# Combine into tabbed interface
demo = gr.TabbedInterface(
    [email_interface, csv_interface],
    tab_names=["Extract Emails", "Download CSV"]
)

demo.launch()