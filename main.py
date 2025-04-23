from plyer import tts 
import re
from kivmob import KivMob, TestIds
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp, sp
from kivy.uix.scrollview import ScrollView


def clean_markup(text):
    # Elimina etiquetas de formato de texto como [color], [b], etc.
    text_without_markup = re.sub(r'\[/?[^\]]+\]', '', text)
    return text_without_markup  

class AccessibleLabel(Label):
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance  # Guardar la instancia de la app
        self.accessibility_enabled = kwargs.get('accessibility_enabled', False)
        self.bind(texture_size=self.update_size)

    def update_size(self, instance, value):
        instance.text_size = (instance.width, None)  
        instance.height = value[1] 

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.accessibility_enabled:  # Verificar accesibilidad
            self.app_instance.speak(self.text)
        return super().on_touch_down(touch)

class AccessibleButton(Button):
    def __init__(self, app_instance, accessibility_enabled, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        self.accessibility_enabled = kwargs.get('accessibility_enabled', False)

    def on_press(self):
        if self.accessibility_enabled:  # Verificar accesibilidad
            self.app_instance.speak(self.text)
        return super().on_press()

class ReglaDeTresApp(App):

    def speak(self, text):
        if self.accessibility_enabled: 
            clean_text = clean_markup(text)
            tts.speak(clean_text)  # Usar la funcionalidad de texto a voz de plyer

    def validate_input(self, instance, value):
        value = re.sub(r'[^0-9.]', '', value)  # Elimina caracteres no permitidos
    
     
        if value.count('.') > 1:
            value = value[:-1]  

        instance.text = value

    def on_textinput_change(self, instance, value):
        if self.accessibility_enabled:  # Solo leer si la accesibilidad esta activa
            self.speak(value)
  
    def build(self):

        self.theme = 'dark'  
        self.dark_bg_color = (0.1, 0.1, 0.1, 1)
        self.light_bg_color = (0.96, 0.96, 0.96, 1)  
        self.dark_text_color = ("FFFFFF")
        self.light_text_color = ("000000")
        
        self.layout = BoxLayout(orientation="vertical",padding=dp(10), spacing=dp(10))
        self.accessibility_enabled = False  
        Window.clearcolor = self.dark_bg_color

        self.build_ui()


        Window.orientation = 'portrait'

        return self.layout

    def toggle_accessibility(self, button_instance):
        # Alternar el estado de accesibilidad
        self.accessibility_enabled = not self.accessibility_enabled

        # Cambiar el texto y color del botón de accesibilidad
        if self.accessibility_enabled:
            button_instance.text = "Accesibilidad de textos: Activada"
            button_instance.background_color = (0, 0.8, 1, 1)  
        else:
            button_instance.text = "Accesibilidad de textos: Desactivada"
            button_instance.background_color = (0.4, 0.4, 0.5, 1) 

        self.update_accessibility() 
    

    def update_accessibility(self):
        all_children = self.etiquetas_contenedor.children + self.layout.children
    
        for widget in all_children:
            if isinstance(widget, AccessibleLabel) or isinstance(widget, AccessibleButton):
                widget.accessibility_enabled = self.accessibility_enabled

            # Si el widget es un BoxLayout (como etiquetas_contenedor), revisar sus hijos
            if isinstance(widget, BoxLayout):
                for subwidget in widget.children:
                    if isinstance(subwidget, AccessibleLabel):
                        subwidget.accessibility_enabled = self.accessibility_enabled

        if hasattr(self, 'etiquetas_contenedor'):
            for label in self.etiquetas_contenedor.children:
                if isinstance(label, AccessibleLabel):
                    label.accessibility_enabled = self.accessibility_enabled

        self.resultado_button.accessibility_enabled = self.accessibility_enabled

        self.resultado_label.accessibility_enabled = self.accessibility_enabled

        self.layout.canvas.ask_update()


    def on_textinput_focus(self, instance, value):
        # Leer el texto de accesibilidad al enfocar un campo
        if value and self.accessibility_enabled:  # Solo hablar si la accesibilidad esta activa
            accessibility_text = getattr(instance, 'accessibility_text', "")
            if accessibility_text:
                self.speak(accessibility_text)

    def build_ui(self):

        self.layout.clear_widgets()

        scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True) 

        # Reservar espacio para el banner en la parte superior
        banner_placeholder = Widget(size_hint_y=None, height=dp(50))
        self.layout.add_widget(banner_placeholder)

        # Inicializar KivMob
        APP_ID = "ca-app-pub-6502630826080845~1902096454"
        BANNER_ID = "ca-app-pub-6502630826080845/1104692550"
        self.ads = KivMob(APP_ID)
        self.ads.new_banner(BANNER_ID)
        self.ads.request_banner()
        self.ads.show_banner()


        self.formulario = GridLayout(
            cols=2,padding=[dp(10)], spacing=(dp(35),dp(20)),size_hint_y=None, height=dp(140))

      # Campos de entrada
       # Campos de entrada con texto de accesibilidad
        self.valor1_input = TextInput(
            hint_text="Valor 1", multiline=False, font_size=sp(23),halign="center",border=(20, 20, 20, 20))
        self.valor1_input.accessibility_text = "Campo de entrada. Ingresa el valor 1."
        self.valor1_input.bind(focus=self.on_textinput_focus)
        self.valor1_input.bind(text=self.validate_input)
        self.valor1_input.bind(text=self.on_textinput_change)


        self.valor2_input = TextInput(
            hint_text="Valor 2", multiline=False, font_size=sp(23),halign="center",border=(20, 20, 20, 20))
        self.valor2_input.accessibility_text = "Campo de entrada. Ingresa el valor 2, equivalente al valor 1."
        self.valor2_input.bind(focus=self.on_textinput_focus)
        self.valor2_input.bind(text=self.validate_input)
        self.valor2_input.bind(text=self.on_textinput_change)


        self.valor3_input = TextInput(
            hint_text="Valor 3", multiline=False, font_size=sp(23),halign="center",border=(20, 20, 20, 20))  # Borde visible)
        self.valor3_input.accessibility_text = "Campo de entrada. Ingresa el valor 3 para calcular equivalente en Resultado."
        self.valor3_input.bind(focus=self.on_textinput_focus)
        self.valor3_input.bind(text=self.validate_input)
        self.valor3_input.bind(text=self.on_textinput_change)


        self.formulario.add_widget(self.valor1_input)
        self.formulario.add_widget(self.valor2_input)
        self.formulario.add_widget(self.valor3_input)


        self.resultado_label = AccessibleLabel(app_instance=self,
            text="[color=#1E90FF]Resultado:[/color]", markup=True, font_size=sp(23),valign="center",halign="center",height=60)

        self.formulario.add_widget(self.resultado_label)
        self.layout.add_widget(self.formulario)

        self.resultado_button = AccessibleButton(app_instance=self, text="[color=#000000]CALCULAR RESULTADO[/color]",markup=True, font_size=sp(23),size_hint_y= None,
        height=dp(40),valign="middle",
        accessibility_enabled=self.accessibility_enabled)
        self.resultado_button.background_color =(3, 1, 0, 1)  
        self.resultado_button.bind(on_press=self.calcular_resultado)
        self.layout.add_widget(self.resultado_button)

    # Crear un contenedor para las etiquetas
       
        self.etiquetas_contenedor = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10),size_hint_y=None, height=dp(70))

        self.etiquetas_contenedor.bind(minimum_height=self.etiquetas_contenedor.setter('height'))
        
        self.etiquetas_contenedor.add_widget(AccessibleLabel(color=self.dark_text_color,
            app_instance=self,
            text=f"Ejemplo:\n Si el 100% es 12 \n ¿el 50% cuánto es?[/color]",
            font_size=sp(22),valign="middle",markup=True,size_hint_y=None,halign = "center",height=dp(30)

        ))
        self.etiquetas_contenedor.add_widget(AccessibleLabel(color=self.dark_text_color,
            app_instance=self,
            text="[b][color=#A21D3D]100%(Valor1)[/color][color=#FFB000] = [/color][color=#388E3C]12 (Valor2)[/color]\n[color=#FF00FF]50% (Valor3)[/color][b][color=#FFB000] = [/color][/b][color=#1E90FF]Resultado (6)[/color][/b]",
            markup=True,
            font_size=sp(20),
            valign="middle",halign = "center", size_hint_y=None,height=dp(30)
        ))

        scroll_view.add_widget(self.etiquetas_contenedor)

        self.layout.add_widget(scroll_view)


        self.borrar_button = AccessibleButton(
            app_instance=self, text="BORRAR CAMPOS",
            markup=True, font_size=sp(23), size_hint_y= None,
            height=dp(40), valign="middle",
            accessibility_enabled=self.accessibility_enabled
            )
        self.borrar_button.background_color = (1, 0.92, 0.23, 1)  # Rojo para indicar acción de borrado
        self.borrar_button.bind(on_press=self.borrar_campos)

        self.layout.add_widget(self.borrar_button)

        self.theme_button = AccessibleButton(app_instance=self, text="CAMBIAR TEMA",markup=True, size_hint_y= None,font_size=sp(19),
            height=dp(40),background_color="#283593",accessibility_enabled=self.accessibility_enabled)
        self.theme_button.bind(on_press=self.toggle_theme)
        self.layout.add_widget(self.theme_button)


        accessibility_button = Button(
            text="Accesibilidad de textos: Desactivada",
            background_color=(0.4, 0.4, 0.5, 1),
            markup=True, size_hint_y= None,
            height=dp(40),font_size=sp(19))
        accessibility_button.bind(on_press=lambda instance: self.toggle_accessibility(accessibility_button))

        self.layout.add_widget(accessibility_button)


    def calcular_resultado(self, instance):
        try:
            valor1 = float(self.valor1_input.text)
            valor2 = float(self.valor2_input.text)
            valor3 = float(self.valor3_input.text)

            if valor1 == 0 or valor2 == 0 or valor3 == 0:
                self.resultado_label.text = "[b][color=#FFB000]No uses 0\ncomo Valor[/color][/b]"
                self.resultado_label.markup = True
            
                if self.accessibility_enabled:
                    self.speak("¡Error! No uses 0 como valor")
                return  

            resultado = (valor2 * valor3) / valor1
            self.resultado_label.text = f"[b][color=#1E90FF]{resultado:.2f}[/color][/b]"
            self.resultado_label.markup = True
            
            
            if self.accessibility_enabled:
                self.speak(f"El resultado es {resultado:.2f}")
        except ValueError:
            self.resultado_label.text = "[b][color=#FFB000]Revisa\n los valores[/color][/b]"
            self.resultado_label.markup = True
            
            if self.accessibility_enabled:
                self.speak("¡Error! Revisa\n los valores")

    def borrar_campos(self, instance):
        self.valor1_input.text = ""
        self.valor2_input.text = ""
        self.valor3_input.text = ""
        if self.accessibility_enabled:
            self.speak(f"Borrar campos")

    def toggle_theme(self, instance):
        if self.theme == 'dark':
            Window.clearcolor = self.light_bg_color
            text_color = self.light_text_color
            self.etiquetas_contenedor.color = (0, 0, 0, 1)
            self.theme = 'light'
        else:
            Window.clearcolor = self.dark_bg_color
            text_color = self.dark_text_color
            self.etiquetas_contenedor.color = text_color
            self.theme = 'dark'

        primera_etiqueta = self.etiquetas_contenedor.children[-1]
        primera_etiqueta.text = f'[color={text_color}]Ejemplo:\n Si el 100% es 12 \n ¿el 50% cuánto es?[/color]'


    def get_current_color(self):
        return self.light_text_color if self.theme == 'light' else self.dark_text_color

if __name__ == "__main__":
    ReglaDeTresApp().run()
