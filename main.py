from task_manager import TaskManager
from cmd_parse import build_parser


def main():

    parser = build_parser()
    args = parser.parse_args()
    manager = TaskManager("saved_tasks.json")
    match args.command:
        case "add":
            manager.add_task(args.title)
        case "list":
            manager.list_tasks(args.mode)
        case "delete":
            manager.delete_task(args.task_id)
        case "update":
            manager.toggle_status(args.task_id, args.status)
        case _:
            print("Invalid Command")

if __name__ == "__main__":
    main()
