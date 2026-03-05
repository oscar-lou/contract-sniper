def setup():
    global pso_1, gameState, greenhouse, menu, bodyguard, bullet, start_game, restart_game, exit_game, next_level, svd, head_w, head_h, scope_w, scope_h, game_over_timer, end_time_start, game_over_delay, svd_scale, bullet_w, bullet_h, rooftop
    global svd_w, svd_h, guard_w, guard_h, guard_spawnX, guard_spawnY, total_time, menu_title, game_over_text, mission_completed, gameOver_x, gameOver_y, hudText_x, xMid, yMid
    size(1280, 1024) #5:4 aspect ratio
    frameRate(60)
    
    #import all images
    pso_1 = loadImage("pso_1.png")
    greenhouse = loadImage("greenhouse.png")
    menu = loadImage("menu.png")
    bodyguard = loadImage("bodyguard.png")
    bullet = loadImage("bullet.png")
    start_game = loadImage("start_game.png")
    restart_game = loadImage("restart_game.png")
    exit_game = loadImage("exit_game.png")
    next_level = loadImage("next_level.png")
    svd = loadImage("svd.png")
    rooftop = loadImage("rooftop.png")
    menu_title = loadImage("menu_title.png")
    game_over_text = loadImage("game_over_text.png")
    mission_completed = loadImage("mission_completed.png")
    
    #dimension of the target's head (head hitbox)
    head_w = 29
    head_h = 36

    
    #Time in seconds to complete the level
    total_time = 30

    #dimensions of the entire target
    guard_w = 80
    guard_h = 258
    
    xMid, yMid = width/2, height/2
    
    
    #(Only for stage 3+) coordinates for spawning at the edges of the patrol area
    guard_spawnX = [xMid, width/1.3, 1500, width/1.1]
    guard_spawnY = [850, yMid, height/1.5, height/1.05]
    
    #coordinates for the sniper's scope position on the window
    scope_w = xMid
    scope_h = yMid
    
    #logo of the gun on the HUD
    svd_scale = 0.4
    svd_w = 1004 * svd_scale
    svd_h = 199 * svd_scale
    
    #bullet logo on the bottom right of the HUD
    bullet_scale = 0.25
    bullet_w = bullet_h = 512 * bullet_scale

    #show intro on bootup (0 = intro)
    gameState = 0
    
    #Delay In Seconds After No Bullets before Game Over Screen
    end_time_start = 0
    game_over_delay = 3
    game_over_timer = False
    
    hudText_x = 20
    
    #coordinates for Game Over Reason Text
    gameOver_x, gameOver_y = xMid, height/2.25


    
def draw():
    
    if gameState == -2:
        intermission()
        
    elif gameState == -1:
        gameOver()

    elif gameState == 0:
        gameIntro()
            
    elif gameState == 1:
        gameStage1()
        
    elif gameState == 2:
        gameStage2()
            
    elif gameState == 3:
        gameStage3()

    
def gameIntro():
    global startTime, targetCount, civilianAlive, level, wind, distance, guardX_initial, guardY_initial, guardKilled, dx
    startTime = millis()
    
    #reset targets kill counter
    targetCount = 0
    
    #reset level
    level = 1
    
    #reset wind & distance variables
    wind = distance = 0
    
    #reset bodyguard speed
    dx = 1
    
    #display background
    imageMode(CENTER)
    image(menu, xMid, yMid)
    
    #display menu title
    fill(255)
    textSize(100)
    textAlign(CENTER)
    image(menu_title, xMid, height/4)
    
    #display instructions
    textSize(40)
    textAlign(CORNER)
    text("Instructions:", 50, yMid + 150)
    text("LMB to shoot", 50, yMid + 200)
    text("Press R to reload", 50, yMid + 250)
    
    #Display Buttons
    image(start_game, xMid, height/1.75)
    image(exit_game, xMid, height/1.25)
    
    #target spawn coordinate parameters
    guardX_initial = random(xMid, width*1.4)
    guardY_initial = height/1.1

    #reset civilianAlive state
    civilianAlive = True
    
    #reset guardKilled state
    guardKilled = False
    
    cursor()
    
