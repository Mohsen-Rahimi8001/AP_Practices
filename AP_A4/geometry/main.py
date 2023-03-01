import turtle
import geometry as gt # it should be exactly gt because it is used in eval function.
from tkinter import *
from tkinter import ttk, messagebox, Event, filedialog
import time
from threading import Thread
import datetime as dt
import os
import random
import math

# main root
root = Tk()
root.title("Geometry")
root.resizable(1, 1)
root.geometry("600x700")

# app flags
is_quiz = False
is_running = True

# shape list
shape_list = gt.ShapeList()

def create_shape_object(shape, *values:str):
    """Creates new shape object and add it to the shape list."""
    
    global shape_list
    success = False
    if shape == 'Circle':
        assert len(values) == 1
        if not values[0].strip().isdigit():
            messagebox.showerror("ValueError", "Invalid inputs")
        else:
            circle = gt.Circle(float(values[0]))
            shape_list.add_shape(circle)
            success = True

    elif shape == 'Triangle':
        assert len(values) == 3 
        if not values[0].strip().isdigit() or not values[1].strip().isdigit() or not values[2].strip().isdigit():
            messagebox.showerror("ValueError", "Invalid inputs")
        else:
            try:
                tri = gt.Triangle(float(values[0]), float(values[1]), float(values[2]))
            except ValueError as exp:
                messagebox.showerror("ValueError", str(exp))
            else:
                shape_list.add_shape(tri)
                success = True
    
    elif shape == 'Equilateral_Triangle':
        assert len(values) == 1
        if not values[0].strip().isdigit():
            messagebox.showerror("ValueError", "Invalid inputs")
        else:
            etri = gt.Equilateral_Triangle(float(values[0]))
            shape_list.add_shape(etri)
            success = True

    elif shape == 'Rectangle':
        assert len(values) == 2
        if not values[0].strip().isdigit() or not values[1].strip().isdigit():
            messagebox.showerror("ValueError", "Invalid inputs")
        else:
            rec = gt.Rectangle(float(values[0]), float(values[1]))
            shape_list.add_shape(rec)
            success = True

    elif shape == 'Square':
        assert len(values) == 1
        if not values[0].strip().isdigit():
            messagebox.showerror("ValueError", "Invalid inputs")
        else:
            sq = gt.Square(float(values[0]))
            shape_list.add_shape(sq)
            success = True
        
    elif shape == 'Regular_Pantagon':
        assert len(values) == 1
        if not values[0].strip().isdigit():
            messagebox.showerror("ValueError", "Invalid inputs")
        else:
            rp = gt.Regular_Pantagon(float(values[0]))
            shape_list.add_shape(rp)
            success = True

    if success:
        messagebox.showinfo("Success", f"{shape} added successfully.")

