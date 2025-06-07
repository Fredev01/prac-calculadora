"""
Calculadora Básica con Tkinter siguiendo principios SOLID
Autor: Desarrollador Python
"""

import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod
from typing import Protocol


# S - Single Responsibility Principle
class CalculatorEngine:
    """Clase responsable únicamente de realizar cálculos matemáticos"""
    
    def add(self, a: float, b: float) -> float:
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("División por cero no permitida")
        return a / b


# O - Open/Closed Principle
class Operation(ABC):
    """Clase abstracta para operaciones - abierta para extensión, cerrada para modificación"""
    
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass
    
    @abstractmethod
    def get_symbol(self) -> str:
        pass


class AddOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a + b
    
    def get_symbol(self) -> str:
        return "+"


class SubtractOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a - b
    
    def get_symbol(self) -> str:
        return "-"


class MultiplyOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a * b
    
    def get_symbol(self) -> str:
        return "×"


class DivideOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("División por cero no permitida")
        return a / b
    
    def get_symbol(self) -> str:
        return "÷"


# L - Liskov Substitution Principle
class CalculatorOperations:
    """Maneja las operaciones de la calculadora usando el principio de sustitución"""
    
    def __init__(self):
        self.operations = {
            '+': AddOperation(),
            '-': SubtractOperation(),
            '×': MultiplyOperation(),
            '÷': DivideOperation()
        }
    
    def calculate(self, operation_symbol: str, a: float, b: float) -> float:
        if operation_symbol not in self.operations:
            raise ValueError(f"Operación {operation_symbol} no soportada")
        
        operation = self.operations[operation_symbol]
        return operation.execute(a, b)


# I - Interface Segregation Principle
class DisplayInterface(Protocol):
    """Interface para el manejo de la pantalla"""
    def update_display(self, value: str) -> None: ...
    def clear_display(self) -> None: ...
    def get_display_value(self) -> str: ...


class ButtonHandlerInterface(Protocol):
    """Interface para el manejo de botones"""
    def handle_number(self, number: str) -> None: ...
    def handle_operation(self, operation: str) -> None: ...
    def handle_equals(self) -> None: ...
    def handle_clear(self) -> None: ...


# D - Dependency Inversion Principle
class CalculatorModel:
    """Modelo de la calculadora - no depende de implementaciones concretas"""
    
    def __init__(self, calculator_ops: CalculatorOperations):
        self.calculator_ops = calculator_ops
        self.reset()
    
    def reset(self):
        self.current_value = 0
        self.stored_value = 0
        self.current_operation = None
        self.waiting_for_operand = True
        self.display_value = "0"
    
    def input_number(self, number: str):
        if self.waiting_for_operand:
            self.display_value = number
            self.waiting_for_operand = False
        else:
            self.display_value = self.display_value + number
    
    def input_operation(self, operation: str):
        if not self.waiting_for_operand:
            self.calculate()
        
        self.stored_value = float(self.display_value)
        self.current_operation = operation
        self.waiting_for_operand = True
    
    def calculate(self):
        if self.current_operation and not self.waiting_for_operand:
            try:
                current = float(self.display_value)
                result = self.calculator_ops.calculate(
                    self.current_operation, 
                    self.stored_value, 
                    current
                )
                self.display_value = str(result)
                self.current_operation = None
                self.waiting_for_operand = True
            except ValueError as e:
                raise e
    
    def clear(self):
        self.reset()


