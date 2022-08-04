import dataclasses
from yoke import YokeRoot


@dataclasses.dataclass
class AgendaItem:
    rank: int = None
    description = None
    root_relative_weight = None
    yoke_path: str = None
    _branch_percent = None

    def edit(
        self,
        rank=None,
        description=None,
        root_relative_weight=None,
        yoke_path=None,
        action_status=None,
    ):
        if rank != None:
            self.rank = rank
        if description != None:
            self.description = description
        if root_relative_weight != None:
            self.root_relative_weight = root_relative_weight
        if yoke_path != None:
            self.yoke_path = yoke_path
        if action_status != None:
            self.action_status = action_status

        self._branch_percent = "Undefined"
        group_relative_weight = self.root_relative_weight * 100
        if group_relative_weight == 100:
            self._branch_percent = f"{str(group_relative_weight)[:3]}%"
        elif group_relative_weight >= 10:
            self._branch_percent = f"{str(group_relative_weight)[:2]}%"
        elif group_relative_weight >= 1:
            self._branch_percent = f"{str(group_relative_weight)[:4]}%"
        elif group_relative_weight > 0.1:
            self._branch_percent = f"{str(group_relative_weight)[:5]}%"
        else:
            self._branch_percent = f"{str(group_relative_weight)[:6]}%"


