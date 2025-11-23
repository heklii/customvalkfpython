import streamlit as st
import os
import copy
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

# --- Configuration ---
st.set_page_config(layout="wide", page_title="Valorant Killfeed Editor")

# Path Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "assets", "ShooterGame")
DEFAULT_FONT_PATH = os.path.join(BASE_DIR, "assets", "fonts", "Moonbeam.ttf")

# --- Mappings ---
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

# --- Renderer (No Tkinter/ImageTk) ---
class KillfeedRenderer:
    def __init__(self):
        self.cache = {}

    def get_font(self, path, size):
        try: return ImageFont.truetype(path, size)
        except: return ImageFont.load_default()

    def get_image(self, name):
        fname = AGENT_ICONS.get(name) or WEAPON_ICONS.get(name) or name
        path = os.path.join(ASSET_PATH, fname)
        
        # Fallback search if file not found directly
        if not os.path.exists(path):
             for root, dirs, files in os.walk(ASSET_PATH):
                if fname in files:
                    path = os.path.join(root, fname)
                    break

        if path in self.cache: return self.cache[path]
        try:
            img = Image.open(path).convert("RGBA")
            self.cache[path] = img
            return img
        except: return Image.new("RGBA", (10,10), (0,0,0,0))

    def render(self, entries, s, scale=1.0):
        row_h = int(s['height'] * scale)
        spacing = int(s.get('row_spacing', 2) * scale)
        safe_padding = int(60 * scale)
        
        total_h = max(int(100*scale), len(entries) * (row_h + spacing) + (safe_padding * 2))
        canvas_w = int(s['width'] * scale) + (safe_padding * 2)
        
        # Background Mode
        bg_mode = s.get('export_bg_mode', 'Transparent')
        if bg_mode == 'Solid Color':
            col = hex_to_rgb(s.get('export_bg_color', '#000000'))
            canvas = Image.new('RGBA', (canvas_w, total_h), col + (255,))
        elif bg_mode == 'Match Gradient':
            b_start = hex_to_rgb(s['border_start'])
            b_end = hex_to_rgb(s['border_end'])
            canvas = create_gradient(canvas_w, total_h, b_start, b_end, s['border_angle'])
        else:
            canvas = Image.new('RGBA', (canvas_w, total_h), (0,0,0,0))

        y = safe_padding
        font_path = DEFAULT_FONT_PATH # Simplify for streamlit (upload font if needed)
        font = self.get_font(font_path, int(s.get('font_size', 22) * scale))
        
        for entry in entries:
            # Check for row overrides
            row_s = s.copy()
            if entry.get('override_style'):
                # In this simple streamlit version, we just handle a few key overrides if present
                pass 

            row_img = self.render_row(entry, row_s, scale, font, safe_padding)
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
        c_w, c_h = w + (padding*2), h + (padding*2)
        container = Image.new('RGBA', (c_w, c_h), (0,0,0,0))
        bx, by = padding, padding
        
        # Colors
        glow_c = hex_to_rgb(s['glow_color'])
        border_s = hex_to_rgb(s['border_start'])
        border_e = hex_to_rgb(s['border_end'])
        dash_c = hex_to_rgb(s['dash_color'])
        bg_c = hex_to_rgb(s['bg_color'])
        att_c = hex_to_rgb(s['att_color'])
        vic_c = hex_to_rgb(s['vic_color'])
        icon_c = hex_to_rgb(s['icon_color'])
        
        # Glow
        if s['glow_enabled']:
            intensity = s['glow_intensity'] * scale
            la = Image.new('RGBA', (c_w, c_h), (0,0,0,0))
            ImageDraw.Draw(la).rectangle([bx, by, bx+w, by+h], fill=glow_c)
            la = la.filter(ImageFilter.GaussianBlur(intensity * 1.5))
            lb = Image.new('RGBA', (c_w, c_h), (0,0,0,0))
            ImageDraw.Draw(lb).rectangle([bx, by, bx+w, by+h], fill=glow_c)
            lb = lb.filter(ImageFilter.GaussianBlur(intensity * 0.5))
            container = Image.alpha_composite(container, la)
            container = Image.alpha_composite(container, lb)

        # Border
        grad = create_gradient(w, h, border_s, border_e, s['border_angle'])
        container.paste(grad, (bx, by), grad)
        
        # BG
        bw = int(s['border_width'] * scale)
        iw, ih = w - (bw*2), h - (bw*2)
        bg_alpha = int(s['bg_opacity'] * 2.55)
        inner_bg = Image.new('RGBA', (iw, ih), bg_c + (bg_alpha,))
        container.paste(inner_bg, (bx+bw, by+bw), inner_bg)
        
        # Content
        content = Image.new('RGBA', (iw, ih), (0,0,0,0))
        cd = ImageDraw.Draw(content)
        cy = ih // 2
        
        if entry['type'] == 'sep':
            txt = entry['text']
            bbox = font.getbbox(txt)
            cd.text(((iw-(bbox[2]-bbox[0]))//2, (ih-(bbox[3]-bbox[1]))//2 - int(4*scale)), txt, font=font, fill=(255,255,255))
        else:
            icon_w, icon_h = int(56*scale), int(28*scale)
            
            # Icons
            att_icon = self.get_image(entry['att_agent']).resize((icon_w, icon_h), Image.Resampling.NEAREST)
            content.paste(att_icon, (0, cy - (icon_h//2)), att_icon)
            
            vic_icon = ImageOps.mirror(self.get_image(entry['vic_agent']).resize((icon_w, icon_h), Image.Resampling.NEAREST))
            content.paste(vic_icon, (iw - icon_w, cy - (icon_h//2)), vic_icon)
            
            # Center
            wep_base = self.get_image(entry['weapon'])
            wep_w, wep_h = 0, 0
            wep_icon = None
            if wep_base.width > 0:
                wep_h = int(19 * scale)
                wep_w = int(wep_h * (wep_base.width / wep_base.height))
                wep_icon = colorize_image(ImageOps.mirror(wep_base.resize((wep_w, wep_h), Image.Resampling.NEAREST)), icon_c)
            
            cx = (iw // 2) + int(s['center_offset'] * scale)
            wx = cx - (wep_w // 2)
            if wep_icon: content.paste(wep_icon, (wx, cy - (wep_h//2)), wep_icon)
            
            mods = []
            mh = int(15 * scale)
            mod_map = {"Headshot":"TX_Kilfeed_Headshot.png", "Wallbang":"TX_Kilfeed_WallPen.png", "Spike":"TX_Killfeed_SpikeExplosion.png"}
            for m in entry['mods']:
                if m in mod_map:
                    mi = self.get_image(mod_map[m])
                    mw = int(mh * (mi.width / mi.height))
                    mods.append(colorize_image(mi.resize((mw, mh), Image.Resampling.NEAREST), icon_c))
            
            msp = int(s['mod_spacing'] * scale)
            mx = wx + wep_w + msp
            for m_img in mods:
                content.paste(m_img, (mx, cy - (mh//2)), m_img)
                mx += m_img.width + msp
            
            # Text
            ab = font.getbbox(entry['att_name'])
            aw, ah = ab[2]-ab[0], ab[3]-ab[1]
            ay_off = int(s['att_offset_y'] * scale)
            
            aa, ax_off = s['att_align'], int(s['att_offset_x'] * scale)
            if aa == 'Right': ax = wx - aw - ax_off
            elif aa == 'Left': ax = icon_w + ax_off
            else: ax = icon_w + ((wx - icon_w)//2) - (aw//2) + ax_off
            cd.text((ax, cy - (ah//2) + ay_off), entry['att_name'], font=font, fill=att_c)
            
            vb = font.getbbox(entry['vic_name'])
            vw, vh = vb[2]-vb[0], vb[3]-vb[1]
            vy_off = int(s['vic_offset_y'] * scale)
            
            va, vx_off = s['vic_align'], int(s['vic_offset_x'] * scale)
            if va == 'Left': vx = mx + vx_off
            elif va == 'Right': vx = (iw - icon_w) - vw - vx_off
            else: vx = mx + (((iw - icon_w) - mx)//2) - (vw//2) + vx_off
            cd.text((vx, cy - (vh//2) + vy_off), entry['vic_name'], font=font, fill=vic_c)

        container.paste(content, (bx+bw, by+bw), content)
        
        mk = int(entry.get('multikill', 1))
        if mk > 1:
            dd = ImageDraw.Draw(container)
            dh = int(4*scale)
            gap = int(2*scale)
            th = (mk*dh) + ((mk-1)*gap)
            sy = by + (h//2) - (th//2)
            dw = int(4*scale)
            dx = bx - int(8*scale)
            for i in range(mk):
                dd.rectangle([dx, sy + i*(dh+gap), dx+dw, sy + i*(dh+gap) + dh], fill=dash_c)
                
        return container

# --- Streamlit App Logic ---

if 'data' not in st.session_state:
    st.session_state['data'] = [{'type':'kill', 'att_name':'hekli', 'att_agent':'Cypher', 'weapon':'Vandal', 'mods':['Headshot'], 'vic_name':'victim', 'vic_agent':'Jett', 'multikill':1}]

if 'settings' not in st.session_state:
    st.session_state['settings'] = {
        'width': 500, 'height': 36, 'border_width': 2, 'border_angle': 180,
        'border_start': '#8e00e7', 'border_end': '#420067',
        'bg_color': '#000000', 'bg_opacity': 90,
        'dash_color': '#8e00e7', 'att_color': '#ffffff', 'vic_color': '#ffffff', 'icon_color': '#ffffff',
        'glow_enabled': True, 'glow_color': '#8200dc', 'glow_intensity': 2,
        'font_size': 22,
        'att_align': 'Left', 'att_offset_x': 8, 'att_offset_y': -4,
        'vic_align': 'Center', 'vic_offset_x': 0, 'vic_offset_y': -4,
        'center_offset': -100, 'mod_spacing': 2, 'row_spacing': 2,
        'export_bg_mode': 'Transparent', 'export_bg_color': '#000000'
    }

renderer = KillfeedRenderer()

# --- Sidebar: Controls ---
with st.sidebar:
    st.header("Editor Controls")
    
    tab_add, tab_style, tab_layout = st.tabs(["Edit", "Style", "Layout"])
    
    with tab_add:
        st.subheader("Add New Kill")
        att_name = st.text_input("Attacker Name", "hekli")
        att_agent = st.selectbox("Attacker Agent", sorted(AGENT_ICONS.keys()), index=sorted(AGENT_ICONS.keys()).index("Cypher"))
        weapon = st.selectbox("Weapon", sorted(WEAPON_ICONS.keys()), index=sorted(WEAPON_ICONS.keys()).index("Vandal"))
        
        col_mods, col_mk = st.columns(2)
        with col_mods:
            mods = st.multiselect("Modifiers", ["Headshot", "Wallbang", "Spike"], default=["Headshot"])
        with col_mk:
            mk = st.number_input("Multikill", 1, 6, 1)
            
        vic_name = st.text_input("Victim Name", "victim")
        vic_agent = st.selectbox("Victim Agent", sorted(AGENT_ICONS.keys()), index=sorted(AGENT_ICONS.keys()).index("Jett"))
        
        if st.button("Add Kill Entry", type="primary"):
            st.session_state['data'].append({
                'type': 'kill',
                'att_name': att_name, 'att_agent': att_agent,
                'weapon': weapon, 'mods': mods,
                'vic_name': vic_name, 'vic_agent': vic_agent,
                'multikill': mk
            })
            st.rerun()
            
        st.markdown("---")
        sep_text = st.text_input("Separator Text", "ROUND 1")
        if st.button("Add Separator"):
            st.session_state['data'].append({'type': 'sep', 'text': sep_text})
            st.rerun()

    with tab_style:
        s = st.session_state['settings']
        st.subheader("Dimensions & BG")
        s['width'] = st.slider("Width", 300, 800, s['width'])
        s['height'] = st.slider("Height", 20, 60, s['height'])
        s['bg_opacity'] = st.slider("BG Opacity", 0, 100, s['bg_opacity'])
        s['bg_color'] = st.color_picker("BG Color", s['bg_color'])
        
        st.subheader("Borders & Glow")
        s['glow_enabled'] = st.checkbox("Enable Glow", s['glow_enabled'])
        s['glow_intensity'] = st.slider("Glow Intensity", 0, 50, s['glow_intensity'])
        s['glow_color'] = st.color_picker("Glow Color", s['glow_color'])
        c1, c2 = st.columns(2)
        s['border_start'] = c1.color_picker("Border Start", s['border_start'])
        s['border_end'] = c2.color_picker("Border End", s['border_end'])
        s['border_angle'] = st.slider("Gradient Angle", 0, 360, s['border_angle'])
        
        st.subheader("Text & Icons")
        s['font_size'] = st.number_input("Font Size", 10, 50, s['font_size'])
        c1, c2, c3 = st.columns(3)
        s['att_color'] = c1.color_picker("Attacker", s['att_color'])
        s['vic_color'] = c2.color_picker("Victim", s['vic_color'])
        s['icon_color'] = c3.color_picker("Icons", s['icon_color'])
        s['dash_color'] = st.color_picker("Dash Color", s['dash_color'])
        
        st.subheader("Export Options")
        s['export_bg_mode'] = st.selectbox("Background Mode", ["Transparent", "Solid Color", "Match Gradient"], index=0)
        if s['export_bg_mode'] == 'Solid Color':
            s['export_bg_color'] = st.color_picker("Export BG Color", s['export_bg_color'])

    with tab_layout:
        l = st.session_state['settings']
        st.markdown("### Attacker Text")
        l['att_align'] = st.selectbox("Align A", ["Left", "Right", "Center"], index=["Left", "Right", "Center"].index(l['att_align']))
        l['att_offset_x'] = st.slider("Offset X (A)", -100, 100, l['att_offset_x'])
        l['att_offset_y'] = st.slider("Offset Y (A)", -20, 20, l['att_offset_y'])
        
        st.markdown("### Victim Text")
        l['vic_align'] = st.selectbox("Align V", ["Left", "Right", "Center"], index=["Left", "Right", "Center"].index(l['vic_align']))
        l['vic_offset_x'] = st.slider("Offset X (V)", -100, 100, l['vic_offset_x'])
        l['vic_offset_y'] = st.slider("Offset Y (V)", -20, 20, l['vic_offset_y'])
        
        st.markdown("### General")
        l['center_offset'] = st.slider("Center Cluster X", -200, 200, l['center_offset'])
        l['mod_spacing'] = st.slider("Icon Gap", 0, 20, l['mod_spacing'])
        l['row_spacing'] = st.slider("Row Gap", 0, 50, l['row_spacing'])

# --- Main Area ---
st.title("Valorant Killfeed Generator")

# Generate Preview
img = renderer.render(st.session_state['data'], st.session_state['settings'], scale=1.0)

# Display Preview
st.image(img, caption="Live Preview", use_column_width=False)

# List of Kills
st.subheader("Current Feed")
if not st.session_state['data']:
    st.info("No kills added yet.")
else:
    for i, entry in enumerate(st.session_state['data']):
        c1, c2 = st.columns([4, 1])
        txt = entry['text'] if entry['type'] == 'sep' else f"{entry['att_name']} -> {entry['vic_name']} ({entry.get('multikill',1)}x)"
        c1.text(f"{i+1}. {txt}")
        if c2.button("Delete", key=f"del_{i}"):
            st.session_state['data'].pop(i)
            st.rerun()

# Download
st.markdown("---")
scale = st.selectbox("Export Resolution", [1, 2, 3, 4], index=0)
if st.button("Render & Download"):
    high_res = renderer.render(st.session_state['data'], st.session_state['settings'], scale=scale)
    # Save to buffer
    import io
    buf = io.BytesIO()
    high_res.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="Download PNG",
        data=byte_im,
        file_name="killfeed.png",
        mime="image/png"
    )