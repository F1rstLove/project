import tkinter
import tkinter.font
import tkinter.messagebox
import random
import threading
import time
import json
import os

# 파일 경로 설정
DATA_FILE = "user_data.json"

# 초기 설정
window = tkinter.Tk()
window.title('Create Habits')
window.geometry('1200x700+50+50')

# 기본 세팅
title_font = tkinter.font.Font(family='휴먼매직체', size=13)

# 사용자 상태 초기화 함수
def initialize_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    else:
        return {
            "Users_mission": [
                "아침 운동하기",
                "독서 30분 하기",
                "일기 쓰기",
                "물 2리터 마시기",
                "영어 단어 20개 외우기",
                "명상 10분 하기",
                "집안 정리하기",
                "저녁 산책하기",
                "호돌선생님 수업 잘 듣기"
            ],
            "Users_status": {
                "level": 1,
                "exp": 0
            }
        }

# 데이터 저장 함수
def save_data():
    data = {
        "Users_mission": Users_mission,
        "Users_status": Users_status
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 초기 데이터 로드
data = initialize_data()
Users_mission = data["Users_mission"]
Users_status = data["Users_status"]

# 레벨업 기준 경험치
LEVEL_UP_EXP = 100

# 경험치 증가 및 레벨업 확인 함수
def gain_exp(amount):
    Users_status["exp"] += amount
    if Users_status["exp"] >= LEVEL_UP_EXP:
        Users_status["exp"] -= LEVEL_UP_EXP
        Users_status["level"] += 1
        tkinter.messagebox.showinfo("레벨 업!", f"레벨 업! 현재 레벨: {Users_status['level']}")
    save_data()
    update_status_label()

# '계획 추가' 버튼 클릭 시 동작 함수 정의
def add_plan():
    content = plan_content.get("1.0", tkinter.END).strip()  # 텍스트 박스의 내용을 가져옴
    if content:  # 내용이 있는 경우에만 추가
        Users_mission.append(content)
        Users_mission_listbox.insert(tkinter.END, content)  # Listbox에 내용 추가
        plan_content.delete("1.0", tkinter.END)  # 텍스트 박스를 비움
        print(f"현재 미션: {Users_mission}")  # 현재 미션 리스트를 콘솔에 출력
        save_data()

# '계획 삭제' 버튼 클릭 시 동작 함수 정의
def delete_plan():
    selected_indices = Users_mission_listbox.curselection()  # 선택된 항목의 인덱스 가져옴
    for index in selected_indices[::-1]:  # 뒤에서부터 삭제
        Users_mission_listbox.delete(index)
        del Users_mission[index]
    save_data()

# '계획 실천 자가체크' 버튼 클릭 시 동작 함수 정의
def check_plan():
    check_window = tkinter.Toplevel(window)
    check_window.title('계획 실천 자가체크')
    check_window.geometry('600x400+100+100')

    checkboxes = []

    for mission in Users_mission:
        var = tkinter.BooleanVar()
        checkbox = tkinter.Checkbutton(check_window, text=mission, variable=var)
        checkbox.pack(anchor='w')
        checkboxes.append(var)

    def submit_checks():
        completed_missions = []
        for i, var in enumerate(checkboxes):
            if var.get():
                completed_missions.append(Users_mission[i])
        
        if completed_missions:
            for mission in completed_missions:
                index = Users_mission.index(mission)
                Users_mission_listbox.delete(index)
                Users_mission.remove(mission)
            message = "\n".join([f"'{mission}' 미션 완료!" for mission in completed_missions])
            tkinter.messagebox.showinfo("미션 완료", message)
            gain_exp(10 * len(completed_missions))  # 미션 하나당 경험치 10 획득
        else:
            tkinter.messagebox.showinfo("미션 완료", "완료된 미션이 없습니다.")

        save_data()

    submit_button = tkinter.Button(check_window, text='제출', command=submit_checks)
    submit_button.pack()

# 매일 자정에 랜덤 미션 설정
def set_random_mission():
    while True:
        now = time.localtime()
        if now.tm_hour == 0 and now.tm_min == 0:  # 자정 체크
            today_mission_listbox.delete(0, tkinter.END)
            random_mission = random.choice(Users_mission)
            today_mission_listbox.insert(tkinter.END, random_mission)
            time.sleep(60)  # 1분 동안 대기하여 자정 반복 실행 방지
        time.sleep(1)  # 1초 대기 후 시간 다시 체크

# 새로운 스레드에서 자정 체크 실행
threading.Thread(target=set_random_mission, daemon=True).start()

# today_mission
today_mission_listbox = tkinter.Listbox(window, width=138, height=9)

# Listbox 생성
Users_mission_listbox = tkinter.Listbox(window, width=138, height=32)

# 미리 정의된 미션들 today_mission_listbox에 추가
for mission in Users_mission:
    today_mission_listbox.insert(tkinter.END, mission)

plan_content = tkinter.Text(window, width=26, height=6)

plan_add = tkinter.Button(window, text='계획 추가', width=20, font=title_font, command=add_plan)

plan_del = tkinter.Button(window, text='계획 삭제', width=20, font=title_font, command=delete_plan)

plan_check = tkinter.Button(window, text='계획 실천 자가체크', width=20, font=title_font, command=check_plan)

# 사용자 상태 표시 라벨
status_label = tkinter.Label(window, text=f"레벨: {Users_status['level']} | 경험치: {Users_status['exp']}/{LEVEL_UP_EXP}")
status_label.place(x=1000, y=200)

today_mission_listbox.place(x=10, y=10)
Users_mission_listbox.place(x=10, y=175)
plan_content.place(x=1000, y=10)
plan_add.place(x=1000, y=100)
plan_del.place(x=1000, y=135)
plan_check.place(x=1000, y=170)

# 경험치 및 레벨 업데이트 함수
def update_status_label():
    status_label.config(text=f"레벨: {Users_status['level']} | 경험치: {Users_status['exp']}/{LEVEL_UP_EXP}")
    window.after(1000, update_status_label)

# 상태 라벨 업데이트 시작
update_status_label()

window.mainloop()