from agent_core_framework import BaseAgent, AgentTask, AgentResponse
from typing import Dict, Any, List
from .data import FACE_SHAPE_RECOMMENDATIONS, HAIR_TYPE_RECOMMENDATIONS, STYLE_PROFILES, HAIR_STYLES_DETAILED


class HairRecommendationAgent(BaseAgent):
    """
    Specialized agent for advanced hairstyle recommendations
    using rule-based systems and scoring algorithms
    """

    def __init__(self):
        super().__init__("HairRecommendation", "1.0.0")
        self.supported_tasks = [
            "get_hairstyle_recommendations",
            "analyze_style_compatibility",
            "get_trending_styles"
        ]

        # Recommendation weights
        self.weights = {
            'face_shape': 0.4,
            'hair_type': 0.3,
            'personal_style': 0.2,
            'trend_factor': 0.1
        }

        # Maintenance levels mapping
        self.maintenance_levels = {
            "low": "Low maintenance - easy to maintain style",
            "medium": "Moderate maintenance - requires some care",
            "high": "High maintenance - needs regular attention"
        }

        # Age group suitability
        self.age_groups = {
            "teen": (13, 19),
            "young_adult": (20, 35),
            "adult": (36, 55),
            "mature": (56, 100)
        }

    def process(self, task: AgentTask) -> AgentResponse:
        try:
            if task.type == "get_hairstyle_recommendations":
                return self._get_hairstyle_recommendations(task.payload)
            elif task.type == "analyze_style_compatibility":
                return self._analyze_style_compatibility(task.payload)
            elif task.type == "get_trending_styles":
                return self._get_trending_styles(task.payload)
            else:
                return AgentResponse(
                    success=False,
                    error=f"Unsupported task: {task.type}",
                    agent_name=self.name
                )

        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"Recommendation error: {str(e)}",
                agent_name=self.name
            )

    def _get_hairstyle_recommendations(self, payload: Dict[str, Any]) -> AgentResponse:
        """Get advanced hairstyle recommendations with scoring"""
        face_shape = payload.get('face_shape')
        hair_type = payload.get('hair_type')
        personal_style = payload.get('personal_style', 'versatile')
        age_group = payload.get('age_group', 'adult')
        gender = payload.get('gender', 'unisex')
        hair_length = payload.get('hair_length')

        # Validate inputs
        if not face_shape or not hair_type:
            return AgentResponse(
                success=False,
                error="Face shape and hair type are required",
                agent_name=self.name
            )

        # Generate scored recommendations
        recommendations = self._generate_scored_recommendations(
            face_shape, hair_type, personal_style, age_group, gender, hair_length
        )

        return AgentResponse(
            success=True,
            data={
                "recommendations": recommendations,
                "analysis": self._get_style_analysis(face_shape, hair_type, personal_style),
                "compatibility_score": self._calculate_overall_compatibility(face_shape, hair_type),
                "seasonal_trends": self._get_seasonal_trends(),
                "professional_advice": self._get_professional_advice(face_shape, hair_type)
            },
            agent_name=self.name
        )

    def _generate_scored_recommendations(self, face_shape: str, hair_type: str,
                                         personal_style: str, age_group: str,
                                         gender: str, hair_length: str = None) -> List[Dict]:
        """Generate recommendations with confidence scores"""
        all_styles = self._get_all_possible_styles()
        scored_recommendations = []

        for style in all_styles:
            score = self._calculate_style_score(style, face_shape, hair_type,
                                                personal_style, age_group, gender)

            # Apply hair length filter if specified
            if hair_length and not self._check_hair_length_compatibility(style, hair_length):
                continue

            if score > 0.3:  # Minimum threshold
                scored_recommendations.append({
                    "style_name": style,
                    "display_name": self._format_style_name(style),
                    "confidence_score": round(score, 2),
                    "face_shape_match": self._get_face_shape_match(style, face_shape),
                    "hair_type_compatibility": self._get_hair_type_compatibility(style, hair_type),
                    "style_alignment": self._get_style_alignment(style, personal_style),
                    "maintenance_level": self._get_maintenance_level(style),
                    "styling_time": self._get_styling_time(style, hair_type),
                    "professional_rating": self._get_professional_rating(style, face_shape),
                    "description": self._get_style_description(style)
                })

        # Sort by confidence score
        scored_recommendations.sort(key=lambda x: x['confidence_score'], reverse=True)
        return scored_recommendations[:8]  # Return top 8

    def _calculate_style_score(self, style: str, face_shape: str, hair_type: str,
                               personal_style: str, age_group: str, gender: str) -> float:
        """Calculate overall score for a hairstyle"""
        scores = {
            'face_shape': self._get_face_shape_score(style, face_shape),
            'hair_type': self._get_hair_type_score(style, hair_type),
            'personal_style': self._get_personal_style_score(style, personal_style),
            'age_suitability': self._get_age_suitability(style, age_group),
            'gender_suitability': self._get_gender_suitability(style, gender)
        }

        # Weighted average
        total_score = sum(scores[key] * self.weights.get(key, 0.2) for key in scores)
        return min(1.0, total_score)

    def _get_face_shape_score(self, style: str, face_shape: str) -> float:
        """Calculate face shape compatibility score"""
        recommendations = FACE_SHAPE_RECOMMENDATIONS.get(face_shape, {})

        if style in recommendations.get('excellent', []):
            return 1.0
        elif style in recommendations.get('good', []):
            return 0.8
        elif style in recommendations.get('fair', []):
            return 0.6
        elif style in recommendations.get('avoid', []):
            return 0.2
        else:
            return 0.4  # Neutral

    def _get_hair_type_score(self, style: str, hair_type: str) -> float:
        """Calculate hair type compatibility score"""
        compatibility = HAIR_TYPE_RECOMMENDATIONS.get(hair_type, {})

        if style in compatibility.get('perfect', []):
            return 1.0
        elif style in compatibility.get('good', []):
            return 0.8
        elif style in compatibility.get('requires_styling', []):
            return 0.5
        else:
            return 0.3

    def _get_personal_style_score(self, style: str, personal_style: str) -> float:
        """Calculate personal style alignment score"""
        if personal_style == 'versatile':
            return 0.7  # Neutral score for versatile style

        profile = STYLE_PROFILES.get(personal_style, {})
        if style in profile.get('recommended_styles', []):
            return 1.0
        else:
            # Check if style is compatible with any profile
            for profile_name, profile_data in STYLE_PROFILES.items():
                if style in profile_data.get('recommended_styles', []):
                    return 0.6  # Somewhat compatible
            return 0.4

    def _get_age_suitability(self, style: str, age_group: str) -> float:
        """Calculate age suitability score"""
        # Default implementation - can be enhanced with age-specific rules
        age_appropriate_styles = {
            "teen": ["beach_waves", "side_swept_bangs", "messy_bun", "curtain_bangs"],
            "young_adult": ["long_layers", "textured_bob", "blunt_bob", "soft_layers"],
            "adult": ["soft_layers", "blunt_bob", "long_layers", "curtain_bangs"],
            "mature": ["soft_layers", "blunt_bob", "pixie_cut", "wispy_bangs"]
        }

        if style in age_appropriate_styles.get(age_group, []):
            return 1.0
        else:
            return 0.7  # Most styles are generally appropriate

    def _get_gender_suitability(self, style: str, gender: str) -> float:
        """Calculate gender suitability score"""
        if gender == 'unisex':
            return 0.8

        gender_specific_styles = {
            "female": ["blunt_bob", "long_layers", "curtain_bangs", "beach_waves"],
            "male": ["textured_crop", "fade_cut", "side_swept_bangs", "soft_layers"]
        }

        if style in gender_specific_styles.get(gender, []):
            return 1.0
        else:
            return 0.6  # Many styles are unisex

    def _analyze_style_compatibility(self, payload: Dict[str, Any]) -> AgentResponse:
        """Analyze compatibility of a specific hairstyle"""
        style = payload.get('style_name')
        face_shape = payload.get('face_shape')
        hair_type = payload.get('hair_type')

        if not style or not face_shape or not hair_type:
            return AgentResponse(
                success=False,
                error="Style name, face shape and hair type are required",
                agent_name=self.name
            )

        analysis = {
            "style_analysis": self._get_detailed_style_analysis(style),
            "face_shape_compatibility": self._get_face_shape_match(style, face_shape),
            "hair_type_requirements": self._get_hair_requirements(style, hair_type),
            "daily_maintenance": self._get_daily_maintenance(style, hair_type),
            "professional_opinion": self._get_professional_opinion(style, face_shape, hair_type),
            "overall_score": self._calculate_style_score(style, face_shape, hair_type, "versatile", "adult", "unisex")
        }

        return AgentResponse(
            success=True,
            data=analysis,
            agent_name=self.name
        )

    def _get_trending_styles(self, payload: Dict[str, Any]) -> AgentResponse:
        """Get currently trending hairstyles"""
        season = payload.get('season', 'all')

        trending_styles = {
            "spring": ["curtain_bangs", "soft_layers", "beach_waves", "wispy_bangs"],
            "summer": ["textured_bob", "messy_bun", "side_swept_bangs", "curly_shag"],
            "fall": ["blunt_bob", "long_layers", "curtain_bangs", "soft_waves"],
            "winter": ["layered_shag", "blunt_bob", "sleek_pony", "defined_curls"],
            "all": ["curtain_bangs", "textured_bob", "soft_layers", "beach_waves"]
        }

        styles = trending_styles.get(season, trending_styles["all"])

        detailed_trends = []
        for style in styles:
            detailed_trends.append({
                "style_name": style,
                "display_name": self._format_style_name(style),
                "description": self._get_style_description(style),
                "popularity_reason": self._get_trend_reason(style, season)
            })

        return AgentResponse(
            success=True,
            data={
                "season": season,
                "trending_styles": detailed_trends,
                "seasonal_advice": self._get_seasonal_advice(season)
            },
            agent_name=self.name
        )

    # Helper methods
    def _get_all_possible_styles(self) -> List[str]:
        """Get all available hairstyles"""
        all_styles = set()
        for shapes in FACE_SHAPE_RECOMMENDATIONS.values():
            for category in ['excellent', 'good', 'fair']:
                all_styles.update(shapes.get(category, []))
        return list(all_styles)

    def _format_style_name(self, style: str) -> str:
        """Format style name for display"""
        return style.replace('_', ' ').title()

    def _get_face_shape_match(self, style: str, face_shape: str) -> str:
        """Get face shape match description"""
        score = self._get_face_shape_score(style, face_shape)
        if score >= 0.8:
            return "Excellent compatibility"
        elif score >= 0.6:
            return "Good compatibility"
        elif score >= 0.4:
            return "Moderate compatibility"
        else:
            return "Not recommended for this face shape"

    def _get_hair_type_compatibility(self, style: str, hair_type: str) -> str:
        """Get hair type compatibility description"""
        score = self._get_hair_type_score(style, hair_type)
        if score >= 0.8:
            return "Perfect for your hair type"
        elif score >= 0.6:
            return "Good for your hair type"
        elif score >= 0.4:
            return "Requires additional styling"
        else:
            return "Not compatible with your hair type"

    def _get_style_alignment(self, style: str, personal_style: str) -> str:
        """Get style alignment description"""
        if personal_style == 'versatile':
            return "Versatile style"

        profile_styles = STYLE_PROFILES.get(personal_style, {}).get('recommended_styles', [])
        if style in profile_styles:
            return f"Perfect for {personal_style} style"
        else:
            return "Adaptable style"

    def _get_maintenance_level(self, style: str) -> str:
        """Get maintenance level description"""
        style_info = HAIR_STYLES_DETAILED.get(style, {})
        maintenance = style_info.get('maintenance', 'medium')
        return self.maintenance_levels.get(maintenance, "Moderate maintenance")

    def _get_styling_time(self, style: str, hair_type: str) -> str:
        """Get estimated styling time"""
        style_info = HAIR_STYLES_DETAILED.get(style, {})
        base_time = style_info.get('styling_time', '10-15 minutes')

        # Adjust based on hair type
        if hair_type in ['curly', 'coily']:
            return f"{base_time} + extra time for definition"
        elif hair_type == 'fine':
            return f"{base_time} + volume products"
        else:
            return base_time

    def _get_professional_rating(self, style: str, face_shape: str) -> str:
        """Get professional rating"""
        score = self._get_face_shape_score(style, face_shape)
        if score >= 0.9:
            return "⭐️⭐️⭐️⭐️⭐️ (Excellent)"
        elif score >= 0.7:
            return "⭐️⭐️⭐️⭐️ (Very Good)"
        elif score >= 0.5:
            return "⭐️⭐️⭐️ (Good)"
        else:
            return "⭐️⭐️ (Fair)"

    def _get_style_description(self, style: str) -> str:
        """Get style description"""
        style_info = HAIR_STYLES_DETAILED.get(style, {})
        return style_info.get('description', 'Modern and versatile style')

    def _check_hair_length_compatibility(self, style: str, hair_length: str) -> bool:
        """Check if style is compatible with hair length"""
        style_info = HAIR_STYLES_DETAILED.get(style, {})
        compatible_lengths = style_info.get('hair_lengths', [])
        return hair_length in compatible_lengths if compatible_lengths else True

    def _get_style_analysis(self, face_shape: str, hair_type: str, personal_style: str) -> Dict:
        """Get overall style analysis"""
        return {
            "strengths": f"Your {face_shape} face shape and {hair_type} hair create great styling opportunities",
            "considerations": "Consider face-framing layers to enhance your features",
            "trend_alignment": f"Your {personal_style} style aligns with current 'effortless chic' trends",
            "professional_tip": "Regular trims will maintain your style's shape and health"
        }

    def _calculate_overall_compatibility(self, face_shape: str, hair_type: str) -> float:
        """Calculate overall compatibility score"""
        # Simplified implementation
        return 0.85  # Can be enhanced with more complex logic

    def _get_seasonal_trends(self) -> Dict:
        """Get seasonal trends"""
        return {
            "current_trends": ["curtain_bangs", "textured_bob", "soft_layers"],
            "emerging_trends": ["micro_bangs", "wolf_cut", "butterfly_layers"],
            "classic_styles": ["blunt_bob", "long_layers", "pixie_cut"]
        }

    def _get_professional_advice(self, face_shape: str, hair_type: str) -> str:
        """Get professional advice"""
        advice_map = {
            "round": "Avoid side volume that widens the face",
            "oval": "You can experiment with almost any style",
            "square": "Prefer styles that soften the jawline",
            "heart": "Focus on balancing the wide forehead",
            "fine": "Use layers to create volume and movement",
            "thick": "Consider thinning for better manageability"
        }
        return advice_map.get(face_shape, "Consult with a professional stylist") + ". " + \
            advice_map.get(hair_type, "Care for your hair type with specific products")

    def _get_detailed_style_analysis(self, style: str) -> Dict:
        """Get detailed analysis for a specific style"""
        style_info = HAIR_STYLES_DETAILED.get(style, {})
        return {
            "description": style_info.get('description', 'Versatile style'),
            "best_for": f"{', '.join(style_info.get('face_shapes', []))} face shapes",
            "maintenance": style_info.get('maintenance', 'medium'),
            "styling_tips": self._get_styling_tips(style),
            "products_recommended": self._get_recommended_products(style)
        }

    def _get_hair_requirements(self, style: str, hair_type: str) -> List[str]:
        """Get hair requirements for a style"""
        requirements = []
        style_info = HAIR_STYLES_DETAILED.get(style, {})

        if hair_type not in style_info.get('hair_types', []):
            requirements.append(f"May require adaptation for {hair_type} hair")

        if style_info.get('maintenance') == 'high':
            requirements.append("Needs regular professional maintenance")

        return requirements if requirements else ["Low special requirements"]

    def _get_daily_maintenance(self, style: str, hair_type: str) -> str:
        """Get daily maintenance routine"""
        maintenance_map = {
            "low": "Wash and air dry naturally",
            "medium": "Occasional use of styling tools",
            "high": "Daily styling routine with products"
        }
        style_info = HAIR_STYLES_DETAILED.get(style, {})
        base_maintenance = maintenance_map.get(style_info.get('maintenance', 'medium'))

        if hair_type in ['curly', 'coily']:
            return f"{base_maintenance} + definition products"
        return base_maintenance

    def _get_professional_opinion(self, style: str, face_shape: str, hair_type: str) -> str:
        """Get professional opinion"""
        face_score = self._get_face_shape_score(style, face_shape)
        hair_score = self._get_hair_type_score(style, hair_type)

        if face_score >= 0.8 and hair_score >= 0.8:
            return "✅ Professional recommendation: Excellent choice"
        elif face_score >= 0.6 and hair_score >= 0.6:
            return "⚠️ Professional recommendation: Good option with some considerations"
        else:
            return "❌ Professional recommendation: Consider other alternatives"

    def _get_styling_tips(self, style: str) -> List[str]:
        """Get styling tips for a specific style"""
        tips_map = {
            "curtain_bangs": ["Use flat iron to create soft waves", "Apply texturizer for movement"],
            "blunt_bob": ["Keep ends straight with flat iron", "Use serum for shine"],
            "beach_waves": ["Apply salt spray on damp hair", "Scrunch with fingers while drying"]
        }
        return tips_map.get(style, ["Consult with your stylist for personalized tips"])

    def _get_recommended_products(self, style: str) -> List[str]:
        """Get recommended products for a style"""
        products_map = {
            "curtain_bangs": ["Texturizer", "Medium hold spray"],
            "blunt_bob": ["Anti-frizz serum", "Ceramic flat iron"],
            "beach_waves": ["Salt spray", "Heat protectant"]
        }
        return products_map.get(style, ["Quality shampoo and conditioner"])

    def _get_trend_reason(self, style: str, season: str) -> str:
        """Get reason why style is trending"""
        reasons = {
            "curtain_bangs": "Versatile and flattering for multiple face shapes",
            "textured_bob": "Modern and easy to maintain",
            "soft_layers": "Adds movement without compromising length"
        }
        return reasons.get(style, "Popular style for its versatility and ease")

    def _get_seasonal_advice(self, season: str) -> str:
        """Get seasonal styling advice"""
        advice_map = {
            "spring": "Fresh styles that allow movement",
            "summer": "Cuts that keep hair away from the face",
            "fall": "Layers that add volume for cooler weather",
            "winter": "Styles that protect from cold and dryness"
        }
        return advice_map.get(season, "Adapt your style to weather conditions")