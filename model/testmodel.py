from model.model import Model
myModel = Model()
myModel.buildGraph(5)
nNodes, nEdges = myModel.getGraphDetails()
print(f"numero di nodi = {nNodes} --- numero di archi = {nEdges}")
