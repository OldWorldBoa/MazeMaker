class GraphRendererState:
    def __init__(self, graph_renderer):
        self.graph = graph_renderer.graph
        self.rows = graph_renderer.rows
        self.columns = graph_renderer.columns
        self.question_height = graph_renderer.question_height
        self.question_width = graph_renderer.question_width
        self.answer_length = graph_renderer.answer_length
        self.answer_width = graph_renderer.answer_width