def get_specification(shape):
    """Gets the specification of the selected new shape."""
    global components_to_delete

    width = 5
    for component in components_to_delete:
        component.destroy()
    components_to_delete.clear()

    get_side_frame = Frame(mainframe)
    get_side_frame.grid(row=1, column=1)

    if shape == 'Circle':
        lbl_radius = Label(get_side_frame, text='Radius: ')
        radius = Entry(get_side_frame, width=width)
        lbl_radius.grid(sticky="w", row=0, column=0)
        radius.grid(sticky="w", row=0, column=1, padx=5, pady=10)
        components_to_delete.extend([lbl_radius, radius])
        radius.bind('<Return>', lambda event:create_shape_object('Circle', radius.get()))

    elif shape == 'Triangle':
        lbl_a = Label(get_side_frame, text='a: ')
        a = Entry(get_side_frame, width=width)

        lbl_a.grid(sticky="w", row=0, column=0)
        a.grid(sticky="w", row=0, column=1, pady=10)
        
        lbl_b = Label(get_side_frame, text='b: ')
        b = Entry(get_side_frame, width=width)

        lbl_b.grid(sticky="w", row=0, column=2)
        b.grid(sticky="w", row=0, column=3, pady=10)

        lbl_c = Label(get_side_frame, text='c: ')
        c = Entry(get_side_frame, width=width)

        lbl_c.grid(sticky="w", row=0, column=4)
        c.grid(sticky="w", row=0, column=5, pady=10)

        components_to_delete.extend([a, b, c, lbl_a, lbl_b, lbl_c])
        
        c.bind('<Return>', lambda event:create_shape_object('Triangle', a.get(), b.get(), c.get()))

    elif shape == 'Equilateral_Triangle':
        lbl_a = Label(get_side_frame, text='a: ')
        a = Entry(get_side_frame, width=width)
        lbl_a.grid(sticky="w", row=0, column=0)
        a.grid(sticky="w", row=0, column=1, padx=5, pady=10)
        components_to_delete.extend([lbl_a, a])
        a.bind('<Return>', lambda event:create_shape_object('Equilateral_Triangle', a.get()))

    elif shape == 'Rectangle':
        lbl_len = Label(get_side_frame, text='l: ')
        len = Entry(get_side_frame, width=width)
        lbl_len.grid(sticky="w", row=0, column=0)
        len.grid(sticky="w", row=0, column=1, padx=5, pady=10)
        
        lbl_wid = Label(get_side_frame, text='w: ')
        wid = Entry(get_side_frame, width=width)
        lbl_wid.grid(sticky="w", row=0, column=2)
        wid.grid(sticky="w", row=0, column=3, padx=5, pady=10)

        components_to_delete.extend([len, wid, lbl_len, lbl_wid])

        wid.bind('<Return>', lambda event:create_shape_object('Rectangle', len.get(), wid.get()))

    elif shape == 'Square':
        lbl_len = Label(get_side_frame, text='length: ')
        len = Entry(get_side_frame, width=width)
        lbl_len.grid(sticky="w", row=0, column=0)
        len.grid(sticky="w", row=0, column=1, padx=5, pady=10)
        components_to_delete.extend([len, lbl_len])
        len.bind("<Return>", lambda event: create_shape_object('Square', len.get()))

    elif shape == 'Regular_Pantagon':
        lbl_a = Label(get_side_frame, text='length: ')
        a = Entry(get_side_frame, width=width)
        lbl_a.grid(sticky="w", row=0, column=0)
        a.grid(sticky="w", row=0, column=1, padx=5, pady=10)

        components_to_delete.extend([a, lbl_a])
        a.bind("<Return>", lambda event: create_shape_object('Regular_Pantagon', a.get()))


def save_shapes_table(shapes_table:str):
    """Asks the user to give a directory and saves the shape table in a md file."""

    directory = filedialog.askdirectory()
    if not os.path.exists(directory):
        messagebox.showerror("Directory error", f"{directory} is a invalid directory.")
    else:
        with open(f'{directory}/shapes_table.md', 'w') as f:
            f.write(shapes_table)
        messagebox.showinfo("Success", f"The file saved at {directory}/shape_table.md")

