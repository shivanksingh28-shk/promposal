import pygame
import random
import asyncio

pygame.init()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("A Paws-itive Promposal!")
clock = pygame.time.Clock()

SKY_BLUE = (135, 206, 235) 
GRASS_GREEN = (50, 160, 50)
DARK_GRASS = (40, 130, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (100, 200, 100)
RED = (200, 100, 100)

CONFETTI_COLORS = [
    (255, 0, 0),    
    (0, 255, 0),    
    (0, 0, 255),    
    (255, 255, 0),  
    (255, 165, 0),  
    (255, 105, 180) 
]

class Puppy:
    def __init__(self):

        self.img_open = pygame.image.load('open1.png').convert_alpha()
        self.img_semi = pygame.image.load('open2.png').convert_alpha()
        self.img_closed = pygame.image.load('closed.png').convert_alpha()
        
        self.base_open = pygame.transform.scale(self.img_open, (128, 128))
        self.base_semi = pygame.transform.scale(self.img_semi, (128, 128))
        self.base_closed = pygame.transform.scale(self.img_closed, (128, 128))
        
        self.rect = self.base_open.get_rect(center=(200, 185))
        self.vel_y = 0          
        self.gravity = 0.8      
        self.jump_power = -13   
        self.ground_y = 185     
        
        self.state = "IDLE"
        self.blink_timer = 0

    def update(self):
        if self.rect.centery >= self.ground_y:
            self.rect.centery = self.ground_y
            self.vel_y = 0
            
            if random.random() < 0.015:
                self.vel_y = self.jump_power
                self.state = "JUMPING"
            else:
                if self.state == "JUMPING":
                    self.state = "IDLE"
                    
                if self.state == "IDLE":
                    if random.random() < 0.01: 
                        self.state = "BLINKING"
                        self.blink_timer = 12 
        
        if self.state == "BLINKING":
            self.blink_timer -= 1
            if self.blink_timer <= 0:
                self.state = "IDLE"

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

    def draw(self, surface):
        if self.state == "IDLE" or self.state == "JUMPING":
            current_img = self.base_open
        else:
            if self.blink_timer > 10: current_img = self.base_semi
            elif self.blink_timer > 3: current_img = self.base_closed
            else: current_img = self.base_semi
            
        if self.rect.centery < self.ground_y:
            if self.vel_y < -2:
                anim_img = pygame.transform.scale(current_img, (110, 145))
            elif self.vel_y > 2:
                anim_img = pygame.transform.scale(current_img, (135, 115))
            else:
                anim_img = current_img
            draw_rect = anim_img.get_rect(center=self.rect.center)
        else:
            anim_img = current_img
            draw_rect = self.rect

        surface.blit(anim_img, draw_rect)

bg_low_res = pygame.Surface((100, 100))
pygame.draw.rect(bg_low_res, SKY_BLUE, (0, 0, 100, 50))
pygame.draw.rect(bg_low_res, GRASS_GREEN, (0, 50, 100, 50))

for _ in range(60): 
    rx = random.randint(0, 99)
    ry = random.randint(50, 99)
    pygame.draw.rect(bg_low_res, DARK_GRASS, (rx, ry, 1, 1))

background_img = pygame.transform.scale(bg_low_res, (400, 400))

flower1_img = pygame.image.load('flower1.png').convert_alpha()
flower2_img = pygame.image.load('flower2.png').convert_alpha()
flower3_img = pygame.image.load('flower3.png').convert_alpha()

f_size = (45, 45)
f1 = pygame.transform.scale(flower1_img, f_size)
f2 = pygame.transform.scale(flower2_img, f_size)
f3 = pygame.transform.scale(flower3_img, f_size)
flower_options = [f1, f2, f3]

garden_data = []
cluster_centers = [(50, 270), (330, 270), (80, 350), (320, 350)]

for cx, cy in cluster_centers:
    cluster_flower = random.choice(flower_options)
    for _ in range(random.randint(4, 6)):
        rx = cx + random.randint(-25, 25)
        ry = cy + random.randint(-15, 15)
        garden_data.append((cluster_flower, (rx, ry)))

hero_flower = random.choice(flower_options)
garden_data.append((hero_flower, (120, 210)))
garden_data.sort(key=lambda item: item[1][1])


scale_factor = 2
small_font = pygame.font.Font(None, 18)

def create_pixel_text(text_string):
    text_small = small_font.render(text_string, False, BLACK)
    return pygame.transform.scale(text_small, (text_small.get_width() * scale_factor, text_small.get_height() * scale_factor))

scaled_text1 = create_pixel_text("It would be paws-itively amazing")
scaled_text1_rect = scaled_text1.get_rect(center=(SCREEN_WIDTH // 2, 25))

scaled_text2 = create_pixel_text("if you'd go to prom with me!")
scaled_text2_rect = scaled_text2.get_rect(center=(SCREEN_WIDTH // 2, 55))

yay_text = create_pixel_text("YAY! Best Prom Ever!")
yay_rect = yay_text.get_rect(center=(SCREEN_WIDTH // 2, 40))

yes_btn = pygame.Rect(100, 85, 70, 35)
no_btn = pygame.Rect(230, 85, 70, 35)

yes_text = create_pixel_text("YES")
yes_text_rect = yes_text.get_rect(center=yes_btn.center)

no_text = create_pixel_text("NO")
no_text_rect = no_text.get_rect(center=no_btn.center)


async def main():
    my_dog = Puppy()
    running = True
    prom_accepted = False
    

    confetti_particles = []

    while running:

        screen.blit(background_img, (0, 0))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if yes_btn.collidepoint(event.pos) and not prom_accepted:
                    prom_accepted = True
                    

                    for _ in range(150):
                        cx, cy = yes_btn.center
                        vx = random.uniform(-6, 6)   
                        vy = random.uniform(-12, -4) 
                        color = random.choice(CONFETTI_COLORS)
                        size = random.randint(4, 8)   
                        

                        confetti_particles.append([cx, cy, vx, vy, color, size])
                

                if no_btn.collidepoint(event.pos):
                    pass 


        if not prom_accepted:
            screen.blit(scaled_text1, scaled_text1_rect)
            screen.blit(scaled_text2, scaled_text2_rect)
            
            pygame.draw.rect(screen, GREEN, yes_btn)
            pygame.draw.rect(screen, BLACK, yes_btn, 3) 
            screen.blit(yes_text, yes_text_rect)
            
            pygame.draw.rect(screen, RED, no_btn)
            pygame.draw.rect(screen, BLACK, no_btn, 3) 
            screen.blit(no_text, no_text_rect)
        else:
            screen.blit(yay_text, yay_rect)
            

            for particle in confetti_particles:
                particle[0] += particle[2]  
                particle[1] += particle[3]  
                particle[3] += 0.4          
                

                pygame.draw.rect(screen, particle[4], (particle[0], particle[1], particle[5], particle[5]))


        for flwr_img, flwr_pos in garden_data:
            screen.blit(flwr_img, flwr_pos)


        my_dog.update()
        my_dog.draw(screen)

        pygame.display.flip()
        clock.tick(60)
        
        await asyncio.sleep(0)


asyncio.run(main())
