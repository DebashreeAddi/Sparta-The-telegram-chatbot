import urllib,time,json,requests,smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from emoji import emojize
import datetime ,calendar 
import sqlite3 as lite
from telepot.delegate import pave_event_space, per_chat_id, create_open
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


class FindersKeepers(telepot.helper.ChatHandler):

    #To obtain the category that the player has chosen while building a team 
    joinTeam_flag = False
    category_flag= False
    indoorGames_flag= outdoorGames_flag= videoGames_flag= False
    play_flag= False

    #Data to be saved in the database of the player building his team 
    name_buildTeam = '' #Name 
    name_joinTeam= ''
    matric_buildTeam= '' #Matriculation Number
    contact_buildTeam= '' #Contact Number 
    contact_joinTeam=''
    booking_date=''  #To get the date for which the booking is made  
    booking_time='' #To get the time for which the booking is made
    email_buildTeam='' #Email of the player
    bd_game_check ='' #To capture the game for which the team is to be built 
    bd_location_check = '' #Captures the loaction
    pmax_buildTeam=''   #Keeps track of maximum players 
    pmin_buildTeam=''   #Keeps track of minimum

    #To obtain the data for the player joining someone else's team 
    matric_joinTeam=''  #Matriculation Number 
    captured_sn_joinTeam=0  #to get the serial number of waitlisted player in the waitlisted database so that its info can be sent to the players in charge 
    sChosen_JD=0 #to get the serial number chosen by the player of the player starting his team in the team setup database 


    date='' #to get the date 
    month_calendar= '' #to show the dates and month in calendar form


    #To keep track of the index value of the databases
    lid = 0 #to increment the serial number in the team setup database
    sn=0 #to increment the serial number in the waitlisted player database (who have requested to join other players)

    

    #list of games 
    moodType= ["I wanna build my own team for a game!!!", "I wanna join a team"]

    #Video Games and indoor games
    video_games= ["WWE", "Fifa", "World of Warcraft", "Grand Theft Auto V", "Resident Evil 4", "Call of Duty", "Other Video Games"]  
    videogames_place= ["Students Activity Center", "Halls"]


    #Indoor Games

    indoor_games= ["Table Tennis", "Gym", "Scrabble", "Chess", "Game of life", "Ludo", "Heads up Charades", "Carrom", "Chess", "Chinese Chess","Other Indoor Games"]
    gym_places= ["North Hill", "Students Recreation Center", "Near Hall 3", "Near Tamarind Hall"]
    other_indoor_places= ["Rooms", "TV Lounge", "Recreational Room"]
    tableTennis_court= ["Students Activity Center", "Nanyang Technopreneurship Center", "Students Recreation Center"]


    #Outdoor Games
    badminton_courts= ["The Wave", "In Hall 7", "North Hill"]
    lawntennis_court= ["Students Recreation Center", "In Hall 7"]
    soccer= ["Students Recreation Center"]
    squash_court= ["Students Recreation Center"]
    swimming= ["Students Recreation Center"]
    basketball_court= ["Students Recreation Center ", "North Hill", "In Hall 7"]

    outdoor_games_loc= [badminton_courts, lawntennis_court, soccer, squash_court, swimming, basketball_court]
    out_loc= badminton_courts + lawntennis_court + soccer + squash_court + swimming + basketball_court
    outdoor_games= ["Badminton", "Lawn Tennis", "Soccer", "Squash", "Swimming", "Basketball"]


    #Categories
    categories_list= [indoor_games, outdoor_games, video_games]
    categories= ["Indoor Games", "Outdoor Games", "Video Games"]

    # ----halls
    halls = ["Hall 1", "Hall 2", "Hall 3", "Hall 4", "Hall 5", "Hall 6", "Hall 7", "Hall 8", "Hall 9", "Hall 10", "Hall 11", "Hall 12", "Hall 13", "Hall 14", "Hall 15", "Hall 16", "Crescent Hall", "Pioneer Hall", "Binjai Hall", "Tanjong Hall", "Banyan Hall"]

    hall_1 = ["BLK 12", "BLK 13", "BLK 14", "BLK 15", "BLK 16", "BLK 17", "BLK 18"]
    hall_2 = ["BLK 1", "BLK 2", "BLK 3", "BLK 4", "BLK 5", "BLK 6", "BLK 7", "BLK 8", "BLK 9", "BLK 10", "BLK 11"]
    hall_3 = ["BLK 3A", "BLK 3B", "BLK 3C", "BLK 3D", "BLK 3E"]
    hall_4 = ["BLK 22", "BLK 23", "BLK 24", "BLK 25", "BLK 26", "BLK 27"]
    hall_5 = ["BLK 28", "BLK 29", "BLK 30", "BLK 31"]
    hall_6 = ["BLK 32", "BLK 33", "BLK 34", "BLK 35"]
    hall_7 = ["BLK 36", "BLK 37", "BLK 38", "BLK 39", "BLK 40"]
    hall_8 = ["BLK 41", "BLK 42", "BLK 43", "BLK 44"]
    hall_9 = ["BLK 45", "BLK 46", "BLK 47", "BLK 48"]
    hall_10 = ["BLK 49", "BLK 50", "BLK 51", "BLK 52"]
    hall_11 = ["BLK 53", "BLK 54", "BLK 55", "BLK 56"]
    hall_12 = ["BLK 57", "BLK 58", "BLK 59", "BLK 60"]
    hall_13 = ["BLK 61", "BLK 62", "BLK 63", "BLK 64"]
    hall_14 = ["BLK 65", "BLK 66", "BLK 67", "BLK 68"]
    hall_15 = ["BLK 69", "BLK 70", "BLK 71", "BLK 72"]
    hall_16 = ["BLK 16A", "BLK 16B", "BLK 16C", "BLK 16D", "BLK 16E"]
    crescent_hall = ["BLK 17A", "BLK 17B", "BLK 17C", "BLK 17D"]
    pioneer_hall = ["BLK 18A", "BLK 18B", "BLK 18C", "BLK 18D"]
    binjai_hall = ["BLK 19A", "BLK 19B"]
    tanjong_hall = ["BLK 20A", "BLK 20B"]
    banyan_hall = ["BLK 21A", "BLK 21B"]

    halls_list= [hall_1, hall_2, hall_3, hall_4, hall_5, hall_6, hall_7, hall_8, hall_9, hall_10, hall_11, hall_12, hall_13, hall_14, hall_15, hall_16, crescent_hall, pioneer_hall, binjai_hall, tanjong_hall, banyan_hall]
    all_halls= hall_1 + hall_2 + hall_3 + hall_4 + hall_5 + hall_6 + hall_7 + hall_8 + hall_9 + hall_10 + hall_11 + hall_12 + hall_13 + hall_14 + hall_15 + hall_16 + crescent_hall + pioneer_hall + binjai_hall + tanjong_hall + banyan_hall

       
    #list of games 
    moodType= ["I wanna build my own team for a game!!!", "I wanna join a team"]

    #Video Games and indoor games
    video_games= ["WWE", "Fifa", "World of Warcraft", "Grand Theft Auto V", "Resident Evil 4", "Call of Duty", "Other Video Games"]  
    videogames_place= ["Students Activity Center", "Halls"]


    #Indoor Games
    indoor_games= ["Table Tennis", "Gym", "Scrabble", "Chess", "Game of life", "Ludo", "Heads up Charades", "Carrom", "Chess", "Chinese Chess","Other Indoor Games"]
    gym_places= ["North Hill", "Students Recreation Center", "Near Hall 3", "Near Tamarind Hall"]
    other_indoor_places= ["Rooms", "TV Lounge", "Recreational Room"]
    tableTennis_court= ["Students Activity Center", "Nanyang Technopreneurship Center", "Students Recreation Center"]


    #Outdoor Games
    badminton_courts= ["The Wave", "In Hall 7", "North Hill",]
    lawntennis_court= ["Students Recreation Center", "In Hall 7"]
    soccer= ["Students Recreation Center"]
    squash_court= ["Students Recreation Center"]
    swimming= ["Students Recreation Center"]
    basketball_court= ["Students Recreation Center ", "North Hill", "In Hall 7"]

    outdoor_games_loc= [badminton_courts, lawntennis_court, soccer, squash_court, swimming, basketball_court]
    outdoor_games= ["Badminton", "Lawn Tennis", "Soccer", "Squash", "Swimming", "Basketball"]
    out_loc= badminton_courts + lawntennis_court + soccer + squash_court + swimming + basketball_court


    #Categories
    categories_list= [indoor_games, outdoor_games, video_games]
    categories= ["Indoor Games", "Outdoor Games", "Video Games"]
    categories_flag= [outdoorGames_flag, videoGames_flag, indoorGames_flag]

    def __init__(self, *args, **kwargs):
        super(FindersKeepers, self).__init__(*args, **kwargs)
        self.text=''
        self.chat=0
        self.message_id=0
        self.name=''
        self.matric_no=''
        self.photo_reply= False
        self.contact= False
        self.username=''
        self.contact_reply= False 
        self.buttons=[]
        self.keyboard=''
        self.date=''
        self.month_calendar=''
        self.rows=[]
        self.name=''
        self.fromaddr=''
        self.toaddr=''
        self.body=''
        self.text=''
        self.count=0 
        self.tstrength_BD=0

        self.count=0 #counter for the program

    def string_length(self, str1):         #Checks the length of the string 
        self.count = 0
        for char in str1:
            self.count += 1
        return self.count 

    def send_notification_email(self, EmailPlayerContacted):
        self.fromaddr = "sportopia05@gmail.com"           #Sends notification via email to the player in charge 
        self.toaddr = EmailPlayerContacted
        msg = MIMEMultipart()
        msg["from"] = self.fromaddr
        msg["to"] = self.toaddr
        msg["subject"] = "Opportunities await you!"
        self.body = "Dear Sir/Madam,\n\nI am very pleased to notify you that a player has joined your team! Click the following link: https://web.telegram.org/ to see more details regarding your team.\n\n\nBest Regards,\nSparta"
        msg.attach(MIMEText(self.body, "plain"))
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.fromaddr, "12345@12345")
        self.text = msg.as_string()
        server.sendmail(self.fromaddr, self.toaddr, self.text)
        server.quit()

    def tstrength_update_TeamSetup(self, Owner, SerialNumberPlayerContacted, chatIDPlayerContacted):
        

        con1= lite.connect("FionDB_sublime.db") #To get the team strength and increment by 1 when a player is added
        with con1:
            cur1= con1.cursor()
            cur1.execute("SELECT TeamStrength FROM TeamSetup WHERE SerialNumber=:SerialNumber",{"SerialNumber":SerialNumberPlayerContacted}) 
            con1.commit()        
            self.rows1= cur1.fetchone()
            self.tstrength_BD= int(self.rows1[0])

            con1= lite.connect("FionDB_sublime.db")
            with con1:
                cur1= con1.cursor()
                cur1.execute("UPDATE TeamSetup SET TeamStrength= ? WHERE SerialNumber=?", ((self.tstrength_BD +1), SerialNumberPlayerContacted))
                con1.commit()
            bot.sendMessage(Owner, emojize("Congrats! Here you can contact your team leader :punch: :ok_woman:", use_aliases = True))
            
            self.con1= lite.connect("FionDB_sublime.db")   #To notify the player to the team in charge and output its info to the person 
            with self.con1:
                self.con1.row_factory= lite.Row
                self.cur1= self.con1.cursor()
                self.cur1.execute("SELECT Name, OrganiserContactNumber, MatriculationNumber, OrganiserEmail, NameGame, DateGame, Venue, TimeGame, TeamStrength FROM TeamSetup WHERE SerialNumber=:SerialNumber",{"SerialNumber": SerialNumberPlayerContacted})
                self.con1.commit()  
                while True:          
                    self.rows1= self.cur1.fetchone()  
                    if self.rows1==None:
                        break       
                    bot.sendMessage(Owner, emojize(("%s %s %s %s %s %s %s %s" % ("Name: " + str(self.rows1["Name"]), "\nContact Number: " + str(self.rows1["OrganiserContactNumber"]), "\nEmail: " + str(self.rows1["OrganiserEmail"]), "\nGame: " + str(self.rows1["NameGame"]), "\nDate: " + str(self.rows1["DateGame"]), "\nVenue: " + str(self.rows1["Venue"]), "\nTime: " + str(self.rows1["TimeGame"]), "\nTeam Strength: " + str(self.rows1["TeamStrength"]))))) 
            bot.sendMessage(Owner, "Press /main to explore more options!")

    def team_update_TeamSetup(self, SerialNumberPlayerContacted, chatIDPlayerContacted):
        

        con2= lite.connect("FionDB_sublime.db") 
        with con2:
            cur2= con2.cursor()
            cur2.execute("SELECT TeamStrength, PlayerMin, PlayerMax, Open, NameGame, DateGame, Venue, TimeGame FROM TeamSetup WHERE SerialNumber=:SerialNumber",{"SerialNumber":SerialNumberPlayerContacted })      #to get the team strength of the players in the current game chosen by the waitlisted player 
            con2.commit()   
            while True:     
                self.rows2= cur2.fetchone()
                if self.rows2==None:
                    break
                if (int(self.rows2[0])== int(self.rows2[1])):           #When the team incharge had succefully created his team with min number of players 
                    bot.sendMessage(chatIDPlayerContacted, emojize("Congrats dude...your team has been formed and has minimum number of players :boom: :cowboy_hat_face: !!!", use_aliases = True))
                    bot.sendMessage(chatIDPlayerContacted, emojize(("%s %s %s %s" % ("Game: " + str(self.rows2[4]), "\nDate: " + str(self.rows2[5]), "\nVenue: " + str(self.rows2[6]), "\nTime: " + str(self.rows2[7]) ))))     
                    
                if (int(self.rows2[0])>= int(self.rows2[2])):
                    con2= lite.connect("FionDB_sublime.db")
                    with con2:
                        cur2= con2.cursor()
                        cur2.execute("UPDATE TeamSetup SET Open= ? WHERE SerialNumber=?", (0, SerialNumberPlayerContacted))
                        con2.commit()

    def add_data_TeamSetup(self, lid, chat, matric_buildTeam, email_buildTeam, contact_buildTeam, name_buildTeam, bd_game_check, booking_date, bd_location_check, booking_time, pmin_buildTeam, pmax_buildTeam):
        #Adds data into the TeamSetup DB 
        con1= lite.connect("FionDB_sublime.db")
        with con1:
            cur1= con1.cursor()
            cur1.execute("INSERT INTO TeamSetup(SerialNumber, Owner, MatriculationNumber, OrganiserEmail, OrganiserContactNumber, Name, NameGame, DateGame, Venue, TimeGame, PlayerMin, PlayerMax, TeamStrength, Open) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);",(lid, chat, matric_buildTeam, email_buildTeam, contact_buildTeam, name_buildTeam, bd_game_check, booking_date, bd_location_check, booking_time, pmin_buildTeam, pmax_buildTeam, 1, 1))                      
                   
    def addData_WaitlistPlayers(self, sn, chat, matric_joinTeam, contact_joinTeam, name_joinTeam, bd_game_check, sChosen_JD, namePlayerContacted, date, time, venue, chatIDPlayerContacted, MatricNumberPlayerContacted, SerialNumberPlayerContacted, EmailPlayerContacted, PhoneNumberPlayerContacted):
              #Adds data to the waitlist Players DB 
        con2= lite.connect("FionDB_sublime.db")
        with con2:
            
            cur2= con2.cursor()
            cur2.execute("INSERT INTO WaitlistPlayers(SerialNumber, Owner, MatriculationNumber, PlayerContactNumber, Name, NameGame, SerialNumberChosen, PlayerNameContacted, DateGame, TimeGame, VENUE, ChatIDPlayerContacted, MatricNumberPlayerContacted, SerialNumberPlayerContacted, EmailPlayerContacted, PhoneNumberPlayerContacted) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",(sn, chat, matric_joinTeam, contact_joinTeam, name_joinTeam, bd_game_check, sChosen_JD, namePlayerContacted, date, time, venue, chatIDPlayerContacted, MatricNumberPlayerContacted, SerialNumberPlayerContacted, EmailPlayerContacted, PhoneNumberPlayerContacted))
            
    def look_for_game_teamsetup(self, chat, bd_game_check):
        
        con1= lite.connect("FionDB_sublime.db")
        with con1:
            con1.row_factory= lite.Row
            cur1=con1.cursor()
            cur1.execute("SELECT SerialNumber, Name, OrganiserContactNumber, DateGame, Venue, TimeGame, TeamStrength, Open FROM TeamSetup WHERE NameGame=:NameGame",{"NameGame": bd_game_check})
            con1.commit()
            while True:
                self.rows= cur1.fetchone()                        
                if self.rows== None:
                    self.sender.sendMessage("Sorry dudee...no records found")
                    self.db_buildTeam= False
                    break
                if (int(self.rows[7]==1)):
                    self.sender.sendMessage(emojize(("%s %s %s %s %s %s %s" % ("Serial Number: " + str(self.rows["SerialNumber"]), "\nName: " + str(self.rows["Name"]), "\nContact Number: " + str(self.rows["OrganiserContactNumber"]), "\nDate: "+ str(self.rows["DateGame"]), "\nVenue: " + str(self.rows["Venue"]), "\nTime: " + str(self.rows["TimeGame"]), "\nTeam Strength: " + str(self.rows["TeamStrength"])))))
                    self.db_buildTeam= True
                    

    def on_chat_message(self, msg):
        
           #command for entering name
        self.useless=msg['text']        #to initiate chat ,user enters any key,which is not stored and whicch doesnt have any use on the program.Hence the first message is useless
        content_type, chat_type, chat_id = telepot.glance(msg)


        if self.count==0 or msg['text']=="/start":
            self.count=0
            bot.sendMessage(chat_id, emojize("Hola Amigos!!! :smile: :snowman:",use_aliases = True))
            bot.sendMessage(chat_id, "I am Sparta")
            self.sender.sendMessage(emojize("Sparta the Bot :hatched_chick:",use_aliases = True))
            self.sender.sendMessage(emojize("Or to be more precise- I am the bot that makes teams for you!!! Great ain't it? :robot_face:",use_aliases = True))
            Keyboard10 = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                                [KeyboardButton(text="Sure")]])
            self.sender.sendMessage(emojize("So... why don't we get started? :face_with_stuck-out_tongue: :ghost:",use_aliases = True))
            self.sender.sendMessage("Press Sure to continue!!",reply_markup=Keyboard10)
            self.count+=1

        elif self.count==1 or msg['text']=='/main':
            self.count=1
            self.useless2=msg['text']

            self.sender.sendMessage(emojize("OKAY! So what do you want to do? :woman_dancing: Start your own game where players can join you or join someone else's team? :relaxed:",use_aliases = True))
            Keyboard_categories5 = ('I wanna build my own team for a game!!!','I wanna join a team!')
            Keyboard5 = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                        [KeyboardButton(text=x)] for x in Keyboard_categories5
                        ])
            self.sender.sendMessage(emojize("*It's Play Time!!!* :baby_angel: :yum:",use_aliases=True ))
            self.sender.sendMessage("Okay so let's choose: ", reply_markup= Keyboard5)
            self.count+=1

        elif self.count==2:
            self.choice1=msg['text']
            if self.choice1 == "I wanna join a team!":
                self.sender.sendMessage(emojize("Let's start by knowing your name?\nSo what do I call you? :cowboy_hat_face: :blue_heart:",use_aliases=True))
                self.a=1
                self.count+=1

            elif self.choice1 == "I wanna build my own team for a game!!!":
                self.sender.sendMessage(emojize("Let's start by knowing your name?\nSo what do I call you? :cowboy_hat_face: :blue_heart:", use_aliases = True))
                self.a=0
                self.count+=1
            else:
                self.sender.sendMessage(emojize("The input you entered was wrong.:sweat_drops:\nDont worry you still get to correct yourself :shit: :shit:\nEnter again-",use_aliases = True))
                self.count=2

        elif self.count==3:
            if self.choice1 == "I wanna join a team!":
                FindersKeepers.name_joinTeam=msg['text']
                self.sender.sendMessage(emojize("Heya "+FindersKeepers.name_joinTeam+" Hope you are gonna really enjoy this experience! :smiling_face_with_halo:", use_aliases = True))
            elif self.choice1=="I wanna build my own team for a game!!!": 
                FindersKeepers.name_buildTeam= msg['text']          
                self.sender.sendMessage(emojize("Heya "+FindersKeepers.name_buildTeam+" Hope you are gonna really enjoy this experience! :smiling_face_with_halo:", use_aliases = True))
            self.sender.sendMessage(emojize("Also carefully enter your matriculation number", use_aliases = True))      
            self.count+=1

        elif self.count==4:                 
                
            if (self.string_length(msg['text'])==9) and (msg['text'][:1]=="U"):
                if self.choice1 == "I wanna join a team!":
                    FindersKeepers.matric_joinTeam=msg['text']
                                    
                elif self.choice1 == "I wanna build my own team for a game!!!":
                    FindersKeepers.matric_buildTeam=msg['text']
                    
                Keyboard_categories1 = ('Indoor Games','Outdoor Games', 'Video Games')
                Keyboard1 = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[[KeyboardButton(text=x)] for x in Keyboard_categories1])
                if self.a:
                    self.sender.sendMessage(emojize("Alrighty, you wanna join a team :star2: \nSet back and prepare yourself for the ride while we look for a team for you :notes: \nCould you please describe what  games you are interested in? :raised_hands:",  use_aliases = True), reply_markup=Keyboard1)
                    self.count=5
                else:
                    self.sender.sendMessage(emojize("Yeyyy are you ready? :sparkles: Let's help you build a team :man_dancing:\nOkay! *Excited?* Let's start by which game you would like to play? :fire:", use_aliases = True), reply_markup=Keyboard1)
                    self.count=5
            else:
                self.sender.sendMessage("Carefully enter the matruiculation number AGAIN")
                self.count=4
            
        elif self.count==5:
            self.game_choice1=msg['text']

            if self.game_choice1=="Indoor Games":
                Keyboard_categories_indoor = ('Table Tennis','Gym','Scrabble','Chess','Game of Life','Ludo','Heads up Charades','Carrom','Chinese chess','Other Indoor Games')
                Keyboard2 = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                                [KeyboardButton(text=event_category)] for event_category in Keyboard_categories_indoor
                                ])
                self.sender.sendMessage("Okie dokie, let's get deeper -",reply_markup=Keyboard2)
                FindersKeepers.bd_game_check=msg['text']
                self.count=6

            elif(self.game_choice1=="Outdoor Games"):
                Keyboard_categories_outdoor = ('Badminton','Lawn Tennis','Soccer','Squash','Swimming','Basketball')
                Keyboard3 = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                                [KeyboardButton(text=event_category)] for event_category in Keyboard_categories_outdoor
                                ])
                self.sender.sendMessage(emojize("Okie dokie, let's get deeper :dancers: :information_desk_person:", use_aliases= True),reply_markup=Keyboard3)

                FindersKeepers.bd_game_check=msg['text']
                self.count=6

            elif(self.game_choice1=="Video Games"):
                Keyboard_categories_video = ('WWE','Fifa','World of Warcraft','Grand Theft Auto V','Resident Evil 4','Call of Duty','Other Video Games')
                Keyboard4=ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                                [KeyboardButton(text=event_category)] for event_category in Keyboard_categories_video
                                ])
                self.sender.sendMessage(emojize("Okie dokie, let's get deeper :dancers: :information_desk_person:", use_aliases= True),reply_markup=Keyboard4)

                FindersKeepers.bd_game_check=msg['text']
                self.count=6

            else:
                self.sender.sendMessage(emojize("The input you entered was wrong. :sweat_drops:\nDont worry you still get to correct yourself :shit: :shit: \nEnter again-", use_aliases = True))
                self.count=5

            

        elif(self.count==6):
            FindersKeepers.bd_game_check= msg['text']
            if self.choice1 == "I wanna build my own team for a game!!!":
                if msg['text'] in FindersKeepers.video_games:
                    keyboard6= ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                                [KeyboardButton(text=x)] for x in FindersKeepers.videogames_place])
                    self.sender.sendMessage("So where exactly do you wanna play?", reply_markup=keyboard6)
                    self.count+=1
                elif msg['text'] in FindersKeepers.indoor_games:
                    if msg['text']=="Gym":
                        keyboard6= ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                                [KeyboardButton(text=x)] for x in FindersKeepers.gym_places])
                        self.sender.sendMessage("So where exactly do you wanna play?", reply_markup=keyboard6)
                        self.count+=3
                    elif msg['text']=="Table Tennis":
                        keyboard6= ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                                    [KeyboardButton(text=x)] for x in FindersKeepers.tableTennis_court])
                        self.sender.sendMessage("So where exactly do you wanna play?", reply_markup=keyboard6)
                        self.count+=3
                    else:
                        keyboard6= ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                                    [KeyboardButton(text=x)] for x in FindersKeepers.other_indoor_places])
                        self.sender.sendMessage("So where exactly do you wanna play?", reply_markup=keyboard6)
                        self.count+=1
                elif msg['text'] in FindersKeepers.outdoor_games:
                    for i in range (len(FindersKeepers.outdoor_games)):
                        if msg['text']== FindersKeepers.outdoor_games[i]:
                            keyboard6= ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                                    [KeyboardButton(text=x)] for x in FindersKeepers.outdoor_games_loc[i]])
                            self.sender.sendMessage("So where exactly do you wanna play?", reply_markup=keyboard6)
                            self.count+=3
                else:
                    self.count=6
                    self.sender.sendMessage("Use custom keyboard pleasee")
            else:
                
                self.count +=13
                self.sender.sendMessage(emojize("Cool! Wouldn't it be convenient if the players who want to join could contact you? :mailbox_with_mail: \nHelp us help you by sending us your contact! :hearts:", use_aliases= True))
                       
                


        elif(self.count==7):
            FindersKeepers.bd_location_check= msg['text']
            if msg['text']=="Halls" or msg['text'] in FindersKeepers.other_indoor_places:
                keyboard7= ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                                    [KeyboardButton(text=x)] for x in FindersKeepers.halls])
                self.sender.sendMessage(emojize("Let's be more specific :construction_worker:", use_aliases= True), reply_markup=keyboard7)
                self.count+=1

        elif (self.count==8):
            FindersKeepers.bd_location_check= FindersKeepers.bd_location_check + ": " +msg['text']
            
            for i in range (len(FindersKeepers.halls)):
                if msg['text']==FindersKeepers.halls[i]:
                    keyboard8= ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                                        [KeyboardButton(text=x)] for x in FindersKeepers.halls_list[i]])
                    self.sender.sendMessage("Okay where exactly?", reply_markup=keyboard8)
                    self.count+=1

        elif (self.count==9):
            if msg['text'] in FindersKeepers.all_halls:
                FindersKeepers.bd_location_check= FindersKeepers.bd_location_check + " :" +msg['text']
            else:
                FindersKeepers.bd_location_check= msg['text'] 
            option= ('Yes', 'Nope..next month please')
            keyboard5= ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                                [KeyboardButton(text=x)] for x in option
                                ])
            self.sender.sendMessage(emojize("Okay! So do you want to make a booking for this month? :smiling_face_with_smiling_eyes:", use_aliases = True), reply_markup= keyboard5)
            self.count+=1
            
        elif(self.count==10):
            self.month_choice=msg["text"]
            if self.month_choice=="Yes":
                date= datetime.date.today()
                month_calendar= calendar.month(date.year, date.month) 
                self.next_month=0
                            
            else:
                date= datetime.date.today()
                month_calendar= calendar.month(date.year, date.month+1) 
                self.next_month=1
            self.sender.sendMessage(month_calendar+"\n\nCarefully now enter a suitable date for the month to build a team for that day!\nJust Enter a 2 digit number. Example: 02: ")
            self.count+=1

        elif(self.count==11):
            self.date=msg['text']
            date= datetime.date.today()
            if (date.day<=int(self.date)<=31 and self.next_month==0):
                FindersKeepers.booking_date= self.date+"/"+str(date.month)+"/"+str(date.year)
                self.sender.sendMessage(emojize("Let's choose an appropriate time? :snowflake:\nYou are just a few steps away from your TEAM! :zap:\nType the time in this format please!\nabcd-wxyz...for example: 0930-1130 (in 24 hour format)", use_aliases= True))
                self.count+=1
            elif(int(self.date)<=31 and self.next_month==1):
                FindersKeepers.booking_date= self.date+"/"+str(date.month+1)+"/"+str(date.year)
                self.sender.sendMessage(emojize("Let's choose an appropriate time? :snowflake:\nYou are just a few steps away from your TEAM! :zap:\nType the time in this format please!\nabcd-wxyz...for example: 0930-1130 (in 24 hour format)", use_aliases= True))
                self.count+=1
            else:
                self.sender.sendMessage("Inappropriate date...Enter again!")
                self.count=11
            
            
        elif(self.count==12):
            FindersKeepers.booking_time= msg['text']
            self.sender.sendMessage(emojize("Amazing we are done! You will be notified when players would want to join you! Congrats!! :hugging_face:", use_aliases = True))
            keyboard11= ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                            [KeyboardButton(text="Sure!")]])
            self.sender.sendMessage("Press sure to continue!", reply_markup= keyboard11)
            self.count+=1

        elif(self.count==13):
            self.useless3=msg['text']
            #buttons = [[{"text": "Send", "request_contact": True}]]
            #keyboard_contact = {"keyboard": buttons, "one_time_keyboard": False, "resize_keyboard": True}
            self.sender.sendMessage(emojize("Cool! Wouldn't it be convenient if the players who want to join could contact you? :mailbox_with_mail: \nHelp us help you by sending us your contact! :hearts:", use_aliases= True))
            self.count+=1

        elif(self.count==14):
            FindersKeepers.contact_buildTeam=msg['text']
            self.sender.sendMessage(emojize("It would be really great if you could pass us your NTU email id so that we can inform whenever someone wanna join your team :mahjong: :smiley:", use_aliases= True))
            self.count+=1

        elif(self.count==15):
            FindersKeepers.email_buildTeam=msg['text']
            if ("@e.ntu.edu.sg" not in msg['text']):
                self.sender.sendMessage("Please input the CORRECT email id again!!!")
                self.count=15
            else:
                self.sender.sendMessage("Umm...what is the minimum players you are looking for?")
                self.count+=1

        elif (self.count==16):
            FindersKeepers.pmin_buildTeam=msg['text']
            self.sender.sendMessage("Ohkay...so what about maximum?")
            self.count+=1

        elif (self.count==17):
            FindersKeepers.pmax_buildTeam= msg['text']         
            self.sender.sendMessage("Alright then I guess we are done here")
            self.sender.sendMessage(emojize("As I said easy peasy lemon squeezy :lemon: ....We guys will inform you with the updates! :stuck_out_tongue_closed_eyes:", use_aliases= True))
            keyboard8= ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                            [KeyboardButton(text="Notify me when players found!")]])
            self.sender.sendMessage(emojize("Well "+FindersKeepers.name_buildTeam+ "! Thanks a ton for your cooperation! :muscle:", use_aliases= True), reply_markup= keyboard8)
            self.count+=1

        elif (self.count==18):
            self.sender.sendMessage("Sure!")
            self.sender.sendMessage(emojize("You will be notified once the minimum number of players have joined your team :information_desk_person:", use_aliases= True))
            self.sender.sendMessage(emojize("To make it convenient, the team will only be visible if the number of players is lesser than the maximum. :smile_cat: :dog:", use_aliases= True))
            self.sender.sendMessage("Press /main to explore more!")
            FindersKeepers.lid=FindersKeepers.lid+1
            self.add_data_TeamSetup(FindersKeepers.lid, chat_id, FindersKeepers.matric_buildTeam, FindersKeepers.email_buildTeam, FindersKeepers.contact_buildTeam, FindersKeepers.name_buildTeam, FindersKeepers.bd_game_check, FindersKeepers.booking_date, FindersKeepers.bd_location_check, FindersKeepers.booking_time, FindersKeepers.pmin_buildTeam, FindersKeepers.pmax_buildTeam)

        
        elif (self.count==19):
            FindersKeepers.contact_joinTeam= msg['text']
            self.sender.sendMessage(emojize("Okay so here is a list of all those players looking for players to build their team in the near future! :dolphin:", use_aliases= True))
            self.sender.sendMessage("Just Enter one of the serial number to contact the person building teams and he will be notified via e-mail!!")
            self.look_for_game_teamsetup(chat_id, FindersKeepers.bd_game_check)
            self.sender.sendMessage("If no record found just press /main to explore more options!!")
            self.count+=1

        elif (self.count==20):
            FindersKeepers.sChosen_JD= int(msg['text'])          

            con3= lite.connect("FionDB_sublime.db") #Gets data from team setup DB and uses it to add some of the data to the waitlist player DB 
            cur3=con3.cursor()
            cur3.execute("SELECT Owner, Name, DateGame, TimeGame, Venue, MatriculationNumber, SerialNumber, OrganiserEmail, OrganiserContactNumber FROM TeamSetup WHERE SerialNumber=:SerialNumber",{"SerialNumber": int(msg['text'])})
            con3.commit()
            while True:
                self.rows= cur3.fetchone()
                if self.rows== None:
                    break
                FindersKeepers.sn=FindersKeepers.sn+1     #keeps track of the serial number of the team setup DB
                self.addData_WaitlistPlayers(FindersKeepers.sn, chat_id, FindersKeepers.matric_joinTeam, FindersKeepers.contact_joinTeam, FindersKeepers.name_joinTeam, FindersKeepers.bd_game_check, FindersKeepers.sChosen_JD, self.rows[1], self.rows[2], self.rows[3], self.rows[4], self.rows[0], self.rows[5], self.rows[6], self.rows[7], self.rows[8])
                FindersKeepers.captured_sn_joinTeam= FindersKeepers.sn #to know where the waitlisted player is added in the waitlist players DB

            self.sender.sendMessage(emojize("Wanna notify the team in charge? :eyes:", use_aliases = True))
            keyboard9= ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                            [KeyboardButton(text="Sure!")]])
            self.sender.sendMessage("Press sure to continue!", reply_markup= keyboard9)
            self.count+=1

        elif (self.count==21):
            con4= lite.connect("FionDB_sublime.db") 
            with con4:
                cur4= con4.cursor()
                cur4.execute("SELECT Owner, SerialNumber, Name, PlayerContactNumber, MatriculationNumber, ChatIDPlayerContacted, MatricNumberPlayerContacted, SerialNumberPlayerContacted, EmailPlayerContacted, PhoneNumberPlayerContacted FROM WaitlistPlayers WHERE SerialNumber=:SerialNumber",{"SerialNumber":FindersKeepers.captured_sn_joinTeam})
                con4.commit()
                self.rows= cur4.fetchone()
                if self.rows== None:  
                    self.count=1                  
                    

                if self.rows[4]!= self.rows[6]:
                    self.send_notification_email(self.rows[8])
                    self.tstrength_update_TeamSetup(self.rows[0], self.rows[7], self.rows[5])
                    self.team_update_TeamSetup(self.rows[7], self.rows[5])   
                    bot.sendMessage(self.rows[5], emojize("Congrats dude :smiling_face_with_sunglasses: ...\nThis player has joined your team!", use_aliases = True))
                    bot.sendMessage(self.rows[5], emojize(("%s %s %s %s" % ("Serial Number: " + str(self.rows[1]), "\nName: " + str(self.rows[2]), "\nContact Number: " + str(self.rows[3]), "\nMatriculation Number: "+ str(self.rows[4])))))
                    bot.sendMessage(self.rows[5], "Press /main to explore more!")
                    
                    
                elif self.rows[4]== self.rows[6]:         #Checks if both the matric numbers of the player in charge and the player making the request is the same so that the player does not accidentally add into his own team 
                    bot.sendMessage(self.rows[0], emojize("Well...Don't joke...you cant join your own team! \nAnd matric number is unique for every individual! :unamused_face:", use_aliases = True))
                    bot.sendMessage(self.rows[0], "Invalid Request...Press /main to restart!")
                    bot.sendMessage(self.rows[0], "Press /main to explore more!")
                    
                elif self.rows== None:
                    bot.sendMessage(chat_id, "No records found")
                    bot.sendMessage(self.rows[0], "Press /main to explore more!")

            self.count=1        


