import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)

research_manager = ResearchManager()

async def handle_initial_query(query: str):
    if not query.strip():
        return [], gr.update(visible=False), gr.update(value="Please enter a query.", visible=True)

    try:
        # Show status
        yield [], gr.update(visible=False), gr.update(value="🤔 **Analyzing your query and generating clarifying questions...**", visible=True)

        questions = await research_manager.get_clarifying_questions(query)

        # Format questions
        questions_markdown = "## ✅ Clarifying Questions Found!\n\nPlease answer the following questions to refine your research:\n\n"
        questions_markdown += "\n\n".join(f"**{i}.** {q}" for i, q in enumerate(questions, 1))

        yield questions, gr.update(visible=True), gr.update(value=questions_markdown, visible=True)
        
    except Exception as e:
        yield [], gr.update(visible=False), gr.update(value=f"❌ **Error:** {str(e)}", visible=True)


async def handle_research_with_answers(query: str, questions: list[str], *answers):
    if not query.strip():
        yield "❌ Please enter a query."
        return

    answers_dict = {q: a for q, a in zip(questions, answers) if a and a.strip()}
    
    yield "🚀 **Starting research...**\n\n"
    
    async for chunk in research_manager.run(query, answers_dict):
        yield chunk


with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    gr.Markdown("Enter your research question below. You'll be asked clarifying questions before the research begins.")

    query_textbox = gr.Textbox(label="What topic would you like to research?", lines=3)
    initial_button = gr.Button("Get Clarifying Questions", variant="primary")

    questions_state = gr.State([])
    questions_display = gr.Markdown(visible=False)

    with gr.Column(visible=False) as answers_section:
        gr.Markdown("### Your Answers")
        answer_boxes = [gr.Textbox(label=f"Answer {i+1}", lines=2) for i in range(3)]
        research_button = gr.Button("Start Research", variant="primary")

    report = gr.Markdown(label="Report")

    initial_button.click(
        fn=handle_initial_query,
        inputs=[query_textbox],
        outputs=[questions_state, answers_section, questions_display],
    )

    research_button.click(
        fn=handle_research_with_answers,
        inputs=[query_textbox, questions_state] + answer_boxes,
        outputs=[report],
    )

ui.launch(inbrowser=True)
