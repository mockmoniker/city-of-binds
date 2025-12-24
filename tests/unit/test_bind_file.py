"""
Unit tests for BindFile class.

These tests focus on BindFile creation, modification, representation, and validation.
"""

import pytest
from pathlib import Path
from CityOfBinds import Bind, BindFile
from CityOfBinds.src.game.utils import _Comment, _CommentBanner


class TestBindFileCreation:
    """Test BindFile object creation."""

    def test_empty_bind_file(self):
        """Should create empty bind file."""
        bf = BindFile()
        assert len(bf.contents) == 0
        assert len(bf.binds) == 0

    def test_with_single_bind(self):
        """Should create bind file with single bind."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        bf = BindFile([bind])
        assert len(bf.contents) == 1
        assert len(bf.binds) == 1

    def test_with_multiple_binds(self):
        """Should create bind file with multiple binds."""
        bind1 = Bind("Q", ["powexectoggleon dark nova"])
        bind2 = Bind("E", ["powexectoggleon black dwarf"])
        bf = BindFile([bind1, bind2])
        assert len(bf.contents) == 2
        assert len(bf.binds) == 2

    def test_with_single_comment(self):
        """Should create bind file with single comment."""
        comment = _Comment("This is a comment")
        bf = BindFile([comment])
        assert len(bf.contents) == 1
        assert len(bf.binds) == 0

    def test_with_multiple_comments(self):
        """Should create bind file with multiple comments."""
        comment1 = _Comment("First comment")
        comment2 = _Comment("Second comment")
        bf = BindFile([comment1, comment2])
        assert len(bf.contents) == 2
        assert len(bf.binds) == 0

    def test_with_comment_banner(self):
        """Should create bind file with comment banner."""
        comment = _CommentBanner("This is a banner")
        bf = BindFile([comment])
        assert len(bf.contents) == 1
        assert len(bf.binds) == 0

    def test_with_comments_and_binds(self):
        """Should create bind file with mixed content."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        comment = _Comment("This is a comment")
        bf = BindFile([comment, bind])
        assert len(bf.contents) == 2
        assert len(bf.binds) == 1


