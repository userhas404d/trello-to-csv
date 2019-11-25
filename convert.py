import json
import csv


class TrelloToCSV:
    def __init__(self, input_tasks_file, output_tasks_file):
        self.input_trello_board_file = input_tasks_file
        self.output_tasks_file = output_tasks_file
        self.tasks_json = self.get_content()
        self.parsed_trello_tasks = self.get_tasks()

    def get_content(self):
        with open(self.input_trello_board_file) as w:
            return json.load(w)

    def get_list(self, list_id):
        for trello_list in self.tasks_json["lists"]:
            if trello_list["id"] == list_id:
                return trello_list["name"]

    def get_tasks(self):
        tasks = []
        for card in self.tasks_json["cards"]:
            task = {}
            try:
                task["label"] = card["labels"][0]["name"]
            except IndexError:
                task["label"] = None
            task["task"] = card["name"]
            task["description"] = card["desc"]
            task["status"] = self.get_list(card["idList"])
            tasks.append(task)
        return tasks

    def write_csv_tasks(self):
        with open(
            self.output_tasks_file, "w", encoding="utf8", newline=""
        ) as output_file:
            fc = csv.DictWriter(
                output_file, fieldnames=self.parsed_trello_tasks[0].keys(),
            )
            fc.writeheader()
            fc.writerows(self.parsed_trello_tasks)


def main():
    trello_tasks = TrelloToCSV("board.json", "tasks.csv")
    trello_tasks.write_csv_tasks()


if __name__ == "__main__":
    main()
