# Pollybooks

# Instructions

1. Install Pandoc https://pandoc.org/installing.html
2. Get an OpenAI API key, save it to .env
3. Get an AWS IAM key, save it to .env

# Usage

1. Create a new book in the `books` directory. It should be a single text file. The format can be anything.

2. Use pandoc to convert the rest to markdown

```bash
pandoc -f html -t markdown -o book.md book.html
```

3. Use csplit to split the markdown into chapters https://christiantietze.de/posts/2019/12/markdown-split-by-chapter/, usually by the header