def gameStage1():
    global gameState, guardX, guardY, game_over_timer, end_time_start, timeleft
    
    #amount of seconds elapsed since stage start
    second = ((millis()- startTime)/1000)
    
    #guard coordinates
    guardX = guardX_initial - mouseX
    guardY = guardY_initial - mouseY
    
    
    #invert mouse coordinates to move all elements except for the sniper scope for stationary scope effect
    invertedX = width - mouseX
    invertedY = height - mouseY
    
    #background
    background(0)
    image(rooftop, invertedX, invertedY)
    
    #display target
    imageMode(CORNER)
    translate(-25, 0)
    image(bodyguard, guardX, guardY, guard_w, guard_h)
    translate(25, 0)

    
    #scope_image
    imageMode(CENTER)
    image(pso_1, scope_w, scope_h)
    
    #sniper_icon
    image(svd, 225, height - 100, svd_w, svd_h)

    #bullet_icon
    for i in range(ammo_mag):
        bullet_x = width-bullet_w - (bullet_w/ammo_mag) * i
        image(bullet, bullet_x, 825, bullet_w, bullet_h)

    
    #display ammo_count
    fill(255)
    textSize(60)
    textAlign(CENTER)
    text(str(ammo_mag) + " / " + str(ammo_reserve), width - 175, height - 75)
    
    
    #display time_left
    timeleft = total_time - second
    textSize(45)
    textAlign(LEFT,TOP)
    text("Time Left: " + str(timeleft) + "s", hudText_x, 10)
    
    
    #display total bodyguards killed
    textSize(45)
    textAlign(LEFT,TOP)
    text("V.I.Ps Killed: " + str(targetCount), hudText_x, 75)
    
    #level_indicator
    text("Level " + str(level), hudText_x, 140)
    
    #Display Wind & Distance variables
    textAlign(RIGHT)
    text("Wind: " + str(wind) + " km/h", width - 15, 50)
    text("Distance: " + str(distance) + " m", width - 15, 120)
    textAlign(LEFT)
    
    #game over condition (out of time)
    if timeleft <= 0:
        gameState = -1
        
    #reload_prompt_start
    elif ammo_mag == 0 and ammo_reserve == 0:
        fill(255)
        textSize(60)
        textAlign(CENTER)
        text("You are out of bullets!", xMid, height/2.1)
        
        #timer starts for delay effect before game over screen
        if game_over_timer == False:
            end_time_start = millis()/1000
            game_over_timer = True
            
        #display game over screen after 3s    
        if (millis()/1000) - end_time_start >= game_over_delay and game_over_timer == True:
            gameState = -1
            end_time_start = 0
            game_over_timer = False
        
    #display reload prompt if bullets are available
    elif ammo_mag == 0:
        fill(255)
        textSize(60)
        textAlign(CENTER)
        text("Press R to reload", xMid, height/1.1)
    #reload_prompt_end


    noCursor()

    