class CalculatorView:
    """Vista de la calculadora - maneja la interfaz gráfica"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.setup_window()
        self.create_display()
        self.create_buttons()
        self.controller = None
    
    def setup_window(self):
        self.root.title("Calculadora Marvin")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
    
    def create_display(self):
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        self.display = tk.Entry(
            self.root,
            textvariable=self.display_var,
            state='readonly',
            justify='right',
            font=('Arial', 16),
            bg='white',
            relief='sunken',
            bd=2
        )
        self.display.pack(fill='x', padx=10, pady=10)
    
    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Definir los botones
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        
        # Crear botones
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text == '0':
                    # Botón 0 ocupa dos columnas
                    btn = self.create_button(button_frame, text, i, j, columnspan=2)
                elif text == '=':
                    # Botón igual ocupa dos columnas
                    btn = self.create_button(button_frame, text, i, j+1, columnspan=1)
                else:
                    btn = self.create_button(button_frame, text, i, j)
    
    def create_button(self, parent, text, row, col, columnspan=1):
        # Colores según tipo de botón
        if text in ['C', '±', '%']:
            bg_color = '#d4d4d2'
        elif text in ['+', '-', '×', '÷', '=']:
            bg_color = '#ff9500'
            fg_color = 'white'
        else:
            bg_color = '#505050'
            fg_color = 'white'
        
        if text not in ['+', '-', '×', '÷', '=']:
            fg_color = 'black'
        
        btn = tk.Button(
            parent,
            text=text,
            font=('Arial', 14),
            bg=bg_color,
            fg=fg_color,
            relief='raised',
            bd=1,
            command=lambda t=text: self.button_click(t)
        )
        
        btn.grid(row=row, column=col, columnspan=columnspan, 
                sticky='nsew', padx=1, pady=1)
        
        # Configurar grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        return btn
    
    def button_click(self, text):
        """Maneja los clics de botones y delega al controlador"""
        if self.controller:
            self.controller.handle_button_click(text)
    
    def set_controller(self, controller):
        """Establece el controlador"""
        self.controller = controller
    
    def update_display(self, value: str):
        """Actualiza la pantalla"""
        self.display_var.set(value)
    
    def clear_display(self):
        """Limpia la pantalla"""
        self.display_var.set("0")
    
    def get_display_value(self) -> str:
        """Obtiene el valor actual de la pantalla"""
        return self.display_var.get()
    
    def show_error(self, message: str):
        """Muestra un mensaje de error"""
        messagebox.showerror("Error", message)


class CalculatorController:
    """Controlador - maneja la lógica de interacción entre vista y modelo"""
    
    def __init__(self, model: CalculatorModel, view: CalculatorView):
        self.model = model
        self.view = view
        self.view.set_controller(self)
    
    def handle_button_click(self, text: str):
        """Maneja los clics de botones y actualiza el modelo"""
        try:
            if text.isdigit():
                self.handle_number(text)
            elif text == '.':
                self.handle_decimal()
            elif text in ['+', '-', '×', '÷']:
                self.handle_operation(text)
            elif text == '=':
                self.handle_equals()
            elif text == 'C':
                self.handle_clear()
            elif text == '±':
                self.handle_sign_change()
            elif text == '%':
                self.handle_percentage()
                
        except ValueError as e:
            self.view.show_error(str(e))
            self.model.clear()
            self.view.update_display(self.model.display_value)
    
    def handle_number(self, number: str):
        """Maneja la entrada de números"""
        self.model.input_number(number)
        self.view.update_display(self.model.display_value)
    
    def handle_decimal(self):
        """Maneja el punto decimal"""
        if '.' not in self.model.display_value:
            if self.model.waiting_for_operand:
                self.model.display_value = "0."
                self.model.waiting_for_operand = False
            else:
                self.model.display_value += "."
            self.view.update_display(self.model.display_value)
    
    def handle_operation(self, operation: str):
        """Maneja las operaciones matemáticas"""
        self.model.input_operation(operation)
        self.view.update_display(self.model.display_value)
    
    def handle_equals(self):
        """Maneja el botón igual"""
        self.model.calculate()
        self.view.update_display(self.model.display_value)
    
    def handle_clear(self):
        """Maneja el botón clear"""
        self.model.clear()
        self.view.update_display(self.model.display_value)
    
    def handle_sign_change(self):
        """Maneja el cambio de signo"""
        current = float(self.model.display_value)
        self.model.display_value = str(-current)
        self.view.update_display(self.model.display_value)
    
    def handle_percentage(self):
        """Maneja el porcentaje"""
        current = float(self.model.display_value)
        self.model.display_value = str(current / 100)
        self.view.update_display(self.model.display_value)


# Función principal para ejecutar la aplicación
def main():
    """Función principal - punto de entrada de la aplicación"""
    root = tk.Tk()
    
    # Crear las dependencias siguiendo el patrón de inyección de dependencias
    calculator_operations = CalculatorOperations()
    model = CalculatorModel(calculator_operations)
    view = CalculatorView(root)
    controller = CalculatorController(model, view)
    
    # Ejecutar la aplicación
    root.mainloop()


if __name__ == "__main__":
    main()