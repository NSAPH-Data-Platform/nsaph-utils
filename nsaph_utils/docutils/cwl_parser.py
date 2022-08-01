import logging
import os
from typing import Dict, List, Optional

import sphinx
import yaml
from docutils import nodes
from sphinx.parsers import Parser

logger = logging.getLogger(__name__)


class CWLParser(Parser):
    supported = ['cwl']

    config_section = "cwl parser"
    config_section_dependencies = ("parsers",)

    def parse(self, inputstring: str, document: nodes.document):
        # self.add_title(inputstring, document)

        content = yaml.safe_load(inputstring)
        self.add_header(content, document)
        self.add_docs(content, document)
        self.add_inputs(content, document)
        self.add_outputs(content, document)
        self.add_steps(content, document)

    def add_title(self, inputstring: str, document: nodes.document):
        title = self.find_title(inputstring) or self.get_filename(document)
        title_node = nodes.title(text=title)
        document.append(title_node)

    def find_title(self, inputstring: str) -> Optional[str]:
        for line in inputstring.splitlines():
            if line.startswith("###"):
                return line.replace("###", "").strip()

    def get_filename(self, document: nodes.document):
        path = document.current_source
        filename = path.split(os.path.sep)[-1]
        return filename

    def add_header(self, content: Dict, document: nodes.document):
        if not content:
            return
        if "tool" in content["class"].lower():
            header = "Tool " + str(content["baseCommand"])  # TODO
        elif "workflow" in content["class"].lower():
            header = "Workflow"
        else:
            header = "Unknown class"

        rubric = nodes.rubric(text=header)
        document.append(rubric)

    def add_docs(self, content: Dict, document: nodes.document):
        if not content or "doc" not in content:
            return

        rubric = nodes.rubric(text="Description")
        rubric.append(nodes.paragraph(text=content["doc"]))
        document.append(rubric)

    def add_inputs(self, content: Dict, document: nodes.document):
        if not content or "inputs" not in content:
            return

        data = []
        for name in content["inputs"]:
            arg = content["inputs"][name]
            if not arg:
                continue

            if isinstance(arg, str):
                doc = name
                tp = arg.replace('?', '')
                df = None
            else:
                doc = arg.get("doc", " ").replace('\n', ' ')
                tp = arg.get("type", "string")
                df = arg.get("default", None)

            if df is not None:
                df = "`{}`".format(df)
            else:
                df = " "

            data.append([name, tp, df, doc])

        self._add_table_block(
            header="Inputs",
            columns=["Name", "Type", "Default", "Description"],
            data=data,
            document=document,
        )

    def add_outputs(self, content: Dict, document: nodes.document):
        if not content or "outputs" not in content:
            return

        data = []
        for name in content["outputs"]:
            arg = content["outputs"][name]
            doc = arg.get("doc", " ").replace('\n', ' ')
            tp = arg.get("type", "string")
            if isinstance(tp, str):
                tp = tp.replace('?', '')
            elif isinstance(tp, dict):
                tp = tp["type"]
            data.append([name, tp, doc])

        self._add_table_block(
            header="Outputs",
            columns=["Name", "Type", "Description"],
            data=data,
            document=document,
        )

    def add_steps(self, content: Dict, document: nodes.document):
        if not content or "steps" not in content:
            return

        steps = content["steps"]
        data = []
        for item in steps:
            if isinstance(item, dict):
                name = item['id']
                arg = item
            else:
                name = item
                arg = steps[name]

            doc = arg.get("doc", " ").replace('\n', ' ')
            runs = arg["run"]
            if isinstance(runs, str):
                refuri = runs.replace(".cwl", ".html")
                target = nodes.reference(internal=False, refuri=refuri, text=refuri)
            else:
                target = runs.get("baseCommand", "command")

            data.append([name, runs, target, doc])

        self._add_table_block(
            header="Steps",
            columns=["Name", "Runs", "Target", "Description"],
            data=data,
            document=document,
        )

    def _add_table_block(self, header: str, columns: List, data: List[List], document: nodes.document):
        rubric = nodes.rubric(text=header)
        table = self._create_table(
            columns=columns,
            data=data,
        )
        rubric.append(table)
        document.append(rubric)

    def _create_table(self, columns: List, data: List[List]) -> nodes.table:
        table = nodes.table()

        tgroup = nodes.tgroup(cols=len(columns))
        table.append(tgroup)
        for _ in columns:
            tgroup.append(nodes.colspec(colwidth=1))

        thead = nodes.thead()
        tgroup.append(thead)
        thead.append(self._create_table_row(columns))

        tbody = nodes.tbody()
        tgroup.append(tbody)
        for data_row in data:
            tbody.append(self._create_table_row(data_row))

        return table

    def _create_table_row(self, row_cells):
        row = nodes.row()
        for cell in row_cells:
            entry = nodes.entry()
            para = nodes.paragraph()
            if isinstance(cell, nodes.reference):
                para += cell
            else:
                text = nodes.Text(cell)
                para += text
            entry += para
            row += entry
        return row


def setup(app):
    app.add_source_parser(CWLParser)

    return {'version': sphinx.__version__, 'parallel_read_safe': True}
