from Tkinter import *


class App:

    def __init__(self, master):
        frame = Frame(root, width=450, height=250)
        frame.pack()
        self.quote = Label(frame, text="hel", height=10, width=30, wraplength=300,
                           bg="#fff", padx=10, fg="#333", font=("Helvetica", 14))
        self.quote.pack()
        self.author = Label(frame, text="-" + "author", anchor="e",
                            justify='right', padx=20, pady=15, bg="#fff", fg="#444", font=("Helvetica", 12))
        self.author.pack(side="right")
        self.button = Button(frame, text="QUIT", fg="red", justify="left")
        self.button.bind("<Button-1>", self.callback)
        self.button.pack()
        self.hi_there = Button(frame, text="Hello",
                               command=self.say_hi, justify="left")
        self.hi_there.pack()

    def say_hi(self):
        print "hi there, everyone!"

    def callback(self, event):
        print "clicked at", event.x, event.y
root = Tk()
root.configure(background='#fff')
app = App(root)
root.mainloop()
