import tkinter as tk
from tkinter import messagebox, ttk
from information import CustomerData, VideoData

class Customer:
    def __init__(self, last, first, addy, p_num, email, cid):
        self.first = first
        self.last = last
        self.addy = addy
        self.p_num = p_num
        self.email = email
        self.cid = cid

    def __str__(self):
        return f"{self.first} {self.last} - {self.email}"

    def get_full_info(self):
        return f"ID: {self.cid}\nName: {self.first} {self.last}\nAddress: {self.addy}\nPhone: {self.p_num}\nEmail: {self.email}"

customerList = []

def addCustomer(customer):
    if any(c.cid == customer.cid for c in customerList):
        return False
    customerList.append(customer)
    return True

def editCustomer(customer):
    for idx, c in enumerate(customerList):
        if c.cid == customer.cid:
            customerList[idx] = customer
            return True
    return False

def removeCustomer(cid):
    global customerList
    customerList = [c for c in customerList if c.cid != cid]
    return True

def getCustomer(cid):
    for c in customerList:
        if c.cid == cid:
            return c
    return None

def listCustomers():
    return customerList

class CustomerForm(tk.Toplevel):
    def __init__(self, master, app, customer=None, is_edit=False):
        super().__init__(master)
        self.app = app
        self.title("Customer Information")
        self.customer = customer
        self.is_edit = is_edit
        self.create_widgets()
        self.grab_set()

    def create_widgets(self):
        self.label_cid = tk.Label(self, text="Customer ID:")
        self.label_cid.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_cid = tk.Entry(self)
        self.entry_cid.grid(row=0, column=1, padx=10, pady=5)

        if self.is_edit and self.customer:
            self.entry_cid.insert(0, self.customer['cid'])
            self.entry_cid.config(state='readonly')
        else:
            self.entry_cid.config(state='normal')

        self.label_first = tk.Label(self, text="First Name:")
        self.label_first.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_first = tk.Entry(self)
        self.entry_first.grid(row=1, column=1, padx=10, pady=5)

        if self.customer:
            self.entry_first.insert(0, self.customer['first'])

        self.label_last = tk.Label(self, text="Last Name:")
        self.label_last.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_last = tk.Entry(self)
        self.entry_last.grid(row=2, column=1, padx=10, pady=5)

        if self.customer:
            self.entry_last.insert(0, self.customer['last'])

        self.label_addy = tk.Label(self, text="Address:")
        self.label_addy.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_addy = tk.Entry(self)
        self.entry_addy.grid(row=3, column=1, padx=10, pady=5)

        if self.customer:
            self.entry_addy.insert(0, self.customer['addy'])

        self.label_pnum = tk.Label(self, text="Phone Number:")
        self.label_pnum.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_pnum = tk.Entry(self)
        self.entry_pnum.grid(row=4, column=1, padx=10, pady=5)

        if self.customer:
            self.entry_pnum.insert(0, self.customer['p_num'])

        self.label_email = tk.Label(self, text="Email:")
        self.label_email.grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_email = tk.Entry(self)
        self.entry_email.grid(row=5, column=1, padx=10, pady=5)

        if self.customer:
            self.entry_email.insert(0, self.customer['email'])

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

    def save(self):
        cid = self.entry_cid.get().strip()
        first = self.entry_first.get().strip()
        last = self.entry_last.get().strip()
        addy = self.entry_addy.get().strip()
        p_num = self.entry_pnum.get().strip()
        email = self.entry_email.get().strip()

        if not cid or not first or not last or not email:
            messagebox.showerror("Error", "Customer ID, First Name, Last Name, and Email are required.")
            return

        new_customer = Customer(last=last, first=first, addy=addy, p_num=p_num, email=email, cid=cid)
        info_customer = CustomerData()
        if self.is_edit:
            editCustomer(new_customer)
            info_customer.edit_customer(new_first=first, new_last=last, new_addy=addy, new_phone=p_num, new_email=email, cust_id=cid)
            messagebox.showinfo("Success", f"Customer {cid} updated.")
        else:
            if addCustomer(new_customer):
                info_customer.add_customer(first=first, last=last, addy=addy, p_num=p_num, email=email, cid=cid)
                messagebox.showinfo("Success", f"Customer {cid} added.")
            else:
                messagebox.showerror("Error", f"Customer with ID {cid} already exists.")
                return
        self.app.refresh_customer_list()
        self.destroy()

