from tkinter import *
from requests import *
window = Tk()
window.title('ChatNow本地版')
window.geometry('500x500')
message = Label(window, text="请输入你要进入的 tid:")
message.pack(pady=10)
tid_input = Entry(window)
tid_input.pack(pady=10)

def get_chatlist(tid):
    url = "https://api.infochat.top/chat.php?action=get_info&tid={}".format(tid)
    response = get(url)
    if(response.status_code == 200):
        data = response.json()
        chatlist = []
        for chat in data:
            chatlist.append({"username": chat["username"], "message": chat["message"]})
        return chatlist
    else:
        return ['ERROR: 无法获取聊天列表']
def open_new_window():
    tid = tid_input.get()
    new_window = Toplevel(window)
    new_window.title(f"ChatNow - {tid}")
    new_window.geometry('446x304')
    welcome_message = Label(new_window, text=f"欢迎进入 tid: {tid} 的聊天界面！", font=("Arial", 14))
    welcome_message.pack(pady=20)
    chat_list = get_chatlist(tid)
    chat_list_box = Listbox(new_window, height=10, width=50)
    for chat in chat_list:
        chat_list_box.insert(0, chat['message'])
    chat_list_box.pack(side=RIGHT,padx=10,pady=10,expand=True)
    username_list = Listbox(new_window, height=10, width=50)
    for chat in chat_list:
        username_list.insert(0, chat['username'])
    username_list.pack(side=LEFT,fill="x",pady=10,expand=True)
    message_input = Entry(new_window, width=50)
    message_input.pack(pady=10)
    with open("config.INFOCHAT", "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("uid="):
                uid = line.split("=")[1].strip()
            elif line.startswith("token="):
                token = line.split("=")[1].strip()
    def send_message():
        message = message_input.get()
        if message:
            url = "https://api.infochat.top/chat.php?action=send_message&tid={}&message={}&uid={}&client_id={}".format(tid, message, uid, token)
            response = get(url)
            if(response.status_code == 200):
                data = response.json()
                if data['status'] == 'ok':
                    chat_list_box.insert(0, message)
                    message_input.delete(0, END)
            else:
                print("ERROR: 发送失败")
    send_button = Button(new_window, text="发送", command=send_message)
    send_button.pack(pady=10)
    close_button = Button(new_window, text="关闭", command=new_window.destroy)
    close_button.pack(pady=10)
send_button = Button(window, text="进入", command=open_new_window)
send_button.pack(pady=20)
def new_window_setting():
    new_window = Toplevel(window)
    new_window.title(f"ChatNow - 设置")
    new_window.geometry('446x304')
    hint1 = Label(new_window, text="请输入你的uid:")
    hint1.pack(pady=10)
    uid_input = Entry(new_window)
    uid_input.pack(pady=10)
    hint2 = Label(new_window, text="请输入你的client_id:")
    hint2.pack(pady=10)
    token_input = Entry(new_window)
    token_input.pack(pady=10)
    def save_setting():
        uid = uid_input.get()
        token = token_input.get()
        with open("config.INFOCHAT", "w") as f:
            f.write(f"uid={uid}\ntoken={token}")
        new_window.destroy()
    save_button = Button(new_window, text="保存", command=save_setting)
    save_button.pack(pady=10)
setting_button = Button(window,text="设置",command=new_window_setting)
setting_button.pack(pady=10)
window.mainloop()