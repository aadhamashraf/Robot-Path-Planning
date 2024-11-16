from Basic_Attributes import * 

def export_frontier(frontier , algorithm):
    dir = rf"{os.getcwd()}\Forntier Results" 

    if not os.path.exists(dir):
        os.mkdir(dir)
    
    with open(os.path.join(dir, f"frontier_{algorithm}.txt"), "w") as f:
        for node in frontier:
            f.write(f"{node}\n")
            
def showDifferences_ExecutionTime(compareAlgos):
    sorted_compareAlgos = dict(sorted(compareAlgos.items(), key=lambda item: item[1]))
    
    plt.figure(figsize=(10, 10))
    plt.barh(list(sorted_compareAlgos.keys()), list(sorted_compareAlgos.values()))
    plt.title("Searching Algorithms Execution Time")
    plt.xlabel("Execution Time")
    plt.ylabel("Searching Algorithm")
    plt.grid(True)
    plt.show()
    
