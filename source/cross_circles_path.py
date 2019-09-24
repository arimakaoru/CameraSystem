import heapq


class Node():
    '''
    各ノード（交点サークル、中点、ブロックサークル）を表す。
    ブロックサークルは使用しないが、座標を揃えるために存在する。
    C:交点サークル
    M:中点
    数字:ブロックサークル
    全てのC、M、数字に座標を割り当てる。

    (0,0) C--M--C--M--C--M--C  (0,6)
          M  1  M  2  M  3  M
          C--M--C--M--C--M--C
          M  4  M  5  M  6  M
          C--M--C--M--C--M--C
          M  7  M  8  M  9  M
    (6,0) C--M--C--M--C--M--C  (6,6)

    属性:
        coorinate: (tuple) 座標
        is_block: (boolian) ブロックが置かれているかどうか(ブロックサークルは全てFalse)
        connected_node: (list) 隣接しているノードのリスト
    '''
    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.is_block = False
        self.connected_node = []


class CrossCircleCoordinate():
    '''
    交点サークル、中点、ブロックサークルの全体を表す。

    属性:
        node_list: (list) Nodeクラスのリスト
    '''
    def __init__(self, block_coordinate):
        self.node_list = []
        for y in range(7):
            for x in range(7):
                self.node_list.append(Node((y, x)))
        
        self.setup_connected_node()
        self.setup_is_block(block_coordinate)
    

    def get_node(self, coordinate):
        for n in self.node_list:
            if n.coordinate == coordinate:
                return n
        return None


    def setup_is_block(self, block_coordinate):
        for n in self.node_list:
            if n.coordinate in block_coordinate:
                n.is_block = True

    
    def setup_connected_node(self):
        CONNECTED_NODE_LIST = [
            [
                [(0, 1), (1, 0)],
                [(0, 0), (0, 2), (1, 0), (1, 2)],
                [(0, 1), (0, 3), (1, 2)],
                [(0, 2), (0, 4), (1, 2), (1, 4)],
                [(0, 3), (0, 5), (1, 4)],
                [(0, 4), (0, 6), (1, 4), (1, 6)],
                [(0, 5), (1, 6)]
            ],
            [
                [(0, 0), (0, 1), (2, 0), (2, 1)],
                [],
                [(0, 1), (0, 2), (0, 3), (2, 1), (2, 2), (2, 3)],
                [],
                [(0, 3), (0, 4), (0, 5), (2, 3), (2, 4), (2, 5)],
                [],
                [(0, 5), (0, 6), (2, 5), (2, 6)]
            ],
            [
                [(1, 0), (2, 1), (3, 0)],
                [(1, 0), (1, 2), (2, 0), (2, 2), (3, 0), (3, 2)],
                [(1, 2), (2, 1), (2, 3), (3, 2)],
                [(1, 2), (1, 4), (2, 2), (2, 4), (3, 2), (3, 4)],
                [(1, 4), (2, 3), (2, 5), (3, 4)],
                [(1, 4), (1, 6), (2, 4), (2, 6), (3, 4), (3, 6)],
                [(1, 6), (2, 5), (3, 6)]
            ],
            [
                [(2, 0), (2, 1), (4, 0), (4, 1)],
                [],
                [(2, 1), (2, 2), (2, 3), (4, 1), (4, 2), (4, 3)],
                [],
                [(2, 3), (2, 4), (2, 5), (4, 3), (4, 4), (4, 5)],
                [],
                [(2, 5), (2, 6), (4, 5), (4, 6)]
            ],
            [
                [(3, 0), (4, 1), (5, 0)],
                [(3, 0), (3, 2), (4, 0), (4, 2), (5, 0), (5, 2)],
                [(3, 2), (4, 1), (4, 3), (5, 2)],
                [(3, 2), (3, 4), (4, 2), (4, 4), (5, 2), (5, 4)],
                [(3, 4), (4, 3), (4, 5), (5, 4)],
                [(3, 4), (3, 6), (4, 4), (4, 6), (5, 4), (5, 6)],
                [(3, 6), (4, 5), (5, 6)]
            ],
            [
                [(4, 0), (4, 1), (6, 0), (6, 1)],
                [],
                [(4, 1), (4, 2), (4, 3), (6, 1), (6, 2), (6, 3)],
                [],
                [(4, 3), (4, 4), (4, 5), (6, 3), (6, 4), (6, 5)],
                [],
                [(4, 5), (4, 6), (6, 5), (6, 6)]
            ],
            [
                [(5, 0), (6, 1)],
                [(5, 0), (5, 2), (6, 0), (6, 2)],
                [(5, 2), (6, 1), (6, 3)],
                [(5, 2), (5, 4), (6, 2), (6, 4)],
                [(5, 4), (6, 3), (6, 5)],
                [(5, 4), (5, 6), (6, 4), (6, 6)],
                [(5, 6), (6, 5)]
            ],
        ]

        for n in self.node_list:
            connected_coordinate = CONNECTED_NODE_LIST[n.coordinate[0]][n.coordinate[1]]
            connected_node = []
            for cc in connected_coordinate:
                connected_node.append(self.get_node(cc))

            n.connected_node = connected_node


