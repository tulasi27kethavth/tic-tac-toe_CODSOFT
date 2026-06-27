
import tkinter as tk
from tkinter import messagebox
import math

PLAYER="X"
AI="O"

board=[""]*9
buttons=[]

root=tk.Tk()
root.title("Tic Tac Toe AI")
root.geometry("420x520")
root.resizable(False,False)

status=tk.Label(root,text="Your Turn (X)",font=("Arial",16,"bold"),fg="blue")
status.pack(pady=10)

frame=tk.Frame(root)
frame.pack()

wins=[
(0,1,2),(3,4,5),(6,7,8),
(0,3,6),(1,4,7),(2,5,8),
(0,4,8),(2,4,6)
]

def winner(p):
    return any(all(board[i]==p for i in w) for w in wins)

def draw():
    return "" not in board

def minimax(maximizing):
    if winner(AI):
        return 1
    if winner(PLAYER):
        return -1
    if draw():
        return 0

    if maximizing:
        best=-math.inf
        for i,v in enumerate(board):
            if v=="":
                board[i]=AI
                best=max(best,minimax(False))
                board[i]=""
        return best
    else:
        best=math.inf
        for i,v in enumerate(board):
            if v=="":
                board[i]=PLAYER
                best=min(best,minimax(True))
                board[i]=""
        return best

def finish(msg):
    messagebox.showinfo("Game Over",msg)

def ai_move():
    status.config(text="AI Thinking...",fg="red")
    root.update()

    best=-math.inf
    move=None
    for i,v in enumerate(board):
        if v=="":
            board[i]=AI
            score=minimax(False)
            board[i]=""
            if score>best:
                best=score
                move=i
    if move is not None:
        board[move]=AI
        buttons[move].config(text=AI,state="disabled")

    if winner(AI):
        finish("AI Wins!")
        disable()
    elif draw():
        finish("Match Draw!")
        disable()
    else:
        status.config(text="Your Turn (X)",fg="blue")

def disable():
    for b in buttons:
        b.config(state="disabled")

def click(i):
    if board[i]!="":
        return
    board[i]=PLAYER
    buttons[i].config(text=PLAYER,state="disabled")
    if winner(PLAYER):
        finish("Congratulations! You Win!")
        disable()
        return
    if draw():
        finish("Match Draw!")
        disable()
        return
    root.after(300,ai_move)

def restart():
    global board
    board=[""]*9
    status.config(text="Your Turn (X)",fg="blue")
    for b in buttons:
        b.config(text="",state="normal")

for i in range(9):
    btn=tk.Button(frame,text="",font=("Arial",24,"bold"),
                  width=4,height=2,
                  command=lambda i=i: click(i))
    btn.grid(row=i//3,column=i%3,padx=2,pady=2)
    buttons.append(btn)

tk.Button(root,text="Restart Game",font=("Arial",14),
          bg="green",fg="white",command=restart).pack(pady=20)

root.mainloop()
