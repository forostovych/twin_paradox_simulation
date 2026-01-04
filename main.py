import pygame
import math
import webbrowser


WIDTH, HEIGHT = 1400, 900
FPS = 60
COLOR_BG = (15, 18, 25)
COLOR_PANEL = (30, 35, 45)
COLOR_TRACK = (60, 60, 75)
COLOR_TEXT_MAIN = (220, 220, 220)
COLOR_TEXT_DIM = (150, 150, 170)
COLOR_ACCENT = (100, 200, 255)
COLOR_BTN = (46, 204, 113)
COLOR_INPUT_BG = (20, 20, 30)
COLOR_INPUT_BORDER = (100, 100, 120)
COLOR_INFO_VAL = (255, 200, 80)
COLOR_SLIDER = (100, 255, 150)


GITHUB_URL = "https://github.com/forostovych/twin_paradox_simulation"
LINK_COLOR = (120, 200, 255)
LINK_HOVER = (180, 230, 255)
HELP_TEXT = "Help"
HELP_COLOR = (120, 200, 255)
HELP_HOVER = (180, 230, 255)


SHOW_HELP = False
HELP_LINES = [
    "Twin Paradox Simulator (Special Relativity)",
    "",
    "1) Speed (c): click+drag inside the box or type (0..0.999999999).",
    "2) Dist. (ly): enter distance in light-years.",
    "3) Duration (s): how many seconds the whole trip lasts on screen.",
    "4) Press START. PAUSE stops. RESET resets both scenarios.",
    "5) After return, DIFF shows how much more time passed on Earth.",
    "",
    "Hotkeys: H = Help, ESC = Close Help",
]


C_LIGHT_KM_S = 299792.458
LY_IN_KM = 9_460_730_472_580.8
CURRENT_SCALE = 150.0


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Twin Paradox: Clean Layout")
font_ui = pygame.font.SysFont("segoeui", 14)
font_mono = pygame.font.SysFont("consolas", 16)
font_val = pygame.font.SysFont("consolas", 14)
font_large = pygame.font.SysFont("segoeui", 22, bold=True)
font_huge = pygame.font.SysFont("segoeui", 26, bold=True)


def draw_text_link(screen, text, rect, color, hover_color):
    col = hover_color if rect.collidepoint(pygame.mouse.get_pos()) else color
    surf = font_ui.render(text, True, col)
    screen.blit(surf, rect)
    return rect


def draw_help_link(screen):
    text = "Help"
    surf = font_ui.render(text, True, LINK_COLOR)
    rect = surf.get_rect(topright=(WIDTH - 15, 35))  # ниже GitHub

    if rect.collidepoint(pygame.mouse.get_pos()):
        surf = font_ui.render(text, True, LINK_HOVER)

    screen.blit(surf, rect)
    return rect


def draw_github_link(screen):
    text = "GitHub"
    rect = font_ui.render(text, True, LINK_COLOR).get_rect(topright=(WIDTH - 15, 15))

    color = LINK_HOVER if rect.collidepoint(pygame.mouse.get_pos()) else LINK_COLOR
    surf = font_ui.render(text, True, color)
    screen.blit(surf, rect)
    return rect


def get_help_close_rect():
    w, h = 860, 360
    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2
    return pygame.Rect(x + w - 44, y + 14, 30, 30)


def draw_help_overlay(screen):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    screen.blit(overlay, (0, 0))

    w, h = 860, 360
    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2
    panel = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, (25, 30, 40), panel, border_radius=14)
    pygame.draw.rect(screen, (90, 100, 120), panel, 2, border_radius=14)

    close_rect = get_help_close_rect()
    pygame.draw.rect(screen, (200, 70, 70), close_rect, border_radius=8)
    x_surf = font_large.render("X", True, (255, 255, 255))
    screen.blit(x_surf, x_surf.get_rect(center=close_rect.center))

    tx = x + 24
    ty = y + 18
    line_h = 22

    for i, line in enumerate(HELP_LINES):
        f = font_large if i == 0 else font_ui
        col = (230, 230, 230) if i == 0 else (190, 190, 205)
        surf = f.render(line, True, col)
        screen.blit(surf, (tx, ty))
        ty += line_h

    return close_rect


def format_time_detailed(years_float):
    """Converts float years to Years Days Hours:Minutes"""
    total_minutes = int(years_float * 525960)
    years = total_minutes // 525960
    rem_m = total_minutes % 525960
    days = rem_m // 1440
    rem_m = rem_m % 1440
    hours = rem_m // 60
    minutes = rem_m % 60
    return f"{years}y {days:03d}d {hours:02d}:{minutes:02d}"