class CustomerApp:
    def __init__(self, root):
        self.root = root
        self.create_widgets()
        self.refresh_customer_list()

    def create_widgets(self):
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(side=tk.TOP, fill=tk.X)

        self.search_label = tk.Label(self.search_frame, text="Search:")
        self.search_label.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind('<KeyRelease>', self.on_search)

        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.customer_listbox = tk.Listbox(self.list_frame, yscrollcommand=self.scrollbar.set)
        self.customer_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.customer_listbox.bind('<<ListboxSelect>>', self.on_select)

        self.scrollbar.config(command=self.customer_listbox.yview)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.add_button = tk.Button(self.button_frame, text="Add Customer", command=self.add_customer)
        self.add_button.pack(fill=tk.X)

        self.edit_button = tk.Button(self.button_frame, text="Edit Customer", command=self.edit_customer)
        self.edit_button.pack(fill=tk.X)

        self.remove_button = tk.Button(self.button_frame, text="Remove Customer", command=self.remove_customer)
        self.remove_button.pack(fill=tk.X)

        self.show_details_button = tk.Button(self.button_frame, text="Show Details", command=self.show_details)
        self.show_details_button.pack(fill=tk.X)

    def refresh_customer_list(self, filter_text=""):
        self.customer_listbox.delete(0, tk.END)
        customer_data = CustomerData()
        all_customers = customer_data.get_all_customers()
        for customer in all_customers:
            display_text = f"{customer['first']} {customer['last']} - {customer['email']}"
            if filter_text.lower() in display_text.lower():
                self.customer_listbox.insert(tk.END, display_text)

    def on_search(self, event):
        filter_text = self.search_entry.get()
        self.refresh_customer_list(filter_text)

    def on_select(self, event):
        pass

    def add_customer(self):
        form = CustomerForm(self.root, app=self)
        self.root.wait_window(form)

    def edit_customer(self):
        selection = self.customer_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No customer selected.")
            return

        selected_text = self.customer_listbox.get(selection[0])

        customer_data = CustomerData()
        all_customers = customer_data.get_all_customers()

        for customer in all_customers:
            if f"{customer['first']} {customer['last']} - {customer['email']}" == selected_text:
                selected_customer = customer
                break
        else:
            messagebox.showerror("Error", "Customer not found.")
            return

        form = CustomerForm(self.root, app=self, customer=selected_customer, is_edit=True)
        self.root.wait_window(form)

    def remove_customer(self):
        selection = self.customer_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No customer selected.")
            return
        selected_text = self.customer_listbox.get(selection[0])

        customer_data = CustomerData()
        all_customers = customer_data.get_all_customers()

        for customer in all_customers:
            if f"{customer['first']} {customer['last']} - {customer['email']}" == selected_text:
                cid = customer['cid']
                break
        else:
            messagebox.showerror("Error", "Customer not found.")
            return

        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to remove customer {cid}?")
        if confirm:
            customer_data.remove_customer(cid)
            messagebox.showinfo("Success", f"Customer {cid} removed.")
            self.refresh_customer_list(self.search_entry.get())

    def show_details(self):
        selection = self.customer_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No customer selected.")
            return

        selected_text = self.customer_listbox.get(selection[0])

        customer_data = CustomerData()
        all_customers = customer_data.get_all_customers()

        for customer in all_customers:
            if f"{customer['first']} {customer['last']} - {customer['email']}" == selected_text:
                customer_info = (
                    f"First Name: {customer['first']}\n"
                    f"Last Name: {customer['last']}\n"
                    f"Address: {customer['addy']}\n"
                    f"Phone Number: {customer['p_num']}\n"
                    f"Email: {customer['email']}\n"
                    f"Customer ID: {customer['cid']}"
                )
                break
        else:
            messagebox.showerror("Error", "Customer not found.")
            return

        messagebox.showinfo("Customer Details", customer_info)