def gameStage2():
    global gameState, guardX, guardY, game_over_timer, end_time_start, timeleft
    
    #amount of seconds elapsed since stage start
    second = ((millis()- startTime)/1000)

    #guard coordinates
    guardX = guardX_initial - mouseX
    guardY = guardY_initial - mouseY
    
    
    #invert mouse coordinates to move all elements except for the sniper scope for stationary scope effect
    invertedX = width - mouseX
    invertedY = height - mouseY
    
    #background
    background(0)
    image(rooftop, invertedX, invertedY)
    
    #Display target
    imageMode(CORNER)
    translate(-25, 0)
    image(bodyguard, guardX, guardY, guard_w, guard_h)
    translate(25, 0)
    
    
    #scope_image
    imageMode(CENTER)
    image(pso_1, scope_w, scope_h)
    
    #sniper_icon
    image(svd, 225, height - 100, svd_w, svd_h)

    #bullet_icon
    for i in range(ammo_mag):
        bullet_x = width-bullet_w - (bullet_w/ammo_mag) * i
        image(bullet, bullet_x, 825, bullet_w, bullet_h)

    
    #display ammo_count
    fill(255)
    textSize(60)
    textAlign(CENTER)
    text(str(ammo_mag) + " / " + str(ammo_reserve), width - 175, height - 75)
    
    
    #display time_left
    timeleft = total_time - second
    textSize(45)
    textAlign(LEFT,TOP)
    text("Time Left: " + str(timeleft) + "s", hudText_x, 10)
    
    
    #display total bodyguards killed
    textSize(45)
    textAlign(LEFT,TOP)
    text("V.I.Ps Killed: " + str(targetCount), hudText_x, 75)
    
    #level_indicator
    text("Level " + str(level), hudText_x, 140)
    
    #Display Wind & Distance variables
    textAlign(RIGHT)
    text("Wind: " + str(wind) + " km/h", width - 15, 50)
    text("Distance: " + str(distance) + " m", width - 15, 120)
    textAlign(LEFT)

    #game over condition (out of time)
    if timeleft <= 0:
        gameState = -1
        
    #reload_prompt_start
    elif ammo_mag == 0 and ammo_reserve == 0:
        fill(255)
        textSize(60)
        textAlign(CENTER)
        text("You are out of bullets!", xMid, height/2.1)
        
        #timer starts for delay effect before game over screen
        if game_over_timer == False:
            end_time_start = millis()/1000
            game_over_timer = True
            
            
        #display game over screen after 3s    
        if (millis()/1000) - end_time_start >= game_over_delay and game_over_timer == True:
            gameState = -1
            end_time_start = 0
            game_over_timer = False
        
    #display reload prompt if bullets are available
    elif ammo_mag == 0:
        fill(255)
        textSize(60)
        textAlign(CENTER)
        text("Press R to reload", xMid, height/1.1)
    #reload_prompt_end


    noCursor()
    
    
    
def gameStage3():
    global gameState, guardX_initial, guardY_initial, guardX, guardY, game_over_timer, end_time_start, direction, timeleft
    
    #amount of seconds elapsed since stage start
    second = ((millis()- startTime)/1000)
    
    #guard coordinates
    guardX = guardX_initial - mouseX
    guardY = guardY_initial - mouseY
    
    
    #invert mouse coordinates to move all elements except for the sniper scope for stationary scope effect
    invertedX = width - mouseX
    invertedY = height - mouseY
    
    #background
    background(0)
    image(greenhouse, invertedX, invertedY)


    #conditions for bodyguard movement
    if direction == 1: #towards bottom-right
        guardX_initial += dx
        guardY_initial += 0.35
        if guardX_initial >= guard_spawnX[2]:
            direction = 2
    elif direction == 2: #towards bottom-left
        guardX_initial -= dx
        guardY_initial += dx
        if guardY_initial >= guard_spawnY[3]:
            direction = 3
    elif direction == 3: #towards top-left
        guardX_initial -= dx
        guardY_initial -= 0.35
        if guardX_initial <= guard_spawnX[0]:
            direction = 4
    elif direction == 4: #towards top-right
        guardX_initial += dx
        guardY_initial -= dx
        if guardY_initial <= guard_spawnY[1]:
            direction = 1
    



    
    #display target
    imageMode(CORNER)
    translate(-25, 0)
    image(bodyguard, guardX, guardY, guard_w, guard_h)
    translate(25, 0)

    
    #scope_image
    imageMode(CENTER)
    image(pso_1, scope_w, scope_h)
    
    #sniper_icon
    image(svd, 225, height - 100, svd_w, svd_h)

    #bullet_icon
    for i in range(ammo_mag):
        bullet_x = width-bullet_w - (bullet_w/ammo_mag) * i
        image(bullet, bullet_x, 825, bullet_w, bullet_h)

    
    #display ammo_count
    fill(255)
    textSize(60)
    textAlign(CENTER)
    text(str(ammo_mag) + " / " + str(ammo_reserve), width - 175, height - 75)
    
    
    #display time_left
    timeleft = total_time - second
    textSize(45)
    textAlign(LEFT,TOP)
    text("Time Left: " + str(timeleft) + "s", hudText_x, 10)
    
    
    #display total bodyguards killed
    textSize(45)
    textAlign(LEFT,TOP)
    text("V.I.Ps Killed: " + str(targetCount), hudText_x, 75)
    
    #level_indicator
    text("Level " + str(level), hudText_x, 140)
    
    #Display Wind & Distance variables
    textAlign(RIGHT)
    text("Wind: " + str(wind) + " km/h", width - 15, 50)
    text("Distance: " + str(distance) + " m", width - 15, 120)
    textAlign(LEFT)

    #game over condition (out of time)
    if timeleft <= 0:
        gameState = -1
        
    #reload_prompt_start
    elif ammo_mag == 0 and ammo_reserve == 0:
        fill(255)
        textSize(60)
        textAlign(CENTER)
        text("You are out of bullets!", xMid, height/2.1)
        
        #timer starts for delay effect before game over screen
        if game_over_timer == False:
            end_time_start = millis()/1000
            game_over_timer = True
            
        #display game over screen after 3s    
        if (millis()/1000) - end_time_start >= game_over_delay and game_over_timer == True:
            gameState = -1
            end_time_start = 0
            game_over_timer = False
        
    #display reload prompt if bullets are available
    elif ammo_mag == 0:
        fill(255)
        textSize(60)
        textAlign(CENTER)
        text("Press R to reload", xMid, height/1.1)
    #reload_prompt_end


    noCursor()
    
