import pygame as pg
import serial
import config
pg.init()

RED = (0xFF, 0x00, 0x00)
BLACK = (0x00, 0x00, 0x00)

class Pixel:    #using pixel class to track and control individual pixels that will be sent to the arduino as they are updated
    def __init__(self, xPos:int, yPos:int, rect:pg.Rect, index: int):
        self.state = False
        self.index = index  #just here in case the pixels some how get out of order in the list.
        self.x = xPos
        self.y = yPos
        self.rect = rect
        self.rect.center = (self.x, self.y)

    def toggle_state(self, mouse_x, mouse_y):
        if self.rect.left <= mouse_x <= self.rect.right:
            if self.rect.top <= mouse_y <= self.rect.bottom:
                self.state = not(self.state)
    
    def draw_surface(self, screen: pg.Surface, surfaces: list):
        screen.blit(surfaces[self.state], self.rect)



def send_serial(data:bytes, device:serial.Serial):  #will send 12 bytes to the arduino that will be used by the device to draw the frame on the matrix
    device.write(data)
    
def get_bytes(pixels: list):
    data_string = ''
    for pix in pixels:
        pix: Pixel
        data_string += str(int(pix.state))
    data = int(data_string, 2).to_bytes(12)
    return data

def format_bytes(pixels: list): #formats bytes for use in uint32_t format for arduino and prints in terminal for user to copy and paste.  Be sure to update variable name in arduino sketch
    number = []
    for p in pixels:
        if p.state == True:
            number.append('1')
        else:
            number.append('0')
    bytes1 = str(hex(int(''.join(number[:32]), 2)))
    bytes2 = str(hex(int(''.join(number[32:64]), 2)))
    bytes3 = str(hex(int(''.join(number[64:]), 2)))
    output = f'uint32_t frame = {{{bytes1}, {bytes2}, {bytes3}}};'
    print(output)

if __name__ == '__main__':
    #setup
    screen_width, screen_height = 800, 600
    columns = 12
    rows = 8
    radius = 25
    thickness = 5
    index = 0
    xSpacer = screen_width / (columns + 1)
    x_list = [int(x * xSpacer) for x in range(1, columns + 1)]
    ySpacer = screen_height / (rows + 1)
    y_list = [int(y * ySpacer) for y in range(1, rows + 1)]
    rect = pg.Rect(0, 0, radius * 2, radius * 2)
    true_surf = pg.Surface(rect.size)
    true_surf.fill(BLACK)
    pg.draw.circle(true_surf, RED, rect.center, radius)
    false_surf = pg.Surface(rect.size)
    false_surf.fill(BLACK)
    surfaces = [false_surf, true_surf]
    pg.draw.circle(false_surf, RED, rect.center, radius, thickness)
    pixel_list = []
    for y in y_list:
        for x in x_list:
            pixel_list.append(Pixel(x, y, rect.copy(), index))
            index += 1
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption('Real Time Matrix Control Arduino')
    arduino = serial.Serial(port = config.port, baudrate = config.baud)
    send_serial(int(0).to_bytes(12), arduino)

    #main loop starts below
    running = True
    update = True
    clicked = False
    p: Pixel
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    format_bytes(pixel_list)
                if event.key == pg.K_r: #resets all pixels to off
                    for p in pixel_list:
                        p.state = False
                        update = True
                if event.key == pg.K_f: #turns all pixels on ('fills')
                    for p in pixel_list:
                        p.state = True
                        update = True
                if event.key == pg.K_u: #updates pixels on arduino manually.  Mostly for debugging.
                    update = True
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                clicked = True
        
        if running and clicked:
            clicked = False
            for p in pixel_list:
                p.toggle_state(mouse_x, mouse_y)
                update = True
        
        if running and update:
            update = False
            screen.fill(BLACK)
            for p in pixel_list:
                p.draw_surface(screen, surfaces)
            matrix_data = get_bytes(pixel_list)
            send_serial(matrix_data, arduino)
            pg.display.flip()
    arduino.write(0x30c79e7fe7fe3fc1f80f0060.to_bytes(12))
    arduino.close()
    pg.quit()
