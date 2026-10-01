import json
from datetime import date, timedelta
from pathlib import Path

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

DATA_FILE = Path(__file__).with_name("habits.json")


class HabitTracker(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(14), spacing=dp(10), **kwargs)
        self.habits = self.load_data()
        self.build_ui()

    def load_data(self):
        if DATA_FILE.exists():
            try:
                return json.loads(DATA_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "Gym": {"completed": []},
            "Coding": {"completed": []},
            "Study": {"completed": []},
            "Music": {"completed": []},
        }

    def save_data(self):
        DATA_FILE.write_text(json.dumps(self.habits, indent=2), encoding="utf-8")

    def build_ui(self):
        self.clear_widgets()

        title = Label(
            text="MY HABIT TRACKER",
            font_size=dp(25),
            bold=True,
            size_hint_y=None,
            height=dp(45),
        )
        self.add_widget(title)

        self.summary = Label(
            text=self.summary_text(),
            font_size=dp(16),
            size_hint_y=None,
            height=dp(45),
        )
        self.add_widget(self.summary)

        add_row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(8))
        self.input = TextInput(
            hint_text="Add a habit...",
            multiline=False,
            font_size=dp(16),
        )
        add_btn = Button(text="ADD", size_hint_x=None, width=dp(80))
        add_btn.bind(on_release=self.add_habit)
        add_row.add_widget(self.input)
        add_row.add_widget(add_btn)
        self.add_widget(add_row)

        scroll = ScrollView()
        self.list_box = GridLayout(cols=1, spacing=dp(8), size_hint_y=None)
        self.list_box.bind(minimum_height=self.list_box.setter("height"))
        scroll.add_widget(self.list_box)
        self.add_widget(scroll)

        reset_btn = Button(
            text="RESET TODAY",
            size_hint_y=None,
            height=dp(48),
        )
        reset_btn.bind(on_release=self.reset_today)
        self.add_widget(reset_btn)

        self.refresh()

    def summary_text(self):
        today = date.today().isoformat()
        total = len(self.habits)
        done = sum(today in h["completed"] for h in self.habits.values())
        pct = int(done / total * 100) if total else 0
        return f"Today: {done}/{total} completed  •  {pct}%"

    def refresh(self):
        self.list_box.clear_widgets()
        today = date.today().isoformat()

        for name, data in self.habits.items():
            row = BoxLayout(size_hint_y=None, height=dp(76), spacing=dp(7))

            info = BoxLayout(orientation="vertical")
            label = Label(
                text=name,
                font_size=dp(18),
                halign="left",
                valign="middle",
            )
            label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
            streak = self.current_streak(data["completed"])
            sub = Label(
                text=f"🔥 {streak} day streak",
                font_size=dp(13),
                halign="left",
                valign="middle",
            )
            sub.bind(size=lambda inst, val: setattr(inst, "text_size", val))
            info.add_widget(label)
            info.add_widget(sub)

            done = today in data["completed"]
            btn = Button(text="✓ DONE" if done else "MARK DONE", size_hint_x=None, width=dp(115))
            btn.bind(on_release=lambda _, n=name: self.toggle_today(n))

            delete = Button(text="×", size_hint_x=None, width=dp(48))
            delete.bind(on_release=lambda _, n=name: self.delete_habit(n))

            row.add_widget(info)
            row.add_widget(btn)
            row.add_widget(delete)
            self.list_box.add_widget(row)

        self.summary.text = self.summary_text()

    def add_habit(self, *_):
        name = self.input.text.strip()
        if not name:
            return
        if name not in self.habits:
            self.habits[name] = {"completed": []}
            self.save_data()
        self.input.text = ""
        self.refresh()

    def toggle_today(self, name):
        today = date.today().isoformat()
        completed = self.habits[name]["completed"]
        if today in completed:
            completed.remove(today)
        else:
            completed.append(today)
        self.save_data()
        self.refresh()

    def delete_habit(self, name):
        self.habits.pop(name, None)
        self.save_data()
        self.refresh()

    def reset_today(self, *_):
        today = date.today().isoformat()
        for data in self.habits.values():
            if today in data["completed"]:
                data["completed"].remove(today)
        self.save_data()
        self.refresh()

    @staticmethod
    def current_streak(days):
        s = set(days)
        d = date.today()
        if d.isoformat() not in s:
            d -= timedelta(days=1)
        count = 0
        while d.isoformat() in s:
            count += 1
            d -= timedelta(days=1)
        return count


class HabitApp(App):
    title = "My Habit Tracker"

    def build(self):
        return HabitTracker()


if __name__ == "__main__":
    HabitApp().run()