def intermission():
    global wind, distance, direction, guardX_initial, guardY_initial, civilianAlive, guardKilled
    
    #display background image
    imageMode(CENTER)
    image(menu, xMid, yMid)
    
    #Display mission complete
    image(mission_completed, xMid, height/4)
    
    #display buttons
    image(next_level, xMid, height/1.75)
    image(exit_game, xMid, height/1.25)
    
    #generate larger random wind and distance variables


        
    #generate less random wind and distance variables
    if level == 2:
        wind = int(random(-5, 6))
        distance = int(random(0, 200))
        #random spawn location per level 2
        guardX_initial = random(xMid, width*1.4)
        
    #generate random starting points for the bodyguard
    elif level >= 3:
       
        #generate larger random wind and distance variables
        wind = int(random(-10, 11))
        distance = int(random(100, 401))
        
        spawn_coordinates = int(random(3))
    
        #limit guard direction relativ to its starting point
        if spawn_coordinates == 0:
            direction = 4
        elif spawn_coordinates == 1:
            direction = 1
        elif spawn_coordinates == 2:
            direction = 2
        elif spawn_coordinates == 3:
            direction = 3
            
        
        
        #update bodyguard coordinates for level 3+
        guardX_initial = guard_spawnX[spawn_coordinates]
        guardY_initial = guard_spawnY[spawn_coordinates]
        civilianAlive = True
        
    guardKilled = False
    
    cursor()

    
def gameOver():
    
    #background_image
    imageMode(CENTER)
    image(menu, xMid, yMid)
    
    #Display Time Left
    fill(255)
    textAlign(LEFT,TOP)
    textSize(45)
    text("Time Left: " + str(timeleft) + "s", hudText_x, 10)
    
    #Displays Bodyguards Killed
    text("V.I.Ps Killed: " + str(targetCount), hudText_x, 75)
    
    #Displays Game Over Message
    image(game_over_text, xMid, height/5.5)
    
    #Display Buttons
    image(restart_game, xMid, height/1.75)
    image(exit_game, xMid, height/1.25)
    
    #Display Game Over Reason
    gameOver_conditions = [
    [not civilianAlive, "YOU KILLED A CIVILIAN!"],
    [timeleft == 0, "YOU RAN OUT OF TIME!"],
    [ammo_mag == 0 and ammo_reserve == 0, "YOU RAN OUT OF BULLETS!"]
    ]
    
    for lose_condition, lose_reason in gameOver_conditions:
        if lose_condition:
            textAlign(CENTER)
            text(lose_reason, gameOver_x, gameOver_y)
            textAlign(LEFT)
            break
    
    cursor()

    
    

