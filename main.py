import sys
import os
import copy
import json
import glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageTk, ImageOps
import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser

# --- Optional: Modern Color Picker ---
try:
    from CTkColorPicker import AskColor
    HAS_MODERN_PICKER = True
except ImportError:
    HAS_MODERN_PICKER = False

# --- Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Path Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "assets", "ShooterGame")
# UPDATED: Default font set to VetoSans-Medium.ttf in assets folder
DEFAULT_FONT_PATH = os.path.join(BASE_DIR, "assets", "VetoSans-Medium.ttf")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# --- Mappings (RESTORED FULL LIST TO FIX ASSET LOADING) ---
AGENT_ICONS = {
    "Astra": "TX_Killfeed_Astra.png", "Breach": "TX_Killfeed_Breach.png", "Brimstone": "TX_Killfeed_Brimstone.png",
    "Chamber": "TX_Killfeed_Chamber.png", "Clove": "TX_Killfeed_Clove.png", "Cypher": "TX_Killfeed_Cypher.png",
    "Deadlock": "TX_Killfeed_Deadlock.png", "Fade": "TX_Killfeed_Fade.png", "Gekko": "TX_Killfeed_Gekko.png",
    "Harbor": "TX_Killfeed_Mage.png", "Iso": "TX_Killfeed_Iso.png", "Jett": "TX_Killfeed_Jett.png",
    "KAY/O": "TX_Killfeed_KAYO.png", "Killjoy": "TX_Killfeed_Killjoy1.png", "Neon": "TX_Killfeed_Neon.png",
    "Omen": "TX_Killfeed_Omen.png", "Phoenix": "TX_Killfeed_Phoenix.png", "Raze": "TX_Killfeed_Raze.png",
    "Reyna": "TX_Killfeed_Reyna.png", "Sage": "TX_Killfeed_Sage1.png", "Skye": "TX_Killfeed_Skye.png",
    "Sova": "TX_Killfeed_Sova1.png", "Tejo": "TX_Killfeed_Tejo.png", "Veto": "TX_Killfeed_Pine.png",
    "Viper": "TX_Killfeed_Viper.png", "Vyse": "TX_Killfeed_Vyse.png", "Waylay (Iso)": "TX_Killfeed_Waylay.png",
    "Yoru": "TX_Killfeed_Yoru.png",
}

WEAPON_ICONS = {
    "Classic": "TX_Hud_Pistol_Classic.png", "Shorty": "TX_Hud_Pistol_Slim.png", "Frenzy": "TX_Hud_Pistol_AutoPistol.png",
    "Ghost": "TX_Hud_Pistol_Luger.png", "Sheriff": "TX_Hud_Pistol_Sheriff.png", "Stinger": "TX_Hud_SMGs_Vector.png",
    "Spectre": "TX_Hud_SMGs_Ninja.png", "Bucky": "TX_Hud_Shotguns_Pump.png", "Judge": "TX_Hud_Shotguns_Persuader.png",
    "Bulldog": "TX_Hud_Rifles_Burst.png", "Guardian": "TX_Hud_Rifles_DMR.png", "Phantom": "TX_Hud_Rifles_Ghost.png",
    "Vandal": "TX_Hud_Rifles_Volcano.png", "Marshal": "TX_Hud_Sniper_Bolt.png", "Operator": "TX_Hud_Sniper_Operater.png",
    "Ares": "TX_Hud_LMG.png", "Odin": "TX_Hud_HMG.png", "Knife": "TX_Hud_Knife_Standard.png",
    "Raze: Showstopper": "TX_Clay_RocketLauncher.png", "Jett: Blade Storm": "TX_Wushu_Daggers.png",
    "Sova: Hunter's Fury": "TX_Hunter_BowBlast.png", "Chamber: Headhunter": "TX_Hud_Deadeye_Q_Pistol.png",
    "Chamber: Tour de Force": "TX_Hud_Deadeye_X_GiantSlayer.png",
}

# --- Helpers ---
def hex_to_rgb(hex_col):
    if not hex_col: return (255, 255, 255)
    h = hex_col.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    safe_rgb = tuple(int(c) for c in rgb[:3])
    return '#%02x%02x%02x' % safe_rgb

def colorize_image(img, color):
    if img.mode != 'RGBA': img = img.convert('RGBA')
    color_layer = Image.new('RGBA', img.size, color)
    return Image.composite(color_layer, Image.new('RGBA', img.size, (0,0,0,0)), img)

def create_gradient(width, height, start_col, end_col, angle=180):
    base = Image.new('RGBA', (width, height), start_col)
    top = Image.new('RGBA', (width, height), end_col)
    mask = Image.new('L', (width, height))
    mask_data = []
    is_vertical = abs(angle - 180) < 45 or abs(angle) < 45
    for y in range(height):
        for x in range(width):
            ratio = y / max(1, height) if is_vertical else x / max(1, width)
            if angle == 0 or angle == 360: ratio = 1.0 - ratio
            mask_data.append(int(255 * ratio))
    mask.putdata(mask_data)
    return Image.composite(top, base, mask)

