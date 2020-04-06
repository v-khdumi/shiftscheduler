import tkinter as tk


class NewScheduleFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.grid_columnconfigure(0, weight=1, uniform='group1')
        self.grid_columnconfigure(1, weight=2, uniform='group1')
        self.grid_rowconfigure(0, weight=1, uniform='group2')

        self.createLeftFrame()
        self.createRightFrame()

    def createLeftFrame(self):
        left_frame = tk.Frame(self)
        left_frame.grid_columnconfigure(0, weight=1, uniform='group1')
        left_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

        weights = (1, 1, 1, 1, 1, 5, 1, 2, 1)
        for i, w in enumerate(weights):
            left_frame.grid_rowconfigure(i, weight=w, uniform='group1')
       
        # Button to open partially filled barebone filed
        open_file_button = tk.Button(left_frame, text='기본 엑셀 파일 불러오기')
        open_file_button.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
        # Opened file name. Empty label if no file is loaded
        open_file_label = tk.Label(left_frame, text='현재 파일: sample.xlsx')
        open_file_label.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

        # Start date, end date of new schedule
        start_date_label = tk.Label(left_frame, text='일정 시작 날짜: 2020년 5월 1일')
        start_date_label.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=5)
        end_date_label = tk.Label(left_frame, text='일정 종료 날짜: 2020년 5월 31일')
        end_date_label.grid(row=3, column=0, sticky=tk.NSEW, padx=5, pady=5)

        # How long should the solver run?
        max_time_frame = tk.Frame(left_frame)
        max_time_frame.grid_columnconfigure(0, weight=4, uniform='group1')
        max_time_frame.grid_columnconfigure(1, weight=1, uniform='group1')
        max_time_frame.grid_columnconfigure(2, weight=1, uniform='group1')
        max_time_frame.grid(row=6, column=0, sticky=tk.NSEW, padx=5, pady=5)

        max_time_label1 = tk.Label(max_time_frame, text='최대 검색 시간')
        max_time_label1.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

        spinbox = tk.Spinbox(max_time_frame, from_=1, to=30)
        spinbox.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)

        max_time_label2 = tk.Label(max_time_frame, text='분')
        max_time_label2.grid(row=0, column=2, sticky=tk.NSEW, padx=5, pady=5)

        # Notice that the solver will stop after the specific time
        max_time_info_label = tk.Label(left_frame, text='시간 내로 조건에 맞는 일정을 찾을 수 없을 시\n작업을 중지합니다')
        max_time_info_label.grid(row=7, column=0, sticky=tk.NSEW, padx=5, pady=5)

        # Start button. Click will validate the input Excel and run the solver
        submit_button = tk.Button(left_frame, text='시작')
        submit_button.grid(row=8, column=0, sticky=tk.NSEW, padx=5, pady=5)


    def createRightFrame(self):
        right_frame = tk.Frame(self)
        right_frame.grid_rowconfigure(0, weight=1, uniform='group1')
        right_frame.grid_rowconfigure(1, weight=9, uniform='group1')
        right_frame.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=5)

        # Right side of the frame only displays status (of validation and solver run)
        label = tk.Label(right_frame, text='진행상황')
        label.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
        text_area = tk.Text(right_frame, state=tk.DISABLED)
        text_area.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)
