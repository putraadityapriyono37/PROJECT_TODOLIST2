import flet
from flet import *
from datetime import datetime
import sqlite3


# Database class for CRUD operations
class Database:
    @staticmethod
    def ConnectToDatabase():
        try:
            db = sqlite3.connect('todo.db')
            c = db.cursor()
            c.execute(
                'CREATE TABLE if not exists tasks (id INTEGER PRIMARY KEY, Task VARCHAR(255) NOT NULL, Date VARCHAR(255) NOT NULL)'
            )
            return db
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None

    @staticmethod
    def ReadDatabase(db):
        c = db.cursor()
        c.execute("SELECT Task, Date FROM tasks")
        return c.fetchall()

    @staticmethod
    def InsertDatabase(db, values):
        c = db.cursor()
        c.execute("INSERT INTO tasks (Task, Date) VALUES (?, ?)", values)
        db.commit()

    @staticmethod
    def DeleteDatabase(db, values):
        c = db.cursor()
        c.execute("DELETE FROM tasks WHERE Task=?", values)
        db.commit()

    @staticmethod
    def UpdateDatabase(db, values):
        c = db.cursor()
        c.execute("UPDATE tasks SET Task=? WHERE Task=?", values)
        db.commit()


# Form container
class FormContainer(UserControl):
    def __init__(self, func):
        self.func = func
        super().__init__()

    def build(self):
        return Container(
            width=280,
            height=80,
            bgcolor="bluegrey500",
            opacity=0,
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
                        on_click=self.func,
                        style=ButtonStyle(
                            bgcolor={"": "black"},
                            shape={"": RoundedRectangleBorder(radius=8)},
                        ),
                    ),
                ],
            ),
        )


# Task container
class CreateTask(UserControl):
    def __init__(self, task: str, date: str, delete_func, update_func):
        self.task = task
        self.date = date
        self.delete_func = delete_func
        self.update_func = update_func
        super().__init__()

    def TaskDeleteEdit(self, icon, color, func):
        return IconButton(
            icon=icon,
            width=30,
            icon_size=18,
            icon_color=color,
            opacity=0,
            animate_opacity=200,
            on_click=lambda e: func(self),
        )

    def ShowIcons(self, e):
        if e.data == "true":
            # Directly access and modify the Row of edit/delete icons
            e.control.content.controls[1].controls[0].opacity = 1
            e.control.content.controls[1].controls[1].opacity = 1
        else:
            # Hide edit and delete icons
            e.control.content.controls[1].controls[0].opacity = 0
            e.control.content.controls[1].controls[1].opacity = 0
        e.control.update()

    def build(self):
        self.task_text = Text(value=self.task, size=10)
        self.date_text = Text(value=self.date, size=9, color="white54")

        return Container(
            width=280,
            height=60,
            border=border.all(0.85, "white54"),
            border_radius=8,
            on_hover=self.ShowIcons,
            padding=10,
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(
                        spacing=1,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.task_text,
                            self.date_text,
                        ],
                    ),
                    Row(
                        spacing=0,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            self.TaskDeleteEdit(
                                icons.DELETE_ROUNDED, "red500", self.delete_func
                            ),
                            self.TaskDeleteEdit(
                                icons.EDIT_ROUNDED, "white70", self.update_func
                            ),
                        ],
                    ),
                ],
            ),
        )

    def update_task_text(self, new_task):
        # Method to directly update task text in the UI
        self.task = new_task
        self.task_text.value = new_task
        self.update()


# Main application
def main(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def AddTaskToScreen(e):
        db = Database.ConnectToDatabase()
        if db is None:
            print("Database connection failed. Task not added.")
            return

        try:
            dateTime = datetime.now().strftime("%b %d, %Y  %I:%M")
            task_description = form.content.controls[0].value
            if task_description:
                Database.InsertDatabase(db, (task_description, dateTime))
                task_control = CreateTask(task_description, dateTime, DeleteFunction, UpdateFunction)
                main_column.controls.append(task_control)
                main_column.update()
                CreateToDoTask(e)
            else:
                print("Task description is empty.")
        except Exception as ex:
            print(f"Error during task addition: {ex}")
        finally:
            if db:
                db.close()

    def DeleteFunction(task_instance):
        db = Database.ConnectToDatabase()
        if db is None:
            print("Database connection failed. Task not deleted.")
            return

        try:
            task_description = task_instance.task
            Database.DeleteDatabase(db, (task_description,))
            main_column.controls.remove(task_instance)
            main_column.update()
        except Exception as ex:
            print(f"Error during task deletion: {ex}")
        finally:
            if db:
                db.close()

    def UpdateFunction(task_instance):
        # Prepare form for update
        form.content.controls[0].value = task_instance.task
        form.content.controls[1].content.value = "Update"
        form.content.controls[1].on_click = lambda e: FinalizeUpdate(task_instance)
        
        # Show form
        if form.height != 200:
            form.height, form.opacity = 200, 1
        form.update()

    def FinalizeUpdate(task_instance):
        db = Database.ConnectToDatabase()
        if db is None:
            print("Database connection failed. Task not updated.")
            return

        try:
            new_task = form.content.controls[0].value
            if new_task.strip():
                old_task = task_instance.task
                Database.UpdateDatabase(db, (new_task, old_task))
                
                # Directly update the task text in the UI
                task_instance.update_task_text(new_task)
                
                # Reset form
                CreateToDoTask(None)
            else:
                print("Task description cannot be empty.")
        except Exception as ex:
            print(f"Error during task update: {ex}")
        finally:
            if db:
                db.close()

    def CreateToDoTask(e):
        if form.height != 200:
            form.height, form.opacity = 200, 1
        else:
            form.height, form.opacity = 80, 0
            form.content.controls[0].value = ""
            form.content.controls[1].content.value = "Add Task"
            form.content.controls[1].on_click = AddTaskToScreen
        form.update()

    main_column = Column(
        expand=True,
        controls=[
            Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text("To-Do List", size=18, weight="bold"),
                    IconButton(
                        icons.ADD_CIRCLE_ROUNDED,
                        on_click=CreateToDoTask,
                    ),
                ],
            ),
            Divider(height=8, color="white24"),
        ],
    )

    page.add(
        Container(
            width=1500,
            height=800,
            bgcolor="bluegrey900",
            alignment=alignment.center,
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Container(
                        width=250,
                        height=530,
                        bgcolor="#0f0f0f",
                        border_radius=40,
                        border=border.all(0.5, "white"),
                        padding=padding.only(top=35, left=20, right=20),
                        content=Column(
                            alignment=MainAxisAlignment.CENTER,
                            expand=True,
                            controls=[
                                main_column,
                                FormContainer(AddTaskToScreen),
                            ],
                        ),
                    )
                ],
            ),
        )
    )

    # Get reference to the form
    form = page.controls[0].content.controls[0].content.controls[1].controls[0]

    # Load existing tasks from database
    db = Database.ConnectToDatabase()
    if db:
        try:
            for task in Database.ReadDatabase(db)[::-1]:
                task_control = CreateTask(task[0], task[1], DeleteFunction, UpdateFunction)
                main_column.controls.append(task_control)
        finally:
            if db:
                db.close()
        main_column.update()


if __name__ == "__main__":
    flet.app(target=main)