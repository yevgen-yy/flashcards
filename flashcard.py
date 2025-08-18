import random
import os
import time
import yaml  # Import the yaml library


# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def load_flashcards_from_yaml(filepath):
    """Loads a list of flashcards from a specific YAML file."""
    try:
        with open(filepath, 'r') as file:
            # The safe_load function parses the YAML file
            data = yaml.safe_load(file)
            return data if data is not None else []
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file '{filepath}': {e}")
        return None


# --- Core Quiz & Menu Logic ---

def run_quiz(cards, subject_name):
    """Runs a quiz session for a given set of cards."""
    random.shuffle(cards)
    card_count = len(cards)
    for i, card in enumerate(cards, 1):
        clear_screen()
        print(f"Subject: {subject_name} | Card {i} of {card_count}\n")

        # Determine question and answer based on mode
        if quiz_mode == '1':  # Term -> Definition
            question = f"Term: {card['term']}"
            answer = f"Definition: {card['full_def']}"
            prompt = "\nThink of the definition, then press Enter to reveal..."
        else:  # Definition -> Term
            question = f"Question: {card['quiz_question']}"
            answer = f"Term: {card['term']}"
            prompt = "\nThink of the term, then press Enter to reveal..."

        print(question)
        input(prompt)
        print(f"\n{answer}")

        input("\nPress Enter to continue to the next card...")

    clear_screen()
    print("✨ Quiz complete! ✨")
    time.sleep(2)


def show_quiz_menu(cards, subject_name):
    """Displays the menu for quiz type and starts the quiz."""
    global quiz_mode
    while True:
        clear_screen()
        print(f"--- 🧠 Studying: {subject_name} ---")
        print("\nChoose a study mode:")
        print("  1. Quiz: Show Term -> Guess Definition")
        print("  2. Quiz: Show Definition -> Guess Term")
        print("  3. Back to Subject Menu")

        choice = input("\nEnter your choice (1-3): ")

        if choice in ['1', '2']:
            quiz_mode = choice
            # Do not run the quiz if there are no cards for that subject
            if not cards:
                print("\nNo cards found for this subject. Returning to menu.")
                time.sleep(2)
                continue
            run_quiz(cards, subject_name)
        elif choice == '3':
            return  # Go back to the main menu
        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")
            time.sleep(2)


# --- Main Application Logic ---

def main():
    """Main function to load data and run the flashcard app."""
    # Load each subject from its own YAML file inside the 'data' folder
    geometry_cards = load_flashcards_from_yaml('data/geometry.yml')
    ela_cards = load_flashcards_from_yaml('data/ela.yml')

    # Exit if any file failed to load
    if geometry_cards is None or ela_cards is None:
        print("\nExiting application due to a data loading error.")
        return

    while True:
        clear_screen()
        print("--- 📚 Flashcard App Main Menu 📚 ---")
        print("\nChoose a subject to study:")
        print("  1. Geometry")
        print("  2. ELA (English Language Arts)")
        print("  3. Study All Subjects")
        print("  4. Exit")

        subject_choice = input("\nEnter your choice (1-4): ")

        if subject_choice == '1':
            show_quiz_menu(geometry_cards, "Geometry")
        elif subject_choice == '2':
            show_quiz_menu(ela_cards, "ELA")
        elif subject_choice == '3':
            all_cards = geometry_cards + ela_cards
            show_quiz_menu(all_cards, "All Subjects")
        elif subject_choice == '4':
            print("\nHappy studying! Goodbye! 👋")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 4.")
            time.sleep(2)


# --- Run the App ---
if __name__ == "__main__":
    quiz_mode = '1'
    main()