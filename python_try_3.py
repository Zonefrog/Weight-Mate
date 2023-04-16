import datetime
import json
import plots

class Report:
    def __init__(self, weight = -1, height = -1, date = datetime.date.today()):
        self.weight = weight
        self.height = height
        self.date = date

    def dictForm(self):
        return {"weight": self.weight, "height": self.height, "date": self.date}

class Goal:
    def __init__(self, goalType = None, goal = -1, initial = -1, rate = -1, end = datetime.date.today()):
        self.goalType = goalType
        self.goal = goal
        self.initial = initial
        self.rate = rate
        self.end = end

    def dictForm(self):
        return {"goalType": self.goalType, "goal": self.goal, "initial": self.initial, "rate":  self.rate, "end": self.end}

class User:
    def __init__(self):
        self.userId = -1
        self.userName = "Uninitiaised Name"
        self.goals = []
        self.reports = []

    def getWeight(self):
        return self.reports[-1].weight

    def getHeight(self):
        return self.reports[-1].height

    def exportData(self, fileName):
        outString = ""
        
        outString += "#user info\n"
        outString += str(self.userId) + "\n"
        outString += str(self.userName) + "\n"

        outString += "#goals\n"
        outString += str(len(self.goals)) + "\n"
        for goal in self.goals:
            outString += str(goal.dictForm()) + "\n"

        outString += "#initial data\n"
        ps = True
        for report in self.reports:
            outString += str(report.dictForm()) + "\n"
            if ps:
                ps = False
                outString += "#reports\n"

        with open(fileName, "w") as f:
            f.write(outString)

    def importData(self, fileName):
        with open(fileName) as f:
            lines = f.readlines()

        mode = "userId"
        self.goals = []
        self.reports = []
        
        for line in lines:
            line.strip()
            if line[0] == "#" or line == "":
                continue

            if mode == "userId":
                self.userId = int(line)
                mode = "userName"

            elif mode == "userName":
                self.userName = line
                mode = "goalNum"

            elif mode == "goalNum":
                goalNum = int(line)
                mode = "goals"

            elif mode == "goals":
                self.goals.append(dictToGoal(eval(line)))
                goalNum -= 1
                if goalNum == 0:
                    mode = "reports"

            elif mode == "reports":
                self.reports.append(dictToReport(eval(line)))

def dictToGoal(inDict):
    return Goal(goalType = inDict["goalType"], goal = inDict['goal'], initial = inDict['initial'], rate = inDict['rate'], end = inDict['end'])

def dictToReport(inDict):
    return Report(weight = inDict['weight'], height = inDict['height'], date = inDict['date'])

def addUser(userName, password):
    with open("User_Data.txt") as f:
        lines = f.readlines()
        
    with open("User_Data.txt", "a") as f:
        f.write(str(userName) + ";" + str(password) + ";" + str(len(lines)) + "\n")

def loginAttempt(userName, password):
    with open("User_Data.txt") as f:
        lines = f.readlines()

    for line in lines:
        lineData = line.split(";")
        if userName == lineData[0] and password == lineData[1]:
            return True, int(lineData[2])

    return False, 0

def choose(options):
    i = -1
    for opt in options:
        i += 1
        print(str(i) + "- " + str(opt))

    inpu = input("> ")
    try:
        options[int(inpu)]
        return int(inpu)

    except:
        print("Invalid option. Try again.")
        return choose(options)

