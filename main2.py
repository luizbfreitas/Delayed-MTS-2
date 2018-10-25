#by Luiz Freitas in 10/17/2018
#Delayed MTS - version 2.0

import tkinter as tk

import tkinter.ttk as ttk

import time

import random

import csv

import os


class Application(tk.Frame):
    # main application window
    def __init__(self, master=None):
        super().__init__(master)
        # set the attributes of the main window
        self.grid(column=0, row=0, sticky=('N', 'W', 'E', 'S'), padx=20, 
        pady=20)
        self.cicle = 0 #variable that will control the stimuli of the cicle
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        
        self.create_widgets()

    def create_widgets(self):
        # creates set the widgets in the main window
        self.start = tk.Button(self, fg="green")
        self.start["text"] = "Start \nSession"
        self.start["command"] = self.define_stimuli
        self.start["height"] = 4
        self.start["width"] = 8
        self.start.grid(column=2, row=10, sticky=('E', 'S'))

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.grid(column=1, row=10, sticky=('W', 'S'))
        
        self.version = tk.Label(self, text='Version 2.0')
        self.version.grid(column=2, row=1, sticky=('N', 'E'), pady=5)
        
        self.pick_part = tk.Label(self, text='Participant:')
        self.pick_part.grid(column=1, row=2, sticky=('W'))
        
        self.part_option = ttk.Combobox(self, state='readonly')
        self.parts = 'participants/'
        self.part_list = [item for item in os.listdir(self.parts) if os.path.isdir(os.path.join(self.parts, item))]
        self.part_option["values"] = self.part_list
        self.part_option.grid(column=2, row=2, sticky=('W'), padx=10)
        
        self.delay = tk.Label(self, text='Choose a delay:')
        self.delay.grid(column=1, row=4, sticky='W')
        
        self.var = tk.IntVar(self)
        
        self.delay0 = tk.Radiobutton(self, value=0, variable=self.var)
        self.delay0["text"] = "0s Delay"
        self.delay0.grid(column=1, row=5, sticky='W')
        
        self.delay2 = tk.Radiobutton(self, value=2000, variable=self.var)
        self.delay2["text"] = "2s Delay"
        self.delay2.grid(column=1, row=6, sticky='W')
        
        self.delay5 = tk.Radiobutton(self, value=5000, variable=self.var)
        self.delay5["text"] = "5s Delay"
        self.delay5.grid(column=1, row=7, sticky='W')
        
        self.delay10 = tk.Radiobutton(self, value=10000, variable=self.var)
        self.delay10["text"] = "10s Delay"
        self.delay10.grid(column=1, row=8, sticky='W')
        
        self.delay20 = tk.Radiobutton(self, value=20000, variable=self.var)
        self.delay20["text"] = "20s Delay"
        self.delay20.grid(column=1, row=9, sticky='W')
        
        self.pick_img = tk.Label(self, text='Choose a category:')
        self.pick_img.grid(column=1, row=3, sticky=('W'))
        
        self.img_option = ttk.Combobox(self, state='readonly')
        self.img = 'images/'
        self.img_list = [item for item in os.listdir(self.img) if os.path.isdir(os.path.join(self.img, item))]
        self.img_option["values"] = self.img_list
        self.img_option.current(0) #defines position 0 as default
        self.img_option.grid(column=2, row=3, sticky=('W'), padx=10, pady=5)

    #def part_hist(self):

    def define_stimuli(self):
        
        #leads the app to the right image folder
        self.img_path = self.img_option.get()
        self.part_path = self.part_option.get()
        print(self.img_path)
        self.path = "images/" + self.img_path + "/"
        self.timedate = time.strftime("%c")
        self.log_list = []
        
        #randomizes the trials in data.csv
        self.list1 = os.listdir(self.path)
        print(self.list1)
        
        with open('data.csv','w', newline='')as self.csvfile:
            self.csv_writer = csv.writer(self.csvfile, delimiter=";")
            self.csv_writer.writerow(["Participant"] + [self.part_path] + [str(self.timedate)])
            self.csv_writer.writerow(["Trial", "Sample", "Comp1", "Comp2"])
            self.countdown_items = 20
            self.trial_num = 1
            while self.countdown_items > 0:
                self.sample_item = random.choice(self.list1)
                self.dice = random.randint(0, 100)
                if self.dice <= 50:
                    self.comp1_item = self.sample_item
                    self.comp2_item = random.choice(self.list1)
                else:
                    self.comp1_item = random.choice(self.list1)
                    self.comp2_item = self.sample_item
                if self.comp1_item != self.comp2_item:
                    self.countdown_items = self.countdown_items - 1
                    self.csv_writer.writerow([self.trial_num] + 
                    [self.sample_item] + 
                    [self.comp1_item] +
                    [self.comp2_item])
                    
                    self.trial_num = self.trial_num + 1
                else: continue
        
        #building a list of trials from a csv file
        self.input_file = csv.reader(open("data.csv"), delimiter =';')
        self.all_trials =[]
        
        for row in self.input_file: #creates a list with all trials
            if row[0] == 'Participant': continue
            if row[0] == 'Trial': continue
            else:
                self.trial = {
                'trial': row[0],
                'sample' : row[1],
                'comp1' : row[2],
                'comp2' : row[3],
                }
                self.all_trials.append(self.trial)
        self.count_down_trials = len(self.all_trials) #number of trials based on number of rows in csv file
        self.trial_number = 0
        self.current_trial = self.all_trials[self.trial_number] #preparation for the loop
        
        self.open_window()
            
    def open_window(self):
        # creates the window the child will interact
        self.correct = 0
        self.incorrect = 0
        self.delay_option = self.var.get()
        
        self.user_window = tk.Toplevel(bg='white')
        self.user_window.attributes('-fullscreen', True)
                      
        self.frame_sample = tk.Frame(self.user_window, bg='white')
        self.frame_sample["height"] = 180
        self.frame_sample["width"] = 320
        self.frame_sample.grid(column=2, row=1, padx=60, pady = 150)
        
        self.frame_comparissons1 = tk.Frame(self.user_window, bg='white')
        self.frame_comparissons1["height"] = 180
        self.frame_comparissons1["width"] = 320
        self.frame_comparissons1.grid(column=1, row=2, padx=100)#original padx=100 - 60 for chromebook
        
        self.frame_comparissons2 = tk.Frame(self.user_window, bg='white')
        self.frame_comparissons2["height"] = 180
        self.frame_comparissons2["width"] = 320
        self.frame_comparissons2.grid(column=2, row=2, padx=100)#original padx=100 - 60 for chromebook
        
        self.frame_comparissons3 = tk.Frame(self.user_window, bg='white')
        self.frame_comparissons3["height"] = 180
        self.frame_comparissons3["width"] = 320
        self.frame_comparissons3.grid(column=3, row=2, padx=100)#original padx=100 - 60 for chromebook
        
        self.last_session_num()
        self.trial_control()

        
    def trial_control(self): #control the cicles
        
        # the first trial has to be different because it doesn't need to forget a previews trial images 
        if self.count_down_trials == len(self.all_trials):
            self.count_down_trials = self.count_down_trials - 1
            self.current_trial = self.all_trials[self.trial_number] #preparation for the loop
            print (self.current_trial) #important to know what trial is this
            #print (trial_number)
            self.trial_number = self.trial_number + 1
            self.set_stimuli()
        
        elif self.count_down_trials < len(self.all_trials) and self.count_down_trials > 0:
            
            self.bsample.grid_forget() #hides the sample for next trial
            self.bcompa1.grid_forget() #hides bcompa1 for next trial
            self.bcompa2.grid_forget() #hides bcompa2 for next trial
            
            self.count_down_trials = self.count_down_trials - 1
            self.current_trial = self.all_trials[self.trial_number] #preparation for the loop
            print (self.current_trial) #important to know what trial is this
            #print (trial_number)
            self.trial_number = self.trial_number + 1
            # sets the timeout
            self.after(5000, self.set_stimuli) #defines the timeout
            
        else:
            #include a function that adds a session for that participant in his control file
            self.write_session_num()
            self.log_writer()
            root.destroy()


    def write_session_num(self):
        self.session_file = self.part_path + '_sessions.txt'
        with open("participants/" + self.part_path + "/" + self.session_file,'r') as file_object:
                self.contents = file_object.read()
                self.contents_list = self.contents.split()
                self.session_num = int(self.contents_list[1])
        with open("participants/" + self.part_path + "/" + self.session_file,'w') as file_object:
                self.new_session_num = self.session_num + 1
                self.new_num = self.part_path + ' ' + str(self.new_session_num)
                file_object.write(self.new_num)


    def last_session_num(self):
        self.session_file = self.part_path+'_sessions.txt'
        try:
            with open("participants/" + self.part_path + "/" + self.session_file,'r') as file_object:
                self.contents = file_object.read()
                self.contents_list = self.contents.split()
                self.session_num = self.contents_list[1]
        except FileNotFoundError:
            print ('File not found. File created!')
            with open("participants/" + self.part_path + "/" + self.session_file,'w') as file_object:
                self.contents = file_object.write(self.part_path + ' 0')
                self.session_num = 0
          
            
    def log_writer(self):
        filename = self.part_path + str(self.new_session_num) + '_log.csv'
        with open("participants/" + self.part_path + "/" + filename,'w', newline='')as self.csvfile2:
            self.csv_writer2 = csv.writer(self.csvfile2, delimiter=";")
            self.csv_writer2.writerow([str(self.timedate)])
            self.csv_writer2.writerow(['Correct'] + [self.correct])
            self.csv_writer2.writerow(['Incorrect'] + [self.incorrect])
            self.csv_writer2.writerow(["Participant", "Trial", "Sample", "Position", "Choice"])
            for row in self.log_list:
                self.csv_writer2.writerow(row)
        
    def set_stimuli(self):
        
        self.bsample = tk.Button(self.frame_sample, relief='flat', bg='white')
        self.photo1 = tk.PhotoImage(file=self.path+self.current_trial['sample']) #set the image of sample
        self.bsample["command"] = self.hide_sample
        self.bsample.config(image=self.photo1, width="300", height="162")
        self.bsample.grid(column=2, row=1)
        
        self.bcompa1 = tk.Button(self.frame_comparissons1, bg='white')
        self.photo2 = tk.PhotoImage(file=self.path+self.current_trial['comp1']) #set the image of comp1
        self.bcompa1["command"] = self.mark_response_left
        self.bcompa1.config(image=self.photo2, width="300", height="162")
        
        
        self.bcompa2 = tk.Button(self.frame_comparissons3, bg='white')
        self.bcompa2["command"] = self.mark_response_right
        self.photo3 = tk.PhotoImage(file=self.path+self.current_trial['comp2']) #set the image of comp1
        self.bcompa2.config(image=self.photo3, width="300", height="162")
        
    def mark_response_left(self):
        
        if self.current_trial['sample'] == self.current_trial['comp1']:
            self.line = [self.part_path, self.trial_number, self.current_trial['sample'], "LEFT", "correct"]
            self.log_list.append(self.line)
            self.correct = self.correct + 1
         
        else:
            self.line = [self.part_path, self.trial_number, self.current_trial['sample'], "LEFT", "incorrect"]
            self.log_list.append(self.line)
            self.incorrect = self.incorrect + 1
           
        self.trial_control()
    
    def mark_response_right(self):
        
        if self.current_trial['sample'] == self.current_trial['comp2']:
            self.line = [self.part_path, self.trial_number, self.current_trial['sample'], "RIGHT", "correct"]
            self.log_list.append(self.line)
            self.correct = self.correct + 1
        else:
            self.line = [self.part_path, self.trial_number, self.current_trial['sample'], "RIGHT", "incorrect"]
            self.log_list.append(self.line)
            self.incorrect = self.incorrect + 1
            
        self.trial_control()
    
    def hide_sample(self):
        
        self.bsample.grid_forget() #hides the sample
        #print (self.delay_option)
        self.after(self.delay_option, self.show_comparissons) #show the comparissons after a presetted delay
        
    def show_comparissons(self):
        self.bcompa1.grid(column=2, row=2)
        self.bcompa2.grid(column=3, row=2)

root = tk.Tk()
app = Application(master=root)
app.master.title('Delayed MTS 2.0')
app.mainloop()
