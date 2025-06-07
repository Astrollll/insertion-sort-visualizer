# Insertion Sort Visualizer

A modern, interactive visualization tool for the Insertion Sort algorithm built with Python and Tkinter. This application provides a visual representation of how the Insertion Sort algorithm works, making it easier to understand the sorting process.

## Features

- **Interactive Visualization**: Watch the insertion sort algorithm in action with animated bars representing array elements
- **Customizable Input**: Input your own array of numbers or generate random arrays
- **Speed Control**: Adjust the animation speed to your preference
- **Step Counter**: Track the progress of the sorting algorithm
- **Modern UI**: Clean and intuitive interface with a contemporary design
- **Real-time Updates**: Visual feedback for each step of the sorting process

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes with Python installation)

## Installation

1. Clone this repository or download the source code
2. Make sure you have Python installed on your system
3. No additional packages are required as the application uses only built-in Python libraries

## Usage

1. Run the application:
   ```bash
   python insertion_sort_visualizer.py
   ```

2. The application window will open with the following controls:
   - **Start Sorting**: Begin the visualization
   - **Reset**: Reset the visualization to its initial state
   - **Generate New Array**: Create a new random array
   - **Animation Speed**: Adjust the speed of the visualization
   - **Custom Array Input**: Enter your own numbers (comma-separated)

3. To use a custom array:
   - Enter numbers separated by commas in the input field
   - Click "Apply" to visualize your array
   - Click "Start Sorting" to begin the visualization

## How It Works

The visualization represents array elements as bars, where:
- The height of each bar represents its value
- Red bars indicate the current element being processed
- Teal bars show the element being compared
- Dark gray bars represent other elements

The algorithm is implemented using a separate thread to prevent UI freezing during sorting, and the visualization updates in real-time to show each step of the process.

## Design Choices

- **Color Scheme**: 
  - Modern, contrasting colors for better visibility
  - Red for current element
  - Teal for comparing element
  - Dark gray for other elements

- **Layout**:
  - Clean, organized interface with logical grouping of controls
  - Responsive canvas that adjusts to window size
  - Clear status indicators and step counter

- **Performance**:
  - Threaded sorting implementation to maintain UI responsiveness
  - Efficient drawing algorithms for smooth animations
  - Optimized bar width calculations for different array sizes

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source and available under the MIT License. 