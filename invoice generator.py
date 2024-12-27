import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
from tkinter import  Tk, Frame, Entry, Label, Button, OptionMenu, StringVar, filedialog, messagebox, Scrollbar, Canvas


# ==== creating main class
class InvoiceGenerator:
   def __init__(self,root):
       self.root = root
       self.root.title("Invoice Generator By Mercy")
       self.root.geometry("750x1000")
       self.root.resizable(True, True)

       # Load last-used country or set default
       self.last_country_file = "last_country.txt"
       self.last_used_country = self.load_last_country()

       # Create a canvas for scrolling
       self.canvas = Canvas(self.root, bg="white")
       self.scrollbar = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
       self.scrollable_frame = Frame(self.canvas, bg="white")

       # Configure scrollbar
       self.scrollable_frame.bind(
           "<Configure>",
           lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
       )
       self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
       self.canvas.configure(yscrollcommand=self.scrollbar.set)

       # Place canvas and scrollbar
       self.canvas.pack(side="left", fill="both", expand=True)
       self.scrollbar.pack(side="right", fill="y")

       # List of countries
       self.countries = ["Netherlands", "United States", "India", "United Kingdom", "Canada"]
       if self.last_used_country not in self.countries:
           self.countries.insert(0, self.last_used_country)

       # creating frame in window
       self.scrollable_frame.place(x=80, y=20, width=600, height=950)  # Adjusted height to match increased form size

       Label(self.scrollable_frame, text="Enter your company details ", font=("times new roman", 25, "bold"),
             bg="white", fg="green").grid(row=0, column=0, columnspan=2, pady=10, padx=20)

       Label(self.scrollable_frame, text="Company Name", font=("times new roman", 15), bg="white", fg="gray").grid(
           row=1, column=0, sticky="w", padx=20, pady=10)
       self.company_name = Entry(self.scrollable_frame, font=("times new roman", 15), bg="light grey")
       self.company_name.grid(row=1, column=1, padx=20, pady=10)

       Label(self.scrollable_frame, text="Address", font=("times new roman", 15), bg="white", fg="gray").grid(
           row=2, column=0, sticky="w", padx=20, pady=10)
       self.address = Entry(self.scrollable_frame, font=("times new roman", 15), bg="light grey")
       self.address.grid(row=2, column=1, padx=20, pady=10)

       Label(self.scrollable_frame, text="City", font=("times new roman", 15), bg="white", fg="gray").grid(
           row=3, column=0, sticky="w", padx=20, pady=10)
       self.city = Entry(self.scrollable_frame, font=("times new roman", 15), bg="light grey")
       self.city.grid(row=3, column=1, padx=20, pady=10)

       Label(self.scrollable_frame, text="Country", font=("times new roman", 15), bg="white", fg="gray").grid(
           row=4, column=0, sticky="w", padx=20, pady=10)
       self.selected_country = StringVar(self.root)
       self.selected_country.set(self.last_used_country)
       OptionMenu(self.scrollable_frame, self.selected_country, *self.countries).grid(row=4, column=1, padx=20, pady=10)

       Label(self.scrollable_frame, text="GST Number", font=("times new roman", 15), bg="white", fg="gray").grid(
           row=5, column=0, sticky="w", padx=20, pady=10)
       self.gst = Entry(self.scrollable_frame, font=("times new roman", 15), bg="light grey")
       self.gst.grid(row=5, column=1, padx=20, pady=10)

       Label(self.scrollable_frame, text="Date", font=("times new roman", 15), bg="white", fg="gray").grid(
           row=6, column=0, sticky="w", padx=20, pady=10)
       self.date = Entry(self.scrollable_frame, font=("times new roman", 15), bg="light grey")
       self.date.grid(row=6, column=1, padx=20, pady=10)

       Label(self.scrollable_frame, text="Contact", font=("times new roman", 15), bg="white", fg="gray").grid(
           row=7, column=0, sticky="w", padx=20, pady=10)
       self.contact = Entry(self.scrollable_frame, font=("times new roman", 15), bg="light grey")
       self.contact.grid(row=7, column=1, padx=20, pady=10)

       Label(self.scrollable_frame, text="Customer Name", font=("times new roman", 15), bg="white", fg="gray").grid(
           row=8, column=0, sticky="w", padx=20, pady=10)
       self.c_name = Entry(self.scrollable_frame, font=("times new roman", 15), bg="light grey")
       self.c_name.grid(row=8, column=1, padx=20, pady=10)

       Label(self.scrollable_frame, text="Authorized Signatory", font=("times new roman", 15), bg="white",
             fg="gray").grid(
           row=9, column=0, sticky="w", padx=20, pady=10)
       self.aus = Entry(self.scrollable_frame, font=("times new roman", 15), bg="light grey")
       self.aus.grid(row=9, column=1, padx=20, pady=10)

       Label(self.scrollable_frame, text="Company Image", font=("times new roman", 15), bg="white", fg="gray").grid(
           row=10, column=0, sticky="w", padx=20, pady=10)
       Button(self.scrollable_frame, text="Browse Files", command=self.browse, font=("times new roman", 15)).grid(
           row=10, column=1, padx=20, pady=10)

       Button(self.scrollable_frame, text="Save Invoice", command=self.save_invoice, font=("times new roman", 15),
              bg="#B00857", fg="white").grid(row=11, column=0, columnspan=2, pady=20)

   # ==== Browse Function
   def browse(self):
       self.file_name = filedialog.askopenfilename(title="Select a File")
       Label(self.scrollable_frame, text=os.path.basename(self.file_name), font=("times new roman", 15)).place(x=270, y=600)

   # ==== Save Invoice Function
   def save_invoice(self):
       # Validate required fields
       if not self.company_name.get().strip():
           messagebox.showerror("Error", "Company Name is required")
           return
       if not self.address.get().strip():
           messagebox.showerror("Error", "Address is required")
           return
       if not self.city.get().strip():
           messagebox.showerror("Error", "City is required")
           return
       if not self.gst.get().strip():
           messagebox.showerror("Error", "GST Number is required")
           return
       # Validate date format (Expected format: DD-MM-YYYY)
       date_input = self.date.get().strip()
       if not date_input:
           messagebox.showerror("Error", "Date is required")
           return
       try:
           datetime.strptime(date_input, "%d-%m-%Y")
       except ValueError:
           messagebox.showerror("Error", "Date format should be DD-MM-YYYY")
           return

       # Validate contact field (numeric and length check)
       contact_input = self.contact.get().strip()
       if not contact_input:
           messagebox.showerror("Error", "Contact is required")
           return
       if not contact_input.isdigit() or len(contact_input) < 10:
           messagebox.showerror("Error", "Contact must be at least 10 digits and numeric")
           return

       if not self.c_name.get().strip():
           messagebox.showerror("Error", "Customer Name is required")
           return
       if not self.aus.get().strip():
           messagebox.showerror("Error", "Authorized Signatory is required")
           return
       if not hasattr(self, 'file_name') or not self.file_name:
           messagebox.showerror("Error", "Company Image is required")
           return

       save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
       if save_path:  # If the user didn't cancel the dialog
           self.generate_invoice(save_path)

       # ==== Invoice Generation Function

   def generate_invoice(self, file_path):
       # Create a canvas with A4 size
       c = canvas.Canvas(file_path, pagesize=A4)
       width, height = A4  # A4 dimensions in points (595x842)

       # Margins
       left_margin = 50
       right_margin = width - 50
       top_margin = height - 50

       # Company Logo and Header
       if hasattr(self, 'file_name') and self.file_name:
           try:
               c.drawImage(self.file_name, left_margin, top_margin - 50, width=100, height=50, preserveAspectRatio=True)
           except Exception as e:
               print(f"Error drawing image: {e}")

       c.setFont("Times-Bold", 16)
       c.drawCentredString((left_margin + right_margin) / 2, top_margin - 20, self.company_name.get())

       c.setFont("Times-Roman", 12)
       c.drawCentredString((left_margin + right_margin) / 2, top_margin - 40, self.address.get())
       c.drawCentredString((left_margin + right_margin) / 2, top_margin - 60,
                           f"{self.city.get()}, {self.selected_country.get()}")
       c.drawCentredString((left_margin + right_margin) / 2, top_margin - 80, f"GST No: {self.gst.get()}")

       # Line Separator
       c.line(left_margin, top_margin - 90, right_margin, top_margin - 90)

       # Invoice Title
       c.setFont("Times-Bold", 18)
       c.drawCentredString((left_margin + right_margin) / 2, top_margin - 110, "INVOICE")

       # Invoice Details
       c.setFont("Times-Roman", 12)
       details_top = top_margin - 140
       c.drawString(left_margin, details_top, "Invoice No.:")
       c.drawString(left_margin + 120, details_top, self.get_timestamp_invoice_number())

       c.drawString(left_margin, details_top - 20, "Date:")
       c.drawString(left_margin + 120, details_top - 20, self.date.get())

       c.drawString(left_margin, details_top - 40, "Customer Name:")
       c.drawString(left_margin + 120, details_top - 40, self.c_name.get())

       c.drawString(left_margin, details_top - 60, "Phone No.:")
       c.drawString(left_margin + 120, details_top - 60, self.contact.get())

       # Table for Orders
       table_top = details_top - 100
       table_height = 300
       row_height = 30
       c.roundRect(left_margin, table_top - table_height, right_margin - left_margin, table_height, 10, stroke=1,
                   fill=0)

       # Horizontal lines for rows
       for row in range(1, 11):  # 10 rows for data
           c.line(left_margin, table_top - row * row_height, right_margin, table_top - row * row_height)

       # Vertical lines for columns
       column_widths = [50, 200, 100, 50, 80]
       x_positions = [left_margin + sum(column_widths[:i]) for i in range(len(column_widths))]
       for x in x_positions:
           c.line(x, table_top, x, table_top - table_height)

       # Table Headers
       c.setFont("Times-Bold", 12)
       headers = ["S.No.", "Orders", "Price", "Qty.", "Total"]
       for i, header in enumerate(headers):
           c.drawCentredString(x_positions[i] + column_widths[i] / 2 - (0 if i == 0 else 10), table_top - 15, header)

       # Footer
       footer_y = 80
       c.setFont("Times-Roman", 12)
       c.drawString(left_margin, footer_y + 10, "This is system generated invoice.")
       c.drawRightString(right_margin, footer_y + 10, f"{self.aus.get()}")
       c.drawRightString(right_margin, footer_y - 10, "Signature")

       # Save the PDF
       c.showPage()
       c.save()

   def get_timestamp_invoice_number(self):
       return datetime.now().strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS

   def save_last_country(self, country):
       with open(self.last_country_file, "w") as f:
           f.write(country)

   def load_last_country(self):
       if os.path.exists(self.last_country_file):
           with open(self.last_country_file, "r") as f:
               return f.read().strip()
       return "Netherlands"  # Default country

       # ==== creating main function

def main():
   # ==== create tkinter window
   root = Tk()
   # === creating object for class InvoiceGenerator
   obj = InvoiceGenerator(root)
   # ==== start the gui
   root.mainloop()

if __name__ == "__main__":
   # ==== calling main function
   main()




# Now we need to add a sql backend to be able to track the invoices generated.
# We can use sqlite3 for this.
# we also need a pyinstaller added


# 2. Save data locally (e.g., SQLite for storing invoices).
# 3. Package the app as an executable using tools like PyInstaller. This eliminates the need for Python installation on their systems.
# 4. Add a feature to view the list of invoices generated in the past.

## ALso why is it that at 100%, the invoice looks small ?
## Now how do I deploy a tkinter app as a web app or a standalone app.