import gradio as gr
from openai import OpenAI
import json
import time

# Connect to the local Ollama server
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# System prompt for the banking extraction
SYSTEM_PROMPT = """You are a strict banking compliance assistant. Your task is to process incoming customer emails.

Follow these rules exactly:
1. Classify the intent into ONE of these categories: "fraud_dispute", "loan_inquiry", "balance_check", "complaint", or "general".
2. Extract the "account_last_four" (as a string, if mentioned).
3. Extract the "amount_usd" (as a float, if mentioned).
4. Extract the "urgency" as either "high", "medium", or "low" based on the language.
5. Output ONLY a valid JSON object. No extra text. No explanations.

Here is the email body:
"""

# This function is called when the user clicks "Process"
def process_email(email_text, history):
    # If no email is entered, return an error
    if not email_text.strip():
        return history, "⚠️ Please paste an email into the text box.", ""
    
    try:
        # Record start time for performance tracking
        start_time = time.time()
        
        # Call the local DeepSeek model
        response = client.chat.completions.create(
            # model="deepseek-r1:7b",
            model="deepseek-r1:1.5b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": email_text}
            ],
            temperature=0.1,
            timeout=120  # Give it up to 2 minutes for the cold start
        )
        
        # Get the raw response
        raw = response.choices[0].message.content
        
        # Extract just the JSON part (handles the <think> tags)
        try:
            clean = raw[raw.find("{"):raw.rfind("}")+1]
            data = json.loads(clean)
            formatted_output = json.dumps(data, indent=2)
            elapsed = time.time() - start_time
            
            # Build a "success" message
            status = f"✅ Processed in {elapsed:.1f} seconds"
            
            # Add to history (format as a readable entry)
            history_entry = f"📧 Email: {email_text[:80]}...\n📊 Output: {formatted_output}\n{'-'*40}\n"
            updated_history = history + history_entry
            
            return updated_history, status, formatted_output
            
        except json.JSONDecodeError:
            # If JSON parsing fails, show the raw output
            return history, "⚠️ Model output was not valid JSON. Here is the raw response:", raw
            
    except Exception as e:
        # Catch any connection or timeout errors
        return history, f"❌ Error: {str(e)}", "Check that Ollama is running and the model is loaded."

# Build the Gradio interface
with gr.Blocks(title="Banking SLM Triage Dashboard", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🏦 Private Banking Email Triage
    **Powered by DeepSeek-R1 (Running 100% Locally)**
    Paste a customer email below and the AI will extract the intent, account number, amount, and urgency.
    """)
    
    # Row 1: Input and Process Button
    with gr.Row():
        with gr.Column(scale=3):
            email_input = gr.Textbox(
                label="📨 Paste Customer Email Here",
                placeholder="Dear Support Team, I saw a charge of $200 on my account ending in 1234 that I didn't authorize...",
                lines=8
            )
            process_btn = gr.Button("🔍 Classify Email", variant="primary")
        
        with gr.Column(scale=2):
            status_output = gr.Textbox(label="📌 Status", lines=1)
            json_output = gr.Textbox(label="📊 Extracted Data (JSON)", lines=8)
    
    # Row 2: History Log
    gr.Markdown("---")
    gr.Markdown("### 📜 Session History")
    history_output = gr.Textbox(label="Processed Emails (Current Session)", lines=12, interactive=False)
    
    # Wire up the button
    process_btn.click(
        fn=process_email,
        inputs=[email_input, history_output],
        outputs=[history_output, status_output, json_output]
    )
    
    # Add a quick example to get started
    gr.Markdown("""
    ---
    **💡 Try this example:**
    *"I just checked my mobile app and saw a withdrawal of $540.20 from my account ending in 8912 that I did not authorize. I am currently traveling abroad and extremely worried. Please freeze my card."*
    """)

# Launch the app
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)