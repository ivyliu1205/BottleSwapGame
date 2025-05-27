import sys
from color_bottle_game_gui import ColorBottleGameGUI

def main():
    """Main function to run the GUI game"""
    try:
        print("Game start >>>\n")
        game = ColorBottleGameGUI()
        game.run()
    except KeyboardInterrupt:
        print("\n<<< Game interrupted. Thanks for playing!")
        sys.exit(0)

if __name__ == "__main__":
    main()