The code as it exists on this branch worked a long time ago on a couple of books after a lot of manual formatting. If I remember right, you have to get each new line to be its own paragraph, and each file to be it's own chapter, in raw txt. Then with CLI options, and an AWS IAM key, you should be able to read the code and get it to convert the book for you.

However, I don't like this process as it is very manual, and this code was written many years ago. With the advent of Large Language Models, I would like to automate the formatting of the books to feed into the text to speech API.

That work is being done on the branch `feature/gpt-preprocessing`, along with a better readme and code refactor. Not currently working, but check it out!