class TestBindFileModification:
    """Test BindFile modification methods."""

    def test_add_bind(self):
        """Should add bind to empty file."""
        bf = BindFile()
        bind = Bind("Q", ["powexectoggleon dark nova"])
        # act
        bf.add_bind(bind)
        # assert
        assert len(bf.contents) == 1
        assert len(bf.binds) == 1
        assert bf.binds[0] == bind

    def test_add_comment(self):
        """Should add comment to file."""
        bf = BindFile()
        comment = _Comment("Test comment")
        # act
        bf.add_comment(comment)
        # assert
        assert len(bf.contents) == 1
        assert len(bf.binds) == 0

    def test_add_mixed_content(self):
        """Should add both binds and comments."""
        bf = BindFile()
        comment = _Comment("Test comment")
        bind = Bind("Q", ["powexectoggleon dark nova"])
        # act
        bf.add_comment(comment)
        bf.add_bind(bind)
        # assert
        assert len(bf.contents) == 2
        assert len(bf.binds) == 1
        assert bf.binds[0] == bind

    def test_chain_content(self):
        """Should chain adding binds and comments."""
        bf = BindFile()
        comment_banner = _CommentBanner("Bind File Banner")
        comment1 = _Comment("Squid Form")
        bind1 = Bind("Q", ["powexectoggleon dark nova"])
        comment2 = _Comment("Lobster Form")
        bind2 = Bind("E", ["powexectoggleon black dwarf"])
        # act
        (
            bf.add_comment(comment_banner)
            .add_comment(comment1)
            .add_bind(bind1)
            .add_comment(comment2)
            .add_bind(bind2)
        )
        # assert
        assert len(bf.contents) == 5
        assert len(bf.binds) == 2
        assert bf.binds[0] == bind1
        assert bf.binds[1] == bind2

    def test_clear(self):
        """Should clear all contents."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        bf = BindFile([bind])
        # act
        bf.clear()
        # assert
        assert len(bf.contents) == 0
        assert len(bf.binds) == 0

    def test_set_contents(self):
        """Should replace all contents."""
        bf = BindFile()
        comment_banner = _CommentBanner("Bind File Banner")
        comment1 = _Comment("Squid Form")
        bind1 = Bind("Q", ["powexectoggleon dark nova"])
        comment2 = _Comment("Lobster Form")
        bind2 = Bind("E", ["powexectoggleon black dwarf"])

        bf.contents = [comment_banner, comment1, bind1, comment2, bind2]
        assert len(bf.contents) == 5
        assert len(bf.binds) == 2


class TestBindFilePreviewRepresentation:
    """Test different BindFile representations"""

    def test_empty_preview(self):
        """Should return empty string for empty file."""
        bf = BindFile()
        assert bf.preview() == ""

    def test_single_bind_preview(self):
        """Should return correct string for single bind."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        bf = BindFile([bind])
        expected = 'Q "powexectoggleon dark nova"'
        assert bf.preview() == expected

    def test_multiple_binds_preview(self):
        """Should return correct string for multiple binds."""
        bind1 = Bind("Q", ["powexectoggleon dark nova"])
        bind2 = Bind("E", ["powexectoggleon black dwarf"])
        bf = BindFile([bind1, bind2])
        expected = 'Q "powexectoggleon dark nova"\nE "powexectoggleon black dwarf"'
        assert bf.preview() == expected

    def test_single_comment_preview(self):
        """Should return correct string for single comment."""
        comment = _Comment("This is a comment")
        bf = BindFile([comment])
        expected = "# This is a comment #"
        assert bf.preview() == expected

    def test_banner_only_preview(self):
        """Should return correct string for banner comment."""
        comment = _CommentBanner("This is a\nmulti-line banner")
        bf = BindFile([comment])
        expected = (
            "# ----------------- #\n"
            "# This is a         #\n"
            "# multi-line banner #\n"
            "# ----------------- #"
        )
        assert bf.preview() == expected

    def test_mixed_content_preview(self):
        """Should return correct string for mixed content."""
        comment_banner = _CommentBanner("binds!\nBinds!!\nBINDS!!!")
        comment1 = _Comment("Squid Form")
        bind1 = Bind("Q", ["powexectoggleon dark nova"])
        comment2 = _Comment("Lobster Form")
        bind2 = Bind("E", ["powexectoggleon black dwarf"])
        bf = BindFile([comment_banner, comment1, bind1, comment2, bind2])
        expected = (
            "# -------- #\n"
            "# binds!   #\n"
            "# Binds!!  #\n"
            "# BINDS!!! #\n"
            "# -------- #\n"
            "# Squid Form #\n"
            'Q "powexectoggleon dark nova"\n'
            "# Lobster Form #\n"
            'E "powexectoggleon black dwarf"'
        )
        assert bf.preview() == expected


