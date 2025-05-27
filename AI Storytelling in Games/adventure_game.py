import random
import tkinter as tk
from tkinter import messagebox, simpledialog, PhotoImage
import os
from pygame import mixer

class AdaptiveNarrative:
    def __init__(self, player_name):
        self.player_name = player_name
        self.story_elements = {
            'intro': [
                f"Welcome, {self.player_name}, to the mystical land of Elaria!",
                f"The world trembles as you, {self.player_name}, awaken to your destiny."
            ],
            'events': [
                "A mysterious figure approaches you, shrouded in darkness.",
                "You stumble upon an ancient artifact humming with power."
            ],
            'outcomes': [
                "The artifact binds to your soul, unlocking unknown powers.",
                "The figure reveals a prophecy that ties you to the fate of the world."
            ]
        }
        self.player_choices = []

    def generate_story(self, stage):
        choice = random.choice(self.story_elements[stage])
        self.player_choices.append(choice)
        return choice

class DynamicDialogue:
    def __init__(self):
        self.dialogue_options = {
            'greet': ["Hello, traveler!", "Greetings, adventurer!"],
            'ask': ["What brings you here?", "How can I assist you?"],
            'farewell': ["Safe travels!", "Until we meet again!"],
            'confused': ["I don't understand your request.", "Could you clarify?"],
            'memory': {}
        }

    def get_response(self, player_input, npc_name):
        player_input = player_input.lower()
        if npc_name not in self.dialogue_options['memory']:
            self.dialogue_options['memory'][npc_name] = []

        if "hello" in player_input:
            response = random.choice(self.dialogue_options['greet'])
        elif "help" in player_input:
            response = random.choice(self.dialogue_options['ask'])
        elif "bye" in player_input:
            response = random.choice(self.dialogue_options['farewell'])
        else:
            response = random.choice(self.dialogue_options['confused'])

        self.dialogue_options['memory'][npc_name].append((player_input, response))
        return response

