from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView

from kivy.config import Config
 
 
Config.set("graphics","resizable","0")
Config.set("graphics","width","640")
Config.set("graphics","height","640")
 
 
class MainApp(App):
    def __init__(self):
        super().__init__()
        self.switch = True
 
    def restart(self, arg):
        self.switch = True
 
        for button in self.buttons:
            button.color = (199, 21, 133)
            button.text = "Тыкай"
            button.disabled = False
    
    def tic_tac(self, arg):
        arg.disabled = True
        arg.text = 'X' if self.switch else 'O'
        self.switch = not self.switch
 
        coordinate = (
            (0,1,2), (3,4,5), (6,7,8), 
            (0,3,6), (1,4,7), (2,5,8), 
            (0,4,8), (2,4,6),          
        )
      
        vector = lambda item: [self.buttons[x].text for x in item]

        colorX = [1, 0, 0]
        colorO = [0, 1, 0]
        
        view = ModalView(size_hint=(None, None), size=(200, 200), background_color = (0, 0, 0, 0))     
        

        
        for item in coordinate:
            
            if vector(item).count('X') == 3:
                
                winner = 'Winner X!'
                view.add_widget(Button(text = f'{winner}',
                                       size_hint = (1, .1),
                                       on_press = view.dismiss,
                                       )
                                )
                view.open()
                
                for i in item:
                    self.buttons[i].color = colorX

                for button in self.buttons:
                    button.disabled = True   
                
        
            if vector(item).count('O') == 3:
                
                winner = 'Winner O!'
                view.add_widget(Button(text = f'{winner}',
                                       size_hint = (1, .1),
                                       on_press = view.dismiss
                                       )
                                )   
                view.open()
                
                for i in item:
                    self.buttons[i].color = colorO

                for button in self.buttons:
                    button.disabled = True
        
    
    def build(self):
        self.title = "Best game"
 
        root = BoxLayout(orientation="vertical", padding = 15, spacing = 10)
 
        grid = GridLayout(cols=3)
        self.buttons = []
        for x in range(9):
            button = Button(
                color = [199, 21, 133],
                font_size = 24,
                text = 'Тыкай',
                disabled = False,
                on_press = self.tic_tac
                
            )
            self.buttons.append(button)
            grid.add_widget(button)
 
        root.add_widget(grid)
        
        root.add_widget(Button( 
                background_normal = '',
                color = [1,0,2],
                text = "Restart",
                size_hint = [1,.1],
                on_press = self.restart
                )
        )
        return root

MainApp().run()