class VideoApp:
    def __init__(self, root):
        self.root = root
        self.create_widgets()
        self.video_list = []
        self.refresh_video_list()

    def create_widgets(self):
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(side=tk.TOP, fill=tk.X)

        self.search_label = tk.Label(self.search_frame, text="Search:")
        self.search_label.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind('<KeyRelease>', self.on_search)

        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.video_listbox = tk.Listbox(self.list_frame, yscrollcommand=self.scrollbar.set)
        self.video_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.video_listbox.bind('<<ListboxSelect>>', self.on_select)

        self.scrollbar.config(command=self.video_listbox.yview)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.add_button = tk.Button(self.button_frame, text="Add Video", command=self.add_video)
        self.add_button.pack(fill=tk.X)

        self.edit_button = tk.Button(self.button_frame, text="Edit Video", command=self.edit_video)
        self.edit_button.pack(fill=tk.X)

        self.remove_button = tk.Button(self.button_frame, text="Remove Video", command=self.remove_video)
        self.remove_button.pack(fill=tk.X)

        self.show_details_button = tk.Button(self.button_frame, text="Show Details", command=self.show_details)
        self.show_details_button.pack(fill=tk.X)

    def refresh_video_list(self, filter_text=""):
        self.video_listbox.delete(0, tk.END)
        video_data = VideoData()
        all_videos = video_data.get_all_videos()
        for video in all_videos:
            display_text = f"{video['title']} ({video['year']}) - {video['director']}"
            if filter_text.lower() in display_text.lower():
                self.video_listbox.insert(tk.END, display_text)

    def on_search(self, event):
        filter_text = self.search_entry.get()
        self.refresh_video_list(filter_text)

    def on_select(self, event):
        pass

    def add_video(self):
        form = VideoForm(self.root, app=self)
        self.root.wait_window(form)

    def edit_video(self):
        selection = self.video_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No video selected.")
            return

        selected_text = self.video_listbox.get(selection[0])
        video_data = VideoData()
        all_videos = video_data.get_all_videos()
        for video in all_videos:
            if f"{video['title']} ({video['year']}) - {video['director']}" == selected_text:
                selected_video = video
                break
        else:
            messagebox.showerror("Error", "Video not found.")
            return

        form = VideoForm(self.root, app=self, video=selected_video, is_edit=True)
        self.root.wait_window(form)

    def remove_video(self):
        selection = self.video_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No video selected.")
            return

        selected_text = self.video_listbox.get(selection[0])
        video_data = VideoData()
        all_videos = video_data.get_all_videos()
        for video in all_videos:
            if f"{video['title']} ({video['year']}) - {video['director']}" == selected_text:
                upc = video['upc']
                confirm = messagebox.askyesno("Confirm", f"Are you sure you want to remove video '{video['title']}'?")
                if confirm:
                    video_data.remove_video(upc_num=upc)
                    messagebox.showinfo("Success", f'Video {upc} removed.')
                    self.refresh_video_list()
                break
        else:
            messagebox.showerror("Error", "Video not found.")
            return

    def show_details(self):
        selection = self.video_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No video selected.")
            return

        selected_text = self.video_listbox.get(selection[0])
        video_data = VideoData()
        all_videos = video_data.get_all_videos()
        for video in all_videos:
            if f"{video['title']} ({video['year']}) - {video['director']}" == selected_text:
                video_info = (
                    f"Name: {video['title']}\n"
                    f"Director: {video['director']}\n"
                    f"Year: {video['year']}\n"
                    f"Rating: {video['rating']}\n"
                    f"Genre: {video['genre']}\n"
                    f"UPC: {video['upc']}\n"
                    f"Quantity: {video['qty']}"
                )
                messagebox.showinfo("Video Details", video_info)
                break
        else:
            messagebox.showerror("Error", "Video not found.")
            return