# --- Renderer ---
class KillfeedRenderer:
    def __init__(self):
        self.cache = {}
        self.base_font_size = 22

    def get_font(self, path, size):
        try: return ImageFont.truetype(path, size)
        except: return ImageFont.load_default()

    def get_image(self, name, folder_scan=True):
        fname = AGENT_ICONS.get(name) or WEAPON_ICONS.get(name) or name
        # Check cache first
        if fname in self.cache: return self.cache[fname]
        
        path = os.path.join(ASSET_PATH, fname)
        
        # If direct path doesn't exist, scan subfolders
        if not os.path.exists(path) and folder_scan:
            for root, dirs, files in os.walk(os.path.join(BASE_DIR, "assets")):
                if fname in files: 
                    path = os.path.join(root, fname)
                    break
        
        try:
            img = Image.open(path).convert("RGBA")
            self.cache[fname] = img
            return img
        except: 
            # Cache failure to avoid re-scanning
            empty = Image.new("RGBA", (10,10), (0,0,0,0))
            self.cache[fname] = empty
            return empty

    def render(self, entries, global_s, scale=1.0):
        # Use row height from global settings
        row_h = int(global_s['height'] * scale)
        spacing = int(global_s.get('row_spacing', 2) * scale)
        safe_padding = int(60 * scale)
        
        total_h = max(int(100*scale), len(entries) * (row_h + spacing) + (safe_padding * 2))
        canvas_w = int(global_s['width'] * scale) + (safe_padding * 2)
        
        bg_mode = global_s.get('export_bg_mode', 'Transparent')
        if bg_mode == 'Solid Color':
            col = tuple(int(c) for c in global_s.get('export_bg_color', (0,0,0))[:3])
            canvas = Image.new('RGBA', (canvas_w, total_h), col + (255,))
        elif bg_mode == 'Match Gradient':
            b_start = tuple(int(c) for c in global_s['border_start'][:3])
            b_end = tuple(int(c) for c in global_s['border_end'][:3])
            canvas = create_gradient(canvas_w, total_h, b_start, b_end, global_s['border_angle'])
        else:
            canvas = Image.new('RGBA', (canvas_w, total_h), (0,0,0,0))

        y = safe_padding
        
        # Font Logic - Always use DEFAULT_FONT_PATH since customization is removed
        font_path = DEFAULT_FONT_PATH
        base_size = global_s.get('font_size', 22)
        font = self.get_font(font_path, int(base_size * scale))
        
        for entry in entries:
            row_settings = global_s
                
            row_img = self.render_row(entry, row_settings, scale, font, safe_padding)
            x = (canvas_w - row_img.width) // 2
            
            if bg_mode == 'Transparent':
                canvas.paste(row_img, (x, y), row_img)
            else:
                canvas.alpha_composite(row_img, (x, y))
            y += row_h + spacing
            
        return canvas

    def render_row(self, entry, s, scale, font, padding):
        w = int(s['width'] * scale)
        h = int(s['height'] * scale)
        
        c_w = w + (padding * 2)
        c_h = h + (padding * 2)
        container = Image.new('RGBA', (c_w, c_h), (0,0,0,0))
        bx, by = padding, padding
        
        # 1. Glow
        if s['glow_intensity'] > 0: # Only draw glow if intensity > 0
            intensity = s['glow_intensity'] * scale
            glow_color = tuple(int(c) for c in s['glow_color'][:3])
            la = Image.new('RGBA', (c_w, c_h), (0,0,0,0))
            ImageDraw.Draw(la).rectangle([bx, by, bx+w, by+h], fill=glow_color)
            la = la.filter(ImageFilter.GaussianBlur(intensity * 1.5))
            lb = Image.new('RGBA', (c_w, c_h), (0,0,0,0))
            ImageDraw.Draw(lb).rectangle([bx, by, bx+w, by+h], fill=glow_color)
            lb = lb.filter(ImageFilter.GaussianBlur(intensity * 0.5))
            container = Image.alpha_composite(container, la)
            container = Image.alpha_composite(container, lb)

        # 2. Border
        b_start = tuple(int(c) for c in s['border_start'][:3])
        b_end = tuple(int(c) for c in s['border_end'][:3])
        grad = create_gradient(w, h, b_start, b_end, s['border_angle'])
        container.paste(grad, (bx, by), grad)
        
        # 3. BG
        bw = int(s['border_width'] * scale)
        iw = w - (bw * 2)
        ih = h - (bw * 2)
        
        bg_rgb = tuple(int(c) for c in s['bg_color'][:3])
        bg_alpha = int(s['bg_opacity'] * 2.55)
        inner_bg = Image.new('RGBA', (iw, ih), bg_rgb + (bg_alpha,))
        
        if s['bg_image'] and os.path.exists(s['bg_image']):
            try:
                bg_src = Image.open(s['bg_image']).convert("RGBA")
                bg_pad = int(s.get('bg_padding', 0) * scale)
                draw_w = iw - (bg_pad * 2)
                draw_h = ih - (bg_pad * 2)
                if draw_w > 0 and draw_h > 0:
                    bg_s = s.get('bg_scale', 100) / 100.0
                    nw, nh = int(draw_w * bg_s), int(draw_w * bg_s * (bg_src.height / bg_src.width))
                    bg_src = bg_src.resize((max(1, nw), max(1, nh)), Image.Resampling.LANCZOS)
                    px, py = s.get('bg_pos_x', 50)/100.0, s.get('bg_pos_y', 50)/100.0
                    dest_x = bg_pad + int((draw_w - nw) * px)
                    dest_y = bg_pad + int((draw_h - nh) * py)
                    inner_bg.paste(bg_src, (dest_x, dest_y), bg_src)
            except: pass
            
        container.paste(inner_bg, (bx+bw, by+bw), inner_bg)
        
        # 4. Content
        content = Image.new('RGBA', (iw, ih), (0,0,0,0))
        cd = ImageDraw.Draw(content)
        cy = ih // 2
        
        if entry['type'] == 'sep':
            txt = entry.get('text', '')
            bbox = font.getbbox(txt)
            cd.text(((iw-(bbox[2]-bbox[0]))//2, (ih-(bbox[3]-bbox[1]))//2 - int(4*scale)), txt, font=font, fill=(255,255,255))
        else:
            icon_w, icon_h = int(56 * scale), int(28 * scale)
            
            # ICONS
            att_icon = self.get_image(entry['att_agent']).resize((icon_w, icon_h), Image.Resampling.NEAREST)
            content.paste(att_icon, (0, cy - (icon_h // 2)), att_icon)
            
            vic_icon = ImageOps.mirror(self.get_image(entry['vic_agent']).resize((icon_w, icon_h), Image.Resampling.NEAREST))
            content.paste(vic_icon, (iw - icon_w, cy - (icon_h // 2)), vic_icon)
            
            # WEAPON
            wep_base = self.get_image(entry['weapon'])
            icon_tint = tuple(int(c) for c in s['icon_color'][:3])
            
            wep_w, wep_h = 0, 0
            wep_icon = None
            
            if wep_base.width > 0:
                wep_h = int(19 * scale)
                wep_w = int(wep_h * (wep_base.width / wep_base.height))
                wep_icon = colorize_image(ImageOps.mirror(wep_base.resize((wep_w, wep_h), Image.Resampling.NEAREST)), icon_tint)
            
            # Fixed center point
            center_x = (iw // 2) + int(s.get('center_offset', 0) * scale)
            wep_draw_x = center_x - (wep_w // 2)
            
            if wep_icon:
                content.paste(wep_icon, (wep_draw_x, cy - (wep_h // 2)), wep_icon)
            
            # Modifiers
            mods = []
            m_h = int(15 * scale)
            mod_map = {"Headshot":"TX_Kilfeed_Headshot.png", "Wallbang":"TX_Kilfeed_WallPen.png", "Spike":"TX_Killfeed_SpikeExplosion.png"}
            for m_key in entry.get('mods', []):
                if m_key in mod_map:
                    mi = self.get_image(mod_map[m_key])
                    if mi.width > 0:
                        mw = int(m_h * (mi.width / mi.height))
                        mods.append(colorize_image(mi.resize((mw, m_h), Image.Resampling.NEAREST), icon_tint))

            mod_sp = int(s.get('mod_spacing', 2) * scale)
            mx = wep_draw_x + wep_w + mod_sp
            
            for m_img in mods:
                content.paste(m_img, (mx, cy - (m_h // 2)), m_img)
                mx += m_img.width + mod_sp
            
            # Text
            atxt, vtxt = entry['att_name'], entry['vic_name']
            ab, vb = font.getbbox(atxt), font.getbbox(vtxt)
            aw, ah = ab[2]-ab[0], ab[3]-ab[1]
            vw, vh = vb[2]-vb[0], vb[3]-vb[1]
            
            ay_off = int(s.get('att_offset_y', -4) * scale)
            vy_off = int(s.get('vic_offset_y', -4) * scale)
            
            ac = tuple(int(c) for c in s['att_color'][:3])
            vc = tuple(int(c) for c in s['vic_color'][:3])
            
            # Attacker Text
            aa, ax_off = s.get('att_align', 'Left'), int(s.get('att_offset_x', 8) * scale)
            if aa == 'Right': ax = wep_draw_x - aw - ax_off
            elif aa == 'Left': ax = icon_w + ax_off
            else: ax = icon_w + ((wep_draw_x - icon_w)//2) - (aw//2) + ax_off
            cd.text((ax, cy - (ah//2) + ay_off), atxt, font=font, fill=ac)
            
            # Victim Text
            cluster_right_edge = mx
            va, vx_off = s.get('vic_align', 'Center'), int(s.get('vic_offset_x', 0) * scale)
            if va == 'Left': vx = cluster_right_edge + vx_off
            elif va == 'Right': vx = (iw - icon_w) - vw - vx_off
            else: vx = cluster_right_edge + (((iw - icon_w) - cluster_right_edge)//2) - (vw//2) + vx_off
            cd.text((vx, cy - (vh//2) + vy_off), vtxt, font=font, fill=vc)

        container.paste(content, (bx+bw, by+bw), content)
        
        mk = int(entry.get('multikill', 1))
        if mk > 1:
            dd = ImageDraw.Draw(container)
            dh = int(4 * scale)
            gap = int(2 * scale)
            th_d = (mk * dh) + ((mk-1)*gap)
            sy = by + (h//2) - (th_d//2)
            dw = int(4 * scale)
            dx = bx - int(8 * scale)
            dash_col = tuple(int(c) for c in s['dash_color'][:3])
            for i in range(mk):
                dy = sy + i*(dh+gap)
                dd.rectangle([dx, dy, dx+dw, dy+dh], fill=dash_col)
                
        return container

# --- UI ---
class KillfeedApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Valorant Killfeed Editor (Ultimate)")
        self.geometry("1600x900")
        
        self.style_vars = {}
        self.layout_vars = {}
        
        self.renderer = KillfeedRenderer()
        self.history, self.history_index, self.editing_index = [], -1, None
        
        # UPDATED DEFAULTS
        self.default_settings = {
            'width': 430, 'height': 32, # Updated Size
            'border_width': 2, 'border_angle': 180,
            'border_start': (142, 0, 231), 'border_end': (66, 0, 103),
            'bg_color': (0, 0, 0), 'bg_opacity': 90,
            # Custom Image Settings
            'bg_image': None, 'bg_scale': 143, 'bg_pos_x': 37, 'bg_pos_y': 100, 'bg_padding': 0,
            'dash_color': (142, 0, 231),
            'att_color': (255, 255, 255), 'vic_color': (255, 255, 255), 'icon_color': (255, 255, 255),
            # Updated Glow
            'glow_enabled': True, 'glow_color': (130, 0, 220), 'glow_intensity': 0,
            'font_path': DEFAULT_FONT_PATH, 'font_size': 22,
            # Updated Offsets
            'att_align': 'Left', 'att_offset_x': 8, 'att_offset_y': -2,
            'vic_align': 'Center', 'vic_offset_x': 0, 'vic_offset_y': -2,
            'center_offset': -55, 'mod_spacing': -3,
            'row_spacing': -3,
            'export_bg_mode': 'Transparent', 
            'export_bg_color': (0, 0, 0)
        }
        self.settings = copy.deepcopy(self.default_settings)
        self.export_scale = ctk.IntVar(value=4) # Default to 4x
        self.data = []
        
        # Load Config
        self.load_from_config()
        if not self.data:
             self.data = [{'type':'kill', 'att_name':'hekli', 'att_agent':'Cypher', 'weapon':'Vandal', 'mods':['Headshot'], 'vic_name':'victim', 'vic_agent':'Jett', 'multikill':1}]

        self.save_state()
        self.build_ui()
        self.update_preview()
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.save_to_config()
        self.destroy()

    def save_to_config(self):
        cfg = {
            'settings': self.settings,
            'data': self.data
        }
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(cfg, f)
        except: pass

    def load_from_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    cfg = json.load(f)
                    if 'settings' in cfg: self.settings.update(cfg['settings'])
                    if 'data' in cfg: self.data = cfg['data']
            except: pass

    def save_state(self):
        if self.history_index < len(self.history) - 1: self.history = self.history[:self.history_index+1]
        self.history.append({'data': copy.deepcopy(self.data), 'settings': copy.deepcopy(self.settings)})
        self.history_index += 1
        
    def undo(self):
        if self.history_index > 0: self.history_index -= 1; self.restore(self.history[self.history_index])
    def redo(self):
        if self.history_index < len(self.history) - 1: self.history_index += 1; self.restore(self.history[self.history_index])
    def restore(self, s):
        self.data, self.settings = copy.deepcopy(s['data']), copy.deepcopy(s['settings'])
        self.refresh_all_ui(); self.update_preview()
    def reset_defaults(self):
        self.settings = copy.deepcopy(self.default_settings)
        self.refresh_all_ui(); self.update_preview()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=3); self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(0, weight=1)
        p = ctk.CTkFrame(self, fg_color="#0a0e17", corner_radius=0); p.grid(row=0, column=0, sticky="nsew")
        self.lbl_preview = ctk.CTkLabel(p, text=""); self.lbl_preview.place(relx=0.5, rely=0.5, anchor="center")
        
        t = ctk.CTkFrame(p, fg_color="transparent"); t.place(relx=0.5, rely=0.95, anchor="s")
        ctk.CTkButton(t, text="Undo", width=60, command=self.undo).pack(side="left", padx=2)
        ctk.CTkButton(t, text="Redo", width=60, command=self.redo).pack(side="left", padx=2)
        
        c = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=0); c.grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(c, text="KILLFEED EDITOR", font=("Arial", 20, "bold"), text_color="#a855f7").pack(pady=10)
        
        tabs = ctk.CTkTabview(c); tabs.pack(fill="both", expand=True, padx=10)
        tabs.add("Edit"); tabs.add("Style"); tabs.add("Layout")
        self.build_edit(tabs.tab("Edit")); self.build_style(tabs.tab("Style")); self.build_layout(tabs.tab("Layout"))
        
        e = ctk.CTkFrame(c, fg_color="transparent"); e.pack(fill="x", padx=10, pady=10)
        ctk.CTkOptionMenu(e, variable=self.export_scale, values=["1","2","3","4"], width=60).pack(side="left")
        ctk.CTkButton(e, text="DOWNLOAD PNG", fg_color="#7c3aed", font=("Arial", 14, "bold"), command=self.download).pack(side="right", fill="x", expand=True, padx=5)

    def build_edit(self, p):
        self.ent_att = ctk.CTkEntry(p, placeholder_text="Attacker"); self.ent_att.insert(0, "hekli"); self.ent_att.pack(fill="x", pady=2)
        self.cmb_att = ctk.CTkComboBox(p, values=sorted(AGENT_ICONS.keys())); self.cmb_att.set("Cypher"); self.cmb_att.pack(fill="x", pady=2)
        self.setup_autocomplete(self.cmb_att, AGENT_ICONS)

        f_mid = ctk.CTkFrame(p, fg_color="transparent"); f_mid.pack(fill="x", pady=2)
        self.cmb_wep = ctk.CTkComboBox(f_mid, values=sorted(WEAPON_ICONS.keys())); self.cmb_wep.set("Vandal"); self.cmb_wep.pack(side="left", fill="x", expand=True)
        self.setup_autocomplete(self.cmb_wep, WEAPON_ICONS)
        
        self.opt_mk = ctk.CTkOptionMenu(f_mid, values=[str(i) for i in range(1,7)], width=70); self.opt_mk.set("1"); self.opt_mk.pack(side="right", padx=5)
        ctk.CTkLabel(f_mid, text="Kills:", width=30).pack(side="right")

        mf = ctk.CTkFrame(p, fg_color="transparent"); mf.pack(fill="x", pady=2)
        self.chk_hs = ctk.CTkCheckBox(mf, text="Headshot", width=20); self.chk_hs.pack(side="left", padx=5)
        self.chk_wb = ctk.CTkCheckBox(mf, text="Wallbang", width=20); self.chk_wb.pack(side="left", padx=5)
        
        self.ent_vic = ctk.CTkEntry(p, placeholder_text="Victim"); self.ent_vic.insert(0, "victim"); self.ent_vic.pack(fill="x", pady=2)
        self.cmb_vic = ctk.CTkComboBox(p, values=sorted(AGENT_ICONS.keys())); self.cmb_vic.set("Jett"); self.cmb_vic.pack(fill="x", pady=2)
        self.setup_autocomplete(self.cmb_vic, AGENT_ICONS)

        # REMOVED: Override Checkbox code entirely as requested
        
        f_btn = ctk.CTkFrame(p, fg_color="transparent"); f_btn.pack(fill="x", pady=10)
        self.btn_add = ctk.CTkButton(f_btn, text="Add New Kill", fg_color="#059669", command=self.add_kill); self.btn_add.pack(fill="x", pady=2)
        f_upd = ctk.CTkFrame(p, fg_color="transparent"); f_upd.pack(fill="x")
        self.btn_upd = ctk.CTkButton(f_upd, text="Update Selected", fg_color="#2563eb", state="disabled", command=self.update_kill); self.btn_upd.pack(side="left", fill="x", expand=True, padx=(0,2))
        self.btn_cancel = ctk.CTkButton(f_upd, text="Cancel", fg_color="gray", state="disabled", width=70, command=self.cancel_edit); self.btn_cancel.pack(side="right")

        self.ent_sep = ctk.CTkEntry(p, placeholder_text="Separator"); self.ent_sep.pack(fill="x", pady=(15,0))
        ctk.CTkButton(p, text="+ Add Separator", fg_color="#475569", command=self.add_sep).pack(fill="x", pady=2)
        self.list_frame = ctk.CTkScrollableFrame(p, height=200); self.list_frame.pack(fill="both", expand=True, pady=5)

    def setup_autocomplete(self, widget, data_source):
        def on_tab(event):
            current = widget.get().lower()
            options = sorted(data_source.keys())
            for opt in options:
                if current in opt.lower():
                    widget.set(opt)
                    return "break"
        try: widget._entry.bind("<Tab>", on_tab)
        except: pass

    def build_style(self, p):
        sf = ctk.CTkScrollableFrame(p, fg_color="transparent"); sf.pack(fill="both", expand=True)
        pf = ctk.CTkFrame(sf, fg_color="transparent"); pf.pack(fill="x", pady=5)
        ctk.CTkButton(pf, text="Def", width=40, command=lambda: self.preset('def')).pack(side="left", padx=1)
        ctk.CTkButton(pf, text="Ally", width=40, fg_color="#0891b2", command=lambda: self.preset('ally')).pack(side="left", padx=1)
        ctk.CTkButton(pf, text="Enemy", width=40, fg_color="#be123c", command=lambda: self.preset('enemy')).pack(side="left", padx=1)
        ctk.CTkButton(pf, text="RESET", width=60, fg_color="#b91c1c", command=self.reset_defaults).pack(side="right", padx=1)
        self.style_vars = {}
        def add_ctrl(lbl, key, mn, mx):
            f = ctk.CTkFrame(sf, fg_color="transparent"); f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=lbl, width=80, anchor="w").pack(side="left")
            var = ctk.StringVar(value=str(self.settings[key]))
            def on_e(e): 
                try: v=float(var.get()); self.settings[key]=int(v); sl.set(v); self.update_preview()
                except: pass
            ent = ctk.CTkEntry(f, textvariable=var, width=50); ent.bind('<Return>', on_e); ent.bind('<FocusOut>', on_e); ent.pack(side="left", padx=5)
            def on_s(v): self.settings[key]=int(v); var.set(str(int(v))); self.update_preview()
            sl = ctk.CTkSlider(f, from_=mn, to=mx, command=on_s, height=16); sl.set(self.settings[key]); sl.pack(side="left", fill="x", expand=True)
            self.style_vars[key] = (var, sl)
        
        def add_col(lbl, key):
            f = ctk.CTkFrame(sf, fg_color="transparent"); f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=lbl, width=80, anchor="w").pack(side="left")
            btn = ctk.CTkButton(f, text="", width=40, height=20, fg_color=rgb_to_hex(self.settings[key]))
            def pick():
                def update_from_picker(c):
                    if c:
                        if isinstance(c, str):
                            self.settings[key] = hex_to_rgb(c)
                            btn.configure(fg_color=c)
                        elif isinstance(c, tuple):
                            self.settings[key] = tuple(int(x) for x in c[:3])
                            btn.configure(fg_color=rgb_to_hex(self.settings[key]))
                        self.update_preview()
                if HAS_MODERN_PICKER: AskColor(color=rgb_to_hex(self.settings[key]), command=update_from_picker)
                else:
                    c = colorchooser.askcolor(color=rgb_to_hex(self.settings[key]))[1]
                    update_from_picker(c)
            btn.configure(command=pick); btn.pack(side="left"); self.style_vars[key] = btn
        
        ctk.CTkLabel(sf, text="Dim/BG", text_color="gray").pack(anchor="w"); add_ctrl("Width", 'width', 300, 800); add_ctrl("Height", 'height', 20, 60); add_ctrl("Opacity", 'bg_opacity', 0, 100); add_col("BG Col", 'bg_color')
        
        ctk.CTkLabel(sf, text="Custom Image Settings", text_color="gray", font=("Arial", 11)).pack(anchor="w", pady=(5,0))
        add_ctrl("Scale", 'bg_scale', 10, 200)
        add_ctrl("Padding", 'bg_padding', 0, 50)
        add_ctrl("Pos X", 'bg_pos_x', 0, 100)
        add_ctrl("Pos Y", 'bg_pos_y', 0, 100)
        ip = ctk.CTkFrame(sf, fg_color="transparent"); ip.pack(fill="x")
        ctk.CTkButton(ip, text="Select Img", width=80, command=self.pick_bg).pack(side="left")
        ctk.CTkButton(ip, text="Clear", width=50, fg_color="#b91c1c", command=self.clear_bg).pack(side="left", padx=5)

        # FONT SETTINGS REMOVED

        ctk.CTkLabel(sf, text="Glow", text_color="gray").pack(anchor="w"); add_ctrl("Intens.", 'glow_intensity', 0, 60); add_col("Color", 'glow_color')
        ctk.CTkLabel(sf, text="Borders", text_color="gray").pack(anchor="w"); add_col("Start", 'border_start'); add_col("End", 'border_end'); add_col("Dash", 'dash_color')
        ctk.CTkLabel(sf, text="Text", text_color="gray").pack(anchor="w"); add_col("Attacker", 'att_color'); add_col("Victim", 'vic_color'); add_col("Icon", 'icon_color')

        # EXPORT SETTINGS
        ctk.CTkLabel(sf, text="EXPORT SETTINGS", text_color="#a855f7", font=("Arial", 12, "bold")).pack(anchor="w", pady=(15,0))
        bg_modes = ["Transparent", "Solid Color", "Match Gradient"]
        self.opt_bg_mode = ctk.CTkOptionMenu(sf, values=bg_modes, command=lambda v: self.set_val('export_bg_mode', v))
        self.opt_bg_mode.set(self.settings['export_bg_mode'])
        self.opt_bg_mode.pack(fill="x", pady=2)
        
        self.btn_bg_col = ctk.CTkButton(sf, text="Set Background Color", fg_color=rgb_to_hex(self.settings['export_bg_color']))
        def pick_ex_bg():
            def upd(c):
                if c:
                    if isinstance(c, str): 
                        self.settings['export_bg_color'] = hex_to_rgb(c)
                        self.btn_bg_col.configure(fg_color=c)
                    elif isinstance(c, tuple):
                        self.settings['export_bg_color'] = tuple(int(x) for x in c[:3])
                        self.btn_bg_col.configure(fg_color=rgb_to_hex(self.settings['export_bg_color']))
                    self.update_preview()
            upd(colorchooser.askcolor(color=rgb_to_hex(self.settings['export_bg_color']))[1])
        self.btn_bg_col.configure(command=pick_ex_bg)
        self.btn_bg_col.pack(fill="x", pady=2)
        self.style_vars['export_bg_color'] = self.btn_bg_col
        self.layout_vars['export_bg_mode'] = self.opt_bg_mode

    def build_layout(self, p):
        sf = ctk.CTkScrollableFrame(p, fg_color="transparent"); sf.pack(fill="both", expand=True)
        self.layout_vars = {}
        def add_l(parent, lbl, key, mn, mx):
            f = ctk.CTkFrame(parent, fg_color="transparent"); f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=lbl, width=80, anchor="w").pack(side="left")
            var = ctk.StringVar(value=str(self.settings[key]))
            def on_e(e):
                try: v=float(var.get()); self.settings[key]=int(v); sl.set(v); self.update_preview()
                except: pass
            ent = ctk.CTkEntry(f, textvariable=var, width=50); ent.bind('<Return>', on_e); ent.bind('<FocusOut>', on_e); ent.pack(side="left", padx=5)
            def on_s(v): self.settings[key]=int(v); var.set(str(int(v))); self.update_preview()
            sl = ctk.CTkSlider(f, from_=mn, to=mx, command=on_s, height=16); sl.set(self.settings[key]); sl.pack(side="left", fill="x", expand=True)
            self.layout_vars[key] = (var, sl)
        def add_o(parent, lbl, key, opts):
            f = ctk.CTkFrame(parent, fg_color="transparent"); f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=lbl, width=80, anchor="w").pack(side="left")
            o = ctk.CTkOptionMenu(f, values=opts, command=lambda v: self.set_val(key, v), width=100); o.set(self.settings[key]); o.pack(side="left", padx=5)
            self.layout_vars[key] = o

        g1 = ctk.CTkFrame(sf); g1.pack(fill="x", pady=5, padx=5)
        ctk.CTkLabel(g1, text="ATTACKER TEXT", text_color="#a855f7", font=("Arial", 12, "bold")).pack(pady=5)
        add_o(g1, "Align", 'att_align', ["Left","Right","Center"])
        add_l(g1, "Offset X", 'att_offset_x', -100, 100)
        add_l(g1, "Offset Y", 'att_offset_y', -20, 20)

        g2 = ctk.CTkFrame(sf); g2.pack(fill="x", pady=5, padx=5)
        ctk.CTkLabel(g2, text="VICTIM TEXT", text_color="#a855f7", font=("Arial", 12, "bold")).pack(pady=5)
        add_o(g2, "Align", 'vic_align', ["Left","Right","Center"])
        add_l(g2, "Offset X", 'vic_offset_x', -100, 100)
        add_l(g2, "Offset Y", 'vic_offset_y', -20, 20)

        g3 = ctk.CTkFrame(sf); g3.pack(fill="x", pady=5, padx=5)
        ctk.CTkLabel(g3, text="GENERAL SPACING", text_color="#a855f7", font=("Arial", 12, "bold")).pack(pady=5)
        add_l(g3, "Cluster X", 'center_offset', -200, 200)
        add_l(g3, "Icon Gap", 'mod_spacing', -10, 20)
        add_l(g3, "Row Gap", 'row_spacing', -10, 50)

    def set_val(self, k, v): self.settings[k]=v; self.update_preview()
    
    def get_form_data(self):
        mods = []
        if self.chk_hs.get(): mods.append("Headshot")
        if self.chk_wb.get(): mods.append("Wallbang")
        
        data = {
            'type':'kill', 
            'att_name':self.ent_att.get(), 'att_agent':self.cmb_att.get(), 
            'weapon':self.cmb_wep.get(), 'mods':mods, 
            'vic_name':self.ent_vic.get(), 'vic_agent':self.cmb_vic.get(), 
            'multikill':int(self.opt_mk.get())
        }
        return data

    def add_kill(self):
        self.save_state()
        self.data.append(self.get_form_data())
        self.editing_index = None # Reset edit state
        self.refresh_list_ui(); self.update_preview()

    def update_kill(self):
        if self.editing_index is None: return
        self.save_state()
        self.data[self.editing_index] = self.get_form_data()
        self.cancel_edit()
        self.refresh_list_ui(); self.update_preview()

    def cancel_edit(self):
        self.editing_index = None
        self.btn_upd.configure(state="disabled")
        self.btn_cancel.configure(state="disabled")
        self.refresh_list_ui()

    def edit_entry(self, i):
        e = self.data[i]
        if e['type'] == 'kill':
            self.editing_index = i
            self.btn_upd.configure(state="normal")
            self.btn_cancel.configure(state="normal")
            
            self.ent_att.delete(0, 'end'); self.ent_att.insert(0, e['att_name'])
            self.cmb_att.set(e['att_agent'])
            self.cmb_wep.set(e['weapon'])
            self.opt_mk.set(str(e.get('multikill', 1)))
            self.ent_vic.delete(0, 'end'); self.ent_vic.insert(0, e['vic_name'])
            self.cmb_vic.set(e['vic_agent'])
            self.chk_hs.deselect(); self.chk_wb.deselect()
            if 'Headshot' in e['mods']: self.chk_hs.select()
            if 'Wallbang' in e['mods']: self.chk_wb.select()

    def add_sep(self): self.save_state(); self.data.append({'type':'sep', 'text':self.ent_sep.get()}); self.refresh_list_ui(); self.update_preview()
    
    def refresh_list_ui(self):
        for w in self.list_frame.winfo_children(): w.destroy()
        for i, e in enumerate(self.data):
            c = "#3b82f6" if i == self.editing_index else "#334155"
            f = ctk.CTkFrame(self.list_frame, fg_color=c); f.pack(fill="x", pady=1)
            txt = e['text'] if e['type']=='sep' else f"{e['att_name']} -> {e['vic_name']} ({e.get('multikill',1)}x)"
            ctk.CTkButton(f, text=txt, fg_color="transparent", anchor="w", command=lambda x=i: self.edit_entry(x)).pack(side="left", fill="x", expand=True)
            ctk.CTkButton(f, text="X", width=30, fg_color="red", command=lambda x=i: self.rem(x)).pack(side="right", padx=2)

    def rem(self, i): 
        self.save_state()
        if i == self.editing_index: self.cancel_edit()
        self.data.pop(i)
        self.refresh_list_ui(); self.update_preview()
    
    def pick_bg(self):
        f = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg")])
        if f: self.settings['bg_image'] = f; self.update_preview()
    def clear_bg(self): self.settings['bg_image'] = None; self.update_preview()

    # REMOVED: pick_font, on_font_select, reset_font

    def preset(self, p):
        if p=='def': self.settings.update(self.default_settings)
        elif p=='ally': self.settings.update({'border_start':(0,255,255), 'border_end':(0,128,128), 'dash_color':(0,255,255), 'glow_enabled':False})
        elif p=='enemy': self.settings.update({'border_start':(255,70,85), 'border_end':(128,0,0), 'dash_color':(255,70,85), 'glow_enabled':False})
        self.refresh_all_ui(); self.update_preview()
        
    def refresh_all_ui(self):
        for d in [self.style_vars, self.layout_vars]:
            for k, w in d.items():
                if isinstance(w, tuple): w[0].set(str(self.settings[k])); w[1].set(self.settings[k])
                elif isinstance(w, ctk.CTkButton): w.configure(fg_color=rgb_to_hex(self.settings[k]))
                elif isinstance(w, ctk.CTkOptionMenu): w.set(self.settings[k])
                
    def update_preview(self):
        img = self.renderer.render(self.data, self.settings, scale=1.0)
        self.preview_img = img
        disp = img.copy(); disp.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
        tk_img = ctk.CTkImage(light_image=disp, dark_image=disp, size=disp.size)
        self.lbl_preview.configure(image=tk_img)
        
    def download(self):
        f = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if f: self.renderer.render(self.data, self.settings, scale=int(self.export_scale.get())).save(f)

if __name__ == "__main__":
    app = KillfeedApp()
    app.mainloop()