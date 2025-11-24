from hair_recommendation_agent.data.face_shape_rules import FACE_SHAPE_RECOMMENDATIONS
from hair_recommendation_agent.data.hair_type_rules import HAIR_TYPE_RECOMMENDATIONS

STYLE_PROFILES = {
    "professional": {
        "description": "Elegant styles appropriate for work environments",
        "recommended_styles": ["blunt_bob", "long_layers", "sleek_pony", "soft_layers", "textured_bob"],
        "hair_lengths": ["short", "medium", "long"],
        "maintenance_level": "medium",
        "styling_time": "10-20 minutes"
    },
    "bohemian": {
        "description": "Natural, effortless styles with movement",
        "recommended_styles": ["beach_waves", "layered_shag", "curtain_bangs", "messy_bun", "side_swept_bangs"],
        "hair_lengths": ["medium", "long"],
        "maintenance_level": "low",
        "styling_time": "5-15 minutes"
    },
    "edgy": {
        "description": "Modern, asymmetrical and bold cuts",
        "recommended_styles": ["asymmetrical_cut", "pixie_cut", "textured_crop", "undercut", "mohawk"],
        "hair_lengths": ["short", "medium"],
        "maintenance_level": "high",
        "styling_time": "15-25 minutes"
    },
    "romantic": {
        "description": "Soft, feminine styles with volume",
        "recommended_styles": ["soft_waves", "curtain_bangs", "wispy_bangs", "long_layers", "beach_waves"],
        "hair_lengths": ["medium", "long"],
        "maintenance_level": "medium",
        "styling_time": "15-20 minutes"
    },
    "minimalist": {
        "description": "Simple, functional low-maintenance styles",
        "recommended_styles": ["blunt_bob", "pixie_cut", "sleek_pony", "textured_crop", "soft_layers"],
        "hair_lengths": ["short", "medium"],
        "maintenance_level": "low",
        "styling_time": "5-10 minutes"
    },
    "glamorous": {
        "description": "Sophisticated and striking styles",
        "recommended_styles": ["voluminous_curls", "sleek_styles", "defined_curls", "beach_waves", "soft_waves"],
        "hair_lengths": ["medium", "long"],
        "maintenance_level": "high",
        "styling_time": "20-30 minutes"
    },
    "natural": {
        "description": "Styles that enhance natural hair texture",
        "recommended_styles": ["afro", "defined_curls", "beach_waves", "curly_shag", "twist_out"],
        "hair_lengths": ["short", "medium", "long"],
        "maintenance_level": "low",
        "styling_time": "5-15 minutes"
    }
}

HAIR_STYLES_DETAILED = {
    "long_layers": {
        "description": "Long layers that add movement and volume",
        "face_shapes": ["oval", "square", "round", "heart"],
        "hair_types": ["straight", "wavy", "curly", "thick"],
        "maintenance": "medium",
        "styling_time": "15-20 minutes",
        "hair_lengths": ["long"],
        "style_profiles": ["professional", "romantic", "bohemian"]
    },
    "blunt_bob": {
        "description": "Straight and defined bob cut",
        "face_shapes": ["oval", "square"],
        "hair_types": ["straight", "fine", "thick"],
        "maintenance": "high",
        "styling_time": "10-15 minutes",
        "hair_lengths": ["short", "medium"],
        "style_profiles": ["professional", "minimalist", "glamorous"]
    },
    "textured_bob": {
        "description": "Bob with texture and movement",
        "face_shapes": ["oval", "round", "square"],
        "hair_types": ["wavy", "straight", "fine"],
        "maintenance": "medium",
        "styling_time": "10-15 minutes",
        "hair_lengths": ["short", "medium"],
        "style_profiles": ["professional", "bohemian", "edgy"]
    },
    "curtain_bangs": {
        "description": "Bangs that frame the face",
        "face_shapes": ["oval", "heart", "diamond", "oblong"],
        "hair_types": ["straight", "wavy", "curly"],
        "maintenance": "high",
        "styling_time": "5-10 minutes",
        "hair_lengths": ["short", "medium", "long"],
        "style_profiles": ["romantic", "bohemian", "professional"]
    },
    "pixie_cut": {
        "description": "Short and modern cut",
        "face_shapes": ["oval", "heart", "diamond"],
        "hair_types": ["fine", "straight", "wavy"],
        "maintenance": "high",
        "styling_time": "5-10 minutes",
        "hair_lengths": ["short"],
        "style_profiles": ["edgy", "minimalist", "professional"]
    },
    "beach_waves": {
        "description": "Natural and effortless waves",
        "face_shapes": ["oval", "square", "round"],
        "hair_types": ["wavy", "straight", "thick"],
        "maintenance": "low",
        "styling_time": "15-20 minutes",
        "hair_lengths": ["medium", "long"],
        "style_profiles": ["bohemian", "romantic", "natural"]
    },
    "afro": {
        "description": "Natural style for afro hair",
        "face_shapes": ["oval", "diamond"],
        "hair_types": ["coily", "curly"],
        "maintenance": "low",
        "styling_time": "5-10 minutes",
        "hair_lengths": ["short", "medium", "long"],
        "style_profiles": ["natural", "bohemian"]
    }
}


def get_personalized_recommendations(face_shape, hair_type, style_profile=None, hair_length=None):
    """Get integrated recommendations based on multiple criteria"""

    face_recs = FACE_SHAPE_RECOMMENDATIONS.get(face_shape, {})
    hair_recs = HAIR_TYPE_RECOMMENDATIONS.get(hair_type, {})

    # Excellent styles for face shape
    excellent_face = set(face_recs.get("excellent", []))

    # Perfect styles for hair type
    perfect_hair = set(hair_recs.get("perfect", []))

    # Intersection - best recommendations
    best_matches = list(excellent_face.intersection(perfect_hair))

    # Filter by style profile if provided
    if style_profile and style_profile in STYLE_PROFILES:
        profile_styles = set(STYLE_PROFILES[style_profile]["recommended_styles"])
        best_matches = [style for style in best_matches if style in profile_styles]

    # Filter by hair length if provided
    if hair_length:
        best_matches = [style for style in best_matches
                        if hair_length in HAIR_STYLES_DETAILED.get(style, {}).get("hair_lengths", [])]

    return {
        "best_matches": best_matches,
        "face_shape_recommendations": face_recs,
        "hair_type_recommendations": hair_recs,
        "style_profiles": STYLE_PROFILES.get(style_profile) if style_profile else None
    }