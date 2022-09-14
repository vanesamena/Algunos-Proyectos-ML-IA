print("Importando librerias...")

from tkinter import *
from chat import obtener_respuesta 

print("Comenzamos...")
# Definimos algunos colores y formatos para el chat
BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

history = [] 

class ChatApplication:

    def __init__(self):
        self.window = Tk() # definimos la ventana de la app
        self._setup_main_window() # esta nos crea el layout
        self.history = []

    def run(self):
        self.window.mainloop() # llama a iniciar la aplicacion

    def _setup_main_window(self): # creamos la ventana y le damos sus funcionalidades
        self.window.title("ChatBot")
        self.window.resizable(width=False, height=False) # queremos que la ventana tenga un tamaño fijo, por defecto
        self.window.configure(width=470, height=550, bg=BG_COLOR) # le damos el tamaño a la ventana y el color de fondo
        
        # Etiqueta en el encabezado - se crea desde self.window. No la creamos con self porque no la usaremos despues
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, # Label es una clase de Tkinter.. como importamos todo podemos acceder directamente 
                           text="Bienvenido al Chat", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1) # es la ubicacion. 
                                     # rel es relativo en todos los casos 
                                     # relwidth es ancho relativo. va de 0 a 1. seleccionando 1 quiere decir que este label usara todo el ancho del espacio de la app
        
        # Pequeño divisor  - es un label tambien y se crea desde self.window
        line = Label(self.window, width=450, bg=BG_GRAY) # le damos width=450 que es un poco menos que el total (470)
        line.place(relwidth=1, rely=0.07, relheight=0.012) # podemos probar otros valores de las posiciones relativas e ir viendo cual nos resulta mejor. esta en porcentaje de 0 a 1
        
        # Widget de texto - Es el area donde vamos a mostrar el texto. llamamos a la clase Text de tkinter. La creamos con self porque la usaremos despues
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED) # lo dejamos deshabilitado
        
        # Barra de desplazamiento - la creamos desde la clase Scrollbar y heredada de self.text_widget, para que ocupe ese lugar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview) # esto es para que cada vez que movemos la barra cambie la posicion en Y del widget de texto
        
        # Etiqueta inferior
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        # Cuadro de entrada de mensaje - usamos la clase Entry. 
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._presionar_enviar)
        
        # Botón de enviar
        send_button = Button(bottom_label, text="Enviar", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._presionar_enviar(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    
    def _presionar_enviar(self, event):
        msg = self.msg_entry.get()
        self._insertar_mensaje(msg, "Usuario")
        
    def _insertar_mensaje(self, msg, sender):
        if not msg:
            return   

        self.msg_entry.delete(0, END) # eliminamos el mensaje del box de entrada
        user_msg = "{}: {}\n\n".format(sender, msg) # le damos el formato que queremos
        self.text_widget.configure(state=NORMAL) # habilitamos el widget de texto para insertar el texto
        self.text_widget.insert(END, user_msg) # lo insertamos
        self.text_widget.configure(state=DISABLED) # volvemos a deshabilitar

        respuesta, history = obtener_respuesta(msg, self.history)
        self.history = history
        bot_msg = "{}: {}\n\n".format('Bot', respuesta)
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, bot_msg)
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END) # siempre nos dejara viendo el ultimo mensjae


if __name__ == "__main__":
    app = ChatApplication()
    app.run()