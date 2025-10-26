"""
Predefined color presets for common objects and materials
Colors are stored as RGB tuples (0-255)
"""

import numpy as np

# Human body colors
HUMAN_COLORS = {
    'Skin - Fair': (255, 224, 189),
    'Skin - Light': (241, 194, 125),
    'Skin - Medium': (224, 172, 105),
    'Skin - Tan': (198, 134, 66),
    'Skin - Brown': (141, 85, 36),
    'Skin - Dark': (92, 64, 51),
    'Hair - Blonde': (230, 206, 168),
    'Hair - Light Brown': (167, 133, 106),
    'Hair - Brown': (101, 67, 33),
    'Hair - Dark Brown': (59, 48, 36),
    'Hair - Black': (28, 26, 24),
    'Hair - Red': (165, 42, 42),
    'Hair - Auburn': (145, 85, 61),
    'Hair - Gray': (128, 128, 128),
    'Hair - White': (235, 235, 235),
    'Lips - Light Pink': (255, 182, 193),
    'Lips - Pink': (255, 105, 180),
    'Lips - Rose': (220, 20, 60),
    'Lips - Red': (178, 34, 34),
    'Lips - Dark Red': (139, 0, 0),
    'Eyes - Blue': (70, 130, 180),
    'Eyes - Green': (34, 139, 34),
    'Eyes - Brown': (101, 67, 33),
    'Eyes - Hazel': (112, 101, 80),
    'Eyes - Gray': (119, 136, 153),
}

# Nature colors
NATURE_COLORS = {
    'Grass - Light Green': (144, 238, 144),
    'Grass - Green': (34, 139, 34),
    'Grass - Dark Green': (0, 100, 0),
    'Grass - Yellow Green': (154, 205, 50),
    'Grass - Dry': (189, 183, 107),
    'Leaves - Spring Green': (0, 250, 154),
    'Leaves - Green': (50, 205, 50),
    'Leaves - Dark Green': (0, 128, 0),
    'Leaves - Autumn Yellow': (255, 215, 0),
    'Leaves - Autumn Orange': (255, 140, 0),
    'Leaves - Autumn Red': (178, 34, 34),
    'Leaves - Brown': (139, 69, 19),
    'Wood - Light': (222, 184, 135),
    'Wood - Oak': (205, 133, 63),
    'Wood - Walnut': (139, 90, 43),
    'Wood - Dark': (101, 67, 33),
    'Wood - Mahogany': (128, 64, 48),
    'Tree Bark': (101, 84, 67),
}

# Earth and stone colors
EARTH_COLORS = {
    'Stone - Light Gray': (211, 211, 211),
    'Stone - Gray': (128, 128, 128),
    'Stone - Dark Gray': (105, 105, 105),
    'Stone - Granite': (131, 131, 130),
    'Stone - Marble': (240, 234, 214),
    'Stone - Sandstone': (237, 201, 175),
    'Ground - Sand': (244, 164, 96),
    'Ground - Dirt': (139, 90, 43),
    'Ground - Clay': (178, 102, 85),
    'Ground - Mud': (101, 67, 33),
    'Ground - Soil': (92, 64, 51),
    'Rock - Brown': (160, 82, 45),
    'Rock - Red': (165, 42, 42),
}

# Sky and water colors
SKY_WATER_COLORS = {
    'Sky - Light Blue': (135, 206, 250),
    'Sky - Blue': (70, 130, 180),
    'Sky - Deep Blue': (0, 105, 148),
    'Sky - Sunset Orange': (255, 140, 0),
    'Sky - Sunset Pink': (255, 182, 193),
    'Sky - Sunset Purple': (147, 112, 219),
    'Sky - Overcast': (176, 196, 222),
    'Cloud - White': (255, 255, 255),
    'Cloud - Gray': (192, 192, 192),
    'Cloud - Dark Gray': (128, 128, 128),
    'Water - Light Blue': (173, 216, 230),
    'Water - Blue': (30, 144, 255),
    'Water - Deep Blue': (0, 0, 139),
    'Water - Turquoise': (64, 224, 208),
    'Water - Teal': (0, 128, 128),
    'Water - Dark': (25, 25, 112),
}