class TestBindFileWriteRepresentation:

    def test_empty_write(self, in_tmp_dir):
        """Should write empty file."""
        bf = BindFile()
        # act
        bf.write_to_file("empty_binds.txt")
        # assert
        file = Path("empty_binds.txt")
        assert file.exists()
        content = file.read_text()
        assert content == ""

    def test_single_bind_write(self, in_tmp_dir):
        """Should write single bind to file."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        bf = BindFile([bind])
        # act
        bf.write_to_file("single_bind.txt")
        # assert
        file = Path("single_bind.txt")
        assert file.exists()
        content = file.read_text()
        expected = 'Q "powexectoggleon dark nova"'
        assert content == expected

    def test_multiple_binds_write(self, in_tmp_dir):
        """Should write multiple binds to file."""
        bind1 = Bind("Q", ["powexectoggleon dark nova"])
        bind2 = Bind("E", ["powexectoggleon black dwarf"])
        bf = BindFile([bind1, bind2])
        # act
        bf.write_to_file("multiple_binds.txt")
        # assert
        file = Path("multiple_binds.txt")
        assert file.exists()
        content = file.read_text()
        expected = 'Q "powexectoggleon dark nova"\nE "powexectoggleon black dwarf"'
        assert content == expected

    def test_banner_only_write(self, in_tmp_dir):
        """Should write only banner comment to file."""
        comment = _CommentBanner("These files were\ngenerated by\nCity of Binds!")
        bf = BindFile([comment])
        # act
        bf.write_to_file("banner_only.txt")
        # assert
        file = Path("banner_only.txt")
        assert file.exists()
        content = file.read_text()
        expected = (
            "# ---------------- #\n"
            "# These files were #\n"
            "# generated by     #\n"
            "# City of Binds!   #\n"
            "# ---------------- #"
        )
        assert content == expected

    def test_mixed_content_write(self, in_tmp_dir):
        """Should write mixed content to file."""
        comment_banner = _CommentBanner("binds!\nBinds!!\nBINDS!!!")
        comment1 = _Comment("Squid Form")
        bind1 = Bind("Q", ["powexectoggleon dark nova"])
        comment2 = _Comment("Lobster Form")
        bind2 = Bind("E", ["powexectoggleon black dwarf"])
        bf = BindFile([comment_banner, comment1, bind1, comment2, bind2])
        # act
        bf.write_to_file("mixed_content.txt")
        # assert
        file = Path("mixed_content.txt")
        assert file.exists()
        content = file.read_text()
        expected = (
            "# -------- #\n"
            "# binds!   #\n"
            "# Binds!!  #\n"
            "# BINDS!!! #\n"
            "# -------- #\n"
            "# Squid Form #\n"
            'Q "powexectoggleon dark nova"\n'
            "# Lobster Form #\n"
            'E "powexectoggleon black dwarf"'
        )
        assert content == expected

    def test_different_directory_write(self, in_tmp_dir):
        """Should write file to specified directory."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        bf = BindFile([bind])
        target_dir = Path("binds_folder")
        target_dir.mkdir()
        # act
        bf.write_to_file(target_dir / "binds.txt")
        # assert
        file = target_dir / "binds.txt"
        assert file.exists()
        content = file.read_text()
        expected = 'Q "powexectoggleon dark nova"'
        assert content == expected

    def test_write_to_directory_method(self, in_tmp_dir):
        """Should write file using write_to_directory method."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        bf = BindFile([bind])
        target_dir = Path("binds_folder")
        target_dir.mkdir()
        # act
        bf.write_to_directory("binds.txt", target_dir)
        # assert
        file = target_dir / "binds.txt"
        assert file.exists()
        content = file.read_text()
        expected = 'Q "powexectoggleon dark nova"'
        assert content == expected


# TODO: write error tests (2025/12/23)
class TestBindFileValidation:
    """Test BindFile validation methods."""

    def test_is_empty_true(self):
        """Should return True for empty bind file."""
        bf = BindFile()
        assert bf.is_empty()

    def test_is_empty_false(self):
        """Should return False for non-empty bind file."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        bf = BindFile([bind])
        assert not bf.is_empty()

    def test_invalid_content_type_in_constructor(self):
        """Should reject invalid content types."""
        with pytest.raises(TypeError, match="All items in contents must be instances"):
            BindFile(["not a bind"])

    def test_invalid_content_list_type(self):
        """Should reject non-list content."""
        with pytest.raises(TypeError, match="Contents must be a list"):
            BindFile("not a list")

    def test_add_invalid_bind_type(self):
        """Should reject invalid bind type."""
        bf = BindFile()
        with pytest.raises(TypeError, match="Expected content of type Bind"):
            bf.add_bind("not a bind")

    def test_add_invalid_comment_type(self):
        """Should reject invalid comment type."""
        bf = BindFile()
        with pytest.raises(TypeError, match="Expected content of type _Comment"):
            bf.add_comment("not a comment")

    def test_validate_binds_success(self):
        """Should validate all binds successfully."""
        bind1 = Bind("F1", ["powexectoggleon super speed"])
        bind2 = Bind("F2", ["say hello"])
        bf = BindFile([bind1, bind2])
        # Should not raise
        bf.validate_binds()

    def test_validate_binds_with_invalid_bind(self):
        """Should raise when bind validation fails."""
        # Create bind that will fail validation (empty bind)
        bind = Bind("F1", [])  # Empty commands
        bf = BindFile([bind])
        with pytest.raises(ValueError):  # Bind validation should fail
            bf.validate_binds()
