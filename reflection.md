# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

The first thing I notice is that only sometimes the go higher or go lower message is inaccurate. The secret was 87 but I enter 10 and it said to go lower which was not correct.

The second thing I found is that when I click new game, it correctly resets my score back to 0 but the history does not clear and the score does not reset either.

The third error I found was that when I make the correct guess, it gives the wrong score.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

The AI tool I used for this project was Claude AI. AI suggested that we fix the incorrect hint by swapping the "go lower" and "go higher" string to correctly match the guess. I verified this result by creating a pytest that verified this output. I also verified this by checking the live game and seeing that the correct message was being outputted. AI did not give any incorrect suggestions but offered a fix for an incorrectly matching score that did not entirely solve the issue. The issue was that the score should be 90 on the first attempt and 80 on the second attempt and this was correctly tested on pytest. However, on the live game, it was 90 on the first attempt and 75 on the second attempt because AI claimed that there was a rendering issue which was correct. This fix was slightly misleading.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was really fixed by actually going to the live game and seeing the fix for myself. The main bug was the incorrect hint that I saw was not matching my guess. In test_game_logic.py, we ran three functions which tested the three possibilites of the guess being too high, too low, or win and asserted the value that we should be recieving. AI helped fix an error where the refactored functions returned a tuple of two strings, the too high or too low and the go higher or go lower hint. The tests only expected one string value, so AI suggested that we fix this error by unpacking the tuple and finally the pytests passed.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret number kept changing in the original app because the status was not correctly reset after a new game was clicked. Streamlit works essentially by having a state that is either the player is playing or the player has won. Once the state hits the won state the player cannot keep playing unless they hit the new game button again. However, this new game button did not work properly and this won state was never changed back to playing state once the player wanted to play a new game. The fix that worked was that we correctly changed the state back to playing when the code initially only changed the attempts amount and secret number.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

Before this project, I never knew about refactoring code in a seperate file and then testing that function by using pytest and finally importing that new function into the original file when it worked. Originally, I would just change the function in the original file immediately. Next time, I would try to have AI explain a little more about the code and what is going on before I try to ask it for a solution. This project has made me think that even AI code should be tested before it is immediately imported into the original file.
