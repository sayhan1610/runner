# Runner

Welcome to **Runner**, an exciting 2D endless runner game built with Pygame! Dodge obstacles, collect power-ups, and see how far you can go!

## Features

- **Jump**: Use the UP arrow key to jump over obstacles.
- **Super Jump**: Press SPACE for a super jump.
- **Duck**: Use the DOWN arrow key to duck under obstacles.
- **Power-ups**: Collect power-ups for invincibility and increased speed.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/sayhan1610/runner.git
   cd runner
   ```

2. **Install Pygame**

   Make sure you have Python installed. Then, install Pygame using pip:

   ```bash
   pip install pygame
   ```

3. **Prepare Assets**

   Ensure you have the necessary assets in the following directories:

   - `audio/`: Contains sound files (`bg_music.mp3`, `crash.mp3`, `run.mp3`)
   - `images/`: Contains image files for backgrounds, player, and obstacles (`bg.png`, `runner1.png`, etc.)

   You can modify or add your own assets as long as you follow the naming conventions used in the code.

## How to Play

1. **Start the Game**

   Run the game script:

   ```bash
   python game.py
   ```

2. **Controls**

   - **UP Arrow**: Jump
   - **SPACE**: Super Jump (after cooldown)
   - **DOWN Arrow**: Duck

   - **Enter**: Start the game or return to Home screen
   - **I**: Show instructions
   - **R**: Retry after game over

3. **Objective**

   - Avoid obstacles and survive as long as possible to achieve a high score.
   - Collect power-ups to gain invincibility and speed boosts.
   - Keep an eye on the score displayed at the top left of the screen.

4. **Game States**

   - **Home**: Main screen where you can start the game or view instructions.
   - **Instructions**: Displays the controls and game instructions.
   - **Game**: The main gameplay screen.
   - **Score Report**: Shows your final score and options to retry.

## Troubleshooting

- **Missing Assets**: Ensure all audio and image files are correctly placed in the respective folders.
- **Sound Issues**: Adjust the volume settings or check your sound system if the background music or sound effects are not playing.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. Your feedback and improvements are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
