"""
Email Summarizer - Desktop App Prototype
==========================================

A simple desktop application built with CustomTkinter that lets you
paste an email and get an AI-generated summary (key points, action
items, and deadlines).

WHAT YOU NEED BEFORE RUNNING THIS:
1. Install the required libraries (run these in your terminal):
       pip install customtkinter
       pip install openai
       pip install python-dotenv

2. Create a file named ".env" in the same folder as this script,
   and put your OpenAI API key inside it like this:
       OPENAI_API_KEY=sk-your-key-here

3. Run this script:
       python email_summarizer_app.py

HOW THE CODE IS ORGANIZED (since this is your first time with the library):
- CustomTkinter (imported as "ctk") is a library for building desktop
  app windows. Think of it like building blocks: a "Frame" is a
  container box, a "Textbox" is a text area, a "Button" is a
  clickable button, etc. You place these blocks inside a "window".
- We define one class, `EmailSummarizerApp`, which represents the
  whole application window. Each method (function inside the class)
  handles one job: building the layout, or reacting to a button click.
- At the very bottom of the file, we actually create the window and
  start the app running.
"""

import os
import threading
import customtkinter as ctk
from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------------------------------------------------------
# STEP 1: Load your API key from the .env file
# ---------------------------------------------------------------------------
# load_dotenv() reads the ".env" file in this folder and makes its contents
# available via os.getenv(). This keeps your API key out of your source code.
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Create the OpenAI client once, so we can reuse it every time we summarize.
# If there's no API key, we still let the app open, but summarizing will fail
# with a clear error message instead of crashing on startup.
client = OpenAI(api_key=api_key) if api_key else None


# ---------------------------------------------------------------------------
# STEP 2: Appearance settings (optional, purely visual)
# ---------------------------------------------------------------------------
# "dark" or "light" - controls the color theme of the whole app.
ctk.set_appearance_mode("dark")
# "blue", "green", or "dark-blue" - controls the accent color of buttons etc.
ctk.set_default_color_theme("blue")