#CONNECTING TO THE DATABASE
con1= lite.connect("FionDB_sublime.db")
with con1:
    cur1= con1.cursor()
    cur1.execute ("DROP TABLE IF EXISTS TeamSetup")
    cur1.execute("CREATE TABLE TeamSetup(SerialNumber INTEGER, Owner INTEGER, MatriculationNumber INTEGER, OrganiserEmail VARCHAR, OrganiserContactNumber VARCHAR, Name TEXT, NameGame TEXT, DateGame TEXT, Venue TEXT, TimeGame TEXT, PlayerMin INTEGER, PlayerMax INTEGER, TeamStrength INTEGER, Open BOOLEAN );")
print ("Creating Database....")

con2= lite.connect("FionDB_sublime.db")
with con2:
    cur2= con2.cursor()
    cur2.execute ("DROP TABLE IF EXISTS WaitlistPlayers")
    cur2.execute("CREATE TABLE WaitlistPlayers(SerialNumber INTEGER, Owner INTEGER, MatriculationNumber INTEGER, PlayerContactNumber VARCHAR, Name TEXT, NameGame TEXT, SerialNumberChosen INTEGER, PlayerNameContacted TEXT, DateGame TEXT, TimeGame TEXT, VENUE TEXT, ChatIDPlayerContacted INTEGER, MatricNumberPlayerContacted INTEGER, SerialNumberPlayerContacted INTEGER, EmailPlayerContacted TEXT, PhoneNumberPlayerContacted TEXT );")
print ("Creating Waitlist Database....")


TOKEN = "464860783:AAFS5o9JDx5kZNjhOiwgnaGa0gd1YA8Ad74"   # add token once new bot made

bot = telepot.DelegatorBot(TOKEN, [
pave_event_space()(
        per_chat_id(), create_open, FindersKeepers,timeout=10000000),
])

bot.message_loop(run_forever='Listening ...')

            
