def mousePressed():
    global ammo_mag, ammo_reserve, gameState, targetCount, civilianAlive, distance, guardKilled, level, startTime, dx
    
    #check if in-game or not
    if gameState >= 1 and mouseButton == LEFT:
        
        #deduct fired bullets
        if ammo_mag > 0:
            ammo_mag -= 1
            
            #corrected_bullet_trajectory using wind and distance variables
            
            #scale relative to sniper scope
            wind_offset = 11 * wind
            if distance > 100: #distance < 100 is negligible
                distance_actual = distance - 100
                
                if distance <= 200:
                    distance_offset = 0.38 * distance_actual
                elif distance <= 300:
                    distance_offset = 0.41 * distance_actual
                elif distance <= 400:
                    distance_offset = 0.43 * distance_actual
            else:
                distance_offset = 0
            
            #civilian_hitbox
            if gameState == 3:
                civ_male_hitbox_x_left = 779 - wind_offset
                civ_male_hitbox_x_right = civ_male_hitbox_x_left + 33
                civ_male_hitbox_y_top = 225 - distance_offset
                civ_male_hitbox_y_bottom = civ_male_hitbox_y_top + 36
                
                civ_female_hitbox_x_left = 254 - wind_offset
                civ_female_hitbox_x_right = civ_female_hitbox_x_left + 24
                civ_female_hitbox_y_top = 473 - distance_offset
                civ_female_hitbox_y_bottom = civ_female_hitbox_y_top + 28
                
                #game over if civilian is shot
                if civ_male_hitbox_x_left <= mouseX <= civ_male_hitbox_x_right and civ_male_hitbox_y_top <= mouseY <= civ_male_hitbox_y_bottom or civ_female_hitbox_x_left <= mouseX <= civ_female_hitbox_x_right and civ_female_hitbox_y_top <= mouseY <= civ_female_hitbox_y_bottom and civilianAlive == True:
                    civilianAlive = False
                    
                if civilianAlive == False:
                    gameState = -1

                
            #bodyguard_head_hitbox
            head_hitbox_x_left =  guardX - wind_offset
            head_hitbox_x_right = head_hitbox_x_left + head_w
            head_hitbox_y_top = guardY - distance_offset
            head_hitbox_y_bottom = head_hitbox_y_top + head_h
                
            #check_for_hitbox
            if head_hitbox_x_left <= scope_w <= head_hitbox_x_right and head_hitbox_y_top <= scope_h <= head_hitbox_y_bottom:
                #kill_registered
                targetCount += 1
                guardKilled = True
                
            #Mission Complete if bodyguard is killed
            if guardKilled == True:
                level += 1
                gameState = -2
    
    #Start_Game or Restart_Game or Next_Level
    elif 465 <= mouseX <= 818 and 530 <= mouseY <= 638:
        if gameState == 0:
            gameState = 1
            ammo_mag = 5
            ammo_reserve = 15
        elif gameState == -1:
            gameState = 0
        elif gameState == -2:
            ammo_mag = 5
            ammo_reserve = 15
            startTime = millis() #reset timer for next level
            gameState = min(3, level)
            if level > 3:
                dx += 0.5
            
    #Exit_Game_Button
    elif 465 <= mouseX <= 818 and 766 <= mouseY <= 874:
            exit()
        

        
        
def keyPressed():
    global ammo_mag, ammo_reserve
        
    #reload_start
    if gameState >= 1:
        if key == "r" or key == "R":
            ammo_tbl = 5 - ammo_mag #tbl = to be loaded
            
            #full magazine condition
            if ammo_reserve - ammo_tbl >= 0:
                ammo_mag += ammo_tbl
                ammo_reserve -= ammo_tbl
                
            else:  #when ammo_reserve < 5
                ammo_mag += ammo_reserve
                ammo_reserve = 0
    #reload_end