class VideoForm(tk.Toplevel):
    def __init__(self, master, app, video=None, is_edit=False):
        super().__init__(master)
        self.app = app
        self.title("Video Information")
        self.video = video
        self.is_edit = is_edit
        self.create_widgets()
        self.grab_set()

    def create_widgets(self):
        self.label_name = tk.Label(self, text="Title:")
        self.label_name.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_name = tk.Entry(self)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        if self.video:
            self.entry_name.insert(0, self.video['title'])

        self.label_director = tk.Label(self, text="Director:")
        self.label_director.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_director = tk.Entry(self)
        self.entry_director.grid(row=1, column=1, padx=10, pady=5)

        if self.video:
            self.entry_director.insert(0, self.video['director'])

        self.label_year = tk.Label(self, text="Year:")
        self.label_year.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_year = tk.Entry(self)
        self.entry_year.grid(row=2, column=1, padx=10, pady=5)

        if self.video:
            self.entry_year.insert(0, self.video['year'])

        self.label_rating = tk.Label(self, text="Rating:")
        self.label_rating.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_rating = tk.Entry(self)
        self.entry_rating.grid(row=3, column=1, padx=10, pady=5)

        if self.video:
            self.entry_rating.insert(0, self.video['rating'])

        self.label_genre = tk.Label(self, text="Genre:")
        self.label_genre.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_genre = tk.Entry(self)
        self.entry_genre.grid(row=4, column=1, padx=10, pady=5)

        if self.video:
            self.entry_genre.insert(0, self.video['genre'])
        
        self.label_upc = tk.Label(self, text="UPC:")
        self.label_upc.grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_upc = tk.Entry(self)
        self.entry_upc.grid(row=5, column=1, padx=10, pady=5)

        if self.video and self.is_edit:
            self.entry_upc.insert(0, self.video['upc'])
            self.entry_upc.config(state='readonly')
        else:
            self.entry_upc.config(state='normal')

        self.label_status = tk.Label(self, text="Quantity:")
        self.label_status.grid(row=6, column=0, padx=10, pady=5, sticky=tk.E)
        self.entry_status = tk.Entry(self)
        self.entry_status.grid(row=6, column=1, padx=10, pady=5)

        if self.video:
            self.entry_status.insert(0, self.video['qty'])

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=7, column=0, columnspan=2, pady=10)

        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

    def save(self):
        title = self.entry_name.get().strip()
        year = self.entry_year.get().strip()
        director = self.entry_director.get().strip()
        rating = self.entry_rating.get().strip()
        genre = self.entry_genre.get().strip()
        upc = self.entry_upc.get().strip()
        quantity = self.entry_status.get().strip()

        if not title or not director:
            messagebox.showerror("Error", "Title and Director are required.")
            return

        new_video = {
            'title': title,
            'year': year,
            'director': director,
            'rating': rating,
            'genre': genre,
            'upc': upc,
            'qty': quantity
        }
        info_video = VideoData()

        if self.is_edit:
            info_video.edit_video(new_title=title, new_year=year, new_director=director, new_rating=rating, new_genre=genre, upc_num=upc, new_qty=quantity)
            messagebox.showinfo("Success", f"Video '{title}' updated.")
        else:
            info_video.add_video(name=title, year=year, director=director, rating=rating, genre=genre, upc=upc, qty=quantity)
            messagebox.showinfo("Success", f"Video '{title}' added.")

        self.app.refresh_video_list()
        self.destroy()

