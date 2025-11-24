import unittest
from hair_recommendation_agent import HairRecommendationAgent
from agent_core_framework import AgentTask


class TestHairRecommendationAgent(unittest.TestCase):
    """Test cases for HairRecommendationAgent"""

    def setUp(self):
        """Set up the test fixture"""
        self.agent = HairRecommendationAgent()

    def test_agent_initialization(self):
        """Test agent initialization"""
        self.assertEqual(self.agent.name, "HairRecommendation")
        self.assertEqual(self.agent.version, "1.0.0")
        self.assertIn("get_hairstyle_recommendations", self.agent.supported_tasks)

    def test_get_hairstyle_recommendations_success(self):
        """Test successful hairstyle recommendations"""
        task = AgentTask(
            type="get_hairstyle_recommendations",
            payload={
                "face_shape": "oval",
                "hair_type": "wavy",
                "personal_style": "bohemian",
                "age_group": "adult",
                "gender": "female",
                "hair_length": "medium"
            }
        )

        response = self.agent.process(task)

        self.assertTrue(response.success)
        # En lugar de assertIsNone, verifica que no haya mensaje de error
        self.assertFalse(response.error)  # Esto pasa si error es None o string vacío
        self.assertEqual(response.agent_name, "HairRecommendation")

        # Check response structure
        data = response.data
        self.assertIn("recommendations", data)
        self.assertIn("analysis", data)
        self.assertIn("compatibility_score", data)
        self.assertIn("seasonal_trends", data)
        self.assertIn("professional_advice", data)

        # Check recommendations
        recommendations = data["recommendations"]
        self.assertLessEqual(len(recommendations), 8)

        if recommendations:
            first_rec = recommendations[0]
            self.assertIn("style_name", first_rec)
            self.assertIn("display_name", first_rec)
            self.assertIn("confidence_score", first_rec)

    def test_get_hairstyle_recommendations_missing_required_fields(self):
        """Test recommendations with missing required fields"""
        task = AgentTask(
            type="get_hairstyle_recommendations",
            payload={
                "hair_type": "wavy"  # Missing face_shape
            }
        )

        response = self.agent.process(task)

        self.assertFalse(response.success)
        self.assertIn("Face shape and hair type are required", response.error)

    def test_analyze_style_compatibility_success(self):
        """Test style compatibility analysis"""
        task = AgentTask(
            type="analyze_style_compatibility",
            payload={
                "style_name": "curtain_bangs",
                "face_shape": "oval",
                "hair_type": "straight"
            }
        )

        response = self.agent.process(task)

        self.assertTrue(response.success)
        self.assertFalse(response.error)  # En lugar de assertIsNone

        data = response.data
        self.assertIn("style_analysis", data)
        self.assertIn("face_shape_compatibility", data)
        self.assertIn("hair_type_requirements", data)
        self.assertIn("daily_maintenance", data)
        self.assertIn("professional_opinion", data)
        self.assertIn("overall_score", data)

    def test_analyze_style_compatibility_missing_fields(self):
        """Test style analysis with missing fields"""
        task = AgentTask(
            type="analyze_style_compatibility",
            payload={
                "style_name": "curtain_bangs"
                # Missing face_shape and hair_type
            }
        )

        response = self.agent.process(task)

        self.assertFalse(response.success)
        self.assertIn("Style name, face shape and hair type are required", response.error)

    def test_get_trending_styles(self):
        """Test trending styles retrieval"""
        task = AgentTask(
            type="get_trending_styles",
            payload={
                "season": "spring"
            }
        )

        response = self.agent.process(task)

        self.assertTrue(response.success)
        self.assertFalse(response.error)  # En lugar de assertIsNone

        data = response.data
        self.assertIn("season", data)
        self.assertIn("trending_styles", data)
        self.assertIn("seasonal_advice", data)

        trending_styles = data["trending_styles"]
        self.assertGreater(len(trending_styles), 0)

    def test_unsupported_task(self):
        """Test unsupported task type"""
        task = AgentTask(
            type="unsupported_task",
            payload={}
        )

        response = self.agent.process(task)

        self.assertFalse(response.success)
        self.assertIn("Unsupported task", response.error)

    def test_calculate_style_score(self):
        """Test style score calculation"""
        score = self.agent._calculate_style_score(
            style="long_layers",
            face_shape="oval",
            hair_type="wavy",
            personal_style="bohemian",
            age_group="adult",
            gender="female"
        )

        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_face_shape_scoring(self):
        """Test face shape scoring logic"""
        # Test excellent match
        excellent_score = self.agent._get_face_shape_score("long_layers", "oval")
        self.assertEqual(excellent_score, 1.0)

        # Test good match
        good_score = self.agent._get_face_shape_score("blunt_bob", "oval")
        self.assertEqual(good_score, 0.8)

        # Test neutral (not specified)
        neutral_score = self.agent._get_face_shape_score("unknown_style", "oval")
        self.assertEqual(neutral_score, 0.4)

    def test_hair_type_scoring(self):
        """Test hair type scoring logic"""
        # Test perfect match
        perfect_score = self.agent._get_hair_type_score("beach_waves", "wavy")
        self.assertEqual(perfect_score, 1.0)

        # Test requires styling
        styling_score = self.agent._get_hair_type_score("blunt_bob", "wavy")
        self.assertEqual(styling_score, 0.5)

    def test_get_all_possible_styles(self):
        """Test retrieval of all possible styles"""
        all_styles = self.agent._get_all_possible_styles()

        self.assertIsInstance(all_styles, list)
        self.assertGreater(len(all_styles), 0)

        # Check that we have some expected styles
        expected_styles = ["long_layers", "blunt_bob", "curtain_bangs"]
        for style in expected_styles:
            self.assertIn(style, all_styles)

    def test_style_name_formatting(self):
        """Test style name formatting"""
        formatted = self.agent._format_style_name("curtain_bangs")
        self.assertEqual(formatted, "Curtain Bangs")

        formatted = self.agent._format_style_name("long_layers")
        self.assertEqual(formatted, "Long Layers")

    def test_face_shape_compatibility_descriptions(self):
        """Test face shape compatibility descriptions"""
        description = self.agent._get_face_shape_match("long_layers", "oval")
        self.assertIn("compatibility", description)

    def test_hair_type_compatibility_descriptions(self):
        """Test hair type compatibility descriptions"""
        description = self.agent._get_hair_type_compatibility("beach_waves", "wavy")
        self.assertIn("Perfect", description)

    def test_maintenance_levels(self):
        """Test maintenance level descriptions"""
        maintenance = self.agent._get_maintenance_level("blunt_bob")
        self.assertIn("maintenance", maintenance)

        maintenance = self.agent._get_maintenance_level("beach_waves")
        self.assertIn("maintenance", maintenance)

    def test_styling_time_calculation(self):
        """Test styling time calculation"""
        styling_time = self.agent._get_styling_time("long_layers", "straight")
        self.assertIsInstance(styling_time, str)
        self.assertIn("minutes", styling_time)

    def test_professional_rating(self):
        """Test professional rating system"""
        rating = self.agent._get_professional_rating("long_layers", "oval")
        self.assertIsInstance(rating, str)
        self.assertIn("⭐", rating)

    def test_style_description(self):
        """Test style description retrieval"""
        description = self.agent._get_style_description("long_layers")
        self.assertIsInstance(description, str)
        self.assertGreater(len(description), 0)

    def test_hair_length_compatibility(self):
        """Test hair length compatibility checking"""
        # Test compatible length
        compatible = self.agent._check_hair_length_compatibility("long_layers", "long")
        self.assertTrue(compatible)

        # Test incompatible length
        compatible = self.agent._check_hair_length_compatibility("long_layers", "short")
        self.assertFalse(compatible)

    def test_error_handling(self):
        """Test error handling for invalid inputs"""
        # Test with invalid face shape
        task = AgentTask(
            type="get_hairstyle_recommendations",
            payload={
                "face_shape": "invalid_shape",
                "hair_type": "wavy"
            }
        )

        response = self.agent.process(task)
        self.assertTrue(response.success)  # Should handle gracefully
        self.assertFalse(response.error)  # No error message

        # Check that we still get some recommendations
        self.assertGreater(len(response.data["recommendations"]), 0)

    def test_performance_recommendations(self):
        """Test performance of recommendations generation"""
        import time

        start_time = time.time()

        task = AgentTask(
            type="get_hairstyle_recommendations",
            payload={
                "face_shape": "oval",
                "hair_type": "wavy"
            }
        )

        response = self.agent.process(task)
        end_time = time.time()

        # Should complete in reasonable time (under 1 second)
        self.assertLess(end_time - start_time, 1.0)
        self.assertTrue(response.success)
        self.assertFalse(response.error)

    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Test with all optional parameters
        task = AgentTask(
            type="get_hairstyle_recommendations",
            payload={
                "face_shape": "round",
                "hair_type": "curly",
                "personal_style": "professional",
                "age_group": "teen",
                "gender": "male",
                "hair_length": "short"
            }
        )

        response = self.agent.process(task)
        self.assertTrue(response.success)
        self.assertFalse(response.error)

        recommendations = response.data["recommendations"]
        # Should return some recommendations even with specific constraints
        self.assertGreater(len(recommendations), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)