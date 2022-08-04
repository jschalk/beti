import dataclasses
from importlib.resources import path


class Path(str):
    pass


@dataclasses.dataclass
class HandUnit:
    base: Path
    hand: Path
    open: float = None
    nigh: float = None


@dataclasses.dataclass
class LimmetUnit:
    path: str
    open: float = None
    nigh: float = None
    _status: bool = None

    def clear_status(self):
        self._status = None

    def is_in_lineage(self, hand: Path):
        is_lineage = False
        if self.path.find(hand) == 0 or hand.find(self.path) == 0:
            is_lineage = True
        return is_lineage

    def set_status(self, hand_unit: HandUnit):
        # set true if limmet is in lineage of hand
        status_x = False
        if self.is_in_lineage(hand=hand_unit.hand):
            if hand_unit.open == None and hand_unit.nigh == None:
                status_x = True
            elif hand_unit.open != None and hand_unit.nigh != None:
                if self.open <= hand_unit.nigh and self.nigh >= hand_unit.open:
                    status_x = True

        self._status = status_x


@dataclasses.dataclass
class LimmitUnit:
    base: Path
    limmets: dict[Path:LimmetUnit]
    _status: bool = None

    def clear_status(self):
        self._status = None
        for limmet in self.limmets.values():
            limmet.clear_status()

    def set_limmet_status(self, hand_unit: HandUnit):
        for limmet in self.limmets.values():
            limmet.set_status(hand_unit=hand_unit)

    def set_status(self, hand_unit: HandUnit):
        self.clear_status()
        self.set_limmet_status(hand_unit=hand_unit)
        self._status = False
        for limmet in self.limmets.values():
            if limmet._status == True:
                self._status = True


@dataclasses.dataclass
class TreeMetrics:
    nodeCount: int = None
    levelCount: dict = None

    def evaluate_node(self, level: int):
        if self.nodeCount == None:
            self.nodeCount = 0
        self.nodeCount += 1

        if self.levelCount == None:
            self.levelCount = {}
        if self.levelCount.get(level) == None:
            self.levelCount[level] = 1
        else:
            self.levelCount[level] = self.levelCount[level] + 1


@dataclasses.dataclass
class YokeCore:
    _dir: str = None
    _children: dict = None
    _weight: int = 1
    _desc: str = None
    _uid: int = None
    _level: int = None
    _limmits: dict[Path:LimmitUnit] = None
    _limmot_status: bool = None
    _root_relative_weight: float = None
    _children_total_weight: int = 0

    def add_child(self, yoke_child):
        if self._children == None:
            self._children = {}
        self._children[yoke_child._desc] = yoke_child

    def set_limmit_unit(self, limmit: LimmitUnit):
        self.set_limmit_empty_if_null()
        self._limmits[limmit.base] = limmit

    def set_limmit_empty_if_null(self):
        if self._limmits == None:
            self._limmits = {}

    def is_heir(self, src: Path, heir: Path):
        heir_status = None
        if heir.find(src) == 0:
            heir_status = True
        else:
            heir_status = False

        return heir_status

    def clear_limmits_status(self):
        self.set_limmit_empty_if_null()
        for limmit in self._limmits.values():
            limmit.clear_status()

    def set_limmits_status(self, hands: dict[HandUnit]):
        self.set_limmit_empty_if_null()

        for limmit in self._limmits.values():
            limmit._status = False
            for hand in hands.values():
                if hand.base == limmit.base:
                    limmit.set_status(hand_unit=hand)

    def set_limmot_status(self, hands: dict[HandUnit]):
        self.clear_limmits_status()
        self.set_limmits_status(hands=hands)
        self._limmot_status = True
        for limmit in self._limmits.values():
            if limmit._status == False:
                self._limmot_status = False


