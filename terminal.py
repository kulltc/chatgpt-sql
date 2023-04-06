import logging
from controller import Controller

# Configure the logging settings
logging.basicConfig(filename='debug.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    print("Ask any question about the data. Enter 'q' to quit. Enter 'r' to reset ChatGPT.")
    controller = Controller()
    while True:
        user_input = input("Question: ")
        if user_input.lower() == 'q':
            break
        if user_input == "r":
            controller.reset()
            continue
        try:
            result = controller.run(message=user_input, sender="USER")
            print(f"ChatGPT: {result}")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

if __name__ == "__main__":
    main()
