import pygame, os, random

pygame.init()
#Variables for Game
gameWidth = 1200
gameHeight = 1920
picSize_width = 128
picSize_height = 192
picSize = 128
gameColumns = 7
gameRows = 6
padding = 10
leftMargin = (gameWidth - ((picSize_width + padding) * gameColumns)) // 2
print("Left:", leftMargin)
rightMargin = leftMargin
topMargin = (gameHeight - ((picSize_height + padding) * gameRows)) // 2
bottomMargin = topMargin
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
BLUE = (0,0,255)
font = pygame.font.Font(None, 48)
selection1 = None
selection2 = None


class Button:
    def __init__(self, text, position, size, color, text_color, action):
        self.rect = pygame.Rect(position, size)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

def restart_game():
    global hiddenImages, num_clicks, selection1, selection2, memPics, memPicsRect, hiddenImages, RESTART
    RESTART = False
    hiddenImages = [False] * len(memoryPictures)
    num_clicks = 0
    selection1, selection2 = None, None
    random.shuffle(memoryPictures)
    memPics = []
    memPicsRect = []
    hiddenImages = []
    for item in memoryPictures:
        picture = pygame.image.load(f'images2/{item}.png')
        picture = pygame.transform.scale(picture, (picSize_width, picSize_height))
        memPics.append(picture)
        pictureRect = picture.get_rect()
        memPicsRect.append(pictureRect)

    for i in range(len(memPicsRect)):
        memPicsRect[i][0] = leftMargin + ((picSize_width + padding) * (i % gameColumns))
        memPicsRect[i][1] = topMargin + ((picSize_height + padding) * (i % gameRows))
        hiddenImages.append(False)

def render_click(screen, num_clicks):
    # Render the text on the text surface
    text_surface = pygame.Surface((300, 50))  # You can adjust the size of the surface
    text_surface.fill(WHITE)
    text = font.render(f'Clicks: {num_clicks}', True, BLACK)  # BLACK is the color of the text
    text_rect = text.get_rect(center=(text_surface.get_width() // 2, text_surface.get_height() // 2))
    text_surface.fill(WHITE)  # Clear the surface to the background color
    text_surface.blit(text, text_rect)  # Blit the text onto the surface
    screen.blit(text_surface, (50, 100))

def render_best(screen, best_score):
    # Render the text on the text surface
    text_surface = pygame.Surface((300, 50))  # You can adjust the size of the surface
    text_surface.fill(WHITE)
    text = font.render(f'Best score : {best_score}', True, BLACK)  # BLACK is the color of the text
    text_rect = text.get_rect(center=(text_surface.get_width() // 2, text_surface.get_height() // 2))
    text_surface.fill(WHITE)  # Clear the surface to the background color
    text_surface.blit(text, text_rect)  # Blit the text onto the surface
    screen.blit(text_surface, (820, 100))


# Loading the pygame screen.
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption('Memory Game')
gameIcon = pygame.image.load('images/Apple.png')
pygame.display.set_icon(gameIcon)



# Load the BackGround image into Python
# bgImage = pygame.image.load('Background.png')
# bgImage = pygame.transform.scale(bgImage, (gameWidth, gameHeight))
# bgImageRect = bgImage.get_rect()

# Create list of Memory Pictures
memoryPictures = []
for item in os.listdir('images2/'):
    memoryPictures.append(item.split('.')[0])
memoryPicturesCopy = memoryPictures.copy()
memoryPictures.extend(memoryPicturesCopy)
memoryPicturesCopy.clear()
random.shuffle(memoryPictures)

print(len(memoryPictures))

# Load each of the images into the python memory
memPics = []
memPicsRect = []
hiddenImages = []
for item in memoryPictures:
    picture = pygame.image.load(f'images2/{item}.png')
    picture = pygame.transform.scale(picture, (picSize_width, picSize_height))
    memPics.append(picture)
    pictureRect = picture.get_rect()
    memPicsRect.append(pictureRect)


for i in range(len(memPicsRect)):
    memPicsRect[i][0] = leftMargin + ((picSize_width + padding) * (i % gameColumns))
    memPicsRect[i][1] = topMargin + ((picSize_height + padding) * (i % gameRows))
    hiddenImages.append(False)
print("Len hidden:", len(hiddenImages))
print("hidden:", hiddenImages)


# print(memoryPictures)
# print(memPics)
# print(memPicsRect)
# print(hiddenImages)

num_clicks = 0
best_score = 0
complete = False
gameLoop = True
RESTART = False
restart_button = Button("Restart", (900, 200), (150, 50), BLUE, WHITE, restart_game)


while gameLoop:
    # Load background image
    #screen.blit(bgImage, bgImageRect)
    screen.fill(WHITE)

    # Input events
    for event in pygame.event.get():
        #restart_button.handle_event(event)
        if event.type == pygame.QUIT:
            gameLoop = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if restart_button.rect.collidepoint(event.pos):
                restart_button.action()
            else:
                for item in memPicsRect:
                    if item.collidepoint(event.pos):
                        if hiddenImages[memPicsRect.index(item)] != True:
                            num_clicks += 1
                            if selection1 != None:
                                selection2 = memPicsRect.index(item)
                                hiddenImages[selection2] = True
                            else:
                                selection1 = memPicsRect.index(item)
                                hiddenImages[selection1] = True

    for i in range(len(memoryPictures)):
        if hiddenImages[i] == True:
            screen.blit(memPics[i], memPicsRect[i])
        else:
            pygame.draw.rect(screen, GRAY, (memPicsRect[i][0], memPicsRect[i][1], picSize_width, picSize_height))

    if RESTART:
        restart_button.draw(screen)
    if complete:
        render_best(screen, best_score)
    render_click(screen, num_clicks)
    pygame.display.update()

    if selection1 != None and selection2 != None:
        if memoryPictures[selection1] == memoryPictures[selection2]:
            selection1, selection2 = None, None
        else:
            pygame.time.wait(1000)
            hiddenImages[selection1] = False
            hiddenImages[selection2] = False
            selection1, selection2 = None, None

    win = 1
    for number in range(len(hiddenImages)):
        win *= hiddenImages[number]

    if win == 1:
        RESTART = True
        restart_button.draw(screen)
        if not complete:
            best_score = num_clicks
            complete = True
        else:
            if num_clicks < best_score:
                best_score = num_clicks
        #gameLoop = False
    if complete:
        render_best(screen, best_score)
    render_click(screen, num_clicks)
    pygame.display.update()

pygame.quit()