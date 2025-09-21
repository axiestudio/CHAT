from textwrap import dedent

from axiestudio.components.data import URLComponent
from axiestudio.components.input_output import ChatOutput, TextInputComponent
from axiestudio.components.openai.openai_chat_model import OpenAIModelComponent
from axiestudio.components.processing import ParserComponent, PromptComponent
from axiestudio.graph import Graph


def blog_writer_graph(template: str | None = None):
    if template is None:
        template = dedent("""Reference 1:

{references}

---

{instructions}

Blog:
""")
    url_component = URLComponent()
    url_component.set(urls=["https://axiestudio.org/", "https://docs.axiestudio.org/"])
    parse_data_component = ParserComponent()
    parse_data_component.set(input_data=url_component.fetch_content)

    text_input = TextInputComponent(_display_name="Instructions")
    text_input.set(
        input_value="Use the references above for style to write a new blog/tutorial about Axie Studio and AI. "
        "Suggest non-covered topics."
    )

    prompt_component = PromptComponent()
    prompt_component.set(
        template=template,
        instructions=text_input.text_response,
        references=parse_data_component.parse_combined_text,
    )

    openai_component = OpenAIModelComponent()
    openai_component.set(input_value=prompt_component.build_prompt)

    chat_output = ChatOutput()
    chat_output.set(input_value=openai_component.text_response)

    return Graph(start=text_input, end=chat_output)
