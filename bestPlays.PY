import random


options = ["60P", "muchWarf", "dame Tu Cosita", "garry", "LordBrandon", "realG"]
random.shuffle(options)
team1 = options[:3]
team2 = options[3:]
print(f"{team1} and {team2}")