class InputBox:
    def __init__(self, x, y, w, h, text, label, is_speed_slider=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INPUT_BORDER
        self.text = text
        self.label = label
        self.active = False
        self.is_speed_slider = is_speed_slider
        self.dragging = False

    def handle_event(self, event):
        changed = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                if self.is_speed_slider:
                    self.dragging = True
                    self._update_from_mouse(event.pos[0])
                    changed = True
            else:
                self.active = False
                self.dragging = False
            self.color = COLOR_ACCENT if self.active else COLOR_INPUT_BORDER

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and self.is_speed_slider:
                self._update_from_mouse(event.pos[0])
                changed = True

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = COLOR_INPUT_BORDER
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                changed = True
            else:
                self.text += event.unicode
                changed = True
        return changed

    def _update_from_mouse(self, mouse_x):
        x = max(self.rect.left, min(mouse_x, self.rect.right))
        ratio = (x - self.rect.left) / self.rect.width
        val = 0.0
        if ratio < 0.5:
            val = ratio * 1.8
        else:
            t = (ratio - 0.5) * 2
            k = 1 + t * 8
            val = 1.0 - math.pow(10, -k)
        if val > 0.99:
            self.text = f"{val:.8f}".rstrip("0")
        else:
            self.text = f"{val:.2f}"

    def draw(self, screen):
        lbl_surf = font_ui.render(self.label, True, COLOR_TEXT_DIM)
        screen.blit(lbl_surf, (self.rect.x, self.rect.y - 20))

        pygame.draw.rect(screen, COLOR_INPUT_BG, self.rect)

        if self.is_speed_slider:
            try:
                val = float(self.text)
                if 0 <= val < 1.0:
                    ratio = 0.0
                    if val <= 0.9:
                        ratio = val / 1.8
                    else:
                        try:
                            k = -math.log10(1 - val)
                            ratio = 0.5 + ((k - 1) / 8) * 0.5
                        except:
                            ratio = 1.0
                    fill_w = int(self.rect.width * min(ratio, 1.0))
                    pygame.draw.rect(
                        screen,
                        COLOR_SLIDER,
                        (self.rect.x, self.rect.y + self.rect.height - 4, fill_w, 4),
                    )
            except ValueError:
                pass

        pygame.draw.rect(screen, self.color, self.rect, 2)

        txt_surf = font_mono.render(self.text, True, COLOR_TEXT_MAIN)
        screen.blit(
            txt_surf,
            (self.rect.x + 10, self.rect.y + (self.rect.height - txt_surf.get_height()) // 2),
        )

    def get_value(self):
        try:
            if not self.text or self.text == "-":
                return 0.0
            val = float(self.text)
            return max(0.0, val)
        except ValueError:
            return 0.0


class Button:
    def __init__(self, x, y, w, h, text, callback, color=COLOR_BTN):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.base_color = color
        self.current_color = color

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = tuple(min(c + 20, 255) for c in self.base_color)
            else:
                self.current_color = self.base_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=8)
        txt_surf = font_large.render(self.text, True, (255, 255, 255))
        rect_txt = txt_surf.get_rect(center=self.rect.center)
        screen.blit(txt_surf, rect_txt)


class Simulation:
    def __init__(self, idx, y_center, color, default_v, default_dist):
        self.idx = idx
        self.y_center = y_center
        self.color = color

        self.panel_rect = pygame.Rect(50, self.y_center - 130, WIDTH - 100, 280)
        self.y_track = y_center + 10
        self.y_timers = y_center - 50
        self.y_status = y_center - 90

        self.y_inputs_1 = y_center + 90

        self.v_c = default_v
        self.dist_ly = default_dist
        self.global_anim_dur = 5.0

        self.update_params(self.v_c, self.dist_ly, self.global_anim_dur)
        self.reset()

    def update_params(self, v, dist, anim_dur):
        self.v_c = max(0.00001, v)
        self.dist_ly = dist
        self.global_anim_dur = max(0.1, anim_dur)

        safe_v = min(self.v_c, 0.999999999)
        self.gamma = 1 / math.sqrt(1 - safe_v**2) if safe_v < 1 else 0

        self.total_trip_years_earth = (2 * self.dist_ly / self.v_c)

        if self.total_trip_years_earth > 0:
            self.time_multiplier = self.total_trip_years_earth / self.global_anim_dur
        else:
            self.time_multiplier = 1.0

        track_width = self.dist_ly * CURRENT_SCALE
        self.start_x = (WIDTH - track_width) // 2
        self.end_x = self.start_x + track_width

        if not is_running:
            self.ship_x = self.start_x

    def reset(self):
        self.earth_time = 0.0
        self.ship_time = 0.0
        self.direction = 1
        self.finished = False
        self.ship_x = self.start_x

    def update(self, dt_real_seconds):
        if self.finished:
            return

        dt_years = dt_real_seconds * self.time_multiplier

        self.earth_time += dt_years

        dt_ship = dt_years / self.gamma
        move_px = (self.v_c * CURRENT_SCALE) * dt_years

        if self.direction == 1:
            self.ship_x += move_px
            if self.ship_x >= self.end_x:
                self.ship_x = self.end_x
                self.direction = -1

        elif self.direction == -1:
            self.ship_x -= move_px
            if self.ship_x <= self.start_x:
                self.ship_x = self.start_x
                self.finished = True

        self.ship_time += dt_ship

    def draw_conversions(self, screen, input_x_pos):
        km_s = self.v_c * C_LIGHT_KM_S
        km_h = km_s * 3600

        str_km_s = f"{km_s:,.0f} KM/S".replace(",", " ")
        str_km_h = f"{km_h:,.0f} KM/H".replace(",", " ")

        x_start = input_x_pos + 110
        label_kms = font_ui.render("KM/S", True, COLOR_TEXT_DIM)
        val_kms = font_val.render(str_km_s, True, COLOR_INFO_VAL)
        screen.blit(label_kms, (x_start, self.y_inputs_1 - 20))
        screen.blit(val_kms, (x_start, self.y_inputs_1 + 5))

        label_kmh = font_ui.render("KM/H", True, COLOR_TEXT_DIM)
        val_kmh = font_val.render(str_km_h, True, COLOR_INFO_VAL)
        screen.blit(label_kmh, (x_start + 160, self.y_inputs_1 - 20))
        screen.blit(val_kmh, (x_start + 160, self.y_inputs_1 + 5))

        dist_input_x = self.panel_rect.x + 620 + 100

        total_km = self.dist_ly * LY_IN_KM
        million_km = total_km / 1_000_000

        str_mil = f"= {million_km:,.0f} million km".replace(",", " ")

        label_dist = font_ui.render("Distance in km", True, COLOR_TEXT_DIM)
        val_dist = font_val.render(str_mil, True, (255, 150, 150))

        screen.blit(label_dist, (dist_input_x, self.y_inputs_1 - 20))
        screen.blit(val_dist, (dist_input_x, self.y_inputs_1 + 5))

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_PANEL, self.panel_rect, border_radius=15)
        title = font_large.render(f"Scenario #{self.idx}", True, COLOR_TEXT_DIM)
        screen.blit(title, (self.panel_rect.x + 25, self.panel_rect.y + 15))

        str_earth = "Earth: " + format_time_detailed(self.earth_time)
        str_ship = "Ship: " + format_time_detailed(self.ship_time)

        if self.finished:
            diff = self.earth_time - self.ship_time
            txt_status = f"DIFF: {format_time_detailed(diff)} ({diff:.1f} y)"
            col_status = (100, 255, 120)
        else:
            txt_status = "• TRAVELING •"
            col_status = COLOR_ACCENT

        surf_e = font_mono.render(str_earth, True, COLOR_TEXT_MAIN)
        surf_s = font_mono.render(str_ship, True, self.color)
        surf_stat = font_huge.render(txt_status, True, col_status)

        stat_x = WIDTH // 2 - surf_stat.get_width() // 2
        screen.blit(surf_stat, (stat_x, self.y_status))

        earth_x = self.panel_rect.x + 40
        screen.blit(surf_e, (earth_x, self.y_timers))
        ship_x = (self.panel_rect.x + self.panel_rect.width) - surf_s.get_width() - 40
        screen.blit(surf_s, (ship_x, self.y_timers))

        pygame.draw.line(screen, COLOR_TRACK, (self.start_x, self.y_track), (self.end_x, self.y_track), 4)
        pygame.draw.circle(screen, (70, 130, 255), (int(self.start_x), int(self.y_track)), 18)
        pygame.draw.circle(screen, (255, 90, 90), (int(self.end_x), int(self.y_track)), 18)

        label_e = font_ui.render("Earth", True, COLOR_TEXT_DIM)
        label_p = font_ui.render("Planet", True, COLOR_TEXT_DIM)
        screen.blit(label_e, (self.start_x - 20, self.y_track + 25))
        screen.blit(label_p, (self.end_x - 30, self.y_track + 25))

        ship_w, ship_h = 25, 16
        pts = [
            (self.ship_x + ship_w / 2 * self.direction, self.y_track),
            (self.ship_x - ship_w / 2 * self.direction, self.y_track - ship_h / 2),
            (self.ship_x - ship_w / 2 * self.direction, self.y_track + ship_h / 2),
        ]
        pygame.draw.polygon(screen, self.color, pts)


