import argparse

def build_parser():
        parser = argparse.ArgumentParser(prog="task-tracker")

        sub_parser = parser.add_subparsers(dest="command", required=True)
    
        # Add
        parser_add = sub_parser.add_parser("add", aliases="a", help="Creates a new task")
        parser_add.add_argument("title", type=str, help="Task Title")
        # Delete
        parser_del = sub_parser.add_parser("delete", aliases="d", help="Remove a task by their ID")
        parser_del.add_argument("task_id", type=int, help="Task ID")
        # Update
        parser_updt = sub_parser.add_parser("update", aliases="u", help="Mark task complete or in progress")
        parser_updt.add_argument("task_id", type=int, help="Task ID")
        parser_updt.add_argument("status", type=str, choices=["done", "progress"], help="done | progress")
        # Display tasks
        parser_list = sub_parser.add_parser("list", aliases="l", help="Displays task based on filter")
        parser_list.add_argument(
            "mode", type=str,
            nargs="?", 
            default="all", 
            choices=["all", "done", "progress", "todo"], 
            help="Filters: all | done | progress | todo"
            )
        return parser