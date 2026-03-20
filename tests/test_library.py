"""Tests for PromptLibrary."""

from playbooks import Prompt, PromptLibrary


class TestPrompt:
    """Test Prompt class."""

    def test_prompt_creation(self):
        """Test creating a Prompt instance."""
        prompt = Prompt(
            id="test-001",
            name="Test Prompt",
            category="deployment",
            version="1.0.0",
            prompt_text="Test prompt: {service_name}",
            metadata={"quality_score": 0.95},
            inputs=[{"name": "service_name"}],
            outputs=[{"name": "result"}],
        )

        assert prompt.id == "test-001"
        assert prompt.name == "Test Prompt"
        assert prompt.category == "deployment"

    def test_prompt_customize(self):
        """Test customizing a prompt."""
        prompt = Prompt(
            id="test-001",
            name="Test",
            category="deployment",
            version="1.0.0",
            prompt_text="Service: {service_name}, Risk: {risk_level}",
            metadata={},
            inputs=[],
            outputs=[],
        )

        customized = prompt.customize(service_name="api", risk_level="critical")
        assert customized == "Service: api, Risk: critical"

    def test_prompt_quality_score(self):
        """Test quality score retrieval."""
        prompt = Prompt(
            id="test-001",
            name="Test",
            category="deployment",
            version="1.0.0",
            prompt_text="Test",
            metadata={"quality_score": 0.85},
            inputs=[],
            outputs=[],
        )

        assert prompt.get_quality_score() == 0.85

    def test_prompt_production_tested(self):
        """Test production tested flag."""
        prompt = Prompt(
            id="test-001",
            name="Test",
            category="deployment",
            version="1.0.0",
            prompt_text="Test",
            metadata={"production_tested": True},
            inputs=[],
            outputs=[],
        )

        assert prompt.is_production_tested() is True

    def test_prompt_test_count(self):
        """Test test count retrieval."""
        prompt = Prompt(
            id="test-001",
            name="Test",
            category="deployment",
            version="1.0.0",
            prompt_text="Test",
            metadata={"test_count": 42},
            inputs=[],
            outputs=[],
        )

        assert prompt.get_test_count() == 42


class TestPromptLibrary:
    """Test PromptLibrary class."""

    def test_library_creation(self):
        """Test creating a PromptLibrary instance."""
        library = PromptLibrary()
        assert library.prompts_dir is not None
        assert isinstance(library.prompts, dict)

    def test_library_list_prompts(self):
        """Test listing prompts."""
        library = PromptLibrary()
        prompts = library.list_prompts()

        # Should have at least the deployment prompt
        assert len(prompts) >= 1
        assert all(isinstance(p, Prompt) for p in prompts)

    def test_library_list_by_category(self):
        """Test listing prompts by category."""
        library = PromptLibrary()
        deployment_prompts = library.list_prompts(category="deployment")

        # Should have the deployment prompt
        assert len(deployment_prompts) >= 1
        assert all(p.category == "deployment" for p in deployment_prompts)

    def test_library_get_prompt(self):
        """Test getting a specific prompt."""
        library = PromptLibrary()
        prompt = library.get_prompt("deployment")

        assert prompt is not None
        assert prompt.category == "deployment"

    def test_library_get_prompt_by_task(self):
        """Test getting prompt by category and task."""
        library = PromptLibrary()
        prompt = library.get_prompt("deployment", "canary")

        assert prompt is not None
        assert "canary" in prompt.id.lower()

    def test_library_get_nonexistent_prompt(self):
        """Test getting a non-existent prompt."""
        library = PromptLibrary()
        prompt = library.get_prompt("nonexistent_category")

        assert prompt is None

    def test_library_list_categories(self):
        """Test listing categories."""
        library = PromptLibrary()
        categories = library.list_categories()

        assert len(categories) >= 1
        assert "deployment" in categories

    def test_library_search(self):
        """Test searching prompts."""
        library = PromptLibrary()
        results = library.search("canary")

        # Should find canary rollout prompt
        assert len(results) >= 1
        assert any("canary" in p.id.lower() for p in results)

    def test_library_search_case_insensitive(self):
        """Test search is case insensitive."""
        library = PromptLibrary()
        results_lower = library.search("canary")
        results_upper = library.search("CANARY")

        assert len(results_lower) == len(results_upper)

    def test_library_search_no_results(self):
        """Test search with no results."""
        library = PromptLibrary()
        results = library.search("nonexistent_prompt_xyz")

        assert len(results) == 0