sims = []
sim_inputs = []
global_input_dur = None
is_running = False


def calculate_auto_scale():
    global CURRENT_SCALE
    max_dist = 0.0
    step = 2
    for i in range(len(sims)):
        d = sim_inputs[i * step + 1].get_value()
        if d > max_dist:
            max_dist = d

    available_width = WIDTH - 200
    if max_dist > 0.001:
        CURRENT_SCALE = available_width / max_dist
    else:
        CURRENT_SCALE = 150.0


def sync_sim_params():
    calculate_auto_scale()
    glob_dur = global_input_dur.get_value()

    step = 2
    for i, sim in enumerate(sims):
        v_val = sim_inputs[i * step].get_value()
        d_val = sim_inputs[i * step + 1].get_value()
        sim.update_params(v_val, d_val, glob_dur)


def cb_start():
    global is_running
    sync_sim_params()
    is_running = True
    for sim in sims:
        if sim.finished:
            sim.reset()


def cb_pause():
    global is_running
    is_running = False


def cb_reset():
    global is_running
    is_running = False
    sync_sim_params()
    for sim in sims:
        sim.reset()


def create_inputs_for_sim(sim, base_y):
    inp_v = InputBox(sim.panel_rect.x + 20, base_y, 80, 35, str(sim.v_c), "Speed (c)", is_speed_slider=True)
    inp_d = InputBox(sim.panel_rect.x + 620, base_y, 80, 35, str(sim.dist_ly), "Dist. (ly)")
    return [inp_v, inp_d]