class POSApp:
    def __init__(self, root, customer_data, video_data):
        self.root = root
        self.customer_data = customer_data
        self.video_data = video_data
        self.selected_customer_id = None  # Store the selected customer ID
        self.selected_movies = []         # Store selected movies
        self.create_widgets()

    class POSApp:
        def __init__(self, root, customer_data, video_data):
            self.root = root
            self.customer_data = customer_data
            self.video_data = video_data
            self.selected_customer_id = None  # Store the selected customer ID
            self.selected_movies = []         # Store selected movies
            self.create_widgets()

    def create_widgets(self):
        # Rental Section
        rental_frame = tk.Frame(self.root)
        rental_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(rental_frame, text="Select Customer").pack()
        self.customer_search_entry = tk.Entry(rental_frame)
        self.customer_search_entry.pack()
        self.customer_search_entry.bind('<KeyRelease>', self.on_customer_search)

        self.customer_listbox = tk.Listbox(rental_frame, selectmode=tk.SINGLE, exportselection=False)
        self.customer_listbox.pack(fill=tk.BOTH, expand=True)
        self.customer_listbox.bind('<<ListboxSelect>>', self.on_customer_select)

        tk.Label(rental_frame, text="Select Movies to Rent").pack()
        self.movie_search_entry = tk.Entry(rental_frame)
        self.movie_search_entry.pack()
        self.movie_search_entry.bind('<KeyRelease>', self.on_movie_search)

        self.movie_listbox = tk.Listbox(rental_frame, selectmode=tk.MULTIPLE, exportselection=False)
        self.movie_listbox.pack(fill=tk.BOTH, expand=True)
        self.movie_listbox.bind('<<ListboxSelect>>', self.on_movie_select)

        self.rent_button = tk.Button(rental_frame, text="Rent Selected Movies", command=self.rent_movies)
        self.rent_button.pack(pady=10)
        self.rent_button.config(state=tk.DISABLED)  # Disable until both selections are made

        # Return Section (Unchanged)
        return_frame = tk.Frame(self.root)
        return_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(return_frame, text="Customers with Rentals").pack()
        self.return_customer_search_entry = tk.Entry(return_frame)
        self.return_customer_search_entry.pack()
        self.return_customer_search_entry.bind('<KeyRelease>', self.on_customer_search)

        self.return_customer_listbox = tk.Listbox(return_frame, exportselection=False)
        self.return_customer_listbox.pack(fill=tk.BOTH, expand=True)
        self.return_customer_listbox.bind('<<ListboxSelect>>', self.on_select_rented_customer)

        tk.Label(return_frame, text="Rented Movies").pack()
        self.rented_movie_listbox = tk.Listbox(return_frame, selectmode=tk.MULTIPLE, exportselection=False)
        self.rented_movie_listbox.pack(fill=tk.BOTH, expand=True)

        self.return_button = tk.Button(return_frame, text="Return Selected Movies", command=self.return_movies)
        self.return_button.pack(pady=10)

        self.refresh_customer_list()
        self.refresh_movie_list()

    def refresh_customer_list(self):
        self.customer_listbox.delete(0, tk.END)
        for customer in self.customer_data.get_all_customers():
            display_text = f"{customer['first']} {customer['last']} - {customer['cid']}"
            self.customer_listbox.insert(tk.END, display_text)

    def return_movies(self):
    # Get the selected customer from the return section
     selection = self.return_customer_listbox.curselection()
     if not selection:
         messagebox.showwarning("Warning", "No customer selected for return.")
         return

     selected_customer_text = self.return_customer_listbox.get(selection[0])
     customer_id = selected_customer_text.split('-')[-1].strip()

    # Get the selected movies to return
     selected_movies = [self.rented_movie_listbox.get(i) for i in self.rented_movie_listbox.curselection()]
     if not selected_movies:
         messagebox.showwarning("Warning", "No movies selected for return.")
         return

    # Process each selected movie return
     for movie in selected_movies:
         title = movie.split('(')[0].strip()
         video = next((v for v in self.video_data.get_all_videos() if v['title'] == title), None)

         if video:
            # Increment quantity of returned video
             self.video_data.quantity_up(video['upc'])
            # Remove rental record from customer
             self.customer_data.remove_rental_from_customer(customer_id, video['upc'])

    # Inform the user of successful returns
     messagebox.showinfo("Return Success", "Movies successfully returned.")
    # Refresh movie and customer lists after return
     self.refresh_movie_list()
     self.refresh_customer_list()


    def on_select_rented_customer(self, event):
        # This method should handle the logic when a rented customer is selected in the return section
        selection = self.return_customer_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "No rented customer selected.")
            return

        selected_text = self.return_customer_listbox.get(selection[0])
        customer_id = selected_text.split('-')[-1].strip()

        # Example: Populate the rented_movie_listbox with movies rented by this customer
        self.rented_movie_listbox.delete(0, tk.END)
        rented_movies = self.customer_data.get_rented_movies(customer_id)
        for movie in rented_movies:
            self.rented_movie_listbox.insert(tk.END, movie)

    def refresh_movie_list(self):
        self.movie_listbox.delete(0, tk.END)
        for video in self.video_data.get_all_videos():
            display_text = f"{video['title']} ({video['year']}) - Qty: {video['qty']}"
            self.movie_listbox.insert(tk.END, display_text)

    def on_customer_search(self, event):
        search_text = self.customer_search_entry.get().lower()
        self.customer_listbox.delete(0, tk.END)
        for customer in self.customer_data.get_all_customers():
            if search_text in f"{customer['first']} {customer['last']}".lower():
                self.customer_listbox.insert(tk.END, f"{customer['first']} {customer['last']} - {customer['cid']}")

    def on_movie_search(self, event):
        search_text = self.movie_search_entry.get().lower()
        self.movie_listbox.delete(0, tk.END)
        for video in self.video_data.get_all_videos():
            if search_text in video['title'].lower():
                self.movie_listbox.insert(tk.END, f"{video['title']} ({video['year']}) - Qty: {video['qty']}")
    

    def on_customer_select(self, event):
        selection = self.customer_listbox.curselection()
        if selection:
            selected_customer = self.customer_listbox.get(selection[0])
            self.selected_customer_id = selected_customer.split('-')[-1].strip()
            self.check_selection_state()

    def on_movie_select(self, event):
        selected_movies = [self.movie_listbox.get(i) for i in self.movie_listbox.curselection()]
        self.selected_movies = selected_movies
        self.check_selection_state()

    def check_selection_state(self):
        # Enable the Rent button only if a customer and at least one movie are selected
        if self.selected_customer_id and self.selected_movies:
            self.rent_button.config(state=tk.NORMAL)
        else:
            self.rent_button.config(state=tk.DISABLED)

    def rent_movies(self):
        if not self.selected_customer_id:
            messagebox.showwarning("Select Customer", "Please select a customer.")
            return

        if not self.selected_movies:
            messagebox.showwarning("Select Movies", "Please select at least one movie.")
            return

        for video_title in self.selected_movies:
            title = video_title.split('(')[0].strip()
            video_data = next((v for v in self.video_data.get_all_videos() if v['title'] == title), None)
            if video_data and video_data['qty'] > 0:
                self.video_data.quantity_down(video_data['upc'])
                self.customer_data.add_rental_to_customer(self.selected_customer_id, video_data['upc'])
            else:
                messagebox.showwarning("Out of Stock", f"{title} is currently out of stock.")

        messagebox.showinfo("Rental Success", "Movies successfully rented.")
        self.refresh_movie_list()
        self.selected_customer_id = None
        self.selected_movies = []
        self.rent_button.config(state=tk.DISABLED)

    # Other methods remain the same...


# Main Application Initialization
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Video Store Management System")

    notebook = ttk.Notebook(root)

    customer_frame = tk.Frame(notebook)
    video_frame = tk.Frame(notebook)
    pos_frame = tk.Frame(notebook)

    notebook.add(customer_frame, text='Customers')
    notebook.add(video_frame, text='Videos')
    notebook.add(pos_frame, text='POS')

    notebook.pack(expand=1, fill='both')

    customer_app = CustomerApp(customer_frame)
    video_app = VideoApp(video_frame)
    pos_app = POSApp(pos_frame, CustomerData(), VideoData())

    root.mainloop()
