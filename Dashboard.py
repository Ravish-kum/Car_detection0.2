import tkinter as tk
import customtkinter
from PIL import Image
import tkvideo
from crashdetection_2 import Detections
detections = Detections()

class CrashDetection(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("CrashDetection")
        self.after(0, lambda:self.state('zoomed'))
        self.iconbitmap('credential_images/logo.ico')
        self.frames = {}
        self.player =None
        '''
        sturcture :
        mainframe
            ---- headerframe
                ----  logolabel
                ----  headlabel

            ---- scrollframe
                ----first_page_scroll

                    ---- definelabel (Crash Detection Software)
                    ---- contentlabel (project one line description)
                    
                    ---- testvideolabel
                    ---- contentvideolabel
                    ---- video_options
                    
                    ---- testimagelabel
                    ---- contentimagelabel
                    ---- image_options

                    ---- aboutlabel
                    ---- objectivelabelcontent

                ---- second_page_scroll

                    ---- heading label
                    ---- data label

        '''
        
        self.mainframe = customtkinter.CTkFrame(self)
        self.mainframe.pack(side=customtkinter.LEFT, fill=customtkinter.BOTH, expand=True)

#======================================================================================================================================================================

        self.headerframe = customtkinter.CTkFrame(self.mainframe, height=500, fg_color="#0C1B33",)
        self.headerframe.pack(fill=customtkinter.X)

        logo_image = customtkinter.CTkImage(light_image=Image.open("credential_images\logo.jpeg"),size=(50,50))
        logo_label = customtkinter.CTkLabel(self.headerframe, text="", image=logo_image)
        logo_label.grid(row=0, column=0, padx=(50,20))

        self.headlabel = customtkinter.CTkLabel(self.headerframe,
                                            text="Crash Detection",
                                            text_color="white",
                                            height=100,
                                            font=("Arial", 40, 'bold'))
        self.headlabel.grid(row=0, column =1)

#=======================================================================================================================================================================
        for scrollfame_num in range(1,3):
            self.create_scrollframe(scrollfame_num)
        self.show_content(1)
    
    def show_content(self, scrollnum):
        for page_frame in self.frames.values():
            page_frame.pack_forget()
        self.frames[scrollnum].pack(fill=customtkinter.X)

    def create_scrollframe(self, scrollfame_num):
        scrollframe = customtkinter.CTkScrollableFrame(self.mainframe,
                                                        height=3000,
                                                        fg_color='#373b41')
        if scrollfame_num == 1:
            self.first_scroll_testing_page(scrollframe)
        elif scrollfame_num == 2:
            self.second_scroll_details_page(scrollframe)
        
        self.frames[scrollfame_num] = scrollframe

    def first_scroll_testing_page(self, scrollframe):
        self.definelabel = customtkinter.CTkLabel(scrollframe,
                                            text="Crash Detection Software",
                                            text_color="white",
                                            height=50,
                                            font=("impact",30, 'bold'))
        self.definelabel.pack(padx=(200,200),pady=(10,1) ,anchor="w")

        project_description = '''
            A Crash Detection system which harnesses AI technology to identify accidents\n and promptly notify the relevent authorities.
            '''
        self.contentlabel = customtkinter.CTkLabel(scrollframe,
                                            text=project_description,
                                            text_color="#d0f0c2",
                                            height=50,
                                            font=("Arial",21,))
        self.contentlabel.pack(padx=(200,200),pady=(0,20) ,anchor="center")

        self.testvideolabel = customtkinter.CTkLabel(scrollframe,
                                            text="Test By Video",
                                            text_color="white",
                                            height=50,
                                            font=("Impact",30, 'bold'))
        self.testvideolabel.pack(padx=(200,200), pady=(10,1) ,anchor="w")

        testing_video_description = '''
            Select any video for detection and observe the performance of our model.
            '''
        self.contentvideolabel = customtkinter.CTkLabel(scrollframe,
                                            text=testing_video_description,
                                            text_color="#c0dbdb",
                                            height=50,
                                            font=("Arial",20,))
        self.contentvideolabel.pack(padx=(135,200), pady=(0,1),anchor="w")
        
        def videodisplay(choice):
            ''' function for selected vedio display '''

            if choice == 'None':
                if self.player:
                    self.player.stop()
                    self.player = None
                    self.videolabel.pack_forget()
                return
            try:
                # Destroy the previous video player instance if it exists
                if self.player:
                    self.player.stop()
                    self.player = None
                    
                self.videolabel.configure(width=1280, height=720,)
                self.player = tkvideo.tkvideo(rf"videos/{choice}.mp4", self.videolabel, loop = 1, size = (1280,720))

            except FileNotFoundError:
                return
            self.player.play()

        self.actionframe_video = customtkinter.CTkFrame(scrollframe, height=45, fg_color='#373b41')
        self.actionframe_video.pack(pady=(0,30))

        
        def action_video():
            video_name = self.video_options.get()
            print(video_name)
            if video_name is not None or video_name != 'None':
                detections.call_for_video(video_name)

        video_options= ['None','video1','video2','video3','video4']
        self.video_options = customtkinter.CTkOptionMenu(self.actionframe_video,
                                                        values=video_options,
                                                        height=40,
                                                        width=400,
                                                        fg_color='white',
                                                        text_color='black',
                                                        font=("",18),
                                                        dropdown_font=("",18),
                                                        command=videodisplay,
                                                        anchor='w',
                                                        button_color='#265e91',
                                                        corner_radius=50)
        
        self.video_options.grid(row=0, column=0, padx=(0,40))

        video_submit_button = customtkinter.CTkButton(self.actionframe_video,
                                                      text="Submit", 
                                                      font=("",15),
                                                      height=40,
                                                      width=60,
                                                      corner_radius=40,
                                                      fg_color='#265e91',
                                                      command=action_video)
        video_submit_button.grid(row=0, column=3)

        self.videolabel = customtkinter.CTkLabel(scrollframe, text='', height=0, width=0)
        self.videolabel.pack(padx=(200,200), pady=(1,1),anchor="center")

        self.testimglabel = customtkinter.CTkLabel(scrollframe,
                                            text="Test By Image",
                                            text_color="white",
                                            height=50,
                                            font=("Impact",30, 'bold'),
                                            anchor='center')
        self.testimglabel.pack(padx=(200,200),pady=(1,1),anchor="w")

        testing_image_description = '''
            Select any image for detection and observe the performance of our model.
            '''
        self.contentimagelabel = customtkinter.CTkLabel(scrollframe,
                                            text=testing_image_description,
                                            text_color="#c0dbdb",
                                            height=50,
                                            font=("Arial",20,))
        self.contentimagelabel.pack(padx=(135,200), pady=(0,1),anchor="w")

        def imagedisplay(choice):
            ''' function for selected image display '''
            if choice == 'None':
                imagelabel.pack_forget()
                return            
            try:
                image = customtkinter.CTkImage(light_image=Image.open(rf"images\{choice}.jpg"),size=(500,500))
            except FileNotFoundError:
                return
            imagelabel.configure(image=image,width=500, height=500,)

        self.actionframe_image = customtkinter.CTkFrame(scrollframe, height=45, fg_color='#373b41')
        self.actionframe_image.pack(pady=(0,30))

        
        def action_image():
            image_name = self.imageoptions.get()
            if image_name is not None or image_name != 'None':
                detections.call_for_image(image_name)

        imageoptions= ['None','image1','image2','image3','image4', 'image5', 'image6', 'image7', 'image8']
        self.imageoptions = customtkinter.CTkOptionMenu(self.actionframe_image,
                                                        values=imageoptions,
                                                        height=40,
                                                        width=400,
                                                        fg_color='white',
                                                        text_color='black',
                                                        font=("",18),
                                                        dropdown_font=("",18),
                                                        button_color='#265e91',
                                                        command=imagedisplay,
                                                        anchor='w',
                                                        corner_radius=50)
        self.imageoptions.grid(row=0, column=0, padx=(0,40))

        image_submit_button = customtkinter.CTkButton(self.actionframe_image,
                                                      text="Submit",
                                                      height=40,
                                                      width=60,
                                                      font=("",15),
                                                      corner_radius=40,
                                                      fg_color='#265e91',
                                                      command=action_image)
        image_submit_button.grid(row=0, column=3)

        imagelabel = customtkinter.CTkLabel(scrollframe,
                                            text="")
        imagelabel.pack(padx=(200,200), pady=(1,1),anchor="center")

        self.aboutlabel = customtkinter.CTkLabel(scrollframe,
                                            text="Problem Solved by Crash Detection Software",
                                            text_color="white",
                                            height=50,
                                            font=("impact",30, 'bold'))
        self.aboutlabel.pack(padx=(200,200), pady=(1,1),anchor="w")

        about_desc = '''
            India is grappling with a significant road safety crisis, with approximately 1.5 lakh people losing their lives in road accidents
            every year. One of the pressing issues contributing to this crisis is the delayed reporting of accidents, often resulting from a
            lack of immediate witnesses. To confront this problem, we propose the development of a crash detection software.\n
            Key Features:\n
            1. Crash Detection: This feature identifies instances of collisions involving multiple vehicles.\n
            2. Speeding Detection: It recognizes when a vehicle is exceeding the legal speed limit.\n
            3. Wrong-Side Detection: The system can determine if a vehicle is traveling on the wrong side of the road.\n
            4. Traffic Congestion Detection: It can discern heavy traffic conditions on a road.\n
            '''
        self.objectivecontentlabel = customtkinter.CTkLabel(scrollframe,
                                            text=about_desc,
                                            text_color="#c0dbdb",
                                            height=50,
                                            width=600,
                                            font=("Arial",20),
                                            justify='left',
                                            )
        self.objectivecontentlabel.pack(padx=(135,200), pady=(0,1),anchor="w")

        def training_details():
            self.show_content(2)

        button_details = tk.Button(scrollframe, text="Know More",
                                    command=training_details, 
                                    bg='#0C1B33', height=2,
                                    width=15,
                                    fg='white',
                                    font=("",10),
                                    )
        button_details.pack()

#========================================================================================================================================================================================================

    def second_scroll_details_page(self, scrollframe):
        def back():
            self.show_content(1)

        heading_label = customtkinter.CTkLabel(scrollframe, text="Crash Detection AI Model",
                                               font=("Helvetica", 30, "bold"),
                                               wraplength=800, 
                                               text_color="#daa875",
                                               height=50,
                                               width=600,
                                               justify='center',)
        heading_label.pack(pady=50)

        # Description
        description_text = "Precision Graph Image: \n\nThis image visualizes the precision metric of the Crash Detection AI model. Precision measures the accuracy of positive predictions, indicating the proportion of correctly predicted crash events among all predicted crash events."
        description_label = customtkinter.CTkLabel(scrollframe, text=description_text,
                                                    wraplength=800, 
                                                    text_color="#c0dbdb",
                                                    height=50,
                                                    width=600,
                                                    font=("Arial",20),
                                                    justify='left',)
        description_label.pack(pady=10)

        # Precision Image
        precision_image = customtkinter.CTkImage(light_image=Image.open("credential_images\P_curve.png"),size=(500,400))
        precision_label = customtkinter.CTkLabel(scrollframe, text ="", image=precision_image)
        precision_label.pack(pady=50)

        # Description
        description_text2 = "Recall Graph Image: \n\nThis image illustrates the recall metric of the Crash Detection AI model. Recall measures the model's ability to identify all relevant crash events, showing the proportion of correctly predicted crash events among all actual crash events."
        description_label2 = customtkinter.CTkLabel(scrollframe, text=description_text2,
                                                    wraplength=800,
                                                    text_color="#c0dbdb",
                                                    height=50,
                                                    width=600,
                                                    font=("Arial",20),
                                                    justify='left',)
        description_label2.pack(pady=10)
        # Recall Image

        recall_image = customtkinter.CTkImage(light_image=Image.open("credential_images\R_curve.png"), size=(500,400))
        recall_label = customtkinter.CTkLabel(scrollframe, image=recall_image, text="")
        recall_label.pack(pady=50)

         # Description
        description_text3 = "Precision-Recall (P-R) Graph Image: \n\nThis image combines both precision and recall metrics in a single graph, showcasing the trade-off between precision and recall as model thresholds vary. It helps in understanding the model's performance across different thresholds for making predictions." 
        description_label3 = customtkinter.CTkLabel(scrollframe, text=description_text3,
                                                    wraplength=800,
                                                    text_color="#c0dbdb",
                                                    height=50,
                                                    width=600,
                                                    font=("Arial",20),
                                                    justify='left',)
        description_label3.pack(pady=10)
        # Precision-Recall Image
        pr_image = customtkinter.CTkImage(light_image=Image.open("credential_images\PR_curve.png"),size=(500,400))
        pr_label = customtkinter.CTkLabel(scrollframe,  text='',image=pr_image,)
        pr_label.pack(pady=10)

        button_back = tk.Button(scrollframe, text="back",
                                        command=back,
                                        bg='#0C1B33',
                                        height=2,
                                        width=10,
                                        fg='white',
                                        font=("",10),
                                        anchor=tk.CENTER)
        button_back.pack()

app = CrashDetection()
app.mainloop()