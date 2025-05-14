from ...src.Model.BiDirectionalGraph import BiDirectionalGraph

def test_GraphConstruction():
  graph = BiDirectionalGraph()

  graph.addVertex("A")
  graph.addVertex("B")
  graph.addVertex("C")
  graph.addVertex("D")
  graph.addVertex("E")
  graph.addVertex("F")
  graph.addVertex("G")
  graph.addVertex("H")
  graph.addVertex("I")

  graph.addEdge("A", "B")
  graph.addEdge("A", "D")
  graph.addEdge("B", "C")
  graph.addEdge("B", "E")
  graph.addEdge("C", "F")
  graph.addEdge("D", "E")
  graph.addEdge("D", "G")
  graph.addEdge("E", "F")
  graph.addEdge("E", "H")
  graph.addEdge("F", "I")
  graph.addEdge("G", "H")
  graph.addEdge("I", "H")

  assert graph.neighbours("A") == ["B", "D"]
  assert graph.neighbours("B") == ["A", "C", "E"]