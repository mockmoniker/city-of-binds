import re

class Comment:
    DEFAULT_ALIGNMENT = 'left'
    TEXT_ALIGNMENT_MAPPINGS = {
        'left': str.ljust,
        'center': str.center,
        'right': str.rjust
    }
    LEFT_EDGE = "# "
    RIGHT_EDGE = " #"
    EDGES_LENGTH = len(LEFT_EDGE) + len(RIGHT_EDGE)
    MINIMUM_COMMENT_WIDTH = EDGES_LENGTH + 1  # At least one character of text

    def __init__(self, comment_text: str, alignment: str = DEFAULT_ALIGNMENT, minimum_comment_width: int = MINIMUM_COMMENT_WIDTH):
        self._text = None  
        self._alignment = None
        self._minimum_width = None

        self.text = comment_text
        self.alignment = alignment
        self.minimum_width = minimum_comment_width

    ### Properties
    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        self._throw_error_on_invalid_comment(comment_text=text)
        sanitized_comment_text = self._sanitize_comment_text(comment_text=text)
        self._text = sanitized_comment_text

    @property
    def alignment(self) -> str:
        return self._alignment

    @alignment.setter
    def alignment(self, alignment: str):
        self._throw_error_on_invalid_alignment(alignment=alignment)
        self._alignment = alignment

    @property
    def minimum_width(self) -> int:
        return self._minimum_width

    @minimum_width.setter
    def minimum_width(self, minimum_width: int):
        self._throw_error_on_invalid_minimum_width(minimum_width=minimum_width)
        self._minimum_width = minimum_width

    @property
    def comment_string(self) -> str:
        if not self.text:
            return ""
        return self._build_comment_string()

    ### Helpers
    def _sanitize_comment_text(self, comment_text: str) -> str:
        return self._sanitize_comment_line(comment_line=comment_text)

    def _sanitize_comment_line(self, comment_line: str) -> str:
        return comment_line.strip()

    def _build_comment_string(self) -> str:
        text_width = self._get_text_width(text_width=len(self.text), minimum_width=self.minimum_width)
        return self._build_comment_line_string(comment_text=self.text, alignment=self.alignment, text_width=text_width)

    def _build_comment_line_string(self, comment_text: str, alignment: str, text_width: int) -> str:
        alignment_function = self.TEXT_ALIGNMENT_MAPPINGS[alignment]
        return f"{self.LEFT_EDGE}{alignment_function(comment_text, text_width)}{self.RIGHT_EDGE}"

    def _get_text_width(self, text_width: int, minimum_width: int) -> int:
        return max(text_width, minimum_width - self.EDGES_LENGTH)

    ### Error Checking/Validation
    def _throw_error_on_invalid_comment(self, comment_text: str):
        self._throw_error_on_invalid_comment_line(comment_text=comment_text)

    def _throw_error_on_invalid_comment_line(self, comment_text: str):
        if '\n' in comment_text:
            raise ValueError("Comment line may not contain line breaks.")
        
    def _throw_error_on_invalid_minimum_width(self, minimum_width: int):
        if minimum_width < self.MINIMUM_COMMENT_WIDTH:
            raise ValueError(f"Minimum width must be at least {self.MINIMUM_COMMENT_WIDTH}.")
        
    def _throw_error_on_invalid_alignment(self, alignment: str):
        if alignment not in self.TEXT_ALIGNMENT_MAPPINGS:
            raise ValueError(f"Invalid text alignment '{alignment}'. Valid options are: {', '.join(self.TEXT_ALIGNMENT_MAPPINGS.keys())}")

    def __str__(self):
        return self.comment_string

class CommentBanner(Comment):
    VALID_BORDER_STYLES = ['-', '=', '*', '~', '#']
    DEFAULT_BORDER_STYLE = VALID_BORDER_STYLES[0]

    def __init__(self, 
                 comment_text: str,
                 alignment: str = Comment.DEFAULT_ALIGNMENT, 
                 minimum_comment_width: int = Comment.MINIMUM_COMMENT_WIDTH,
                 border_style: str = DEFAULT_BORDER_STYLE):
        self._border_style = None

        super().__init__(comment_text=comment_text, alignment=alignment, minimum_comment_width=minimum_comment_width)

        self.border_style = border_style

    ### Properties
    @property
    def border_style(self) -> str:
        return self._border_style

    @border_style.setter
    def border_style(self, border_style: str):
        self._throw_error_on_invalid_border_style(border_style=border_style)
        self._border_style = border_style

    @property
    def line_count(self) -> int:
        return self.comment_string.count('\n') + 1 if self.comment_string else 0

    ### Helpers
    def _sanitize_comment_text(self, comment_text: str) -> str:
        ### remove any blank lines and trims leading/trailing whitespace for each line
        return '\n'.join([self._sanitize_comment_line(line) for line in comment_text.split('\n') if line.strip()])

    def _build_comment_string(self):
        longest_line_width = self._get_longest_line_width(comment_text=self.text)
        text_width = self._get_text_width(text_width=longest_line_width, minimum_width=self.minimum_width)
        return self._build_comment_banner_string(
            comment_text=self.text,
            alignment=self.alignment,
            text_width=text_width,
            border_style=self.border_style
        )

    def _build_comment_banner_string(self, comment_text: str, alignment: str, text_width: int, border_style: str) -> str:
        border = Comment(f"{border_style * text_width}").comment_string

        comment_lines = "\n".join(
            self._build_comment_line_string(line, alignment, text_width) for line in comment_text.split('\n')
        )

        return f"{border}\n{comment_lines}\n{border}"

    def _get_longest_line_width(self, comment_text: str) -> int:
        return max(len(line) for line in comment_text.split('\n')) if comment_text else 0

    ### Error Checking/Validation
    def _throw_error_on_invalid_comment(self, comment_text: str):
        pass  # Allow multi-line comments, so skip parent validation

    def _throw_error_on_invalid_border_style(self, border_style: str):
        if border_style not in self.VALID_BORDER_STYLES:
            raise ValueError(f"Invalid border style '{border_style}'. Valid options are: {', '.join(self.VALID_BORDER_STYLES)}")
