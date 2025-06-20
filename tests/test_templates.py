from deepseek_browser.templates import TaskTemplate, TemplateLibrary


def test_template_render_and_variables():
    tpl = TaskTemplate(name="search", content="Find {topic} news")
    assert tpl.variables() == {"topic"}
    assert tpl.render(topic="AI") == "Find AI news"


def test_template_missing_variable():
    tpl = TaskTemplate(name="search", content="Find {topic} news")
    try:
        tpl.render()
        assert False, "expected error"
    except ValueError as exc:
        assert "Missing variables" in str(exc)


def test_library_add_and_versioning():
    lib = TemplateLibrary()
    tpl_v1 = TaskTemplate(name="t", content="A {x}")
    lib.add(tpl_v1)
    tpl_v2 = TaskTemplate(name="t", content="B {x}", version=2)
    lib.add(tpl_v2)
    assert lib.render("t", x="1") == "B 1"
    # older version should fail
    try:
        lib.add(tpl_v1)
        assert False, "expected error"
    except ValueError:
        pass


def test_compose_and_io():
    lib = TemplateLibrary()
    lib.add(TaskTemplate(name="a", content="Hello {name}"))
    lib.add(TaskTemplate(name="b", content="How are {name}?", version=2))
    desc = lib.compose(["a", "b"], name="Bob")
    assert desc == "Hello Bob How are Bob?"
    data = lib.export_json()
    lib2 = TemplateLibrary.import_json(data)
    assert lib2.render("a", name="Bob") == "Hello Bob"
