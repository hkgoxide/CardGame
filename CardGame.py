from tkinter import *
import copy
import random

Game = 'CardGame'
Version = '0.01'
Author = 'ChuShu'

length , width = 7, 3

'''


考量點
    坦克&膠登人物可共用機制
	如坦克 = 肉盾
      	    SPG(自走炮) = 遠程攻擊
     	    TD(驅逐坦克) = 狙擊手
    紅方為玩家 藍方為電腦 先完成紅方
    連線對戰 需Python技術支援 <<< To do
進度表:
###
基礎卡牌 未完成
    各種卡牌機制 未完成
        主師 未完成
            加資源
        坦克 未完成
            主力
        TD 未完成
            直行攻擊 高攻      
        SPG 未完成
            大射程 低攻
        支援 未完成
        狗 亂入的:0)
        
    卡牌圖片 未完成 < 圖片size最大為50x50
    牌組 未完成
    
機制
    發配卡牌 完成
    移動功能 完成
    計cost 完成
    攻擊功能 未完成 <<< To do, add to Object_rightclick
        右click敵方卡牌
        扣血(card.hp -= atk)
        攻擊次數歸0 (card.atks = 0)
    AI出牌 未完成
    

    顯示手牌資料 完成
    顯示地圖上卡牌資料 未完成 << To do, add to main.update
        顯示icon卡在方格上(如晴天狗)
        要bind做所在方格內既click evevnt
        右click 顯示卡牌資料(cost, hp, etc)
        
To do:
睇下啲code有乜位可以寫得簡潔啲


###

同一牌MAX3
地形X回合改變

牌組
    以敵資源補給自己
    廣域資源/強補給
    戰術卡 加強能力/資源
    情報卡
'''
"""
Comments @ 21:15 HKT 19 Nov
1.For the round actions, you can make them into more specific functions. For example:
instead of if (card.pos == (x,y)), you can try
def findCardAtPos(x,y,playerCards): (or a tuple)
	card = None
	cardList = [c for c in playerCards if c.pos == (x,y)]
	if cardList:
		card = cardList[0]
	return card

2. You can try using dicts for decks. It is simple to use like lists:
{ "sunny dog" : 10 , "ice" : 5, "big cum" : 1 }

3. You can also try to make players into objects, each player have the following attributes/methods:
deck: their current deck
handcard (better call it "hand"): their current hand
playerType: AI or player, which makes it more flexible

4. See below; concerning [x for x in (enumerator)]
"""

