# hangman

A terminal based app. The traditional hangman word guessing game with a few api requests and data plots. A coding exercise for practise and learning **Python**. Topics include use of modules, API requests, error handling, matplotlib, numpy. Add to that creating a github project where code review and contributions are invited. 

Using [RapidAPI](https://rapidapi.com/marketplace) for word definitions. Free sign up at [RapidAPI](rapidapi.com) will get you an api key. 
In the ```def twinword_request(args)``` function look for the line ```'x-rapidapi-key': 'env_file.env',``` and replace ```'env_file.env'``` with your rapidapi key. The app *may* work without this and instead will just go to [Datamuse](https://www.datamuse.com/api/) for the definition.   

1. An English word is generated. Parameters for random (word) may be set in the script.
2. Player has 11 tries to guess the word
3. Gallows / noose advances for every wrong guess
4. Wikipedia entry based on the word along with definitions of the word is diplayed when word is guessed or no guesses left.
5. A message is displayed if word guessed is in the top 5000 most used English words.
6. Player may choose to see graphical depiction of word / letter data (matplotlib tables)
7. Game loops to start

Contributions are welcomed. See [CONTRIBUTING](https://github.com/alxtrnr/hangman/blob/master/CONTRIBUTING.md) for how.

If you over from [PyBites](pybites.slack.com) thank you! Code / project review would be great! Bit muddled about returning and passing values between functions. Any pointers on this or anything else would be wonderful. Thank you.  
