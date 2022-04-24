import os

def password_list():
    password=[]
    try:
        os.system("secretsdump.exe -just-dc-ntlm smallwood/Administrator:Password1@192.168.0.100 > hashes.txt")#this is the command to retrieve the passwords from the ssh server
        os.system("john.exe --format=NT --rules -w=dictionary.txt hashes.txt")#these next commands decrypt the passwords if possible
        os.system("john.exe --show --format=NT hashes.txt > password.txt")
        f = open('password.txt', 'r')#opens decrypted passwords file
        password = f.readlines()
    except IOError as inst:
        print('ERROR', inst.errno, inst.strerror)
    return password

def get_password(password):
    userList=[]
    crackedList=[]
    for l in password:#splits decrypted passswords file into the usernames and passwords
        if l != "\n":#ends spliting up file once file introduces text thats not needed
            user, cracked, bin1, bin2, bin3, bin4, bin5, bin6 = l.split(":") #spilts file using the colons
            userList.append(user)
            crackedList.append(cracked)
        else:
            break
    return userList, crackedList

def comparePassword(userList, crackedList):
    f = open('dictionary.txt', 'r')#opens list of passswords to compare cracked passwords too
    passList = f.readlines()
    list = []
    for l in range(0, len(crackedList)):#compares the passwords
        for i in range(0, len(passList)):
            passList[i] = passList[i].strip()
            if crackedList[l] == passList[i]:
                list.append(userList[l])
                list.append(" password is unsafe and needs changed. \n")
    with open('output.txt', 'w') as f:#outputs the usernames where the passwords were decrypted
        f.writelines(list)

def main():
    password = password_list()
    userList, crackedList = get_password(password)
    comparePassword(userList, crackedList)

main()