class MainGame(Frame):
    def __init__(self, parent): 
        Frame.__init__(self, parent)  
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
        self.parent.title('Python')
        self.pack(fill = BOTH, expand = 1)
        self.canvas = Canvas(self)


        self.ObjectID = 0
        
        for y in range(width):
            for x in range(length):
                xy = x, y
                self.canvas.create_rectangle(self.xy(xy), outline = '#000000', fill = '#CDCDCD', tags = 'grids')

        self.canvas.pack(fill = BOTH, expand = YES)
        self.canvas.tag_bind('grids', '<ButtonPress-1>', self.Object_click)
        self.canvas.tag_bind('grids', '<ButtonPress-3>', self.Object_rightclick)
        self.cost = Label(self, text = 0)
        self.cost.place(x = 250, y = 250)
        
        w, h = 85, 145
        self.button1 = Button(self, width = w, height = h, text = '', command = lambda: self.set_card(0))
        self.button2 = Button(self, width = w, height = h, text = '', command = lambda: self.set_card(1))
        self.button3 = Button(self, width = w, height = h, text = '', command = lambda: self.set_card(2))
        self.button4 = Button(self, width = w, height = h, text = '', command = lambda: self.set_card(3))
        self.button5 = Button(self, width = w, height = h, text = '', command = lambda: self.set_card(4))
        self.button6 = Button(self, width = w, height = h, text = '', command = lambda: self.set_card(5))
        self.button7 = Button(self, width = w, height = h, text = '', command = lambda: self.set_card(6))
        self.turn_end = Button(self, width = 12, height = 5, text = '結束回合', command = None)
        self.turn_end.place(x = 350, y = 250)

        x1 = -60
        self.buttons = [self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, self.button7]
        for button in self.buttons:
            x1 += 93
            button.place(x = x1, y = 375)
            
    def set_card(self, i):
        name = battle.card_find(battle.red_handcard[i]).name
        pos = main.ObjectID 
        side = 'red'

        xy = self.Object_pos(pos)
        for card in battle.red_card:
            if card.pos == xy:
                return None
        battle.set_card(name, xy, side, cost=True)
        main.update()
        
    def update(self):
        self.cost['text'] = '資源%s' % battle.red_cost
        
        for i in range(width * length):
            self.canvas.itemconfig(i + 1, fill = '#CDCDCD')
        self.canvas.itemconfig(self.ObjectID + 1, fill = '#DCDCDC')
  
        red_card = battle.red_card
        red_handcard = battle.red_handcard
        blue_card = battle.blue_card
        for card in red_card:
            xy = self.Object_xy(card.pos) + 1
            self.canvas.itemconfig(xy, fill = '#FF7C80')

        for button in self.buttons:
            button['text'] = '---'
            button['state'] = 'disable'
            
        for card, button in zip(red_handcard, self.buttons):
            if card is not None:
                card_info = self.cards_show(card)
                button['text'] = card_info
                if battle.red_cost >= battle.card_find(card).cost:
                    button['state'] = 'normal'
                    
        for card in blue_card:
            xy = self.Object_xy(card.pos) + 1
            self.canvas.itemconfig((xy), fill = '#4876FF')

        for card in red_card:
            xy = self.ObjectID - self.ObjectID // 7 * 7, self.ObjectID // 7
            if card.pos == xy or xy not in [(0, 0), (1, 1), (0, 2)]:
                for button in self.buttons:
                    button['state'] = 'disable'

        self.pic_none = PhotoImage(file = 'None.png')
        if red_handcard:
            for i, button in enumerate(self.buttons):
                if i < len(red_handcard):
                    card = battle.card_find(red_handcard[i])
                    button.config(image = battle.pics[card.pic], compound = 'top')               
                else:
                    button.config(image = self.pic_none, compound = 'top')
                
    def cards_show(self, name):
        card = battle.card_find(name)
        card_info = None
        
        card_name = card.name
        card_type = card.card_type
        cost = card.cost
        atk = card.atk
        hp = card.hp
        
        if card_type == 'leader':
            card_type = '主師'
        elif card_type == 'tank':
            card_type = '坦克'
        elif card_type == 'spg':
            card_type = 'spg'
        elif card_type == 'dog':
            card_type = '狗'
        elif card_type == 'support':
            card_type = '支援'
        
        card_info = '{%s} \n\n[%s]\nCost(%s)\nAtk(%s)\nHp(%s)' % (card_type, card_name, cost, atk, hp)
        return card_info
       
    def Object_click(self, event):
        object_closest = event.widget.find_closest(event.x, event.y)
        self.ObjectID = object_closest[0] - 1
        self.update()

    def Object_rightclick(self, event):
        object_closest = event.widget.find_closest(event.x, event.y)
        self.RightClickID = object_closest[0] - 1

        x, y = self.Object_pos(self.RightClickID)
        x1, y1 = self.Object_pos(self.ObjectID)

        for card in battle.red_card:
            if card.pos == (x1, y1):
                if card.moves > 0:
                    if (x, y) in battle.pos((x1, y1)):
                        card.pos = x, y
                        card.moves -= 1
		    else:
			#Attacking
			#finding the enemy card(s) that can be attacked at (x,y)
			#Just to note, you can use a = [x for x in (some iterator) (criteria - optional)]
			#to extract members from a iterator with some criteria
			enemyCards = [c for c in battle.blue_card if c.pos == (x,y)]
			#check if list is empty. Empty list evalutes to "False"
			if enemyCards:
				battle.attack(card,enemyCard[0])
        self.update()

    def Object_pos(self, pos):
        y = pos // 7
        x = pos - y * 7
        return x, y
    
    def Object_xy(self, xy):
        x, y = xy
        pos = x + y * 7
        return pos
        
    def xy(self, xy):
        x, y = xy
        x1 = x * 50 + 20
        y1 = y * 50 + 20
        x2 = x1 + 50
        y2 = y1 + 50
        return [x1, y1, x2, y2]
        
class card(object):
    def __init__(self, name, card_type, pic, cost, atk, hp, moves, atks, *leader):
        self.name = name
        self.card_type = card_type
        self.pic = pic
        self.cost = cost
        self.atk = atk
        self.hp = hp
        self.moves = moves
        self.atks = atks

deck1 = ['冰','晴天狗', '晴天狗', '晴天狗','驅逐坦克ZEN',
         '重坦克碧琴型', '重坦克碧琴型', '自走炮碧琴型', '自走炮碧琴型']

deck2 = ['大麻', '晴天狗', '晴天狗', '晴天狗', '晴天狗',
         '晴天狗', '晴天狗', '晴天狗', '晴天狗', '晴天狗',
         '晴天狗', '晴天狗', '晴天狗', '晴天狗', '晴天狗',
         '晴天狗', '晴天狗', '晴天狗', '晴天狗', '晴天狗',
         '補給兵', '補給兵', '補給兵', '補給兵', '補給兵',
         '補給兵', '補給兵', '補給兵', '自走炮碧琴型', '自走炮碧琴型',]