class Turtle:
    """Turtle class"""

    def __init__(self):
        # control the root of the turtle.
        window = turtle.getscreen()
        canvas = window.getcanvas()
        self.root = canvas.winfo_toplevel() # root of the turtle object
        self.root.protocol("WM_DELETE_WINDOW", self.close) # it avoides closing turtle window before the program is closed.
        
        # turtle object
        self.tur = turtle.Turtle()
        self.tur.color('purple', 'orange')
    
    def draw_circle(self, r):
        """Draws a circle with the radius of r."""
        self.tur.circle(r)

    def draw_triangle(self, a, b, c, a_b, a_c, b_c):
        """Draws a triangle with sides a, b, c and angles a_b, a_c, b_c"""
        self.tur.forward(a * 10)
        self.tur.left(180 - a_b)
        self.tur.forward(b * 10)
        self.tur.left(180 - b_c)
        self.tur.forward(c * 10)
        self.tur.left(180 - a_c)

    def draw_rectangle(self, a, b):
        """Draws a rectangle with sides a, b."""
        self.tur.forward(a)
        self.tur.left(90)
        self.tur.forward(b)
        self.tur.left(90)
        self.tur.forward(a)
        self.tur.left(90)
        self.tur.forward(b)
        self.tur.left(90)

    def draw_regular_pantagon(self, a):
        """Draws a regular pantagon with the side of a."""
        self.tur.forward(a)
        self.tur.left(72)
        self.tur.forward(a)
        self.tur.left(72)
        self.tur.forward(a)
        self.tur.left(72)
        self.tur.forward(a)
        self.tur.left(72)
        self.tur.forward(a)

    def draw(self, shape_str):
        """Draws the given shape."""

        self.tur.clear()
        shape = eval('gt.' + shape_str)
        self.tur.begin_fill()

        if isinstance(shape, gt.Circle):
            self.draw_circle(shape.r)

        elif isinstance(shape, gt.Triangle):
            a = shape.a
            b = shape.b
            c = shape.c
            area = shape.get_area()
            # S = 1/2 * ab * sin(a_b) = sqrt(s(s-a)(s-b)(s-c)) --> a_b = arcsin(2 * S / ab)
            a_b = math.asin(2 * area / (a*b)) * 180 / math.pi 
            a_c = math.asin(2 * area / (a*c)) * 180 / math.pi
            b_c = math.asin(2 * area / (b*c)) * 180 / math.pi
            self.draw_triangle(a, b, c, a_b, a_c, b_c)

        elif isinstance(shape, gt.Equilateral_Triangle):
            a = shape.a * 10
            self.draw_triangle(a, a, a, 60, 60, 60)
            
        elif isinstance(shape, gt.Rectangle):
            a = shape.a * 10
            b = shape.b * 10
            self.draw_rectangle(a, b)

        elif isinstance(shape, gt.Square):
            a = shape.a * 10
            self.draw_rectangle(a, a)

        elif isinstance(shape, gt.Regular_Pantagon):
            a = shape.a * 10
            self.draw_regular_pantagon(a)

        self.tur.end_fill()

    def close(self):
        """closes the turtle root if is_running flag is False"""
        # if is_running flag is True the turtle root should remain open.
        if is_running:
            messagebox.showerror("Close Error", "You can not close turtle window before closing the whole app.")
        else:
            turtle.bye()

def get_shape_to_draw(row):
    """Gets the shape to be drawn."""
    shape = StringVar()
    combo = ttk.Combobox(mainframe, textvariable=shape, values=shape_list.shapes)
    combo['state'] = 'readonly'
    combo.grid(sticky="news", row=row, column=1, padx=10, pady=10)
    
    combo.bind("<<ComboboxSelected>>", lambda event: tur.draw(shape.get()))

def show_formula(shape_formula, row):
    """Shows the formula of the given shape."""

    global info_components

    if is_quiz:
        messagebox.showwarning("Quiz mode warning", "you are in quiz mode. you can use this option after your quiz.")
        return
    
    txt_formula = Text(mainframe, height=4, width=30)
    info_components.append(txt_formula)
    
    txt_formula.grid(sticky="news", row=row, column=1, padx=10, pady=10)
    if shape_formula == 'Circle':
        text = f"""area: {gt.Circle.get_area_formula()}
perimeter: {gt.Circle.get_perimeter_formula()}
        """
    elif shape_formula == 'Triangle':
        text = f"""area: {gt.Triangle.get_area_formula()}
perimeter: {gt.Triangle.get_perimeter_formula()}
        """
    elif shape_formula == 'Equilateral_Triangle':
        text = f"""area: {gt.Equilateral_Triangle.get_area_formula()}
perimeter: {gt.Equilateral_Triangle.get_perimeter_formula()}
        """
    elif shape_formula == 'Rectangle':
        text = f"""area: {gt.Rectangle.get_area_formula()}
perimeter: {gt.Rectangle.get_perimeter_formula()}
        """
    elif shape_formula == 'Square':
        text = f"""area: {gt.Square.get_area_formula()}
perimeter: {gt.Square.get_perimeter_formula()}
        """
    elif shape_formula == 'Regular_Pantagon':
        text = f"""area: {gt.Regular_Pantagon.get_area_formula()}
perimeter: {gt.Regular_Pantagon.get_perimeter_formula()}
        """
    txt_formula.insert(END, text)


def get_shape_to_show_formula(row):
    """Gets the shape to show its formula"""

    shape_formula = StringVar()
    combo_shapes_formula = ttk.Combobox(mainframe, textvariable=shape_formula, values=shape_list.AVAILABLE_SHAPES)
    combo_shapes_formula['state'] = 'readonly'
    combo_shapes_formula.grid(sticky="news", row=row, column=1, padx=10, pady=10)

    combo_shapes_formula.bind("<<ComboboxSelected>>", lambda event: show_formula(shape_formula.get(), row+1))

