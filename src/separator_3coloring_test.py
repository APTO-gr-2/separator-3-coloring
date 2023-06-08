import time

from graph_tool import load_graph, GraphView
from graph_tool.draw import graph_draw
from numpy import average

from src.generate_planar import generate_planar_graph
from src.separator_3coloring import separator_3coloring
from src.three_coloring import check_coloring, start_three_coloring

if __name__ == "__main__":
    test_cases = [
        (40, 20, 10),
        (40, 24, 10),
        (40, 28, 10),
        (40, 32, 10),
        (40, 36, 10),
        (40, 40, 10),
        (40, 44, 10),
        (40, 48, 10),
        (40, 52, 10),
        (40, 56, 10),
        (40, 60, 10),
        (40, 64, 10),
        (40, 68, 10),
        (40, 70, 10),
        (40, 74, 10),
        (40, 78, 10),
        (40, 82, 10),
        (40, 86, 10),
        (40, 90, 10),
        (40, 94, 10),
        (40, 98, 10),
    ]
    with open('tests/tests_d.csv', 'w') as file:
        file.write(f'v,e,n,t1,t2\n')
        for test_case in test_cases:
            times1 = []
            times2 = []
            for i in range(10):
                result = False
                while not result:
                    G, pos = generate_planar_graph(test_case[0], test_case[1])
                    print(f"Generated {test_case}, {i}")

                    start_time = time.time()
                    coloring = separator_3coloring(G, test_case[2], show_progress=False)
                    end_time = time.time()
                    if coloring is None:
                        continue
                    print(end_time - start_time)
                    time1 = end_time - start_time
                    check_coloring(G, GraphView(G), coloring)

                    start_time = time.time()
                    coloring = start_three_coloring(G)
                    end_time = time.time()
                    if coloring is None:
                        continue
                    print(end_time - start_time)
                    time2 = end_time - start_time
                    check_coloring(G, GraphView(G), coloring)

                    times1.append(time1)
                    times2.append(time2)
                    result = True
            file.write(f'{test_case[0]}, {test_case[1]}, {test_case[2]}, {average(times1)}, {average(times2)}\n')
            file.flush()

            G.vp["pos"] = pos
            G.save(f"graph-b-{test_case[0]}-{test_case[1]}-{test_case[2]}.gt.gz")