@dataclasses.dataclass
class YokeChild(YokeCore):
    _sibling_total_weight: int = None
    action: bool = False
    _open: float = None
    _nigh: float = None
    _ancestor_action_count: int = None

    def _get1action(self):
        x_int = 0
        if self.action == True:
            x_int = 1
        return x_int


class YokeRoot(YokeCore):
    _hands: dict[str:str] = {}  # dimm_path_base : dimm_path_hands

    def set_hands(self, base: Path, hand: Path, open: float = None, nigh: float = None):
        hands_unit = None
        if open == None and nigh == None:
            hands_unit = HandUnit(base=base, hand=hand)
        elif open != None and nigh != None:
            hands_unit = HandUnit(base=base, hand=hand, open=open, nigh=nigh)

        if self._hands == None:
            self._hands = {}
        self._hands[hands_unit.base] = hands_unit

    def get_tree_metrics(self):
        tree_metrics = TreeMetrics()
        self._level = 0
        tree_metrics.evaluate_node(level=self._level)

        yoke_list = []
        for key, yoke_child in self._children.items():
            yoke_child._level = self._level + 1
            tree_metrics.evaluate_node(level=yoke_child._level)
            yoke_list.append(yoke_child)

        while yoke_list != []:
            yoke_x = yoke_list.pop()
            if yoke_x._children != None:
                for key, yoke_child in yoke_x._children.items():
                    yoke_child._level = yoke_x._level + 1
                    tree_metrics.evaluate_node(level=yoke_child._level)
                    yoke_list.append(yoke_child)

        return tree_metrics

    def get_node_count(self):
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.nodeCount

    def get_level_count(self, level):
        tree_metrics = self.get_tree_metrics()
        levelCount = None
        try:
            levelCount = tree_metrics.levelCount[level]
        except KeyError:
            levelCount = 0
        return levelCount

    def add_yoke(self, yoke_child: YokeCore, path: str):
        self._level = 0
        dir = path.split(",")
        if len(dir) == self._level + 1:
            self.add_child(yoke_child=yoke_child)
        elif len(dir) == self._level + 2:
            self._children[dir[1]].add_child(yoke_child=yoke_child)
        elif len(dir) == self._level + 3:
            self._children[dir[1]]._children[dir[2]].add_child(yoke_child=yoke_child)
        elif len(dir) == self._level + 4:
            self._children[dir[1]]._children[dir[2]]._children[dir[3]].add_child(
                yoke_child=yoke_child
            )
        elif len(dir) == self._level + 5:
            self._children[dir[1]]._children[dir[2]]._children[dir[3]]._children[
                dir[4]
            ].add_child(yoke_child=yoke_child)
        elif len(dir) == self._level + 6:
            self._children[dir[1]]._children[dir[2]]._children[dir[3]]._children[
                dir[4]
            ]._children[dir[5]].add_child(yoke_child=yoke_child)
        elif len(dir) == self._level + 7:
            self._children[dir[1]]._children[dir[2]]._children[dir[3]]._children[
                dir[4]
            ]._children[dir[5]]._children[dir[6]].add_child(yoke_child=yoke_child)
        else:
            raise Exception("Unable to add 9th level children")

    def root_set_limmit_unit(self, path: str, limmit: LimmitUnit):
        self._level = 0
        dir = path.split(",")
        if len(dir) == self._level + 1:
            self.set_limmit_unit(limmit=limmit)
        elif len(dir) == self._level + 2:
            self._children[dir[1]].set_limmit_unit(limmit=limmit)
        elif len(dir) == self._level + 3:
            self._children[dir[1]]._children[dir[2]].set_limmit_unit(limmit=limmit)
        elif len(dir) == self._level + 4:
            self._children[dir[1]]._children[dir[2]]._children[dir[3]].set_limmit_unit(
                limmit=limmit
            )
        elif len(dir) == self._level + 5:
            self._children[dir[1]]._children[dir[2]]._children[dir[3]]._children[
                dir[4]
            ].set_limmit_unit(limmit=limmit)
        elif len(dir) == self._level + 6:
            self._children[dir[1]]._children[dir[2]]._children[dir[3]]._children[
                dir[4]
            ]._children[dir[5]].set_limmit_unit(limmit=limmit)
        elif len(dir) == self._level + 7:
            self._children[dir[1]]._children[dir[2]]._children[dir[3]]._children[
                dir[4]
            ]._children[dir[5]]._children[dir[6]].set_limmit_unit(limmit=limmit)
        else:
            raise Exception("Unable to edit th level children")

    def get_action_items(self):
        action_items = []
        all_yokes = self.get_yoke_list()
        for yoke in all_yokes:
            if yoke.action == True and yoke._limmot_status == True:
                action_items.append(yoke)
        return action_items

    def _set_root_attributes(self):
        self._level = 0
        self._dir = self._desc
        self.set_limmot_status(hands=self._hands)
        self._weight = 1
        self._children_total_weight = 0
        for yoke in self._children.values():
            self._children_total_weight += yoke._weight
        self._root_relative_weight = 1

    def _set_children_attributes(
        self, yoke_child: YokeChild, parent_yoke: YokeChild = None
    ):
        parent_level = None
        parent_dir = None
        parent_limmot_status = None
        parent_children_total_weight = None
        parent_root_relative_weight = None
        parent_ancestor_action_count = None
        parent_action_1or0 = None

        if parent_yoke == None:
            parent_level = self._level
            parent_dir = self._dir
            parent_limmot_status = self._limmot_status
            parent_children_total_weight = self._children_total_weight
            parent_root_relative_weight = self._root_relative_weight
            parent_ancestor_action_count = 0
            parent_action_1or0 = 0
        else:
            parent_level = parent_yoke._level
            parent_dir = parent_yoke._dir
            parent_limmot_status = parent_yoke._limmot_status
            parent_children_total_weight = parent_yoke._children_total_weight
            parent_root_relative_weight = parent_yoke._root_relative_weight
            parent_ancestor_action_count = parent_yoke._ancestor_action_count
            parent_action_1or0 = parent_yoke._get1action()

        yoke_child._level = parent_level + 1
        yoke_child._dir = f"{parent_dir},{yoke_child._desc}"
        if parent_limmot_status == False:
            yoke_child._limmot_status = False
        else:
            yoke_child.set_limmot_status(hands=self._hands)
        yoke_child._sibling_total_weight = parent_children_total_weight
        yoke_child._children_total_weight = 0
        if yoke_child._children == None:
            yoke_child._children = {}
        for yoke in yoke_child._children.values():
            yoke_child._children_total_weight += yoke._weight
        yoke_child._root_relative_weight = self.get_root_relative_weight(
            parent_root_relative_weight=parent_root_relative_weight,
            weight=yoke_child._weight,
            sibling_total_weight=yoke_child._sibling_total_weight,
        )
        yoke_child._ancestor_action_count = (
            parent_ancestor_action_count + parent_action_1or0
        )

        return yoke_child

    def get_root_relative_weight(
        self, parent_root_relative_weight: float, weight: int, sibling_total_weight: int
    ):
        root_relative_weight = None
        sibling_ratio = weight / sibling_total_weight
        root_relative_weight = parent_root_relative_weight * sibling_ratio
        return root_relative_weight

    def get_yoke_list(self):
        return_yoke_list = []
        self._set_root_attributes()

        cache_yoke_list = []
        for key, yoke_child in self._children.items():
            cache_yoke_list.append(self._set_children_attributes(yoke_child))

        while cache_yoke_list != []:
            parent_yoke = cache_yoke_list.pop()
            return_yoke_list.append(parent_yoke)

            if parent_yoke._children != None:
                for key, yoke_child in parent_yoke._children.items():
                    cache_yoke_list.append(
                        self._set_children_attributes(
                            yoke_child=yoke_child, parent_yoke=parent_yoke
                        )
                    )
        return return_yoke_list