def show_largest_by_area(row, col):
    """Shows the largest area in the shape list by its area."""

    global info_components

    if is_quiz:
        messagebox.showwarning("Quiz mode warning", "you are in quiz mode. you can use this option after your quiz.")
        return

    if largest := shape_list.get_largest_shape_by_area():
        tur.draw(str(largest))
        txt_formula = Text(mainframe, height=4, width=25)
        info_components.append(txt_formula)
        txt_formula.grid(sticky="news", row=row, column=col, padx=10, pady=10)
        txt_formula.insert(END, f"shape: {largest}\narea: {largest.get_area()}")

def show_largest_by_perimeter(row, col):
    """Shows the largest area in the shape list by its perimeter."""

    global info_components
    
    if is_quiz:
        messagebox.showwarning("Quiz mode warning", "you are in quiz mode. you can use this option after your quiz.")
        return

    if largest := shape_list.get_largest_shape_by_perimeter():
        tur.draw(str(largest))
        txt_formula = Text(mainframe, height=4, width=25)
        info_components.append(txt_formula)
        txt_formula.grid(sticky="news", row=row, column=col, padx=10, pady=10)
        txt_formula.insert(END, f"shape: {largest}\nperimeter: {largest.get_perimeter()}")

def show_all_shapes(row, col):
    """Shows all the shapes in the shape list."""

    global info_components
    
    if is_quiz:
        messagebox.showwarning("Quiz mode warning", "you are in quiz mode. you can use this option after your quiz.")
        return

    if len(shape_list.shapes):
        txt_formula = Text(mainframe, height=8, width=35)
        info_components.append(txt_formula)
        txt_formula.grid(sticky="news", row=row, column=col, padx=10, pady=10)
        for shape in shape_list.shapes:
            txt_formula.insert(END, str(shape) + '\n')
            txt_formula.see(END)
            tur.draw(str(shape))
            root.after(2000)

def check_the_answer(area:str, perimeter:str, shape, frame:ttk.LabelFrame):
    """Checks the user answer to the question."""
    
    global is_quiz
    is_quiz = False
    frame.destroy()

    try:
        area, perimeter = float(area), float(perimeter)
    except ValueError:
        messagebox.showerror("Value Error", "Your answer is not valid.")
    else:
        correct_ans = (shape.get_area(), shape.get_perimeter())
        if math.isclose(area, correct_ans[0]) and math.isclose(perimeter, correct_ans[1]):
            messagebox.showinfo("Result", "Congrats, your answer is true!")
        else:
            messagebox.showinfo("Result", f"Your answer is wrong.\nThe corrct answer is:\nArea: {correct_ans[0]}, Perimeter: {correct_ans[1]}\n"
                f"the formula is:\nArea: {shape.get_area_formula()}, Perimeter: {shape.get_perimeter_formula()}")

def timer(minutes:int, row:int, col:int, frame:Frame):
    """Timer for the quiz. it should be used in a separate thread."""
    
    remainder_time = dt.datetime(1, 1, 1, 0, int(minutes))
    lbl_timer = Label(frame, text=remainder_time.strftime("%M:%S"))
    lbl_timer.grid(row=row, column=col)

    while remainder_time > dt.datetime(1, 1, 1, 0, 0):
        remainder_time -= dt.timedelta(seconds=1)
        time.sleep(1)
        lbl_timer.configure(text=remainder_time.strftime("%M:%S"))
    
    messagebox.showinfo("Time notification", "Times up!!!")
    frame.destroy()

