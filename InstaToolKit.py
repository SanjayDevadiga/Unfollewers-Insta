import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import instaloader
from threading import Thread

def login(username, password):
    try:
        L = instaloader.Instaloader()
        L.login(username, password)

        user_profile = instaloader.Profile.from_username(L.context, username)

        return user_profile

    except instaloader.TwoFactorAuthRequiredException:
        print("Two-factor authentication enabled!")
        return []
    
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_following(user_profile2):
    return user_profile2.get_followees()

def get_followers(user_profile2):
    return user_profile2.get_followers()

def on_button_click():
    username = entry1.get()
    password = entry2.get()

    profile = login(username, password)

    list_follower = []
    list_un_follower = []
    
    followers = get_followers(profile)
    for follower in followers:
        list_follower.append(follower.username)

    following = get_following(profile)
    for followee in following:
        list_un_follower.append(followee.username)

    not_following_back = [f for f in list_un_follower if f not in list_follower]
    not_following_back_str = "\n".join(not_following_back)

    messagebox.showinfo("Unfollowers", f"Inhone dhoka diya tereko:\n\n{not_following_back_str}")
    loader_label.pack_forget()

def start_process():
    loader_label.pack(pady=(10, 0))
    Thread(target=on_button_click).start()

def toggle_password():
    if show_password_var.get():
        entry2.config(show="")
    else:
        entry2.config(show="*")

root = tk.Tk()
root.title("Insta Dokebaz Finder")

root.geometry("400x300")

frame = tk.Frame(root)
frame.pack(pady=20)

label1 = tk.Label(frame, text="Username:")
label1.grid(row=0, column=0, padx=10, pady=5, sticky="e")

entry1 = tk.Entry(frame, width=30)
entry1.grid(row=0, column=1, padx=10, pady=5)

label2 = tk.Label(frame, text="Password:")
label2.grid(row=1, column=0, padx=10, pady=5, sticky="e")

entry2 = tk.Entry(frame, width=30, show="*")
entry2.grid(row=1, column=1, padx=10, pady=5)

show_password_var = tk.BooleanVar()
show_password_check = tk.Checkbutton(frame, text="Show Password", variable=show_password_var, command=toggle_password)
show_password_check.grid(row=2, columnspan=2)

button = tk.Button(root, text="Show Unfollowers", command=start_process)
button.pack(pady=20)

loader_label = ttk.Label(root, text="Loading...", font=("Helvetica", 10, "italic"))

label3 = tk.Label(root, text="Note: Disable Two-Factor authentication!", fg="red")
label3.pack(pady=(10, 0))

root.mainloop()