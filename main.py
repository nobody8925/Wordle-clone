import random
import pygame

def load_dict(file_name):
    file=open(file_name)
    words=file.readlines()
    file.close()
    return [word[:5].upper() for word in words]

DICT_GUESSING=load_dict(".\Files\Dictionary.txt")
DICT_ANSWERS=load_dict(".\Files\Wordle_Dictionary.txt")
ANSWER=random.choice(DICT_ANSWERS)

WIDTH=1400
HEIGHT=800
MARGIN=10
TOP_MARGIN=80
BOTTOM_MARGIN=80
LR_MARGIN=500

GREY=(70,70,80)
GREEN=(41,214,148)
YELLOW=(245,175,47)

INPUT=""
FOUND=0
GUESSES=[]
ALPHABETS="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NOT_GUESSED=ALPHABETS
GAME_OVER=False
f=0
g=0

pygame.init()
pygame.font.init()
pygame.display.set_caption("Guess Word")

SQUARE_SIZE=(WIDTH-5*MARGIN-2*LR_MARGIN)//5
FONT=pygame.font.SysFont("free sans bold",SQUARE_SIZE)
FONT_MEDIUM=pygame.font.SysFont("free sans bold",SQUARE_SIZE//2)
FONT_SMALL=pygame.font.SysFont("free sans",SQUARE_SIZE//4)

def determine_unguessed_letters(guesses):
    guessed_letters="".join(guesses)
    not_guessed_letters=""
    for letter in ALPHABETS:
        if letter not in guessed_letters:
            not_guessed_letters=not_guessed_letters+letter
    return not_guessed_letters

def determine_colors(guess,j):
    letter=guess[j]
    if letter==ANSWER[j]:
        return GREEN
    elif letter in ANSWER:
        n_target=ANSWER.count(letter)
        n_correct=0
        n_occurence=0
        for i in range(5):
            if guess[i]==letter:
                if i<=j:
                    n_occurence+=1
                if letter == ANSWER[i]:
                    n_correct+=1
        if n_target-n_correct-n_occurence>=0:
            return YELLOW
    return GREY

#screen
screen=pygame.display.set_mode((WIDTH,HEIGHT))

IMG = pygame.image.load(".\Files\Logo.jpg")

IMG=pygame.transform.scale(IMG,(300,200))

def img(x,y):
    screen.blit(IMG, (x,y))

#animation
animating=True;
while animating:
    
    #background
    screen.fill("black")

    #logo
    img(100,20)

    #instructions to play
    howto=FONT_MEDIUM.render("How to Play",False,(255,255,255))
    left=howto.get_rect(center=(WIDTH//12,HEIGHT//2.5))
    screen.blit(howto,left)

    first=FONT_SMALL.render("1.) Guess the word in 6 tries.",False,(255,255,255))
    left1=first.get_rect(center=(WIDTH//8.75,HEIGHT//2.2))
    screen.blit(first,left1)

    second=FONT_SMALL.render("2.) Each guess must be a valid 5-letter word.",False,(255,255,255))
    left2=second.get_rect(center=(WIDTH//6.69,HEIGHT//2))
    screen.blit(second,left2)

    third=FONT_SMALL.render("3.) Hit the enter button to submit.",False,(255,255,255))
    left3=third.get_rect(center=(WIDTH//8.1,HEIGHT//1.85))
    screen.blit(third,left3)

    four1=FONT_SMALL.render("4.) After each guess, the color of the tiles will",False,(255,255,255))
    left4=four1.get_rect(center=(WIDTH//6.7,HEIGHT//1.72))
    screen.blit(four1,left4)
    
    four2=FONT_SMALL.render("change to show how close your guess was",False,(255,255,255))
    left5=four2.get_rect(center=(WIDTH//6.3,HEIGHT//1.63))
    screen.blit(four2,left5)

    four3=FONT_SMALL.render("to the word.",False,(255,255,255))
    left6=four3.get_rect(center=(WIDTH//11.3,HEIGHT//1.55))
    screen.blit(four3,left6)

    five=FONT_SMALL.render("5.) Green means the letter is in correct spot.",False,(255,255,255))
    left7=five.get_rect(center=(WIDTH//6.75,HEIGHT//1.47))
    screen.blit(five,left7)

    six1=FONT_SMALL.render("6.) Yellow means the letter is in the word but",False,(255,255,255))
    left8=six1.get_rect(center=(WIDTH//6.75,HEIGHT//1.39))
    screen.blit(six1,left8)

    six2=FONT_SMALL.render("in the wrong spot.",False,(255,255,255))
    left9=six2.get_rect(center=(WIDTH//9.5,HEIGHT//1.34))
    screen.blit(six2,left9)

    seven=FONT_SMALL.render("7.) Grey means the letter is not in the word.",False,(255,255,255))
    left10=seven.get_rect(center=(WIDTH//6.9,HEIGHT//1.28))
    screen.blit(seven,left10)

    #show unguessed letters
    determine_unguessed_letters(GUESSES)

    #draw guesses
    y=TOP_MARGIN
    for i in range(6):
        x=LR_MARGIN//0.75
        for j in range(5):

            #square
            square=pygame.Rect(x,y,SQUARE_SIZE,SQUARE_SIZE)
            pygame.draw.rect(screen,GREY,square,width=2,border_radius=10)
            
            #letters already guessed
            if i<len(GUESSES):
                color=determine_colors(GUESSES[i],j)
                pygame.draw.rect(screen,color,square,border_radius=10)
                letter=FONT.render(GUESSES[i][j],False,(255,255,255))
                surface=letter.get_rect(center=(x+SQUARE_SIZE//2,y+SQUARE_SIZE//2))
                screen.blit(letter,surface)
            
            #user input
            if i==len(GUESSES) and j<len(INPUT):
                letter=FONT.render(INPUT[j],False,(255,255,255))
                surface=letter.get_rect(center=(x+SQUARE_SIZE//2,y+SQUARE_SIZE//2))
                screen.blit(letter,surface)


            x+=SQUARE_SIZE+MARGIN
        
        y+=SQUARE_SIZE+MARGIN


    #draw unguessed words
    letters=FONT_SMALL.render(NOT_GUESSED,False,GREY)
    surface=letters.get_rect(center=(WIDTH//1.62,TOP_MARGIN//2))
    screen.blit(letters,surface)

    #show correct answer after game is over
    if len(GUESSES)==6 and GUESSES[5]!=ANSWER:
        GAME_OVER=True
        msg=FONT_SMALL.render("The answer was",False,(255,255,255))
        surface2=msg.get_rect(center=(WIDTH//1.65,HEIGHT//1.3))
        screen.blit(msg,surface2)
        letters=FONT.render(ANSWER,False,(255,255,255))
        surface=letters.get_rect(center=(WIDTH//1.65,HEIGHT-BOTTOM_MARGIN//0.6-MARGIN))
        screen.blit(letters,surface)
        msg=FONT_SMALL.render("Press Spacebar to restart, Esc to exit",False,(255,255,255))
        surface5=msg.get_rect(center=(WIDTH//1.65,HEIGHT-BOTTOM_MARGIN//0.8-MARGIN))
        screen.blit(msg,surface5)

    #if user gets the right answer
    if FOUND:
        succ_msg=FONT_SMALL.render("RIGHT!!",False,(255,255,255))
        surface3=succ_msg.get_rect(center=(WIDTH//1.65,HEIGHT//1.3))
        screen.blit(succ_msg,surface3)
        ans=FONT.render(ANSWER,False,(255,255,255))
        surface4=ans.get_rect(center=(WIDTH//1.65,HEIGHT-BOTTOM_MARGIN//0.6-MARGIN))
        screen.blit(ans,surface4)
        msg=FONT_SMALL.render("Press Spacebar to restart, Esc to exit",False,(255,255,255))
        surface5=msg.get_rect(center=(WIDTH//1.65,HEIGHT-BOTTOM_MARGIN//0.8-MARGIN))
        screen.blit(msg,surface5)

    #invalid word entered
    if f:
        err_msg=FONT_SMALL.render("Word does not exist",False,(255,255,255))
        surface3=err_msg.get_rect(center=(WIDTH//1.65,HEIGHT//1.3))
        screen.blit(err_msg,surface3)

    #word is repeated
    if g:
        err_msg2=FONT_SMALL.render("Word already entered",False,(255,255,255))
        surface3=err_msg2.get_rect(center=(WIDTH//1.65,HEIGHT//1.3))
        screen.blit(err_msg2,surface3)

    #screen update
    pygame.display.flip()

    #track user interaction
    for event in pygame.event.get():

        #stop animation after window is closed
        if event.type==pygame.QUIT:
            animating=False
        
        #user presses key
        elif event.type==pygame.KEYDOWN:

            #escape key to quit animation
            if event.key==pygame.K_ESCAPE:
                animating=False

            #space bar to restart
            if event.key==pygame.K_SPACE and (len(GUESSES)==6 or FOUND):
                GAME_OVER=False
                ANSWER=random.choice(DICT_ANSWERS)
                GUESSES=[]
                NOT_GUESSED=ALPHABETS
                INPUT=""
                FOUND=0

            #backspace to clear a square
            if event.key==pygame.K_BACKSPACE:
                if len(INPUT)>0:
                    INPUT=INPUT[:len(INPUT)-1]
            
            #return key to submit a guess
            elif event.key==pygame.K_RETURN:
                if len(INPUT)==5 and INPUT:
                    #user entered invalid word
                    if DICT_GUESSING.count(INPUT)==0:
                        INPUT=""
                        f=1
                        g=0
                        continue
                    
                    #user entered word already used 
                    if GUESSES.count(INPUT):
                        g=1
                        f=0
                        INPUT=""
                        continue;

                    f=0
                    g=0
                    GUESSES.append(INPUT)
                    NOT_GUESSED=determine_unguessed_letters(GUESSES)

                    #user entered correct word
                    if INPUT==ANSWER:
                        GAME_OVER=True
                        FOUND=1
                    else:
                        GAME_OVER=False
                    INPUT=""

            #regular text input
            elif len(INPUT)<5 and not GAME_OVER and event.unicode.isalpha():
                INPUT=INPUT+event.unicode.upper()