def get_quiz(row, col):
    """Gets quiz"""

    global info_components, is_quiz, quiz_frame

    for cmp in info_components:
        cmp.destroy()

    info_components.clear()
    is_quiz = True
    shape = random.choice(shape_list.AVAILABLE_SHAPES)
    
    if shape == 'Circle':
        shape = gt.Circle(random.randint(1, 10))
    elif shape == 'Triangle':
        first, second = random.randint(1, 10), random.randint(1, 10)
        third = first + second - 1
        shape = gt.Triangle(first, second, third)
    elif shape == 'Equilateral_Triangle':
        shape = gt.Equilateral_Triangle(random.randint(1, 10))
    elif shape == 'Rectangle':
        shape = gt.Rectangle(random.randint(1, 10), random.randint(1, 10))
    elif shape == 'Square':
        shape = gt.Square(random.randint(1, 10))
    elif shape == 'Regular_Pantagon':
        shape = gt.Square(random.randint(1, 10))
    
    quiz_frame = ttk.LabelFrame(mainframe, text='Quiz')
    lbl_question = Label(quiz_frame, text=f'{shape}?')
    lbl_area = Label(quiz_frame, text='Area: ')
    lbl_perimeter = Label(quiz_frame, text='Perimeter: ')
    e_area = Entry(quiz_frame)
    e_perimeter = Entry(quiz_frame)
    btn_submit = Button(quiz_frame, text='Submit', command=lambda:check_the_answer(e_area.get(), e_perimeter.get(), shape, quiz_frame))
    
    lbl_question.grid(sticky="news", row=0, column=0, padx=10, pady=10)
    time_thread = Thread(target=lambda:timer(5, 0, 2, quiz_frame))
    time_thread.start()
    lbl_area.grid(sticky="news", row=1, column=1, padx=10, pady=10)
    e_area.grid(sticky="news", row=1, column=2, padx=10, pady=10)
    lbl_perimeter.grid(sticky="news", row=2, column=1, padx=10, pady=10)
    e_perimeter.grid(sticky="news", row=2, column=2, padx=10, pady=10)
    btn_submit.grid(sticky="news", row=2, column=0, padx=10, pady=10)

    quiz_frame.grid(sticky="news", row=row, column=col)

def close_the_program():
    """Controls the close button."""
    global is_running, tur
    is_running = False
    root.destroy()
    tur.close()

# these components will collect the specification of new shapes and should be removed after creating new shape.
components_to_delete = []

# Components that should be deleted when the user is in quiz mode.
info_components = []

# turtle object
tur = Turtle()

# main frame of the window.
mainframe = Frame(root)
mainframe.grid(sticky="news", row=0, column=0, padx=50, pady=10)

# title of Add new shape option
lbl_title = Label(mainframe, text="Add new shape", font=('Helvetica', 12) )
lbl_title.grid(sticky="news", row=0, column=0, padx=10, pady=10)

# gets new shape type
shape = StringVar()
combo_shapes = ttk.Combobox(mainframe, textvariable=shape, values=shape_list.AVAILABLE_SHAPES)
combo_shapes['state'] = 'readonly'
combo_shapes.grid(sticky="news", row=1, column=0, padx=10, pady=10)
combo_shapes.bind('<<ComboboxSelected>>', lambda event:get_specification(shape.get()))

# button to save the shape table in a file.
btn_save_table = Button(mainframe, text="Save table", command=lambda:save_shapes_table(shape_list.get_shapes_table()))
btn_save_table.grid(sticky="news", row=2, column=0, padx=10, pady=10)

# button to draw shapes.
btn_draw_by_turtle = Button(mainframe, text="Draw with turtle", command=lambda:get_shape_to_draw(3))
btn_draw_by_turtle.grid(sticky="news", row=3, column=0, padx=10, pady=10)

# button to show formula
btn_show_formula = Button(mainframe, text="Show Formula", command=lambda:get_shape_to_show_formula(4))
btn_show_formula.grid(sticky="news", row=4, column=0, padx=10, pady=10)

# button to show the largest shape by its area
btn_largest_by_area = Button(mainframe, text='Largest by area', command=lambda:show_largest_by_area(7, 0))
btn_largest_by_area.grid(sticky="news", row=6, column=0, padx=10, pady=10)

# button to show the largest shape by its perimeter
btn_largest_by_perimeter = Button(mainframe, text='Largest by perimeter', command=lambda:show_largest_by_perimeter(7, 1))
btn_largest_by_perimeter.grid(sticky="news", row=6, column=1, padx=10, pady=10)

# button to show all shapes.
btn_show_all_shapes = Button(mainframe, text='Show all shapes', command=lambda:show_all_shapes(9, 0))
btn_show_all_shapes.grid(sticky="news", row=8, column=0, padx=10, pady=10)

# quiz section
quiz_frame = Frame(mainframe)
btn_quiz = Button(mainframe, text='Quiz', command=lambda:get_quiz(11, 0))
btn_quiz.grid(sticky="news", row=10, column=0, padx=10, pady=10)

# controls close button.
root.protocol("WM_DELETE_WINDOW", close_the_program)

root.mainloop()
