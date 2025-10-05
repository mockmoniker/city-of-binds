import re

class CommentBanner:
    VALID_BORDER_STYLES = ['-', '=', '*', '~']

    def __init__(self, comment_text: str, border_style: str = '-'):
        self._comment_text = None
        self._border_style = None

        self.comment_text = comment_text
        self.border_style = border_style

    ### Properties
    @property
    def comment_text(self) -> str:
        return self._comment_text

    @comment_text.setter
    def comment_text(self, comment_text: str):
        formatted_comment_text = self._sanitize_comment_text(comment_text)
        self._comment_text = formatted_comment_text

    @property
    def border_style(self) -> str:
        return self._border_style

    @border_style.setter
    def border_style(self, border_style: str):
        self._throw_error_on_invalid_border_style(border_style=border_style)
        self._border_style = border_style

    @property
    def comment_banner_string(self) -> str:
        return self._build_comment_banner_string(comment_text=self.comment_text, border_style=self.border_style)

    ### Helpers
    def _sanitize_comment_text(self, comment_text: str) -> str:
        ### remove any blank lines and trims leading/trailing whitespace for each line
        return '\n'.join([line.strip() for line in comment_text.split('\n') if line.strip()])

    def _build_comment_banner_string(self, comment_text: str, border_style: str) -> str:
        if not comment_text:
            return ""
        comment_lines = comment_text.split('\n')
        max_line_length = max(len(line) for line in comment_lines)
        border = f"# {border_style * (max_line_length)} #"
        banner_lines = [border] + [f"# {line.ljust(max_line_length)} #" for line in comment_lines] + [border]
        return '\n'.join(banner_lines) + '\n'

    ### Error Checking/Validation
    def _throw_error_on_invalid_border_style(self, border_style: str):
        if border_style not in self.VALID_BORDER_STYLES:
            raise ValueError(f"Invalid border style '{border_style}'. Valid options are: {', '.join(self.VALID_BORDER_STYLES)}")