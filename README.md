# Typing speed test
This application allows you to find out how many words you are able to type in a minute, as well as how accurate you can be when it comes to spelling and, finally, your overall speed (your words per minute versus your accuracy).

## Getting started
1. Clone the repository:
```
git clone https://github.com/while-is-alex/typing-speed-test.git
```

2. Change the directory to the project folder.

3. Create a virtual environment:
```
py -m venv venv
venv/Scripts/activate
```

4. Install the required packages:
```
pip install -r requirements.txt
```

5. Finally, to get started with the test, run the `main.py` file. The app will launch and diplsay the home screen.

![home-screen.png](https://i.ibb.co/MNqpMJd/home-screen.png)

## Features
### The test screen
The test screen will load and display the first sentence of one of the texts, randomly chosen from the `data.py` file. The user has indefinite time to familiarize themselves with the interface, as the timer only starts when the user types the first character into the entry box. The entry-box text automatically clears once the user clicks on it, allowing the user to immediately start typing. The user has the option to stop the test at anytime by pressing the "stop" button, which will trigger the processing of the numbers collected up to that moment, and will still generate results, even with incomplete data.

![test-screen.png](https://i.ibb.co/zFh4bN2/test-screen.png)

### Checking for accuracy

Once the user starts typing, the application will start processing the user's input and comparing it to the text to be transcribed. If the user's input matches that text, the user receives a visual feedback in the form of the correct text turning green. The user can also always keep track of how much time they have left and how many words (regardless of being correct or incorrect) they have currently typed.

![test-running.png](https://i.ibb.co/x2S9qQ4/test-running.png)

### Results

Finally, after the timer runs out or after the user presses the "stop" button, the results screen is displayed, where the user can find out the number of words they have typed within that minute, the percentage of those words that have matches the correct spelling and their net speed, which is the number of words typed times the accuracy percentage.

![results-screen.png](https://i.ibb.co/1JVMcL5/results-screen.png)

## Requirements

This app requires the following:

+ Python 3
+ Tkinter

```
pip install -r requirements.txt
```