@dataclasses.dataclass
class AgendaDocket:
    root_yoke: YokeRoot
    _action_items: list[list] = None

    def __post_init__(self):
        self.set_agenda_list()

    def set_agenda_list(self):
        self._action_items = []

        x_action_items = self.root_yoke.get_action_items()
        for yoke in x_action_items:
            new_agenda_item = AgendaItem()
            new_agenda_item.description = yoke._desc
            new_agenda_item.yoke_path = yoke._dir
            new_agenda_item.root_relative_weight = yoke._root_relative_weight
            self._action_items.append(new_agenda_item)

    def get_agenda_list(self, agenda_todo: bool = True, agenda_state: bool = True):
        agenda_list_x = []
        for action_yoke in self._action_items:
            # if agenda_item.action_status == "action_state" and agenda_state == True:
            #     agenda_list_x.append(agenda_item)
            # if (agenda_item.action_status == "action_todo" and agenda_todo == True) or (
            #     agenda_item.action_status == "action_state" and agenda_state == True
            # ):
            #     agenda_list_x.append(agenda_item)
            agenda_list_x.append(action_yoke)
        return agenda_list_x

    def _validate_yoke_exists(self, yo_id: int):
        yoke_id_exists = False
        for agenda_item in self.agenda_list:
            if agenda_item.yoke_id == yo_id:
                yoke_id_exists = True

        if yoke_id_exists == False:
            raise ValueError(f"{yo_id=} is not in agenda")

    def _get_agenda_item(self, yo_id: int):
        item_x = None
        for agenda_item in self.agenda_list:
            if agenda_item.yoke_id == yo_id:
                item_x = agenda_item
        return item_x

    def _get_bigger_agenda_item(self, agenda_lesser: AgendaItem):
        # find all agenda items with RRW > yo_rrw (Greater Agenda Items: GAI)
        # find GAI with least RRW (Target GAI: TAI) & (TAI_RRW)
        agenda_greater = None
        for agenda_item in self.agenda_list:
            if (
                agenda_item.root_relative_weight > agenda_lesser.root_relative_weight
            ) or (
                agenda_item.root_relative_weight == agenda_lesser.root_relative_weight
                and agenda_item.yoke_id != agenda_lesser.yoke_id
            ):
                agenda_greater = agenda_item
        if agenda_greater == None:
            raise Exception(
                f"Unable to find bigger agenda item {agenda_lesser.yoke_id=}"
            )
        return agenda_greater

    def set_greater_weight(self, yo_id_lesser: int, yo_id_greater: int):
        ai_lesser = None
        ai_greater = None
        for agenda_item in self.agenda_list:
            if agenda_item.yoke_id == yo_id_lesser:
                ai_lesser = agenda_item
            if agenda_item.yoke_id == yo_id_greater:
                ai_greater = agenda_item

        ai_greater_rank = ai_greater.rank
        # leftover while loop debugging print statements...
        # print(f"yo_id: {ai_lesser.yoke_id=} target: {ai_greater.yoke_id=}")
        # print(f"yo_id: {ai_lesser.rank=} target: {ai_greater.rank=}")
        # print(
        #     f"First yo_id: {ai_lesser.root_relative_weight=} target: {ai_greater.root_relative_weight=}"
        # )

        iter_count = 0
        max_count_x = 50

        while iter_count < max_count_x and ai_lesser.rank >= ai_greater.rank:
            # leftover while loop debugging print statements...
            iter_count += 1
            ai_lesser = self._change_yoketree_weights_once(agenda_lesser=ai_lesser)
            # print(
            #     f"yo_id: {ai_lesser.yoke_id}({ai_lesser.rank}) {ai_lesser.root_relative_weight} {iter_count}/{max_count_x} target: {self.agenda_list[0].yoke_id}"
            # )
            ai_greater = self._get_agenda_item(yo_id=ai_greater.yoke_id)
            # print(
            #     f"yo_id: {ai_lesser.yoke_id}({ai_lesser.rank}) {ai_lesser.root_relative_weight} {iter_count}/{max_count_x} target: {ai_greater.yoke_id}({ai_greater.rank})"
            # )

        # go in order of deepest an
        # print(f"{agenda_lesser.yoke_id=} {agenda_lesser.root_relative_weight=} ")
        # print(f"Next agenda item to jump: {agenda_big.yoke_id=}")
        # print(f"Ratio of difference: {proportional_difference=}")
        # print(f"Greatest common ancestor: {most_recent_common_anc_id=}")
        # x1 = "YO"
        # xa = "increase"
        # print(
        #     f"{iter_count}/{max_count_x} yo_id: {yoke_x.yoke_id}({yoke_x.rank}) target: {agenda_big.yoke_id}({agenda_big.rank}) {x1}{level_siblings.level}_anc_yo_id: {level_siblings.yo_id} {level_siblings.yo_weight} to {new_weight}"
        # )
        # else:
        #     print(
        #         f"{iter_count}/{max_count_x} yo_id: {yoke_x.yoke_id}({yoke_x.rank}) target: {agenda_big.yoke_id}({agenda_big.rank}) {x1}_anc_id L{level_siblings.level}: {level_siblings.yo_id} weight={level_siblings.yo_weight}/{str(level_siblings._level_weight_avg)[0:4]}"
        #     )
        # x1 = "TA"
        # xa = "decrease"

        # print(
        #     f"{iter_count}/{max_count_x} yo_id: {yoke_x.yoke_id}({yoke_x.rank}) target: {agenda_big.yoke_id}({agenda_big.rank}) {x1}{level_siblings.level}_anc_yo_id: {level_siblings.yo_id} {level_siblings.yo_weight} to {new_weight}"
        # )

        # else:
        #     print(
        #         f"{iter_count}/{max_count_x} yo_id: {yoke_x.yoke_id}({yoke_x.rank}) target: {agenda_big.yoke_id}({agenda_big.rank}) {x1}_anc_id L{level_siblings.level}: {level_siblings.yo_id} weight={level_siblings.yo_weight}/{str(level_siblings._level_weight_avg)[0:4]}"
        #     )

        # x1 = "TA"
        # xa = "decrease"

        #         print(
        #             f"{iter_count}/{max_count_x} yo_id: {yoke_x.yoke_id}({yoke_x.rank}) target: {agenda_big.yoke_id}({agenda_big.rank}) {x1}{level_siblings.level}_anc_yo_id: {level_siblings.yo_id} rrw: {rrw_cac_t}"
        #         )
        #         # print(
        #         #     f"{iter_count}/{max_count_x} yo_id: {yoke_x.yoke_id}({yoke_x.rank}) target: {agenda_big.yoke_id}({agenda_big.rank}) {x1}{level_siblings.level}_anc_yo_id: {level_siblings.yo_id} weight {cac_t_weight}"
        #         # )

        # x1 = "YO"
        # xa = "increase"

    def _increase_any_below_average_weight_to_avg(
        self, yoke_small_lineage, oldest_anc_id: int, agenda_unchanged: bool
    ):
        for level_siblings in yoke_small_lineage:
            if (
                agenda_unchanged
                and level_siblings.yo_id != oldest_anc_id
                and level_siblings.yo_weight < int(level_siblings._level_weight_avg)
            ):
                new_weight = int(level_siblings._level_weight_avg) + 1
                yoke = iYokeNodeUnit()
                yoke.select(id=level_siblings.yo_id)
                yoke.edit(weight=new_weight)
                yoke.update()
                yoke = None
                agenda_unchanged = False

        return agenda_unchanged

    def _decrease_any_below_average_weight_to_avg(
        self, yoke_big_lineage, oldest_anc_id: int, agenda_unchanged: bool
    ):
        for level_siblings in yoke_big_lineage:
            if (
                agenda_unchanged
                and level_siblings.yo_id != oldest_anc_id
                and level_siblings.yo_weight > int(level_siblings._level_weight_avg)
            ):
                new_weight = int(level_siblings._level_weight_avg) - 1
                yoke = iYokeNodeUnit()
                yoke.select(id=level_siblings.yo_id)
                yoke.edit(weight=new_weight)
                yoke.update()
                yoke = None
                agenda_unchanged = False

        return agenda_unchanged

    def _increase_common_ancestor_child_weight(
        self, yoke_big_lineage, yoke_small_lineage, most_recent_common_anc_id: int
    ):
        # the most_recent_common_anc_id has one child "cac_t" on the target path and one child "cay_t" on yoke_x path
        # if setting all the deeper deeper relative weights are average then
        rrw_cac_t = None
        rrw_cay_t = None
        for level_siblings in yoke_big_lineage:
            if level_siblings.parent_id == most_recent_common_anc_id:
                yoke_cac_t = iYokeNodeUnit()
                yoke_cac_t.select(id=level_siblings.yo_id)
                rrw_cac_t = yoke_cac_t.root_relative_weight

        for level_siblings in yoke_small_lineage:
            if level_siblings.parent_id == most_recent_common_anc_id:
                yoke_cay_t = iYokeNodeUnit()
                yoke_cay_t.select(id=level_siblings.yo_id)
                rrw_cay_t = yoke_cay_t.root_relative_weight
                # print(
                #     f"{iter_count}/{max_count_x} yo_id: {yoke_x.yoke_id}({yoke_x.rank}) target: {agenda_big.yoke_id}({agenda_big.rank}) {x1}{level_siblings.level}_anc_yo_id: {level_siblings.yo_id} rrw: {rrw_cay_t}"
                # )

                new_weight = int(level_siblings.yo_weight * (rrw_cay_t / rrw_cac_t)) + 1
                # print(f"{rrw_cay_t=}")
                # print(f"{rrw_cac_t=}")
                # print(f"{rrw_cay_t / rrw_cac_t=}")
                # print(
                #     f"{iter_count}/{max_count_x} yo_id: {yoke_x.yoke_id}({yoke_x.rank}) target: {agenda_big.yoke_id}({agenda_big.rank}) {x1}{level_siblings.level}_anc_yo_id: {level_siblings.yo_id} old_w: {level_siblings.yo_weight} new_weight {new_weight}"
                # )

                yoke_cay_t.edit(weight=new_weight)
                yoke_cay_t.update()
                yoke = None
                agenda_unchanged = False
        return agenda_unchanged

    def _change_yoketree_weights_once(self, agenda_lesser: AgendaItem):
        if agenda_lesser == None:
            raise Exception("Small Agenda Item cannot be empty")
        agenda_unchanged = True
        agenda_big = None
        agenda_big = self._get_bigger_agenda_item(agenda_lesser=agenda_lesser)
        if agenda_big == None:
            raise Exception("Big Agenda Item cannot be empty")

        most_recent_common_anc_id = YokeTreeUnit_methods.get_common_ancester(
            yo1=agenda_lesser.yoke_id, yo2=agenda_big.yoke_id
        )
        yoke_small_lineage = YokeTreeUnit_methods.get_lineage(
            anc_yo_id=most_recent_common_anc_id, des_yo_id=agenda_lesser.yoke_id
        )
        agenda_unchanged = self._increase_any_below_average_weight_to_avg(
            yoke_small_lineage=yoke_small_lineage,
            oldest_anc_id=most_recent_common_anc_id,
            agenda_unchanged=agenda_unchanged,
        )

        yoke_big_lineage = YokeTreeUnit_methods.get_lineage(
            anc_yo_id=most_recent_common_anc_id, des_yo_id=agenda_big.yoke_id
        )
        agenda_unchanged = self._decrease_any_below_average_weight_to_avg(
            yoke_big_lineage=yoke_big_lineage,
            oldest_anc_id=most_recent_common_anc_id,
            agenda_unchanged=agenda_unchanged,
        )

        if agenda_unchanged:
            agenda_unchanged = self._increase_common_ancestor_child_weight(
                yoke_small_lineage=yoke_small_lineage,
                yoke_big_lineage=yoke_big_lineage,
                most_recent_common_anc_id=most_recent_common_anc_id,
            )

        if agenda_unchanged:
            raise ValueError(
                f"Agenda item is not first but unable to identify any action to move to first."
            )

        elif agenda_unchanged == False:
            self.set_agenda_list()
            agenda_item_now_more_important = self._get_agenda_item(
                yo_id=agenda_lesser.yoke_id
            )

        return agenda_item_now_more_important
