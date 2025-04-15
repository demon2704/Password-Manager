import sqlite3
import gradio as gr

# --- DATABASE SETUP ---
conn = sqlite3.connect("passwords.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
""")
conn.commit()

# --- BACKEND FUNCTIONS ---
def add_entry(site, username, password):
    cursor.execute("INSERT INTO credentials (site, username, password) VALUES (?, ?, ?)", (site, username, password))
    conn.commit()
    return f"Added entry for {site}"

def get_all_entries():
    cursor.execute("SELECT site, username, password FROM credentials")
    rows = cursor.fetchall()
    if not rows:
        return "No credentials saved."
    return "\n".join([f"{site} | {username} | {password}" for site, username, password in rows])

def search_entry(site):
    cursor.execute("SELECT username, password FROM credentials WHERE site = ?", (site,))
    row = cursor.fetchone()
    if row:
        return f"Username: {row[0]}\nPassword: {row[1]}"
    else:
        return "No credentials found for this site."

def delete_entry(site):
    cursor.execute("DELETE FROM credentials WHERE site = ?", (site,))
    conn.commit()
    return f"Deleted entries for {site}"

# --- GRADIO INTERFACE ---
with gr.Blocks() as demo:
    gr.Markdown("## Simple Password Manager")

    with gr.Tab("Add Entry"):
        site = gr.Textbox(label="Website")
        username = gr.Textbox(label="Username")
        password = gr.Textbox(label="Password", type="password")
        add_btn = gr.Button("Add")
        add_output = gr.Textbox(label="Output")
        add_btn.click(fn=add_entry, inputs=[site, username, password], outputs=add_output)

    with gr.Tab("View All"):
        view_btn = gr.Button("Show All Credentials")
        view_output = gr.Textbox(label="All Saved Credentials", lines=10)
        view_btn.click(fn=get_all_entries, inputs=[], outputs=view_output)

    with gr.Tab("Search"):
        search_input = gr.Textbox(label="Website to Search")
        search_btn = gr.Button("Search")
        search_output = gr.Textbox(label="Search Result")
        search_btn.click(fn=search_entry, inputs=search_input, outputs=search_output)

    with gr.Tab("Delete"):
        delete_input = gr.Textbox(label="Website to Delete")
        delete_btn = gr.Button("Delete")
        delete_output = gr.Textbox(label="Delete Status")
        delete_btn.click(fn=delete_entry, inputs=delete_input, outputs=delete_output)

# --- RUN APP ---
demo.launch()