cards_type = ['leader', 'tank', 'TD', 'spg', 'dog']
cards = [#card('卡名', '卡類', 費用, 攻擊,血量, 移動力, 攻擊次)
         card('冰', 'leader', None, 1, 1, 1, None, None),
         card('大麻', 'leader', None, 1, 1, 1, None, None),
         card('ZEN', 'leader', None, 1, 1, 1, None, None),

         card('補給兵', 'support', None, 2, 1, 3, None, None),
         card('油田', 'support', None, 3, 2, 3, None, None),
         card('雷達', 'support', None, 3, 2, 3, None, None),

         card('晴天狗', 'dog', '28.gif', 1, 1, 2, 1, 1),
         card('流氓犬', 'dog', '28.gif', 2, 2, 4, 1, 1),

         card('自走炮松溪型', 'spg', 'SPG.png', 4, 5, 2, 1, 1),
         card('自走炮碧琴型', 'spg', 'SPG.png', 3, 3, 1, 1, 1),
         
         card('驅逐坦克ZEN', 'TD', None, 6, 6, 2, 1, 1),
         
         card('重坦克松溪型', 'tank', 'Tank1.png', 5, 4, 4, 1, 1),
         card('重坦克碧琴型', 'tank', 'Tank1.png', 5, 4, 3, 1, 1),

         card('中坦克甲型', 'tank', None, 3, 2, 3, 1, 1),
         card('中坦克乙型', 'tank', None, 3, 2, 3, 1, 1),]


class combat(object):
    def __init__(self):
        deck_1 = self.card_in_class(deck1)
        deck_2 = self.card_in_class(deck2)
        deck_1 = self.random_deck(deck1)
        deck_2 = self.random_deck(deck2)
        self.deck_red = list(deck_1)
        self.deck_blue = list(deck_2)
        
        self.red_ap = 0
        self.red_card = []
        self.red_handcard = []
        self.red_cost = 0
        
        self.blue_ap = 0
        self.blue_card = []
        self.blue_handcard = []
        self.blue_cost = 0

        self.pics = self.set_pics()
        
    def attack(self, atk_card, def_card):
        atk_damage = atk_card.atk
        def_card.hp -= atk_damage
        if def_card.hp <= 0:
            if def_card.side == 'red':
                self.red_card.remove(def_card)
            elif def_card.side == 'blue':
                self.blue_card.remove(def_card)
        main.update()
                         
    def dealt(self):
        while len(self.red_handcard) < 7 and len(self.deck_red) > 0:
            card = self.deck_red[-1]
            self.red_handcard.append(card)
            self.deck_red.remove(card)
        main.update()
        
    def set_card(self, name, pos, side, cost=False, leader=False):
        card_data = self.card_info(name, pos, side)
        if leader:
            if side == 'red':
                self.deck_red.remove(name)
                self.red_card.append(card_data)
            elif side == 'blue':
                self.deck_blue.remove(name)
                self.blue_card.append(card_data)            
        else:
            if side == 'red':
                self.red_handcard.remove(name)
                self.red_card.append(card_data)
                if cost:
                    self.red_cost -= card_data.cost
            elif side == 'blue':
                self.blue_handcard.remove(name)
                self.blue_card.append(card_data)
        main.update()
    
    def card_info(self, name, pos, side):
        card = self.card_find(name)
        card_data = copy.copy(card)
        card_data.pos = pos
        card_data.side = side
        return card_data

    def card_find(self, name):
        for card in cards:
            if card.name == name:
                return card
    
    def random_deck(self, deck):
        old_deck = list(deck)
        new_deck = []
        
        leader = old_deck[0]
        old_deck.remove(leader)
        
        while len(old_deck) > 0:
            r = random.choice(old_deck)
            old_deck.remove(r)
            new_deck.append(r)
        new_deck.insert(0, leader)
        return new_deck
    
    def pos(self, pos):
        x, y = pos
        e, s, w, n = (x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)
        dirt = [e, s, w, n]
        dirt_new = dirt
        for j in range(2):
            for i in dirt:
                x, y = i
                nearby = i
                if x < 0 or y < 0 or y > 2:
                    dirt_new.remove(nearby)
                else:
                    for card in self.red_card:
                        if card.pos == nearby:
                            dirt_new.remove(nearby)
                    for card in self.blue_card:
                        if card.pos == nearby:
                            dirt_new.remove(nearby)
        return dirt_new
    
    def card_in_class(self, deck):
        cards = []
        for name in deck:
            found_card = self.card_find(name)
            card = copy.copy(found_card)
            cards.append(card)
        return cards

    def turn_end(self):
        for card in self.red_card:
            card.moves = 1
            card.atks = 1
        for card in self.blue_card:
            card.moves = 1
            card.atks = 1
        battle.red_cost += 5
        battle.blue_cost += 5
        self.dealt()

    def set_pics(self):
        pic_none = PhotoImage(file = 'None.png')
        pics = {None: pic_none}
        for card in cards:
            if card.pic:
                pic = PhotoImage(file = card.pic)
                pics[card.pic] = pic
        return pics
    
root = Tk()
root.geometry('850x650+0+0')
main = MainGame(root)
battle = combat()

battle.set_card(battle.deck_red[0], (0, 1), 'red', leader=True)
battle.set_card(battle.deck_blue[0], (6, 1), 'blue', leader=True)
battle.dealt()
battle.red_cost = 5
battle.blue_cost = 5
main.turn_end['command'] = battle.turn_end
