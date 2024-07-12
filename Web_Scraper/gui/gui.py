import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from scraper.scraper import scrape_website
from scraper.data_handler import save_to_csv, upload_to_google_sheets
import webbrowser

# Define global variables
url_entry = None
var = None
elements_frame = None
elements = []
auth_entry = None
sheet_label = None
add_element_button = None
data_filter_label = None
hint_icon = None

# Define the ToolTip class
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event):
        x = y = 0
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = ttk.Label(tw, text=self.text, justify="left", background="yellow", relief="solid", borderwidth=1)
        label.pack(ipadx=1)
    
    def hide_tip(self, event):
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None

def start_scraping():
    url = url_entry.get()
    selected_option = var.get()

    selectors = [(element['selector'].get(), element['include'].get()) for element in elements]

    if selected_option == "CSV":
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            data = scrape_website(url, selectors)
            save_to_csv(data, filename)
            messagebox.showinfo("CSV Saved", f"Data saved to {filename}")
    elif selected_option == "Google Sheets":
        spreadsheet_url = auth_entry.get()
        if spreadsheet_url:
            data = scrape_website(url, selectors)
            success = upload_to_google_sheets(data, spreadsheet_url)
            if success:
                messagebox.showinfo("Google Sheets Uploaded", "Data uploaded to Google Sheets")
            else:
                messagebox.showerror("Error", "Failed to upload data to Google Sheets")

def open_google_sheets():
    webbrowser.open("https://sheets.google.com")

def handle_option_selection(*args):
    selected_option = var.get()
    if selected_option == "CSV" or selected_option == "Google Sheets":
        data_filter_label.grid(column=0, row=2, columnspan=4, pady=(10, 0))
        elements_canvas.grid(column=0, row=3, columnspan=4, pady=5, padx=5, sticky="ew")
        add_element_button.grid(column=2, row=1, padx=5, pady=5, sticky='e')
        hint_icon_label.grid(column=3, row=1, padx=5, pady=5, sticky='w')
        if selected_option == "Google Sheets":
            sheet_label.grid(column=0, row=4, sticky='e', padx=5, pady=5)
            auth_entry.grid(column=1, row=4, columnspan=2, sticky='w', padx=5, pady=5)
            auth_button.grid(column=3, row=4, padx=5, pady=5)
        else:
            sheet_label.grid_forget()
            auth_entry.grid_forget()
            auth_button.grid_forget()
    else:
        data_filter_label.grid_forget()
        elements_canvas.grid_forget()
        add_element_button.grid_forget()
        hint_icon_label.grid_forget()
        for widget in elements_frame.winfo_children():
            widget.grid_forget()
        elements.clear()
    update_start_button()

def add_element():
    row = len(elements)
    selector_var = tk.StringVar()
    include_var = tk.BooleanVar(value=True)
    entry = ttk.Entry(elements_frame, textvariable=selector_var, width=50)
    entry.grid(column=0, row=row, padx=5, pady=5, sticky='ew')
    checkbutton = ttk.Checkbutton(elements_frame, variable=include_var)
    checkbutton.grid(column=1, row=row, padx=5, pady=5)
    remove_button = ttk.Button(elements_frame, text="Remove", command=lambda: remove_element(row))
    remove_button.grid(column=2, row=row, padx=5, pady=5)
    elements_frame.grid_columnconfigure(0, weight=1)
    elements.append({'selector': selector_var, 'include': include_var, 'remove_button': remove_button, 'entry': entry, 'checkbutton': checkbutton})
    update_elements()

def remove_element(index):
    for widget in elements[index].values():
        if isinstance(widget, (ttk.Entry, ttk.Checkbutton, ttk.Button)):
            widget.grid_forget()
    elements.pop(index)
    update_elements()

