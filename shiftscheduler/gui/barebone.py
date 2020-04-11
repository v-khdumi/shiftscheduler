
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import tkcalendar as tkc 

from shiftscheduler.data_types import data_types
from shiftscheduler.excel import output as excel_output
from shiftscheduler.gui import util


# TkInter frame for getting barebone Excel file
class BareboneExcelFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        util.SetGridWeights(self, column_weights=(1, 2))

        self.createLeftFrame()
        self.createRightFrame()

    # Create left side of the frame
    def createLeftFrame(self):
        left_frame = tk.Frame(self)
        util.SetGrid(left_frame, 0, 0)
        util.SetGridWeights(left_frame, row_weights=(1, 9))  

        label = tk.Label(left_frame, text='간호사 이름을 입력하세요')
        util.SetGrid(label, 0, 0) #, sticky=tk.W)  # For some reason, tk.NSEW does not work
        self.names_text_area = tk.Text(left_frame)
        util.SetGrid(self.names_text_area, 1, 0)

    # Create right side of the frame
    def createRightFrame(self):
        right_frame = tk.Frame(self)
        util.SetGrid(right_frame, 0, 1)
        util.SetGridWeights(right_frame, row_weights=(1, 1, 1, 1, 1, 5, 1))
        
        # Start date widgets
        start_date_label = tk.Label(right_frame, text='시작날짜')
        util.SetGrid(start_date_label, 0, 0)
        self.start_cal = tkc.DateEntry(right_frame, year=2020, month=5, day=1)
        util.SetGrid(self.start_cal, 1, 0)

        # End date widgets
        end_date_label = tk.Label(right_frame, text='끝날짜')
        util.SetGrid(end_date_label, 2, 0)
        self.end_cal = tkc.DateEntry(right_frame, year=2020, month=5, day=31)
        util.SetGrid(self.end_cal, 3, 0)

        # Instruction label
        instruction = """
        사용 방법
        1.간호사 이름을 한줄씩 적어주세요
        2.일정의 시작-끝 날짜를 지정합니다
        3."엑셀 파일 받기"를 눌러 파일을 저장합니다
        4."날짜별 설정" 시트에서 필요 인원을 입력합니다
        5."간호사별 설정"에서 근무일수를 입력합니다
        6."일정표"에서 기존에 정해진 일정을 입력합니다
        7."새 일정" 탭에서 다음 단계를 진행해 주세요
        """
        instruction_label = tk.Label(right_frame, text=instruction, justify=tk.LEFT)
        util.SetGrid(instruction_label,5, 0)

        # Download button
        def callback_func():
            error = self.validateValues()
            if error:
                messagebox.showerror(message=error)
                return

            filepath = filedialog.asksaveasfilename(title='기본 엑셀 파일 저장하기')
            if filepath:
                self.CreateExcel(filepath)
            
        download_button = tk.Button(right_frame, text='기본 엑셀 파일 다운 받기', command=callback_func)
        util.SetGrid(download_button, 6, 0)

    # Get values from GUI
    def getValues(self):
        text_area_value = self.names_text_area.get('1.0', 'end').strip()
        names = text_area_value.split('\n')
        # Filter out all empty names
        names = [name.strip() for name in names if name and not name.isspace()]
        start_date = self.start_cal.get_date()
        end_date = self.end_cal.get_date()
        return (names, start_date, end_date)

    def validateValues(self):
        names, start_date, end_date = self.getValues()

        # No name input
        if not names:
            return '이름을 입력해 주세요'
        
        if start_date > end_date:
            return '일정 시작날짜가 끝 날짜 후입니다'

        # Check for duplicate names
        nameset = set()
        duplicates = set()
        for name in names:
            if name not in nameset:
                nameset.add(name)
            else:
                duplicates.add(name)
        
        if duplicates:
            return '중복되는 이름이 있습니다: %s' % ','.join(sorted(duplicates))

        return ''  # No error

    def CreateExcel(self, filepath):
        names, start_date, end_date = self.getValues()

        sw_config = data_types.SoftwareConfig(start_date=start_date, end_date=end_date, num_person=len(names))
        person_configs = [
            data_types.PersonConfig(name, None, None, None, None) for name in names]
        barebone_schedule = data_types.TotalSchedule(
            software_config=sw_config, person_configs=person_configs, date_configs=[],
            assignment_dict=dict())
        excel_output.FromTotalSchedule(barebone_schedule, filepath)
        