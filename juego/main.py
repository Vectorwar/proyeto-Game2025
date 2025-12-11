"""This is a pilot test file for the juego package.
create by Jose juan Padilla"""
import pygame
import random
import sqlite3
from datetime import datetime 

pygame.init()

# Database setup
def init_database():
    """Initialize the SQLite database and create the scores table"""
    conn = sqlite3.connect('space_rain_scores.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_score(player_name, score):
    """Save a score to the database"""
    conn = sqlite3.connect('space_rain_scores.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO scores (player_name, score, date) VALUES (?, ?, ?)',
                   (player_name, score, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def get_top_scores(limit=10):
    """Get the top scores from the database"""
    conn = sqlite3.connect('space_rain_scores.db')
    cursor = conn.cursor()
    cursor.execute('SELECT player_name, score, date FROM scores ORDER BY score DESC LIMIT ?', (limit,))
    top_scores = cursor.fetchall()
    conn.close()
    return top_scores

def show_start_menu(screen, width, height):
    """Display start menu and get player name"""
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    
    player_name = ""
    input_active = True
    
    while input_active:
        screen.fill((0, 20, 40))
        
        # Title
        title_text = font_large.render("SPACE RAIN", True, (255, 215, 0))
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 80))
        
        # Subtitle
        subtitle_text = font_small.render("Dodge the meteors and survive!", True, (200, 200, 200))
        screen.blit(subtitle_text, (width // 2 - subtitle_text.get_width() // 2, 160))
        
        # Instructions
        instructions = [
            "Controls:",
            "Arrow Keys - Move",
            "ESC - Quit"
        ]
        y_pos = 240
        for instruction in instructions:
            inst_text = font_small.render(instruction, True, (150, 150, 255))
            screen.blit(inst_text, (width // 2 - inst_text.get_width() // 2, y_pos))
            y_pos += 40
        
        # Name input box
        input_label = font_medium.render("Enter Your Name:", True, (255, 255, 255))
        screen.blit(input_label, (width // 2 - input_label.get_width() // 2, 380))
        
        # Input box background
        input_box = pygame.Rect(width // 2 - 150, 440, 300, 50)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        pygame.draw.rect(screen, (30, 30, 60), input_box)
        
        # Display player name
        name_text = font_medium.render(player_name, True, (255, 255, 255))
        screen.blit(name_text, (input_box.x + 10, input_box.y + 10))
        
        # Start instruction
        start_text = font_small.render("Press ENTER to Start", True, (0, 255, 0))
        screen.blit(start_text, (width // 2 - start_text.get_width() // 2, 520))
        
        # Create by Jose Juan Padilla
        credit_text = font_small.render("Created by Jose Juan Padilla", True, (200, 200, 200))
        screen.blit(credit_text, (width - credit_text.get_width() - 10, height - 30))
        
        # extra message
        extra_text = font_small.render("Star wars es bueno, pero StarTrek es mejor !", True, (200, 200, 200))
        screen.blit(extra_text, (30, 30))
        pygame.display.flip() 
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_name.strip():  # Only start if name is not empty
                        return player_name.strip()
                elif event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 15:  # Limit name length
                        player_name += event.unicode
    
    return None

def show_game_over_screen(screen, player_name, final_score, width, height):
    """Display game over screen with top scores"""
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    font_tiny = pygame.font.Font(None, 28)
    
    screen.fill((20, 0, 0))
    
    # game over text
    game_over_text = font_large.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, 30))
    
    # player info
    player_text = font_medium.render(f"{player_name}: {final_score}", True, (255, 255, 255))
    screen.blit(player_text, (width // 2 - player_text.get_width() // 2, 120))
    
    # top 10 scores
    top_scores = get_top_scores(10)
    title_text = font_medium.render("TOP 10 SCORES", True, (255, 215, 0))
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 180))
    
    # table headers
    header_text = font_tiny.render("#   Player              Score    Date", True, (150, 150, 150))
    screen.blit(header_text, (50, 240))
    
    for i, (name, score, date) in enumerate(top_scores, 1):
        # Truncate name if too long
        display_name = name[:12] + "..." if len(name) > 12 else name
        score_line = font_tiny.render(
            f"{i:<3} {display_name:<15} {score:<8} {date[:10]}", 
            True, 
            (255, 255, 0) if name == player_name and score == final_score else (255, 255, 255)
        )
        screen.blit(score_line, (50, y_position))
        y_position += 30
    
    # instructions
    continue_text = font_small.render("Press SPACE to play again or ESC to quit", True, (200, 200, 200))
    screen.blit(continue_text, (width // 2 - continue_text.get_width() // 2, height - 40))
    
    pygame.display.flip()
    
    # wait for player input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False
    return False

# Initialize database
init_database()

# Screen dimensions
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Rain Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Music of game
pygame.mixer.init()
try:
    pygame.mixer.Sound(r"C:\Users\ThinkPad\OneDrive\Desktop\proyeto-Game2025\juego\Scripts\assets\audio\vader.mp3").play(-1)
except:
    print("Background music not found")

# Player properties
player_width = 70
player_height = 70

# Load images
try:
    player_image = pygame.image.load("nave.png").convert_alpha()
    meteor_image = pygame.image.load("meteor.png").convert_alpha()
    background_image = pygame.image.load("fondo.png").convert()
    
    # Resize images
    player_size = (70, 70)
    meteor_size = (50, 50)
    player_image = pygame.transform.scale(player_image, player_size)
    meteor_image = pygame.transform.scale(meteor_image, meteor_size)
    background_image = pygame.transform.scale(background_image, (width, height))
except:
    print("Images not found, using colored rectangles")
    player_image = None
    meteor_image = None
    background_image = None

# Meteor properties
meteor_width = 50
meteor_height = 50

# Game clock
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Main game loop
game_active = True
while game_active:
    # Show start menu and get player name
    player_name = show_start_menu(screen, width, height)
    
    if player_name is None:
        game_active = False
        continue
    
    # Reset game variables
    player = pygame.Rect(width // 2 - player_width // 2,
                         height - player_height - 10,
                         player_width,
                         player_height)
    meteors = []
    score = 0
    running = True
    
    # Background scroll variables
    bg_y1 = 0
    bg_y2 = -height
    bg_scroll_speed = 2
    
    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_active = False
        
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.right < width:
            player.x += 5
        if keys[pygame.K_UP] and player.top > 0:
            player.y -= 5
        if keys[pygame.K_DOWN] and player.bottom < height:
            player.y += 5
        
        # Meteor generation
        if len(meteors) < 7:
            meteor = pygame.Rect(random.randint(0, width - meteor_width),
                                 0, meteor_width, meteor_height)
            meteors.append(meteor)
        
        # Meteor movement
        for meteor in meteors[:]:
            meteor.y += 5
            if meteor.top > height:
                meteors.remove(meteor)
                score += 1
        
        # Collision detection
        for meteor in meteors:
            if player.colliderect(meteor):
                try:
                    pygame.mixer.Sound(r"C:\Users\ThinkPad\OneDrive\Desktop\proyeto-Game2025\juego\Scripts\assets\audio\aoom.mp3").play()
                except:
                    pass
                
                # Save score to database with player name
                save_score(player_name, score)
                
                pygame.time.delay(1000)
                running = False
        
        # Drawing
        screen.fill(black)
        
        # Mover el fondo
        bg_y1 += bg_scroll_speed
        bg_y2 += bg_scroll_speed
        
        # Reset posición cuando el fondo sale de la pantalla
        if bg_y1 >= height:
            bg_y1 = -height
        if bg_y2 >= height:
            bg_y2 = -height
        
        # Dibujar dos copias del fondo para efecto continuo
        if background_image:
            screen.blit(background_image, (0, bg_y1))
            screen.blit(background_image, (0, bg_y2))
        
        if player_image:
            screen.blit(player_image, player)
        else:
            pygame.draw.rect(screen, red, player)
        
        for meteor in meteors:
            if meteor_image:
                screen.blit(meteor_image, meteor)
            else:
                pygame.draw.rect(screen, white, meteor)
        
        # Score display
        score_text = font.render(f"{player_name}: {score}", True, white)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    # Show game over screen if still active
    if game_active:
        game_active = show_game_over_screen(screen, player_name, score, width, height)

pygame.quit()