def update_elements():
    for i, element in enumerate(elements):
        element['entry'].grid(column=0, row=i, padx=5, pady=5, sticky='ew')
        element['checkbutton'].grid(column=1, row=i, padx=5, pady=5)
        element['remove_button'].grid(column=2, row=i, padx=5, pady=5)
    update_start_button()
    if var.get() == "Google Sheets":
        sheet_label.grid(column=0, row=4, sticky='e', padx=5, pady=5)
        auth_entry.grid(column=1, row=4, columnspan=2, sticky='w', padx=5, pady=5)
        auth_button.grid(column=3, row=4, padx=5, pady=5)

def update_start_button():
    start_button.grid(column=0, row=5, columnspan=4, pady=10, sticky='ew')

def on_frame_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def start_gui():
    global url_entry, var, elements_frame, auth_entry, auth_button, sheet_label, add_element_button, start_button, elements_canvas, data_filter_label, hint_icon_label

    root = tk.Tk()
    root.title("Web Scraper")

    ttk.Label(root, text="Enter Website to Scrape:").grid(column=0, row=0, sticky='e', padx=5, pady=5)
    url_entry = ttk.Entry(root, width=50)
    url_entry.grid(column=1, row=0, columnspan=3, sticky='w', padx=5, pady=5)

    ttk.Label(root, text="Choose output format:").grid(column=0, row=1, sticky='e', padx=5, pady=5)
    var = tk.StringVar()
    var.set("Select an Option")
    options = ["Select an Option", "CSV", "Google Sheets"]
    option_menu = ttk.OptionMenu(root, var, *options, command=handle_option_selection)
    option_menu.grid(column=1, row=1, padx=5, pady=5, sticky='w')

    add_element_button = ttk.Button(root, text="Add Element", command=add_element)
    add_element_button.grid(column=2, row=1, padx=5, pady=5, sticky='e')
    add_element_button.grid_forget()

    # Load the icon image
    hint_icon = tk.PhotoImage(file="info_icon.png")
    hint_icon_label = tk.Label(root, image=hint_icon)
    hint_icon_label.grid(column=3, row=1, padx=5, pady=5, sticky='w')
    hint_icon_label.grid_forget()

    # Tooltip for the hint icon
    tooltip_text = (
        "Standard Scrape Filters:\n"
        "- a[href]\n"
        "- img[src]\n"
        "- div.class_name\n"
        "- p#id\n\n"
        "Amazon Filters:\n"
        "- product_name: span.a-size-medium\n"
        "- price: span.a-price-whole\n"
        "- rating: span.a-icon-alt\n"
        "- reviews: span.a-size-base"
    )
    ToolTip(hint_icon_label, tooltip_text)

    # Label for the Data Filter section
    data_filter_label = ttk.Label(root, text="Data Filter")
    data_filter_label.grid_forget()

    # Create a canvas to hold the scrollable frame
    elements_canvas = tk.Canvas(root, height=200)
    elements_canvas.grid_forget()

    # Add a scrollbar to the canvas
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=elements_canvas.yview)
    scrollbar.grid(column=4, row=3, sticky='ns')
    elements_canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    elements_frame = ttk.Frame(elements_canvas)
    elements_frame.bind("<Configure>", lambda e: on_frame_configure(elements_canvas))

    # Add the frame to a window in the canvas
    elements_canvas.create_window((0, 0), window=elements_frame, anchor="nw")

    sheet_label = ttk.Label(root, text="Enter Google Sheet URL:")
    sheet_label.grid(column=0, row=4, sticky='e', padx=5, pady=5)
    sheet_label.grid_forget()

    auth_entry = ttk.Entry(root, width=50)
    auth_entry.grid(column=1, row=4, columnspan=3, sticky='w', padx=5, pady=5)
    auth_entry.grid_forget()

    auth_button = ttk.Button(root, text="Open Google Sheets", command=open_google_sheets)
    auth_button.grid(column=4, row=4, padx=5, pady=5)
    auth_button.grid_forget()
    auth_button.grid_forget()

    start_button = ttk.Button(root, text="Start Scraping", command=start_scraping)
    start_button.grid(column=0, row=5, columnspan=5, pady=10, sticky='ew')
    start_button.grid_forget()

    root.mainloop()

if __name__ == "__main__":
    start_gui()
