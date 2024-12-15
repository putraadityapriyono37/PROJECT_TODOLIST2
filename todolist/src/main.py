import flet
from flet import *
from datetime import datetime
import sqlite3

# Let's create the form class first so we can get some data
class FormContainer(UserControl):
    # at this point, we can pass in a function from the main() so we can expand.minimize the form
    def __init__(self):
        self.func = None
        super().__init__()
        
    def build(self):
        return Container(
            width=280,
            height=80,
            bgcolor="bluegrey500",
            opacity=0, #change later => change this to 0 and reverese when called
            border_radius=40,
            margin=margin.only(left=-20, right=-20),
            animate=animation.Animation(400, "decelerate"),
            animate_opacity=200,
            padding=padding.only(top=45, bottom=45),
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    TextField(
                        height=48,
                        width=255,
                        filled=True,
                        text_size=12,
                        color="black",
                        border_color="transparent",
                        hint_text="Description...",
                        hint_style=TextStyle(size=11, color="black"),
                    ),
                    IconButton(
                        content=Text("Add Task"), 
                            width=180,
                            height=44,
                            on_click=self.func, # pass function here
                            style=ButtonStyle(
                                bgcolor={"": "black"},
                                shape={"": RoundedRectangleBorder(radius=8)
                                },
                            ),
                        ),
                    ],
                ),
            )
        
        
# 
    

def main(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    
    # function to show/hide form container
    def CreateToDoTask(e):
        # when we click ehe ADD iconbutton ...
        if form.height != 150:
            form.height, form.opacity = 150, 1
            form.update()
        else:
            form.height, form.opacity = 80, 0
            form.update()
    
    _main_column_ = Column(
        scroll="hidden",
        expand=True,
        alignment=MainAxisAlignment.START,
        controls=[
            Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    # Some title stuff ...
                    Text("To-Do List", size=18, weight="bold"),
                    IconButton(
                        icons.ADD_CIRCLE_ROUNDED,
                        icon_size=18,
                        on_click=lambda e: CreateToDoTask(e),
                    ),
                ],
            ),
            Divider(height=8, color="white24"),
        ],
    )
    
    # set up some bg and main container
    # The general UI will copy that of a mobile app
    page.add(
        # this is just a bg container
        Container(
            width=1500, 
            height=800, 
            margin=-10,
            bgcolor="bluegrey900",
            alignment=alignment.center,
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    # Main container
                    Container(
                        width=250, 
                        height=530, 
                        bgcolor="#0f0f0f",
                        border_radius=40,
                        border=border.all(0.5, "white"),
                        padding=padding.only(top=35, left=20, right=20),
                        clip_behavior=ClipBehavior.HARD_EDGE, # clip contents to container
                        content=Column(
                            alignment=MainAxisAlignment.CENTER,
                            expand=True,
                            controls=[
                                # main column here..
                                _main_column_,
                                FormContainer(),
                            ]
                        )
                    )
                ],
            ),
        )
    )
    page.update()
    
    # the form container index is as follows. We can set the long element index as a variable so it can be called faster and easier.
    form = page.controls[0].content.controls[0].content.controls[1].controls[0]
    # now we can call form whenever we want to do something with it...

if __name__ == "__main__":
    flet.app(target=main)