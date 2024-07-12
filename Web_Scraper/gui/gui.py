import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from scraper.scraper import scrape_website
from scraper.data_handler import save_to_csv, upload_to_google_sheets
import webbrowser

# Define global variables
url_entry = None
var = None
auth_entry = None
sheet_label = None

def start_scraping():
    url = url_entry.get()
    selected_option = var.get()

    if selected_option == "CSV":
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            data = scrape_website(url)
            save_to_csv(data, filename)
            messagebox.showinfo("CSV Saved", f"Data saved to {filename}")
    elif selected_option == "Google Sheets":
        spreadsheet_url = auth_entry.get()
        if spreadsheet_url:
            data = scrape_website(url)  # Ensure data is a list of full URLs
            success = upload_to_google_sheets(data, spreadsheet_url)
            if success:
                messagebox.showinfo("Google Sheets Uploaded", "Data uploaded to Google Sheets")
            else:
                messagebox.showerror("Error", "Failed to upload data to Google Sheets")

def open_google_sheets():
    webbrowser.open("https://sheets.google.com")

def handle_option_selection(*args):
    selected_option = var.get()
    if selected_option == "CSV":
        auth_entry.grid_forget()
        auth_button.grid_forget()
        sheet_label.grid_forget()
    elif selected_option == "Google Sheets":
        sheet_label.grid(column=0, row=2)
        auth_entry.grid(column=1, row=2)
        auth_button.grid(column=2, row=2)
    elif selected_option == "Select an Option":
        auth_entry.grid_forget()
        auth_button.grid_forget()
        sheet_label.grid_forget()

def start_gui():
    global url_entry, var, auth_entry, auth_button, sheet_label

    root = tk.Tk()
    root.title("Web Scraper")

    ttk.Label(root, text="Enter URL:").grid(column=0, row=0)
    url_entry = ttk.Entry(root, width=50)
    url_entry.grid(column=1, row=0)

    ttk.Label(root, text="Choose output format:").grid(column=0, row=1)
    var = tk.StringVar()
    var.set("Select an Option")
    options = ["Select an Option", "CSV", "Google Sheets"]
    option_menu = ttk.OptionMenu(root, var, *options, command=handle_option_selection)
    option_menu.grid(column=1, row=1)

    sheet_label = ttk.Label(root, text="Enter Google Sheet URL:")
    sheet_label.grid_forget()

    auth_entry = ttk.Entry(root, width=50)
    auth_entry.grid_forget()

    start_button = ttk.Button(root, text="Start Scraping", command=start_scraping)
    start_button.grid(column=1, row=3)

    auth_button = ttk.Button(root, text="Open Google Sheets", command=open_google_sheets)
    auth_button.grid_forget()

    root.mainloop()

if __name__ == "__main__":
    start_gui()