class CrossCircleSolver():
    '''
    ある交点サークル(または中点)から別の交点サークル(または中点)への移動経路を計算する。
    属性:
        crossCircleCoordinate: (CrossCirclecoordinate) ブロックビンゴエリアの状態を表す
        direction: (int) 開始ノードでの走行体の向きを表す。0:上, 1:右, 2:下, 3:左
    '''
    def __init__(self, direction, block_coordinate):
        self.crossCircleCoordinate = CrossCircleCoordinate(block_coordinate)
        self.direction = direction


    def aster(self, start, goal):
        '''A*アルゴリズムを用いて、startからgoalまでの経路を求める
        Args:
            start: (tuple) スタートの座標
            goal: (tuple) ゴールの座標
        Returns:
            (list) 座標のリスト
            リストの最初はstart、最後はgoalである
            例:[(0,0), (0,1), (0,3)]
        '''
        passed_list = [start]
        start_cost = self.cost_g(passed_list) + self.cost_h(start, goal)
        checked = {start: start_cost}
        searching_heap = []
        heapq.heappush(searching_heap, (start_cost, passed_list))

        while len(searching_heap) > 0:
            cost, passed_list = heapq.heappop(searching_heap)
            # 最後に探索したノードを取得
            last_passed_node = self.crossCircleCoordinate.get_node(passed_list[-1])
            # 最後に探索したノードが目的地なら探索ヒープを返す
            if last_passed_node.coordinate == goal:
                return passed_list

            # 最後に探索したノードに隣接するノードを探索
            for node in last_passed_node.connected_node:
                if not node.is_block or node.coordinate == goal:
                    # ブロックが置いていないノードのみ探索する。ただし、ゴールはブロックが置いていても探索する
                    # 経路リストに探索中の座標を追加した一時リストを作成
                    tmp_passed_list = passed_list + [node.coordinate]
                    # 一時リストのスコアを計算
                    tmp_cost = self.cost_g(tmp_passed_list) + self.cost_h(node.coordinate, goal)
                    # 探索中の座標が、他の経路で探索済みかどうかチェック
                    # 探索済みの場合、前回のスコアと今回のスコアを比較
                    # 今回のスコアのほうが大きい場合、次のノードの探索へ
                    if node.coordinate in checked and checked[node.coordinate] <= tmp_cost:
                        continue
                    # 今回のスコアのほうが小さい場合、チェック済みリストに格納
                    # 探索ヒープにスコアと経路リストを格納
                    checked[node.coordinate] = tmp_cost
                    heapq.heappush(searching_heap, (tmp_cost, tmp_passed_list))
        return []


    def cost_h(self, current, goal):
        return abs(goal[0] - current[0]) + abs(goal[1] - current[1])


    def cost_g(self, route):
        COST_1 = 1
        COST_2 = 2
        COST_3 = 3
        COST_4 = 4
        move_cost = 0
        current_direction = self.direction
        for i, coordinate in enumerate(route):
            if i == 0:
                pre_coordinate = coordinate
            else:
                x_diff = coordinate[1] - pre_coordinate[1]
                y_diff = coordinate[0] - pre_coordinate[0]
                if current_direction == 0:
                    if x_diff == 0:
                        if y_diff > 0:
                            # 上、正面
                            move_cost += COST_1
                        elif y_diff < 0:
                            # 下、後ろ
                            move_cost += COST_3
                            current_direction = 2
                    elif y_diff == 0:
                        if x_diff > 0:
                            # 右、90
                            move_cost += COST_2
                            current_direction = 1
                        elif x_diff < 0:
                            # 左、90
                            move_cost += COST_2
                            current_direction = 3
                    else:
                        # 斜めとか
                        move_cost += COST_4
                elif current_direction == 1:
                    if x_diff == 0:
                        if y_diff > 0:
                            # 上
                            move_cost += COST_2
                            current_direction = 0
                        elif y_diff < 0:
                            # 下
                            move_cost += COST_2
                            current_direction = 2
                    elif y_diff == 0:
                        if x_diff > 0:
                            # 右
                            move_cost += COST_1
                        elif x_diff < 0:
                            # 左
                            move_cost += COST_3
                            current_direction = 3
                    else:
                        # 斜めとか
                        move_cost += COST_4
                elif current_direction == 2:
                    if x_diff == 0:
                        if y_diff > 0:
                            # 上
                            move_cost += COST_3
                            current_direction = 0
                        elif y_diff < 0:
                            # 下
                            move_cost += COST_1
                    elif y_diff == 0:
                        if x_diff > 0:
                            # 右
                            move_cost += COST_2
                            current_direction = 1
                        elif x_diff < 0:
                            # 左
                            move_cost += COST_2
                            current_direction = 3
                    else:
                        # 斜めとか
                        move_cost += COST_4
                elif current_direction == 3:
                    if x_diff == 0:
                        if y_diff > 0:
                            # 上
                            move_cost += COST_2
                            current_direction = 0
                        elif y_diff < 0:
                            # 下
                            move_cost += COST_2
                            current_direction = 2
                    elif y_diff == 0:
                        if x_diff > 0:
                            # 右
                            move_cost += COST_3
                            current_direction = 1
                        elif x_diff < 0:
                            # 左
                            move_cost += COST_1
                            current_direction = 3
                    else:
                        # 斜めとか
                        move_cost += COST_4
        return move_cost


if __name__ == '__main__':
    # route = [Node(False, (0, 0)), Node(False, (0, 1)), Node(False, (0, 2)), Node(False, (1, 2)), Node(False, (2, 2)), Node(False, (3, 2)), Node(False, (2, 3)), Node(False, (2, 4))]
    # print(cost_g(route, 1))

    # bingoArea = BingoArea()
    # for e in bingoArea.node_list:
    #     print(e.coordinate)
    #     if len(e.connected_node) > 0:
    #         for c in e.connected_node:
    #             if c != None:
    #                 print(c.coordinate)
    #     print("--------")

    block_coordinate = [(0,0), (0,4), (2,2), (2,6), (4,0), (6,2), (6,6)]
    crossCircleSolver = CrossCircleSolver(1, block_coordinate)
    print(crossCircleSolver.aster((6,2), (0,2)))