class EmailSummarizerApp(ctk.CTk):
    """
    The main application window.

    In CustomTkinter, you build a custom window by creating a class that
    inherits from `ctk.CTk` (this IS the window itself). Inside `__init__`,
    we build all the visual pieces (widgets) and arrange them.
    """

    def __init__(self):
        # Always call the parent class's __init__ first - this sets up
        # the underlying window before we start adding things to it.
        super().__init__()

        # --- Basic window setup ---
        self.title("Email Summarizer")
        self.geometry("600x650")  # width x height, in pixels

        # --- Build the UI ---
        self._build_widgets()

    def _build_widgets(self):
        """
        Creates and arranges every widget (button, textbox, label) in the
        window. Keeping this in its own method (instead of stuffing
        everything into __init__) makes the class easier to read.
        """

        # ---------- Section 1: Input label + textbox ----------
        # A CTkLabel is just a piece of text on screen (not clickable).
        input_label = ctk.CTkLabel(
            self,
            text="Paste the email below:",
            font=("Arial", 14, "bold"),
        )
        # .pack() is one way to place a widget in the window. It stacks
        # widgets vertically (or horizontally) automatically.
        # padx/pady = padding (space) around the widget, in pixels.
        # anchor="w" means "align to the west (left) side".
        input_label.pack(padx=20, pady=(20, 5), anchor="w")

        # A CTkTextbox is a multi-line text area the user can type/paste into.
        self.email_textbox = ctk.CTkTextbox(self, height=220)
        self.email_textbox.pack(padx=20, pady=5, fill="x")

        # ---------- Section 2: Paste button ----------

        self.paste_button = ctk.CTkButton(
            self,
            text="Paste",
            command=self.on_paste_click,
            width=80,
        )
        self.paste_button.pack(padx=(0, 5), pady=(0, 5), anchor="e", side="right")

        # ---------- Section 3: Summarize button ----------
        self.summarize_button = ctk.CTkButton(
            self,
            text="Summarize",
            command=self.on_summarize_click,  # function to run when clicked
        )
        self.summarize_button.pack(padx=20, pady=15)

        # A small status label to show "Summarizing..." or error messages.
        self.status_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.status_label.pack(padx=20, pady=(0, 5))

        # ---------- Section 4: Output label + textbox ----------
        output_label = ctk.CTkLabel(
            self,
            text="AI Summary:",
            font=("Arial", 14, "bold"),
        )
        output_label.pack(padx=20, pady=(10, 5), anchor="w")

        self.output_textbox = ctk.CTkTextbox(self, height=220)
        self.output_textbox.pack(padx=20, pady=(5, 20), fill="both", expand=True)
        # Read-only isn't a direct option in CustomTkinter, so we simulate it
        # by disabling the textbox until we need to write into it.
        self.output_textbox.configure(state="disabled")

    # -----------------------------------------------------------------------
    # Event handlers (functions triggered by user actions)
    # -----------------------------------------------------------------------
    def on_paste_click(self):
        """
        Reads whatever is currently on the system clipboard (e.g. an email
        you copied from your Mail app) and inserts it into the input
        textbox, replacing anything already there.
        """
        try:
            clipboard_text = self.clipboard_get()
        except Exception:
            # This happens if the clipboard is empty or contains something
            # that isn't text (e.g. an image).
            clipboard_text = ""

        self.email_textbox.delete("1.0", "end")  # clear existing content
        self.email_textbox.insert("1.0", clipboard_text)  # insert clipboard text

    def on_summarize_click(self):
        """
        Runs when the user clicks the "Summarize" button.

        We don't call the OpenAI API directly here. Instead, we start a
        background "thread". This matters because API calls take a second
        or two - if we ran that directly on the click, the whole window
        would freeze (become unresponsive) while waiting for the response.
        Running it in a separate thread keeps the window responsive.
        """
        email_text = self.email_textbox.get("1.0", "end").strip()

        # Basic validation: don't call the API with empty text.
        if not email_text:
            self.status_label.configure(text="Please paste an email first.")
            return

        if client is None:
            self.status_label.configure(
                text="No API key found. Check your .env file."
            )
            return

        # Disable the button and show a status message while we work,
        # so the user knows something is happening and can't double-click.
        self.summarize_button.configure(state="disabled", text="Summarizing...")
        self.status_label.configure(text="")

        # Start the actual API call in a background thread.
        thread = threading.Thread(target=self._summarize_in_background, args=(email_text,))
        thread.start()

    def _summarize_in_background(self, email_text):
        """
        Does the actual work of calling the OpenAI API. This runs on a
        background thread (not the main window thread), so it can take
        as long as it needs without freezing the UI.
        """
        try:
            summary = self._call_openai(email_text)
            # We can't safely touch the UI directly from a background
            # thread, so we schedule the update to run back on the main
            # thread using `self.after(...)`.
            self.after(0, lambda: self._show_summary(summary))
        except Exception as error:
            error_message = str(error)
            self.after(0, lambda: self._show_error(error_message))

    def _call_openai(self, email_text):
        """
        Sends the email text to the OpenAI API and returns the summary text.
        This is the same logic from the original script, just wrapped in a
        function so the GUI code can call it.
        """
        prompt = f"""
        Summarize the following email into:
        - key points
        - action items
        - deadlines (if any)

        Email:
        {email_text}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes emails."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content

    def _show_summary(self, summary_text):
        """
        Updates the output textbox with the summary. Must be called on the
        main thread (see the `self.after(...)` call above).
        """
        self.output_textbox.configure(state="normal")   # temporarily unlock
        self.output_textbox.delete("1.0", "end")          # clear old content
        self.output_textbox.insert("1.0", summary_text)   # write new summary
        self.output_textbox.configure(state="disabled")  # lock again

        self.summarize_button.configure(state="normal", text="Summarize")
        self.status_label.configure(text="Done.")

    def _show_error(self, error_message):
        """
        Displays an error message if something goes wrong (e.g. bad API key,
        no internet connection).
        """
        self.summarize_button.configure(state="normal", text="Summarize")
        self.status_label.configure(text=f"Error: {error_message}", text_color="red")


# ---------------------------------------------------------------------------
# STEP 3: Actually run the app
# ---------------------------------------------------------------------------
# This "if" check is a common Python pattern: it means "only run this code
# if this file is run directly (not imported into another file)".
if __name__ == "__main__":
    app = EmailSummarizerApp()
    app.mainloop()  # This starts the app and keeps the window open,
                     # listening for clicks/typing, until you close it.
