translate_dict = {
    'Betekintési szög': "display_viewangle",
    'Csatlakozók': "plugins",
    'Egyéb jellemzők': "other",
    'Energiaosztály': "energyclass",
    'HDMI csatlakozók száma': "num_hdmi",
    'Hangfal típus': "sound",
    'Kijelző felbontása': "display_resolution",
    'Kijelző méret': "display_size",
    'Kijelző típusa': "display_type",
    'Képarány': "display_ratio",
    'Képernyő felbontás': "display_resolution",
    'Képernyő típus': "display_type",
    'Képfrissítés': "display_updaterate",
    'Képátló': "display_size",
    'MKV videó formátum': "format_mkv",
    'Magasság': "dim_height",
    'Mélység': "dim_depth",
    'Smart': "smart",
    'Szélesség': "dim_width",
    'Szín': "dim_color",
    'Súly': "dim_weight",
    'Tulajdonságok': "properties",
    'Tuner típusa': "tuner",
    'USB csatlakozó': "usb",
    'USB portok száma': "num_usb",
    'USB-ről lejátszható formátumok': "format_usb",
    'Válaszidő': "display_responsetime",
    'WiFi': "wifi",
    'Ívelt kijelző': "display_curved",
}

float_cols = [
    "display_size", 
    "dim_height",
    "dim_width",
    "dim_depth",
    "dim_weight",
]

int_cols = [
    "num_usb",
    "num_hdmi",
]

label_encoder = { 
    "display_type": ["TN", "LCD", "LED", "OLED", "QLED", "NANOCELL", "QNED"][::-1], # best to worst
    "energyclass": ["A","B","C","D","E","F","G"], # best to worst
    "display_resolution": ["HD", "Full HD", "4K", "8K"][::-1], # best to worst [720,1080,2160,4320]
    "dim_color": ["Fehér","Ezüst","Szürke","Bézs","Korall","Kék","Fekete"], # brightest to darkest
}

binary_cols = [
    "smart",
    "usb",
    "wifi"
]

companies = [
    'samsung', 'lg', 'hisense', 'tcl', 'sony', 'philips', 'panasonic',
    'dyras', 'tesla', 'loewe', 'smart', 'nokia', 'gaba', 'vortex','strong'
]

def density_ready(record):
    for prop in ["dim_weight","dim_height","dim_width","dim_depth"]:
        if prop not in record:
            return False
    return True

def pixel_ready(record):
    for prop in ["display_resolution","dim_height","dim_width"]:
        if prop not in record:
            return False
    return True

def energy_ready(record):
    for prop in ["display_resolution","energyclass"]:
        if prop not in record:
            return False
    return True


res2pixs = {
    "HD": 1280 * 720, 
    "Full HD": 1920 * 1080, 
    "4K": 3840 * 2160, 
    "8K": 7680 * 4320
}

def resolution2pixel(code):
    tech = label_encoder["display_resolution"][-code-1]
    return res2pixs[tech]