# Material colors
MATERIAL_COLORS = {
    'Metal - Silver': (192, 192, 192),
    'Metal - Gold': (255, 215, 0),
    'Metal - Bronze': (205, 127, 50),
    'Metal - Copper': (184, 115, 51),
    'Metal - Iron': (112, 128, 144),
    'Metal - Steel': (169, 169, 169),
    'Metal - Chrome': (211, 211, 211),
    'Glass - Clear': (240, 248, 255),
    'Glass - Blue': (176, 224, 230),
    'Glass - Green': (152, 251, 152),
    'Glass - Amber': (255, 191, 0),
}

# Fabric colors
FABRIC_COLORS = {
    'Fabric - White': (255, 255, 255),
    'Fabric - Cream': (255, 253, 208),
    'Fabric - Beige': (245, 245, 220),
    'Fabric - Gray': (128, 128, 128),
    'Fabric - Black': (0, 0, 0),
    'Fabric - Red': (220, 20, 60),
    'Fabric - Blue': (65, 105, 225),
    'Fabric - Navy': (0, 0, 128),
    'Fabric - Green': (34, 139, 34),
    'Fabric - Yellow': (255, 215, 0),
    'Fabric - Orange': (255, 140, 0),
    'Fabric - Purple': (128, 0, 128),
    'Fabric - Pink': (255, 192, 203),
    'Fabric - Brown': (139, 69, 19),
    'Fabric - Denim': (21, 96, 189),
}

# Common objects
OBJECT_COLORS = {
    'Car - Red': (220, 20, 60),
    'Car - Blue': (0, 0, 255),
    'Car - Black': (0, 0, 0),
    'Car - White': (255, 255, 255),
    'Car - Silver': (192, 192, 192),
    'Car - Yellow': (255, 215, 0),
    'Building - Brick Red': (178, 34, 34),
    'Building - Concrete': (169, 169, 169),
    'Building - White': (255, 255, 255),
    'Building - Beige': (245, 245, 220),
    'Road - Asphalt': (64, 64, 64),
    'Road - Concrete': (192, 192, 192),
    'Roof - Red Tile': (178, 34, 34),
    'Roof - Gray Shingle': (105, 105, 105),
    'Roof - Black': (28, 28, 28),
    'Door - Wood': (139, 90, 43),
    'Door - White': (255, 255, 255),
    'Door - Red': (178, 34, 34),
    'Window - Glass': (176, 224, 230),
    'Flower - Red': (255, 0, 0),
    'Flower - Pink': (255, 192, 203),
    'Flower - Yellow': (255, 255, 0),
    'Flower - Purple': (128, 0, 128),
    'Flower - White': (255, 255, 255),
    'Flower - Orange': (255, 165, 0),
}

# All categories combined
COLOR_CATEGORIES = {
    'Human': HUMAN_COLORS,
    'Nature': NATURE_COLORS,
    'Earth & Stone': EARTH_COLORS,
    'Sky & Water': SKY_WATER_COLORS,
    'Materials': MATERIAL_COLORS,
    'Fabrics': FABRIC_COLORS,
    'Objects': OBJECT_COLORS,
}

def get_category_colors_array(category_name):
    """Get colors for a category as numpy array (N, 3) with values 0-255"""
    if category_name not in COLOR_CATEGORIES:
        return None
    colors = COLOR_CATEGORIES[category_name]
    return np.array(list(colors.values()), dtype=np.uint8)

def get_category_color_names(category_name):
    """Get color names for a category"""
    if category_name not in COLOR_CATEGORIES:
        return None
    return list(COLOR_CATEGORIES[category_name].keys())

def get_all_categories():
    """Get list of all category names"""
    return list(COLOR_CATEGORIES.keys())
