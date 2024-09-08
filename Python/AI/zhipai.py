import random

SUIT_TUPLE={'Spades黑桃','Hearts红心','Clubs梅花','Diamonds方块'}
RANK_TUPLE={'Ace','1','2','3','4','5','6','7','8','9','10','Jack','Queen','King'}

def getCard(deckListIn):
    thisCard = deckListIn.pop()
    return thisCard

def shuffle(deckListIn):
    deckListOut=deckListIn.copy()
    random.shuffle(deckListOut)
    return deckListOut

print('欢迎来到高低纸牌游戏')
print('您必须选择要选择要显示的下一张卡是高于还是低于当前卡')
print('做对了增加20分，做戳了，丢掉15分')
print('初始分为50分')
print()

startingDeckList=[]
for suit in SUIT_TUPLE:
    for thisValue,rank in enumerate(RANK_TUPLE):
        cardDict={'suit':suit,'rank':rank}
        startingDeckList.append(cardDict)

score=50

while True:
    print()
    gameDeckList=shuffle(startingDeckList)
    currentCardDict=getCard(gameDeckList)
    currentCardRank=currentCardDict['rank']
    currentCardValue=currentCardDict['value']
    currentCardSuit=currentCardDict['suit']
    print('Starting card is:',currentCardRank+'of'+currentCardSuit)
    print()


while True:
    for cardNumber in range(0,NCARDS):
        answer=input('下一张牌是高于还是低于'+ currentCardRank+'of'+currentCardSuit+ '?'(enter h or 1))
        nextCardDict=getCard(gameDeckList)
        nextCardDict=nextCardDict['rank']
        nextCardSuit=nextCardDict['suit']
        nextCardValue=nextCardDict['value']
        print('下一张牌是：',nextCardRank+'of'+nextCardSuit)

        if answer=='h':
            if nextCardValue>currentCardValue:
                print('You got it right, it was higher')
                score+=20
            else:
                print('Sorry,it was not higher')
                score-=15
        elif answer=='1':
            if nextCardValue<currentCardValue:
                score+=20
                print('You got it right, it was lower')
            else:
                score-=15
                print('Sorry,it was not lower')
        print('Your score is:',score)
        print()

    while True:
        goAgain=input('To play again,press ENTER , or"q" to quit')
        if goAgain=='q':
            break
print('OK bye')