def init_app():
    global global_input_dur
    s1 = Simulation(1, 220, (255, 230, 0), 0.1, 1.0)
    sims.append(s1)
    sim_inputs.extend(create_inputs_for_sim(s1, s1.y_inputs_1))
    s2 = Simulation(2, 570, (0, 240, 240), 0.9, 1.0)
    sims.append(s2)
    sim_inputs.extend(create_inputs_for_sim(s2, s2.y_inputs_1))
    btn_start_x = WIDTH // 2 - 180
    global_input_dur = InputBox(btn_start_x - 140, HEIGHT - 75, 100, 45, "5.0", "Duration (s)")
    sync_sim_params()


buttons = [
    Button(WIDTH // 2 - 180, HEIGHT - 80, 110, 50, "START", cb_start),
    Button(WIDTH // 2 - 60, HEIGHT - 80, 110, 50, "PAUSE", cb_pause, color=(200, 150, 50)),
    Button(WIDTH // 2 + 60, HEIGHT - 80, 110, 50, "RESET", cb_reset, color=(200, 70, 70)),
]


def main():
    global SHOW_HELP

    init_app()
    clock = pygame.time.Clock()
    running = True
    github_rect = font_ui.render("GitHub", True, LINK_COLOR).get_rect(topright=(WIDTH - 15, 15))
    help_rect   = font_ui.render("Help",  True, LINK_COLOR).get_rect(topright=(WIDTH - 15, 35))

    while running:
        dt = clock.tick(FPS) / 1000.0

        help_close_rect = get_help_close_rect()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    SHOW_HELP = not SHOW_HELP
                if SHOW_HELP and event.key == pygame.K_ESCAPE:
                    SHOW_HELP = False

            if SHOW_HELP:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if help_close_rect.collidepoint(event.pos):
                        SHOW_HELP = False
                continue

            any_changed = False
            for box in sim_inputs:
                if box.handle_event(event):
                    any_changed = True

            if global_input_dur.handle_event(event):
                any_changed = True

            if any_changed:
                sync_sim_params()

            for btn in buttons:
                btn.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if github_rect.collidepoint(event.pos):
                    webbrowser.open(GITHUB_URL)
                elif help_rect.collidepoint(event.pos):
                    SHOW_HELP = True

        if is_running:
            for sim in sims:
                sim.update(dt)

        screen.fill(COLOR_BG)

        for i, sim in enumerate(sims):
            sim.draw(screen)
            input_x = sim_inputs[i * 2].rect.x
            sim.draw_conversions(screen, input_x)

        for box in sim_inputs:
            box.draw(screen)

        global_input_dur.draw(screen)

        for btn in buttons:
            btn.draw(screen)

        github_rect = draw_github_link(screen)

        help_color = LINK_HOVER if help_rect.collidepoint(pygame.mouse.get_pos()) else LINK_COLOR
        help_surf = font_ui.render("Help", True, help_color)
        help_rect = help_surf.get_rect(topright=(WIDTH - 15, 35))
        screen.blit(help_surf, help_rect)

        if SHOW_HELP:
            draw_help_overlay(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
