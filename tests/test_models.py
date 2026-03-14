from app.models import Admin, Profile, Project, Skill, Experience, Message, CodingProfile


def test_admin_password(db):
    """Test Admin password hashing."""
    admin = Admin(username="testuser")
    admin.set_password("secret123")
    db.session.add(admin)
    db.session.commit()

    assert admin.check_password("secret123")
    assert not admin.check_password("wrong")


def test_profile_creation(db):
    """Test Profile model creation."""
    profile = Profile(name="John Doe", title="Developer", bio="Hello world")
    db.session.add(profile)
    db.session.commit()

    assert profile.id is not None
    assert profile.name == "John Doe"


def test_project_creation(db):
    """Test Project model creation."""
    project = Project(title="My Project", description="A test project")
    db.session.add(project)
    db.session.commit()

    assert project.id is not None


def test_skill_creation(db):
    """Test Skill model creation."""
    skill = Skill(name="Python")
    db.session.add(skill)
    db.session.commit()

    assert skill.id is not None
    assert skill.name == "Python"


def test_coding_profile_creation(db):
    """Test CodingProfile model creation."""
    cp = CodingProfile(
        platform="LeetCode",
        username="testuser",
        problems_solved=150,
        rating="1800",
    )
    db.session.add(cp)
    db.session.commit()

    assert cp.id is not None
    assert cp.platform == "LeetCode"


def test_message_creation(db):
    """Test Message model creation."""
    msg = Message(name="Test", email="test@test.com", subject="Hi", message="Hello")
    db.session.add(msg)
    db.session.commit()

    assert msg.id is not None
    assert msg.created_at is not None
