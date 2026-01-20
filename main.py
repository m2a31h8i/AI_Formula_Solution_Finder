from tkinter import *
from tkinter import ttk, messagebox
import sympy as sp

Formula_finder = Tk()
Formula_finder.geometry("400x600")
Formula_finder.minsize(175,350)
Formula_finder.title("🧠 Formula Finder")

back = Frame(Formula_finder, width=400, height=600, bg="peachpuff", relief=SUNKEN)
back.pack()

search_bar = Label(back, text="🔍 Search for a Formula:", font=("Arial", 12), relief=SUNKEN)
search_bar.pack()

Formula_finder.search_var = StringVar()
search_entry = ttk.Entry(back, textvariable=Formula_finder.search_var)
search_entry.pack()

# --------------- FORMULA DATABASE ---------------
formulas = {
    "Ohm's Law": "V = I * R",
    "Kinetic Energy": "KE = 0.5 * m * v**2",
    "Newton's Second Law": "F = m * a",
    "Gravitational Force": "F = G * m1 * m2 / r**2",
    "Density": "ρ = m / V",
    "Speed": "s = d / t",
    "Work": "W = F * d",
    "Power (mechanical)": "P = W / t",
    "Power (electrical)": "P = V * I",
    "Momentum": "p = m * v",
    "Pressure": "P = F / A",
    "Acceleration": "a = (v - u) / t",
    "Potential Energy": "PE = m * g * h",
    "Frequency": "f = 1 / T",
    "Coulomb's Law": "F = k * q1 * q2 / r**2",
    "Ideal Gas Law": "PV = n * R * T",
    "Wave Speed": "v = f * λ",
    "Circle Circumference": "C = 2 * pi * r",
    "Volume of Sphere": "V = (4/3) * pi * r**3",
    "Area of Circle": "A = pi * r**2",
}

# --------------- PARSE FORMULAS ---------------
parsed_formulas = {}
for name, expression in formulas.items():
    lhs, rhs = expression.split("=")
    lhs = lhs.strip()
    rhs = rhs.strip()
    equation = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
    parsed_formulas[name] = equation

def update_list(event=None):
    search_term = Formula_finder.search_var.get().lower()
    Formula_finder.formula_listbox.delete(0, END)
    for name in formulas.keys():
        if search_term in name.lower() or search_term in formulas[name].lower():
            Formula_finder.formula_listbox.insert(END, name)

last_selected_formula = [None]

def formula_selected(event):
    selected_index = Formula_finder.formula_listbox.curselection()
    if not selected_index:
        return

    formula_name = Formula_finder.formula_listbox.get(selected_index)
    if last_selected_formula[0] == formula_name:
        return  # Don't recreate if already selected
    last_selected_formula[0] = formula_name

    for widget in Formula_finder.input_frame.winfo_children():
        widget.destroy()

    selected_index = Formula_finder.formula_listbox.curselection()
    if not selected_index:
        return

    formula_name = Formula_finder.formula_listbox.get(selected_index)
    Formula_finder.eq = parsed_formulas[formula_name]
    variables = list(Formula_finder.eq.free_symbols)

    # Dropdown to select variable to solve for
    Label(Formula_finder.input_frame, text="Select variable to solve for:", font=("Arial", 11)).pack()
    Formula_finder.solve_var = StringVar()
    solve_for_menu = ttk.Combobox(Formula_finder.input_frame, values=[str(v) for v in variables], textvariable=Formula_finder.solve_var)
    solve_for_menu.pack(pady=5)
    solve_for_menu.bind("<Return>", lambda e: solve_formula())

    # Entry fields for each variable
    Formula_finder.inputs = {}
    for var in variables:
        row = Frame(Formula_finder.input_frame)
        row.pack(fill="x", pady=2)
        Label(row, text=f"Enter {var}:", width=15, anchor="w").pack(side="left")
        entry = Entry(row)
        entry.pack(side="left", fill="x", expand=True)
        Formula_finder.inputs[str(var)] = entry
        entry.bind("<Return>", lambda e: solve_formula())

def solve_formula():
    try:
        variable = Formula_finder.solve_var.get()
        if not variable:
            messagebox.showerror("Error", "Please select a variable to solve for.")
            return

        known_values = {}
        for name, input_field in Formula_finder.inputs.items():
            if name == variable:
                continue
            value = input_field.get().strip()
            if not value:
                messagebox.showerror("Missing Input", f"Please enter a value for '{name}'.")
                return
            known_values[sp.Symbol(name)] = float(value)

        target_symbol = sp.Symbol(variable)
        solutions = sp.solve(Formula_finder.eq, target_symbol)

        if not solutions:
            messagebox.showerror("Error", "No solution could be found for that variable.")
            return

        first_solution = solutions[0]
        result = first_solution.subs(known_values).evalf()

        Formula_finder.result_label.config(text=f"{variable} = {result:.4f}")

    except Exception as error:
        messagebox.showerror("Error", f"Something went wrong:\n{error}")

# Listbox for formulas
Formula_finder.formula_listbox = Listbox(back, height=10, font=("Arial", 11))
Formula_finder.formula_listbox.pack(pady=5)
for name in formulas.keys():
    Formula_finder.formula_listbox.insert(END, name)
Formula_finder.formula_listbox.bind("<<ListboxSelect>>", formula_selected)

Formula_finder.input_frame = Frame(back)
Formula_finder.input_frame.pack(pady=10)

Formula_finder.result_label = Label(back, text="", font=("Arial", 12), bg="peachpuff")
Formula_finder.result_label.pack(pady=10)

solve = Button(back, text="🧮 Solve", font=("Arial", 12), command=solve_formula)
solve.pack(pady=5, padx=1, side=BOTTOM)

# Bind search entry to update list taki vo list auto off na ho 
search_entry.bind("<KeyRelease>", update_list)

update_list()

Formula_finder.mainloop()
