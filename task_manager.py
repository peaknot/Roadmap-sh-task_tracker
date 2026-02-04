import json
from datetime import datetime
from pathlib import Path


class TaskManager():
    def __init__(self, filename: str):
        base_dir = Path(__file__).resolve().parent
        self.filename = str(base_dir / filename)

    def _now(self) -> str:
        return datetime.now().strftime("%m-%d %A %H:%M:%S.%f")
    
    def _print_task(self, task):
        stat_symbol = "✅" if task["completed"] else "⏳" if task["in_progress"] else " "
        print(f"[{stat_symbol}] {task['id']}. {task['title']} -- (Updated: {task['updated_at']})")


    def load(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"tasks": []}
        
    def save(self, data):
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def add_task(self, title):
        data = self.load()
        new_id: int = len(data["tasks"]) + 1


        task = {
            "id": new_id,
            "title": title,
            "completed": False,
            "in_progress": False,
            "created_at": self._now(),
            "updated_at": self._now()
        }

        data["tasks"].append(task)
        self.save(data)
        print("Task Added.")

    def delete_task(self, task_id):
        data = self.load()
        task_id = int(task_id)

        for k, v in enumerate(data["tasks"]):
            if task_id == v["id"]:
                data["tasks"].pop(k)
                self.save(data)
                print("Task Deleted.")
                return

        print("Task ID not found.")
    
    def toggle_status(self, task_id, status):
        data = self.load()

        task_id = int(task_id)
        for task in data["tasks"]:
            if task["id"] == task_id:
                match status:
                    case "done":
                        task["completed"] = True
                        task["in_progress"] = False
                    case "progress":
                        task["completed"] = False
                        task["in_progress"] = True
                    case _:
                        print("Usage: done | progress")
                        return
                
                task["updated_at"] = self._now()
                self.save(data)
                print("Task updated")
                return
        print("Task ID not found") 

    def list_tasks(self, mode):
        data = self.load()

        if not data["tasks"]:
            print("There are no tasks to display.")
            return
        
        match mode:
            case "all":
                filtered = data["tasks"]
            case "done":
                filtered = [
                    task for task in data["tasks"]if task["completed"]]
            case "progress":
                filtered = [task for task in data["tasks"]if task["in_progress"]]
            case "todo":
                filtered = [
                    task for task in data["tasks"]if not task["completed"] and not task["in_progress"]]
            case _:
                print("Invalid command\n"
                    "Usage: python main.py list all|done|progress|todo|")
                return
        
        if not filtered:
            print("No matching tasks found.")
            return
        for task in filtered:
            self._print_task(task)
        

            

        

