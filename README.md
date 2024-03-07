# Spoty-parser
Conviniently parse a txt file containing a list of songs into a resulting file with parsed song names, artists and spotify links

### Input file
![before](/static/raw_txt.png)
### Result
![before](/static/results.png)

## Requirements 
- You would need a CLIENT_ID and CLIENT_SCRET from the official Spotify API 
- Store them into a .env file
- If you already have a token you can store it there, otherwise you can use the `get_token` function inside `main.py`

The projects dependencies are listed in `requirements.txt` 
You can install them using: 
```bash
pip install -r requirements.txt
```

## Todos
 - [ ] Add option for CSV output
 - [ ] Make a CLI