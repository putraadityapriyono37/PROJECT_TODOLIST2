import flet
from flet import *
from datetime import datetime
import sqlite3

# Let's create the form class first so we can get some data
class FormContainer(UserControl):
    # at this point, we can pass in a function from the main() so we can expand.minimize the form
    # go back to the FormContainer() and add a argument as such..
    def __init__(self, func):
        self.func = func
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
        
        
# Now, we need a class to generate a task when the user adds one
class CreateTask(UserControl):
    def __init__(self, task: str, date: str, func1, func2):
        # create two arguments so we can pass in the delete function and edit function when we create an instance of this
        self.task = task
        self.date = date
        self.func1 = func1
        self.func2 = func2
        super().__init__()

    def TaskDeleteEdit(self, nama, color, func):
        return IconButton(
            icon=name,
            width=30,
            icon_size=18,
            icon_color=color,
            opacity=0,
            animate_opacity=200,
            # to use it, we need to keep it in our delete and edit iconbuttons
            on_click=lambda e: func(self.GetContainerInstance(e))
        )
    
    # we need a final thing from here, and that is the instance itself.
    # we need the instance identidier so that we can delete it needs to be delete
    def GetContainerInstance(self):
        return self # we return the self instance
    
    def ShowIcons(self, e):
        if e.data == "true":
            # these are the index's of each icon
            (
                e.control.content.controls[1].controls[0].opacity,
                e.control.content.controls[1].controls[1].opacity, 
            ) = (1,1)
            e.control.content.update()
        else:
            (
                e.control.content.controls[1].controls[0].opacity,
                e.control.content.controls[1].controls[1].opacity,
            ) = (0,0)
            e.control.content.update()

    def build(self):
        return Container(
            width=280,
            height=60,
            border=border.all(0.85, "white54"),
            border_radius=8,
            # let's show the icons when we hover over them..
            on_hover=lambda e: self.ShowIcons(e),
            clip_behavior=ClipBehavior.HARD_EDGE,
            padding=10,
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(
                        spacing=1,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Text(value=self.task, size=10),
                            Text(value=self.date, size=9, color='white54'),
                        ],
                    ),
                    # Icons Delete and Edit
                    Row(
                        spacing=0,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            # make sure to pass the args here first !!
                            self.TaskDeleteEdit(icons.DELETE_ROUNDED, "red500", self.func1),
                            self.TaskDeleteEdit(icons.EDIT_ROUNDED, "white70", self.func2),
                        ],
                    ),
                ],
            ),
        )
    

def main(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def AddTaskToScreen(e):
        # now, everytime the user adds a task, we need to fetch the data nad output it to the main column ..
        # there are 2 data we need: the task + the data
        # 
        dateTime = datetime.now().strftime("%b %d, %Y  %I:%M")

        # now recall that we set the form container to form variable. we can use this now to see if there's any content in the textfield
        if form.content.controls[0].value: # this checks the textfield's value
            _main_column_.controls.append[
                # here, we can create an instance of CreateTask() class ...
                CreateTask(
                    # now, it takes two arguments
                    form.content.controls[0].value, # task deskription ..
                    dateTime,
                    # now, the instance takes two more arguments whe called...
                    DeleteFunction,
                    UpdateFunction,
                )
            ]
            _main_column_.update()

            # we can recall the show.hide function for the form here
            CreateToDoTask(e)
    
    def DeleteFunction(e):
        # when we want to delete, recall that these instances are in a list => so that means we can simply remove them when we want to

        # let's show what e is..
        # so the instance is passed on as e
        _main_column_.controls.remove(e) # e is the instance itself
        _main_column_.update()

    def UpdateFunction(e):
        # the update needs a little bit more work..
        # we want to update from the form, so we need to pass whatever the user had from the instance back to the form, then change the functions and pass it back again...
        form.height, form.opacity = 200, 1 # show the form
        (
            
        )

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
                                # Form class here ..
                                # pass in the argument for the form class here
                                FormContainer(lambda e: AddTaskToScreen(e)),
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