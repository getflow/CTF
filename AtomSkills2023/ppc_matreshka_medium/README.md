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
MATRESHKA_FLAG=flag{test}
MATRESHKA_COUNT=1000
```

# How it works

Service gives you a doll as shown below:
```
Doll #0

⠀⠀⠀⢀⣤⣴⣶⣤⣀
⠀⠀⠀⣾⠛⠉⠉⠙⢿⡆
⠀⠀⠀⡇⠀⠀⠀⠀⠀⡇
⠀⠀⠀⣿⣄⣀⣀⣠⣾⡇⠀
⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⡀
⠀⠀⠻⠿⢿⣿⣿⣿⠿⠿⠃
⠀⠐⣷⣶⣤⣤⣤⣤⣶⣶⣿
⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⠇
⠀⠀⠀⠻⠿⠿⠿⠿⠿⠋

```

You need to get the key to see the next doll. Remember, if you make a mistake, you will start from the beginning.

After opening all the dolls you will get a flag. Good luck!
