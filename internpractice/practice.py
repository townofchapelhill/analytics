# Import 
import secrets

# Credentials 
username = secrets.randomusername
password = secrets.randompassword

# Open file
writefile = open("secretsinfo.txt", "w")

# Write 
writefile.write("USERNAME: ")
for letter in username:
    if letter == "U":
        writefile.write(letter)
    else: 
        writefile.write("X")
        
writefile.write("\nPASSWORD: ")
for anotherletter in password:
    if anotherletter == "P":
        writefile.write(anotherletter)
    else: 
        writefile.write("X")