import sys
import re
import argparse


COMMENT_PATTERN = r"<!--.*?-->"
HEADING_PATTERN = r"^(#+)\s*(.*)$"
HOLIZONTAL_RULE_PATTERN = r"^[-=\*]{3,}$"
RUBY_PATTERN = r"｜(.+)《(.+)》"


class Linter:
    def __init__(self, ignore_comment=False):
        self.ignore_comment = ignore_comment

    # レベル1の見出しが配列の最初（空文字列は除く）にあり、かつ配列に複数個含まれていないことを確認する
    def _validate_h1_position(self, lines):
        if not lines:
            return

        h1_count = 0
        for i, line in enumerate(lines):
            match = re.match(HEADING_PATTERN, line)
            if match:
                if len(match.group(1)) == 1:
                    h1_count += 1
                    if not all(line.strip() == "" for line in lines[:i]):
                        self._raise_compile_error("Level 1 heading must be the first line.", i + 1)
                    elif h1_count > 1:
                        self._raise_compile_error("More than one level 1 heading found.", i + 1)

    # HTMLコメントを検出する
    def _validate_comment(self, lines):
        if not lines:
            return

        for i, line in enumerate(lines):
            if re.match(COMMENT_PATTERN, line):
                self._raise_compile_error("HTML comment found.", i + 1)

    def _raise_compile_error(self, msg, line_num):
        print(f"MPC Compile Error: {msg} (at line {line_num})", file=sys.stderr)
        exit(1)

    def lint(self, lines):
        if not lines:
            return

        # Check for HTML comments
        if not self.ignore_comment:
            self._validate_comment(lines)

        # Check for level 1 headings
        self._validate_h1_position(lines)


def main():
    parser = argparse.ArgumentParser(description="Process a markdown file.")
    parser.add_argument("input", help="Input markdown file")
    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress output messages")
    parser.add_argument("-s", "--strict", action="store_true", help="Compile Check the input file")
    parser.add_argument("-ic", "--ignore-comment", action="store_true", help="Ignore HTML style comments (<!---->) in the input file. Note: This option overrides the strict mode.")

    args = parser.parse_args()
    input_file_path = args.input
    output_file_path = args.output if args.output else input_file_path.replace(".md", "_compiled.txt")

    with open(input_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if args.strict:
            linter = Linter(ignore_comment=args.ignore_comment)
            linter.lint(lines)

        output_lines = []
        for line in lines:
            line = re.sub(COMMENT_PATTERN, "", line) if args.ignore_comment else line

            # Check for headings
            heading_match = re.match(HEADING_PATTERN, line)
            if heading_match:
                level = len(heading_match.group(1))
                if level == 1:
                    continue

                output_lines.append(re.sub(HEADING_PATTERN, r"[chapter:\2]", line))

                continue

            # Check for horizontal rules
            if re.match(HOLIZONTAL_RULE_PATTERN, line):
                output_lines.append("[newpage]\n")

                continue

            line = re.sub(RUBY_PATTERN, r"[[rb:\1 > \2]]", line)

            output_lines.append(line)

    output_string = ""
    # 重複する空行を削除する
    for line in [line for line in output_lines if line.strip() != ""]:
        output_string += f"{line}\n"

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(output_string)
        f.close()

        if not args.quiet:
            print(f"Processed {len(lines)} lines.")
            print(f"Output written to {output_file_path}.")


if __name__ == "__main__":
    main()
