    db = Database.ConnectToDatabase()
        if db is None:
            print("Database connection failed. Task not updated.")
            return

        try:
            new_task = form.content.controls[0].value
            if new_task.strip():
                old_task = task_instance.task
                # Update the task in the database
                Database.UpdateDatabase(db, (new_task, old_task))
                
                # Update the task_instance with the new task text
                task_instance.task = new_task
                
                # Update the task display immediately
                task_instance.controls[0].controls[0].value = new_task  # Update task text
                task_instance.controls[0].controls[0].update()  # Refresh the task display
                
                # Update the form and close it
                form.height, form.opacity = 80, 0
                form.content.controls[0].value = ""
                form.content.controls[1].content.value = "Add Task"
                form.content.controls[1].on_click = AddTaskToScreen
                form.update()  # Ensure the form is updated
                
                # Update the main column to reflect the new task
                main_column.update()  # Ensure that the main column is updated with the latest changes
            else:
                print("Task description cannot be empty.")
        except Exception as ex:
            print(f"Error during task update: {ex}")
        finally:
            db.close()