class GameNarrative:
    def __init__(self, player_name, root):
        self.player_name = player_name
        self.scenes = {
            'scene1': "You enter a bustling village filled with strange creatures.",
            'scene2': "You encounter a wise old man who offers cryptic advice: 'Beware the choices you make.'",
            'scene3': "You face a challenging decision at a fork in the road: one path leads to safety, the other to danger.",
            'exploration': "You wander through the wilderness, discovering hidden treasures and lurking dangers."
        }
        self.player_choices = []
        self.dialogue_system = DynamicDialogue()
        self.narrative = AdaptiveNarrative(player_name)
        self.inventory = []
        self.emotions = {
            'positive': 0,
            'negative': 0
        }
        self.analytics = {
            'decisions': [],
            'items_collected': 0,
            'interactions': 0
        }
        self.root = root
        self.bg_image = None
        self.current_music = None
        self.setup_gui()
        mixer.init()

    def setup_gui(self):
        self.main_frame = tk.Frame(self.root, bg="black")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Background image
        if os.path.exists("background.png"):
            self.bg_image = PhotoImage(file="background.png")
            bg_label = tk.Label(self.main_frame, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)

        # Main text area
        self.text_area = tk.Text(self.main_frame, wrap=tk.WORD, bg="white", fg="black", font=("Helvetica", 14))
        self.text_area.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        self.text_area.insert(tk.END, "Welcome to the game!")
        self.text_area.config(state=tk.DISABLED)

        # Button frame
        self.button_frame = tk.Frame(self.main_frame, bg="black")
        self.button_frame.pack(fill=tk.X)

        self.action_button = tk.Button(self.button_frame, text="Start Game", command=self.start_game, bg="green", fg="white", font=("Helvetica", 12))
        self.action_button.pack(pady=10)

        self.inventory_button = tk.Button(self.button_frame, text="View Inventory", command=self.show_inventory, bg="blue", fg="white", font=("Helvetica", 12))
        self.inventory_button.pack(pady=10)

        self.stats_button = tk.Button(self.button_frame, text="View Stats", command=self.show_stats, bg="purple", fg="white", font=("Helvetica", 12))
        self.stats_button.pack(pady=10)

    def update_text_area(self, message):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, f"\n{message}")
        self.text_area.config(state=tk.DISABLED)

    def play_music(self, track):
        if self.current_music != track:
            mixer.music.load(track)
            mixer.music.play(-1)
            self.current_music = track

    def show_inventory(self):
        inventory_str = "\n".join(self.inventory) if self.inventory else "Your inventory is empty."
        messagebox.showinfo("Inventory", inventory_str)

    def show_stats(self):
        stats_str = f"Decisions Made: {len(self.analytics['decisions'])}\nItems Collected: {self.analytics['items_collected']}\nNPC Interactions: {self.analytics['interactions']}"
        messagebox.showinfo("Player Stats", stats_str)

    def play_scene(self, scene_key):
        self.update_text_area(self.scenes[scene_key])
        self.player_choices.append(scene_key)
        self.analytics['decisions'].append(scene_key)

    def make_decision(self):
        decision_window = tk.Toplevel(self.root)
        decision_window.title("Make a Decision")
        tk.Label(decision_window, text="What do you want to do?").pack()

        def choose(option):
            if option == '1':
                self.play_scene('scene1')
                self.add_to_emotion('positive')
            elif option == '2':
                self.talk_to_npc("Wise Old Man")
                self.add_to_emotion('positive')
            elif option == '3':
                self.play_scene('scene3')
                self.add_to_emotion('negative')
            elif option == '4':
                self.play_scene('exploration')
                self.collect_item()
            decision_window.destroy()

        tk.Button(decision_window, text="1: Explore the village", command=lambda: choose('1')).pack()
        tk.Button(decision_window, text="2: Talk to the wise man", command=lambda: choose('2')).pack()
        tk.Button(decision_window, text="3: Take the risky path", command=lambda: choose('3')).pack()
        tk.Button(decision_window, text="4: Wander the wilderness", command=lambda: choose('4')).pack()

    def talk_to_npc(self, npc_name):
        self.analytics['interactions'] += 1
        npc_window = tk.Toplevel(self.root)
        npc_window.title(f"Talk to {npc_name}")

        def respond():
            user_input = entry.get()
            response = self.dialogue_system.get_response(user_input, npc_name)
            self.update_text_area(f"{npc_name}: {response}")
            if "bye" in user_input.lower():
                npc_window.destroy()

        tk.Label(npc_window, text=f"You approach {npc_name}. What do you say?").pack()
        entry = tk.Entry(npc_window)
        entry.pack()
        tk.Button(npc_window, text="Send", command=respond).pack()

    def collect_item(self):
        items = ["Ancient Amulet", "Mysterious Key", "Healing Potion"]
        found_item = random.choice(items)
        self.inventory.append(found_item)
        self.analytics['items_collected'] += 1
        self.update_text_area(f"You found a {found_item}! It has been added to your inventory.")

    def add_to_emotion(self, emotion_type):
        if emotion_type == 'positive':
            self.emotions['positive'] += 1
        elif emotion_type == 'negative':
            self.emotions['negative'] += 1

    def determine_outcome(self):
        if self.emotions['positive'] > self.emotions['negative']:
            return "Your journey ends on a hopeful note, filled with promise."
        elif self.emotions['negative'] > self.emotions['positive']:
            return "Your journey concludes in uncertainty and peril."
        else:
            return "Your journey leaves a balanced legacy, neither good nor bad."

    def ask_to_play_again(self):
        replay_window = tk.Toplevel(self.root)
        replay_window.title("Play Again")
        tk.Label(replay_window, text="Would you like to play the story again?").pack()

        def replay(option):
            if option == 'yes':
                self.start_game()
            elif option == 'no':
                self.root.quit()
            replay_window.destroy()

        tk.Button(replay_window, text="Yes", command=lambda: replay('yes')).pack()
        tk.Button(replay_window, text="No", command=lambda: replay('no')).pack()

    def start_game(self):
        self.play_music("background_music.mp3")
        self.update_text_area(self.narrative.generate_story('intro'))
        self.make_decision()
        self.update_text_area(self.narrative.generate_story('events'))
        self.update_text_area(self.determine_outcome())
        self.ask_to_play_again()

# Example of running the game narrative
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Adventure Game")
    root.geometry("800x600")

    player_name = simpledialog.askstring("Name", "Enter your character's name:")
    if player_name:
        adventure_game = GameNarrative(player_name, root)
    root.mainloop()
