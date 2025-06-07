import tkinter as tk
from abc import ABC, abstractmethod

# ----------------------------
# Lógica de cálculo (S, O)
# ----------------------------

class OperationStrategy(ABC):
    @abstractmethod
    def execute(self, a, b):
        pass

class Add(OperationStrategy):
    def execute(self, a, b):
        return a + b

class Subtract(OperationStrategy):
    def execute(self, a, b):
        return a - b

class Multiply(OperationStrategy):
    def execute(self, a, b):
        return a * b

class Divide(OperationStrategy):
    def execute(self, a, b):
        if b == 0:
            raise ValueError("No se puede dividir entre cero.")
        return a / b

# ----------------------------
# Calculadora principal (S)
# ----------------------------

class Calculator:
    def __init__(self):
        self.result = 0

    def calculate(self, a, b, operation: OperationStrategy):
        return operation.execute(a, b)

# ----------------------------
# Interfaz gráfica (S)
# ----------------------------

class CalculatorGUI:
    def __init__(self, master):
        self.calculator = Calculator()
        self.master = master
        master.title("Calculadora SOLID")
        # master.geometry("500x500")

        self.entry1 = tk.Entry(master)
        self.entry2 = tk.Entry(master)
        self.result_label = tk.Label(master, text="Resultado: ")

        self.entry1.grid(row=0, column=1, padx=5, pady=5)
        self.entry2.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(master, text="Número 1:").grid(row=0, column=0)
        tk.Label(master, text="Número 2:").grid(row=1, column=0)
        self.result_label.grid(row=2, column=0, columnspan=2)

        # Botones
        self._create_buttons()

    def _create_buttons(self):
        tk.Button(self.master, text="+", command=self.add).grid(row=3, column=0)
        tk.Button(self.master, text="-", command=self.subtract).grid(row=3, column=1)
        tk.Button(self.master, text="×", command=self.multiply).grid(row=4, column=0)
        tk.Button(self.master, text="÷", command=self.divide).grid(row=4, column=1)
        tk.Button(self.master, text="Limpiar", command=self.clear_inputs).grid(row=5, column=0, columnspan=2)

    def _get_values(self):
        try:
            a = float(self.entry1.get())
            b = float(self.entry2.get())
            return a, b
        except ValueError:
            self.result_label.config(text="Error: Ingresa números válidos.")
            return None, None

    def _calculate_and_display(self, operation):
        a, b = self._get_values()
        if a is not None:
            try:
                result = self.calculator.calculate(a, b, operation)
                self.result_label.config(text=f"Resultado: {result}")
            except Exception as e:
                self.result_label.config(text=f"Error: {e}")

    def add(self):
        self._calculate_and_display(Add())

    def subtract(self):
        self._calculate_and_display(Subtract())

    def multiply(self):
        self._calculate_and_display(Multiply())

    def divide(self):
        self._calculate_and_display(Divide())
    # add method for clean inputs
    def clear_inputs(self):
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.result_label.config(text="Resultado: ")

# ----------------------------
# Lanzar aplicación
# ----------------------------

if __name__ == "__main__":
    root = tk.Tk()
    root.tk.call("tk", "scaling", 5.0)
    app = CalculatorGUI(root)
    root.mainloop()
