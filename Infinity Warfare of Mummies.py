import pygame
import random
pygame.init()
fs = pygame.FULLSCREEN
resx = 430
resy = 336
win = pygame.display.set_mode((resx,resy), fs)

pygame.display.set_caption("FIRST GAME PROJECT")


FPS = pygame.time.Clock()


pygame.mixer.init()
bulletSound = pygame.mixer.Sound("sfx\Bullet.wav")
bulletHitSound = pygame.mixer.Sound("sfx\BulletHit.wav")
fireballSound = pygame.mixer.Sound("sfx\Fireball.wav")
fireballHitSound = pygame.mixer.Sound("sfx\FireballHit.wav")
playerDeathSound = pygame.mixer.Sound("sfx\PlayerDeathSound.wav")
muDie = pygame.mixer.Sound("sfx\Mu_die.wav")

bgMusic_1 = pygame.mixer.music.load("sfx\Arcade.mp3")


pygame.mixer.music.play(-1)

class Player(object):
    walkRight = [pygame.image.load('pics\Rr0.png'), pygame.image.load('pics\Rr1.png'), pygame.image.load('pics\Rr2.png'),
                 pygame.image.load('pics\Rr3.png'), pygame.image.load('pics\Rr4.png'), pygame.image.load('pics\Rr5.png')]
    walkLeft = [pygame.image.load('pics\Rl0.png'), pygame.image.load('pics\Rl1.png'), pygame.image.load('pics\Rl2.png'),
                pygame.image.load('pics\Rl3.png'), pygame.image.load('pics\Rl4.png'), pygame.image.load('pics\Rl5.png')]
    bg = pygame.image.load('pics\Bg.png')
    idle = [pygame.image.load('pics\Idle1.png'), pygame.image.load('pics\Idle2.png'), pygame.image.load('pics\Idle3.png')]
    idle_ = [pygame.image.load('pics\-Idle1.png'), pygame.image.load('pics\-Idle2.png'), pygame.image.load('pics\-Idle3.png')]
    jump = [pygame.image.load('pics\J0.png'), pygame.image.load('pics\J1.png'), pygame.image.load('pics\J2.png')]
    heart = pygame.image.load("pics\heart.png")
    def __init__(self,x ,y ,width, height, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 2.5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.jumpDrawCheck = False
        self.walkCount = 0
        self.idleCount = 0
        self.jumpDrawCount = 0
        self.standingDir = 0
        self.hitbox = (self.x + self.width/4, self.y , self.width/2, self.height)
        self.health = health

    def draw(self, win):
        if man.walkCount + 1 > 72:
            man.walkCount = 0
        if man.idleCount + 1 > 72:
            man.idleCount = 0
        if man.jumpDrawCount + 1 > 72:
            man.jumpDrawCount = 0
        if man.left:
            win.blit(Player.walkLeft[man.walkCount // 12], (man.x, man.y))
            man.walkCount += 1
            man.standingDir = -1
        elif man.right:
            win.blit(Player.walkRight[man.walkCount // 12], (man.x, man.y))
            man.walkCount += 1
            man.standingDir = 1
        elif man.jumpDrawCheck:
            win.blit(Player.jump[man.jumpDrawCount // 36], (man.x, man.y))
            man.jumpDrawCount += 1
        else:
            if man.standingDir == -1:
                win.blit(Player.idle_[man.idleCount// 36], (man.x,man.y))
                man.idleCount += 1
                man.walkCount = 0
            else:
                win.blit(Player.idle[man.idleCount // 36], (man.x, man.y))
                man.idleCount += 1
                man.walkCount = 0
        if self.health > 0:
            gap = 0
            for _ in range(self.health):
                win.blit(Player.heart, (180 + gap, 24))
                gap += 25

    def hitboxdraw(self, win):
        self.hitbox = (self.x + self.width / 4, self.y, self.width / 2, self.height)
        #pygame.draw.rect(win, (0, 255, 0), self.hitbox, 1)

    def hit(self):
        global score
        global keys
        global event
        self.x = 50
        self.y = 280
        man.isJump = True
        self.health -= 1
        fontpix = pygame.font.Font("Font\FFont.otf", 12)
        font2 = pygame.font.Font("Font\FFont.otf", 30)
        playerDeathSound.play()
        text = fontpix.render("Enemy is hit you, you lost your 1 health", 1, (120,200,50))
        win.blit(text, (resx/2 - text.get_width()/2, resy/2-10))
        pygame.display.update()
        if self.health == 0:
            text = fontpix.render("You are TOTALLY DEAD NOW, Press ESC", 1, (120, 200, 50))
            textScore = font2.render("SCORE {}".format(score), 1, (0,255,255))
            win.blit(textScore, (resx/2 - text.get_width()/2 + 100, resy/ 2 - 100))
            win.blit(text, (resx / 2 - text.get_width() / 2, resy / 2 + 20))
            pygame.display.update()
            i = 0
            while i < 10000000:
                pygame.time.delay(72 * 4)
                i += 1
                for event in pygame.event.get():
                    keys = pygame.key.get_pressed()

                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    pygame.quit()


            win.blit(text, (resx / 2 - text.get_width() / 2, resy / 2 - 10))
        pygame.display.update()
        i = 0
        while i < 10:
            pygame.time.delay(72*4)
            i += 1
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    i = 72*4+1
                    pygame.quit()

    def hitCheck(self, en_target):
        if en_target.visible:
            if en_target.standingDir == -1:
                if self.hitbox[1] > en_target.leftHitbox[1] - 5 and \
                        self.hitbox[1] + self.hitbox[3] < en_target.leftHitbox[1] + en_target.leftHitbox[3] :
                    if self.hitbox[0] + self.hitbox[2] > en_target.leftHitbox[0] + 25 and \
                            self.hitbox[0] < en_target.leftHitbox[0] + en_target.leftHitbox[2] + 25 :
                        man.hit()
            else:
                if self.hitbox[1] > en_target.rightHitbox[1] - 5\
                        and self.hitbox[1] + self.hitbox[3] < en_target.rightHitbox[1] + en_target.rightHitbox[3]:
                    if self.hitbox[0] + self.hitbox[2] > en_target.rightHitbox[0] -25 and \
                            self.hitbox[0] < en_target.rightHitbox[0] + en_target.rightHitbox[2]-25:
                        man.hit()

class Projectile(object):
    def __init__(self, x, y, radius, color, facing, vel, damage, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = vel * facing
        self.damage = damage
        self.name = name
    def draw(self, win):

            pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    @staticmethod
    def proj_move():
        for enemy in enemies:
            for projectile in projectiles:

                Projectile.collideCheck(projectile, enemy)
        for projectile in projectiles:
            if resx > projectile.x > 0:
                projectile.x += projectile.vel
            else:
                projectiles.pop(projectiles.index(projectile))
    @staticmethod
    def collideCheck(projectile, en_target ):
            if en_target.visible:
                #for left hit box
                if projectile.y + projectile.radius / 2 > en_target.leftHitbox[1] and projectile.y + projectile.radius \
                        < en_target.leftHitbox[1] + en_target.leftHitbox[3]:
                    if en_target.leftHitbox[0] < projectile.x + projectile.radius / 2 < en_target.leftHitbox[0] + \
                            en_target.leftHitbox[2]:
                        en_target.hit(projectile.name)
                        projectiles.pop(projectiles.index(projectile))
                #for right hit box
                if projectile.y + projectile.radius / 2 > en_target.rightHitbox[1] and projectile.y + projectile.radius < \
                        en_target.rightHitbox[1] + en_target.leftHitbox[3]:
                    if en_target.rightHitbox[0] < projectile.x + projectile.radius / 2 < en_target.rightHitbox[0] + \
                            en_target.rightHitbox[2]:
                        en_target.hit(projectile.name)
                        projectiles.pop(projectiles.index(projectile))


class Enemy():
    muWalkLeft = [pygame.image.load('pics\muwalk1l.png'), pygame.image.load('pics\muwalk2l.png'),
                pygame.image.load('pics\muwalk3l.png'), pygame.image.load('pics\muwalk4l.png'),
                pygame.image.load('pics\muwalk5l.png'), pygame.image.load('pics\muwalk6l.png')]

    muWalkRight = [pygame.image.load('pics\muwalk6r.png'), pygame.image.load('pics\muwalk5r.png'),
                 pygame.image.load('pics\muwalk4r.png'), pygame.image.load('pics\muwalk3r.png'),
                 pygame.image.load('pics\muwalk2r.png'), pygame.image.load('pics\muwalk1r.png')] # I did the order wrong while saving images so i fixed it here.

    muIdleLeft = [pygame.image.load('pics\muidle1l.png'), pygame.image.load('pics\muidle2l.png'),
              pygame.image.load('pics\muidle3l.png'), pygame.image.load('pics\muidle4l.png')]

    muIdleRight = [pygame.image.load('pics\muidle4r.png'), pygame.image.load('pics\muidle3r.png'),
                   pygame.image.load('pics\muidle2r.png'), pygame.image.load('pics\muidle1r.png'), ]

    muAttackLeft = [pygame.image.load('pics\muattack0l.png'), pygame.image.load('pics\muattack1l.png'),
                    pygame.image.load('pics\muattack2l.png'), pygame.image.load('pics\muattack3l.png'),
                    pygame.image.load('pics\muattack4l.png'), pygame.image.load('pics\muattack5l.png')]

    muAttackRight = [pygame.image.load('pics\muattack5r.png'), pygame.image.load('pics\muattack4r.png'),
                     pygame.image.load('pics\muattack3r.png'), pygame.image.load('pics\muattack2r.png'),
                     pygame.image.load('pics\muattack1r.png'), pygame.image.load('pics\muattack0r.png')]

    muDie = [pygame.image.load('pics\die0.png'), pygame.image.load('pics\die1.png'),
             pygame.image.load('pics\die2.png'), pygame.image.load('pics\die3.png'),
             pygame.image.load('pics\die4.png'), pygame.image.load('pics\die5.png')]

    muDie_ = [pygame.image.load('pics\die_0.png'), pygame.image.load('pics\die_1.png'),
             pygame.image.load('pics\die_2.png'), pygame.image.load('pics\die_3.png'),
             pygame.image.load('pics\die_4.png'), pygame.image.load('pics\die_5.png')]

    def __init__(self,x ,y ,width, height, vel, health, standingdir):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.left = False
        self.right = False
        self.walkCount = 0
        self.idleCount = 0
        self.standingDir = standingdir
        self.waitCount = 72
        self.movementCount = 200
        self.leftHitbox = (self.x, self.y + self.height/4 , self.width/2, 3*(self.height/4))
        self.rightHitbox = (self.x + self.width / 2 , self.y + self.height / 4, self.width / 2, 3 * (self.height / 4))
        self.health = health
        self.maxHealth = health
        self.dieAnima = False
        self.dieAnimaCount = 0
        self.visible = True
        self.mov_neg = 1

    @staticmethod
    def draw (win):
        for enemy in enemies:
            if enemy.visible :
                enemy.movement(enemy)
                if enemy.walkCount +1 > 72:
                    enemy.walkCount = 0
                if enemy.idleCount +1 > 72:
                    enemy.idleCount = 0
                if enemy.left:
                    win.blit(Enemy.muWalkLeft[enemy.walkCount // 12], (enemy.x, enemy.y))
                    enemy.walkCount += 1
                    enemy.standingDir = -1
                elif enemy.right:
                    win.blit(Enemy.muWalkRight[enemy.walkCount // 12], (enemy.x, enemy.y))
                    enemy.walkCount += 1
                    enemy.standingDir = 1
                else:
                    if enemy.standingDir == -1:
                        win.blit(Enemy.muIdleLeft[enemy.idleCount// 36], (enemy.x,enemy.y))
                        enemy.idleCount += 1
                        enemy.walkCount = 0
                    else:
                        win.blit(Enemy.muIdleRight[enemy.idleCount // 36], (enemy.x, enemy.y))
                        enemy.idleCount += 1
                        enemy.walkCount = 0

                pygame.draw.rect(win, (255, 0, 0), (enemy.leftHitbox[0], enemy.leftHitbox[1] - 20, 50, 10))
                pygame.draw.rect(win, (0, 255, 0),
                                 (enemy.leftHitbox[0], enemy.leftHitbox[1] - 20, 50 - (5*(enemy.maxHealth - enemy.health)), 10))

            if enemy.dieAnimaCount == 72:
                enemy.dieAnima = False
                enemy.visible = False


            if enemy.dieAnima and enemy.standingDir == -1:
                win.blit(Enemy.muDie[enemy.dieAnimaCount//12], (enemy.x, enemy.y))
                enemy.dieAnimaCount += 1
                enemy.walkCount = 0
                enemy.left = False
                enemy.right = False
                enemy.idleCount = 0

            elif enemy.dieAnima and enemy.standingDir == 1:
                win.blit(Enemy.muDie_[enemy.dieAnimaCount // 12], (enemy.x, enemy.y))
                enemy.dieAnimaCount += 1
                enemy.walkCount = 0
                enemy.left = False
                enemy.right = False
                enemy.idleCount = 0

    @staticmethod
    def dieSound():
        global diesoundcounter
        for enemy in enemies:
            if enemy.health == 0 and diesoundcounter//2 == 0: # Its plays two times for one death so i did //2.
                muDie.play()
                diesoundcounter += 2
    @staticmethod
    def movement(enemy):
        if enemy.mov_neg == 1:
            enemy.left = True
            enemy.right = False

        else:
            enemy.left = False
            enemy.right = True

        if enemy.x >= 0:
            enemy.mov_neg = enemy.mov_neg * -1

        if enemy.x <= resx - 48:
            enemy.mov_neg = enemy.mov_neg * -1
        enemy.x -= enemy.vel * enemy.mov_neg




    def hitboxdraw(self, win):
        self.leftHitbox = (self.x, self.y + self.height / 4, self.width / 2, 3 * (self.height / 4))
        self.rightHitbox = (self.x + self.width / 2, self.y + self.height / 4, self.width / 2, 3 * (self.height / 4))
        #if self.standingDir == 1:
         #   pygame.draw.rect(win, (0, 255, 0), self.leftHitbox, 1)
        #else:
        #    pygame.draw.rect(win, (0, 255, 0), self.rightHitbox, 1)


    def hit(self, name):
        global score
        if name == "fireball":
            fireballHitSound.play()
            self.health -= fireball.damage
        if name == "bullet":
            bulletHitSound.play()
            self.health -= bullet.damage
        if self.health <= 0:
            self.dieAnima = True
            self.visible = False
            score += 1

def redrawGameWindow():
    win.blit(Player.bg, (0, 0))
    win.blit((font.render("Score: {}".format(score), 1, (0,255,255))), (resx-100, 10))
    win.blit((font.render("R: {}".format(drawcooldown), 1, (255,255, 0))), (10, 10))
    man.draw(win)

    Enemy.draw(win)
    for projectile in projectiles:
        projectile.draw(win)
    man.hitboxdraw(win)
    for enemy in enemies:
        enemy.hitboxdraw(win)
    pygame.display.update()


diesoundcounter = 0
font = pygame.font.SysFont("arial", 20, True)
man = Player(50, 280, 50, 37, 3)
#mummy = Enemy(350, 270, 48, 48, 0.7, 10, 1)
run = True
projectiles = []
enemies = []
flag = 0
flagProj_0 = 0
flagProj_1 = -72*4
mov_neg = 1
score = 0
fireball_cooldown = 0
enemyCooldown = 72 * 2.5
enemyCooldownCounter = 72
increasingEnemyVel = 0.5



#mainloop
while run:
    print(diesoundcounter)
    if fireball_cooldown > 0:
        fireball_cooldown -= 1
    drawcooldown = round(fireball_cooldown/72)
    flag += 1
    FPS.tick(72)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            run = False

    Projectile.proj_move()

    for enemy in enemies:
        man.hitCheck(enemy)

    #Creating enemies
    enemyCooldownCounter += 1
    if enemyCooldownCounter == enemyCooldown:
        randomx = random.randint(0,2)
        x = 0
        standingdir = 1
        if randomx == 0:
            x = 50
            standingdir = -1

        if randomx == 1:
            x = resx - 50
            standingdir = 1

        enemy = Enemy(x, 270, 48, 48, increasingEnemyVel, 10, standingdir)
        enemies.append(enemy)
        enemyCooldownCounter = 0
        increasingEnemyVel += 0.1


    Enemy.dieSound()

    #Creating Bullets
    if keys[pygame.K_SPACE]:
        if  flagProj_0 + 18 < flag:
            bulletSound.play()
            bullet = Projectile(round(man.x + man.width/2),
                                          round(man.y + (man.height/2)),
                                          5,
                                          (110 ,110 ,100),
                                          man.standingDir,
                                          4,
                                          1, "bullet")
            projectiles.append(bullet)
            flagProj_0 = flag

    #Creating FireBalls
    if keys[pygame.K_r]:
        if flagProj_1 + 72*4 < flag:
            fireballSound.play()
            fireball = Projectile(round(man.x + man.width/2),
                                          round(man.y + (man.height/2)),
                                          12,
                                          (255 ,0 ,0),
                                          man.standingDir,
                                          3,
                                          5, "fireball")
            projectiles.append(fireball)
            flagProj_1 = flag
            fireball_cooldown = 4*72


    if keys[pygame.K_LEFT] and man.x > 0 + man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.jumpDrawCheck = False


    elif keys[pygame.K_RIGHT] and man.x < resx- 50 - man.vel:
        man.x += man.vel
        man.left = False
        man.right = True
        man.jumpDrawCheck = False


    else:
        man.right = False
        man.left = False
        man.jumpDrawCheck = False
        man.walkCount = 0

    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0
    if man.isJump:
        man.jumpDrawCheck = True

        if man.jumpCount >= -10:
            neg = 1

            if man.jumpCount <= 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) /6 * neg # /value this decrease the flight height
            man.jumpCount -= 0.5

        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()


pygame.quit()





