```

⠀⠀⠀⢀⣤⣴⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣾⠛⠉⠉⠙⢿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡇⠀⠀⠀⠀⠀⡇⠀⢀⣴⠶⠶⢦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣿⣄⣀⣀⣠⣾⡇⠀⢸⠃⠀⠀⠀⢿⠀⠀⡴⠶⠶⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⡀⢸⣦⣀⣀⣠⣇⠀⠀⠀⠀⠀⡹⠀⢀⡴⠶⡄⠀⠀
⠀⠀⠻⠿⢿⣿⣿⣿⠿⠿⠃⢸⣿⣿⣿⣿⣿⡄⢠⣷⣶⣾⣧⠀⢸⣀⢀⡇⠀⠀
⠀⠐⣷⣶⣤⣤⣤⣤⣶⣶⣿⠀⣉⣉⣉⣉⣩⣄⠈⠿⠿⠿⠟⠂⢸⣿⣿⣧⠀⠀
⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⠇⢸⣿⣿⣿⣿⣿⡏⢠⣶⣶⣶⣶⡇⢠⣄⣀⣤⠀⠀
⠀⠀⠀⠻⠿⠿⠿⠿⠿⠋⠀⠘⠿⠿⠿⠿⠟⠀⠘⠿⠿⠿⠟⠀⠸⠿⠿⠏⠀⠀

```

# Run 
```#bash
docker-compose build
docker-compose up -d --remove-orphans
```

# Constants

```#bash
BARCODE_FLAG=flag{test}
BARCODE_COUNT=1000
```

# How it works

Service gives you a glasses of beer as shown below:
```
Glass #0

.~~~~.
i====i_
|cccc|_)
|cccc|   hjw
`-==-'

```

You need to solve a task to pay and drink. Remember, if you make a mistake, you will start from the first glass.

After drinking all the glasses you will get a flag. Good luck!
