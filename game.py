# OUSDC Software Speedrun - Game Development Track
# code template adapted from www.pygame.org/docs/
import pygame
import math

# pygame setup
pygame.init()
window = (1280, 720)
screen = pygame.display.set_mode(window)
pygame.display.set_caption('Software Speedrun Cookie Clicker')
clock = pygame.time.Clock()
running = True
dt = 0

cookie_count = 0
cookie_text = str(cookie_count)

upgrade_box_height = 100
upgrades = {
    "cursor": {
        "owned": 0,
        "base_price": 15,
        "current_price": 15,
        "price_multiplier": 1.1,
        "cookies_per_sec": 0.2
    },
    "grandmas": {
        "owned": 0,
        "base_price": 100,
        "current_price": 100,
        "price_multiplier": 1.35,
        "cookies_per_sec": 1
    },
    "farm": {
        "owned": 0,
        "base_price": 1100,
        "current_price": 1100,
        "price_multiplier": 1.35,
        "cookies_per_sec": 8
    },
    "mine": {
        "owned": 0,
        "base_price": 12000,
        "current_price": 12000,
        "price_multiplier": 1.35,
        "cookies_per_sec": 47
    },
    "factory": {
        "owned": 0,
        "base_price": 130000,
        "current_price": 130000,
        "price_multiplier": 1.35,
        "cookies_per_sec": 260
    }
}

def abbreviate_count(count):
    if count >= 1_000_000_000:
        return f"{count / 1_000_000_000:.1f}b"
    elif count >= 1_000_000:
        return f"{count / 1_000_000:.1f}m"
    elif count >= 1_000:
        return f"{count / 1_000:.1f}k"
    else:
        return str(count)

def purchase_upgrade(upgrade_name):
    global cookie_count
    for upgrade, stats in upgrades.items():
        if upgrade != upgrade_name:
            continue
        if cookie_count > stats["current_price"]:
            cookie_count -= stats["current_price"]
            stats["owned"] += 1
            stats["current_price"] = stats["base_price"]*math.pow(stats["price_multiplier"], stats["owned"])

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if math.sqrt(math.pow(pos[1] - window[1]/2, 2) + math.pow(pos[0] - window[0]/4, 2)) < window[0]/8:
                cookie_count += 1
            i = 0
            for upgrade, stats in upgrades.items():
                if pos[0] > window[0]/2 and pos[1] > i*upgrade_box_height and pos[1] < (i+1)*upgrade_box_height:
                    purchase_upgrade(upgrade)
                i += 1
        if event.type == pygame.VIDEORESIZE:
            window = pygame.display.get_window_size()

    ## Add cookies from upgrades
    for upgrade, stats in upgrades.items():
        cookie_count += stats["owned"]*stats["cookies_per_sec"]*dt

    cookie_text = str(round(cookie_count))

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray")

    ## The Cookie
    pygame.draw.rect(screen, "antiquewhite", ((0, 0), (window[0]//2, window[1])))
    pygame.draw.circle(screen, "antiquewhite4", (window[0]/4, window[1]/2), window[0]/8)

    font = pygame.font.Font(None, 100)
    text = font.render(cookie_text, True, (0, 0, 0))
    screen.blit(text, (window[0]/4 - text.get_width()/2, 100))

    ## Upgrades section
    i = 0
    for upgrade, stats in upgrades.items():
        pygame.draw.rect(screen, "antiquewhite2", ((window[0]/2,i*upgrade_box_height), (window[0], upgrade_box_height)))
        pygame.draw.rect(screen, "gray", ((window[0]/2,i*upgrade_box_height), (window[0], upgrade_box_height)), 2)
        
        font = pygame.font.Font(None, 75)
        text = font.render(abbreviate_count(stats["owned"]), True, (0,0,0))
        screen.blit(text, (window[0]/2 + 15, i*upgrade_box_height + upgrade_box_height/2 - text.get_height()/2))
        owned_text_width = text.get_width()
        text = font.render(upgrade, True, (0,0,0))
        screen.blit(text, (window[0]/2 + 30 + owned_text_width, i*upgrade_box_height + upgrade_box_height/2 - text.get_height()/2))
        text = font.render(abbreviate_count(round(stats["current_price"])), True, (0,0,0))
        screen.blit(text, (window[0] - text.get_width() - 15, i*upgrade_box_height + upgrade_box_height/2 - text.get_height()/2))
        i += 1

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