def main():
    page = "landing"
    ACTIVE_USERID = None
    running = True
    while running:
        if page == "landing":
            options = ["Login", "Sign-Up", "Quit"]
            print("[landing page text]")
            choice = options[choose(options)]
            if choice == "Quit":
                print("Exiting.")
                running = False

            elif choice == "Login":
                page = "login"

            elif choice == "Sign-Up":
                page = "sign-up"

        elif page == "sign-up":
            options = ["Create account", "Back"]
            print("[sign-up page text]")
            choice = options[choose(options)]
            if choice == "Back":
                page = "landing"

            elif choice == "Create account":
                print("Enter a username.")
                user_in = input("> ")
                print("Enter a password.")
                pass_in = input("> ")
                print("Account Created.")
                addUser(user_in, pass_in)
                suc, ACTIVE_USERID = loginAttempt(user_in, pass_in)
                active_user = User()
                active_user.userName = user_in
                active_user.userId = ACTIVE_USERID

                print("Time for your first report!")
                print("Enter weight for today.")
                w_in = input("> ")
                print("Enter a height for today.")
                h_in = input("> ")
                n_rep = Report(weight = int(w_in), height = int(h_in))
                active_user.reports.append(n_rep)
                print("Report added and goals updated.")
                
                page = "goal modifier"

        elif page == "login":
            options = ["Login", "Back"]
            print("[login page text]")
            choice = options[choose(options)]
            if choice == "Back":
                page = "landing"

            elif choice == "Login":
                print("Enter your username.")
                user_in = input("> ")
                print("Enter your password.")
                pass_in = input("> ")
                succeed, ACTIVE_USERID = loginAttempt(user_in, pass_in)
                if not succeed:
                    print("Login failed.")

                else:
                    print("Login Successful.")
                    active_user = User()
                    active_user.importData(str(ACTIVE_USERID) + "_Personal_Data.txt")
                    print("Welcome, " + str(user_in))
                    page = "personal"

        elif page == "personal":
            options = ["Display Goal Graphs", "Stats on Goals", "BMI Caclulator", "Goal Setter", "Make Report", "Save", "Logout"]
            print("[personal page text]")
            choice = options[choose(options)]
            if choice == "Save":
                print("Data saved.")
                active_user.exportData(str(ACTIVE_USERID) + "_Personal_Data.txt")

            elif choice == "Logout":
                print("Logged out.")
                active_user.exportData(str(ACTIVE_USERID) + "_Personal_Data.txt")
                page = "landing"
                ACTIVE_USERID = None
                active_user = None

            elif choice == "Display Goal Graphs":
                for goal in active_user.goals:
                    if goal.goalType in ["gain","loss"]:
                        plots.pie_progress(goal.initial, active_user.getWeight(), goal.goal)

            elif choice == "Stats on Goals":
                print("Here is each goal that you have:")
                i = -1
                for goal in active_user.goals:
                    i += 1
                    print(str(i) + "- " + str(goal.goalType) + " wieght to " + str(goal.goal) + " lbs at a rate of " + str(goal.rate) + " by " + str(goal.end) + ".")

            elif choice == "BMI Caclulator":
                print("Your current BMI is " + str(703 * active_user.getWeight() / (active_user.getHeight()**2)) + ".")

            elif choice == "Weight-Over Time Graph":
                #Todo
                pass

            elif choice == "Goal Setter":
                page = "goal modifier"

            elif choice == "Make Report":
                page = "reports"

        elif page == "goal modifier":
            options = ["Set Goal", "Home"]
            print("[goal page text]")
            choice = options[choose(options)]
            if choice == "Home":
                page = "personal"

            elif choice == "Set Goal":
                print("What type of goal do you want?")
                g_in = ["gain", "loss"][choose(["gain","loss"])]
                print("How many pounds?")
                p_in = int(input("> "))
                print("How many days to accomplish this?")
                d_in = int(input("> "))
                print("Goal added.")
                rec_w = active_user.reports[-1].weight
                if g_in == "gain":
                    g_w = rec_w + p_in

                else:
                    g_w = rec_w - p_in
                    
                temp_goal = Goal(goalType = g_in, goal = g_w, initial = rec_w, rate = int(p_in * 1.0 / d_in), end = datetime.date.today() + datetime.timedelta(days = d_in))
                active_user.goals.append(temp_goal)

            elif choice == "Segguest Goal":
                #todo

                
                g_in = "" #set with segguester. is gain or loss
                p_in = 0 #is an int to gain/lose
                d_in = 0  #is an int of days to do it
                rec_w = active_user.reports[-1].weight
                if g_in == "gain":
                    g_w = rec_w + p_in

                else:
                    g_w = rec_w - p_in
                    
                temp_goal = Goal(goalType = g_in, goal = g_w, initial = rec_w, rate = int(p_in * 1.0 / d_in), end = datetime.date.today() + datetime.timedelta(days = d_in))
                active_user.goals.append(temp_goal)

        elif page == "reports":
            options = ["Make Report", "Home"]
            print("[goal page text]")
            choice = options[choose(options)]
            if choice == "Home":
                page = "personal"

            elif choice == "Make Report":
                print("Enter weight for today.")
                w_in = input("> ")
                print("Enter a height for today.")
                h_in = input("> ")
                n_rep = Report(weight = int(w_in), height = int(h_in))
                active_user.reports.append(n_rep)
                print("Report added and goals updated.")
                #update each goal according to the new data
                for goal in active_user.goals:
                    if goal.end < datetime.date.today() and goal.goalType in ["gain", "loss"]:
                        goal.goalType = "expired " + goal.goalType
            
if __name__ == "__main__":
    main()
