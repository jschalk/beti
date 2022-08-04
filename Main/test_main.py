from email.errors import NonPrintableDefect
from agenda import AgendaDocket
from yoke import (
    YokeCore,
    YokeRoot,
    YokeChild,
    LimmetUnit,
    LimmitUnit,
    HandUnit,
)


def get_yoke_with_4_levels():
    yoke_grandchildU = YokeChild(_weight=20, _desc="Sunday")
    yoke_grandchildM = YokeChild(_weight=20, _desc="Monday")
    yoke_grandchildT = YokeChild(_weight=20, _desc="Tuesday")
    yoke_grandchildW = YokeChild(_weight=20, _desc="Wednesday")
    yoke_grandchildR = YokeChild(_weight=30, _desc="Thursday")
    yoke_grandchildF = YokeChild(_weight=40, _desc="Friday")
    yoke_grandchildA = YokeChild(_weight=50, _desc="Saturday")
    yoke_child_weekdays = YokeChild(_weight=40, _desc="weekdays")
    yoke_child_weekdays.add_child(yoke_grandchildU)
    yoke_child_weekdays.add_child(yoke_grandchildM)
    yoke_child_weekdays.add_child(yoke_grandchildT)
    yoke_child_weekdays.add_child(yoke_grandchildW)
    yoke_child_weekdays.add_child(yoke_grandchildR)
    yoke_child_weekdays.add_child(yoke_grandchildF)
    yoke_child_weekdays.add_child(yoke_grandchildA)

    yoke_grandgrandchild_usa_texas = YokeChild(_weight=50, _desc="Texas")
    yoke_grandgrandchild_usa_oregon = YokeChild(_weight=50, _desc="Oregon")
    yoke_grandchild_usa = YokeChild(_weight=50, _desc="USA")
    yoke_grandchild_usa.add_child(yoke_grandgrandchild_usa_texas)
    yoke_grandchild_usa.add_child(yoke_grandgrandchild_usa_oregon)

    yoke_grandchild_france = YokeChild(_weight=50, _desc="France")
    yoke_grandchild_brazil = YokeChild(_weight=50, _desc="Brazil")
    yoke_child_states = YokeChild(_weight=30, _desc="nation-state")
    yoke_child_states.add_child(yoke_grandchild_france)
    yoke_child_states.add_child(yoke_grandchild_brazil)
    yoke_child_states.add_child(yoke_grandchild_usa)

    yoke_child_work = YokeChild(_weight=30, _desc="work", action=True)
    yoke_child_feedcat = YokeChild(_weight=30, _desc="feed cat", action=True)
    root_x = YokeRoot(_weight=10, _desc="promises")
    root_x.add_child(yoke_child_weekdays)
    root_x.add_child(yoke_child_feedcat)
    root_x.add_child(yoke_child_work)
    root_x.add_child(yoke_child_states)
    return root_x


def get_yoke_with_4_levels_and_2limmits():
    root_x = get_yoke_with_4_levels()
    wednesday = f"{root_x._desc},weekdays,Wednesday"
    weekday = f"{root_x._desc},weekdays"
    wed_limmet = LimmetUnit(path=wednesday)
    usa = f"{root_x._desc},nation-state,USA"
    nationstate = f"{root_x._desc},nation-state"
    usa_limmet = LimmetUnit(path=usa)
    work_wk_limmit = LimmitUnit(base=weekday, limmets={wed_limmet.path: wed_limmet})
    nationstate_limmit = LimmitUnit(
        base=nationstate, limmets={usa_limmet.path: usa_limmet}
    )
    root_x.root_set_limmit_unit(path=f"{root_x._desc},work", limmit=work_wk_limmit)
    root_x.root_set_limmit_unit(path=f"{root_x._desc},work", limmit=nationstate_limmit)
    return root_x


def get_yoke_with_4_levels_and_2limmits_2hands():
    root_x = get_yoke_with_4_levels_and_2limmits()
    wednesday = f"{root_x._desc},weekdays,Wednesday"
    weekday = f"{root_x._desc},weekdays"
    states = f"{root_x._desc},nation-state"
    usa_path = f"{root_x._desc},nation-state,USA"
    root_x.set_hands(base=weekday, hand=wednesday)
    root_x.set_hands(base=states, hand=usa_path)
    return root_x


def get_yoke_with7amCleanTableLimmit():
    root_x = get_yoke_with_4_levels_and_2limmits_2hands()
    yoke_01 = YokeChild(_weight=50, _desc="1")
    yoke_02 = YokeChild(_weight=50, _desc="2")
    yoke_03 = YokeChild(_weight=50, _desc="3")
    yoke_am = YokeChild(_weight=50, _desc="am")
    yoke_am.add_child(yoke_01)
    yoke_am.add_child(yoke_02)
    yoke_am.add_child(yoke_03)
    yoke_pm = YokeChild(_weight=50, _desc="pm")
    yoke_24hr_day = YokeChild(_weight=40, _desc="24hr day", _open=0.0, _nigh=24.0)
    yoke_24hr_day.add_child(yoke_am)
    yoke_24hr_day.add_child(yoke_pm)
    yoke_timeline = YokeChild(_weight=40, _desc="timetech")
    yoke_timeline.add_child(yoke_24hr_day)
    root_x.add_child(yoke_child=yoke_timeline)

    yoke_picksoap = YokeChild(_weight=40, _desc="pick soap", action=True)
    yoke_tablesoap = YokeChild(_weight=40, _desc="get soap", action=True)
    yoke_tablesoap.add_child(yoke_child=yoke_picksoap)

    yoke_tabledishs = YokeChild(_weight=40, _desc="remove dishs", action=True)
    yoke_cleantable = YokeChild(_weight=40, _desc="clean table", action=True)
    yoke_cleantable.add_child(yoke_child=yoke_tabledishs)
    yoke_cleantable.add_child(yoke_child=yoke_tablesoap)

    yoke_housework = YokeChild(_weight=40, _desc="housework")
    yoke_housework.add_child(yoke_child=yoke_cleantable)
    root_x.add_child(yoke_child=yoke_housework)

    clean_table_7am_base = f"{root_x._desc},timetech,24hr day"
    clean_table_7am_limmet_path = f"{root_x._desc},timetech,24hr day"
    clean_table_7am_limmet_open = 7.0
    clean_table_7am_limmet_nigh = 7.0
    clean_table_7am_limmet = LimmetUnit(
        path=clean_table_7am_limmet_path,
        open=clean_table_7am_limmet_open,
        nigh=clean_table_7am_limmet_nigh,
    )
    clean_table_7am_limmit = LimmitUnit(
        base=clean_table_7am_base,
        limmets={clean_table_7am_limmet.path: clean_table_7am_limmet},
    )
    root_x.root_set_limmit_unit(
        path=f"{root_x._desc},housework,clean table", limmit=clean_table_7am_limmit
    )
    root_x.root_set_limmit_unit(
        path=f"{root_x._desc},work", limmit=clean_table_7am_limmit
    )
    return root_x


def test_yoke_core_exists():
    new_obj = YokeCore()
    assert new_obj
    assert new_obj._children == None
    assert new_obj._weight >= 1
    assert new_obj._desc == None
    assert new_obj._uid == None


def test_yoke_root_exists():
    new_obj = YokeRoot()
    assert new_obj
    assert new_obj._children == None
    assert new_obj._hands == {}


def test_yoke_child_exists():
    new_obj = YokeChild()
    assert new_obj
    assert new_obj._children == None


def test_root_has_children():
    root_x = YokeRoot(_weight=10)
    yoke1 = YokeChild(_weight=30, _desc="work")
    yoke2 = YokeChild(_weight=40, _desc="ulty")
    root_x.add_child(yoke_child=yoke1)
    root_x.add_child(yoke_child=yoke2)
    assert root_x._weight == 10
    assert root_x._children


def test_child_can_have_children():
    root_x = get_yoke_with_4_levels()

    assert root_x._weight == 10
    assert root_x._children
    assert root_x.get_node_count() == 17
    assert root_x.get_level_count(level=0) == 1
    assert root_x.get_level_count(level=1) == 4
    assert root_x.get_level_count(level=2) == 10
    assert root_x.get_level_count(level=3) == 2


def test_can_add_child_to_root_yoke():
    root_x = get_yoke_with_4_levels()
    assert root_x.get_node_count() == 17
    assert root_x.get_level_count(level=1) == 4

    new_yoke_parent_path = root_x._desc
    new_yoke = YokeChild(_weight=40, _desc="new_yoke")

    root_x.add_yoke(yoke_child=new_yoke, path=new_yoke_parent_path)
    print(f"{(root_x._desc == new_yoke_parent_path[0])=}")
    print(f"{(len(new_yoke_parent_path) == 1)=}")
    assert root_x.get_node_count() == 18
    assert root_x.get_level_count(level=1) == 5


def test_can_add_child_to_child_yoke():
    root_x = get_yoke_with_4_levels()
    assert root_x.get_node_count() == 17
    assert root_x.get_level_count(level=2) == 10

    new_yoke_parent_path = f"{root_x._desc},work"
    new_yoke = YokeChild(_weight=40, _desc="new_yoke")

    root_x.add_yoke(yoke_child=new_yoke, path=new_yoke_parent_path)
    print(f"{(root_x._desc == new_yoke_parent_path[0])=}")
    print(root_x._children["work"])
    print(f"{(len(new_yoke_parent_path) == 1)=}")
    assert root_x.get_node_count() == 18
    assert root_x.get_level_count(level=2) == 11


def test_can_add_child_to_grandchild_yoke():
    root_x = get_yoke_with_4_levels()

    assert root_x.get_node_count() == 17
    assert root_x.get_level_count(level=3) == 2
    new_yoke_parent_path = f"{root_x._desc},weekdays,Wednesday"
    new_yoke = YokeChild(_weight=40, _desc="new_yoke")
    root_x.add_yoke(yoke_child=new_yoke, path=new_yoke_parent_path)
    print(f"{(root_x._desc == new_yoke_parent_path[0])=}")
    print(root_x._children["work"])
    print(f"{(len(new_yoke_parent_path) == 1)=}")
    assert root_x.get_node_count() == 18
    assert root_x.get_level_count(level=3) == 3


def test_yoke_lineage_check_works():
    root_x = get_yoke_with_4_levels()
    sunday_path = f"{root_x._desc},weekdays,Sunday"
    weekday_path = f"{root_x._desc},weekdays"
    assert root_x.is_heir(src=weekday_path, heir=sunday_path)
    assert root_x.is_heir(src=sunday_path, heir=weekday_path) == False


def test_limmet_clear_works():
    limmet = LimmetUnit(path="promises,work,check email")
    assert limmet._status == None
    limmet._status = True
    assert limmet._status == True
    limmet.clear_status()
    assert limmet._status == None


def test_limmet_set_status_CorrectlySetsStatus_1():
    limmet = LimmetUnit(path="home,weekday,wednesday")
    lifeworld_hand = HandUnit(base="home,weekday", hand="home,weekday,wednesday")
    assert limmet._status == None
    limmet.set_status(hand_unit=lifeworld_hand)
    assert limmet._status == True


def test_limmet_set_status_CorrectlySetsStatus_2():
    limmet_2 = LimmetUnit(path="home,weekday,wednesday,wed_afternoon")
    lifeworld_hand_2 = HandUnit(base="home,weekday", hand="home,weekday,wednesday")
    assert limmet_2._status == None
    limmet_2.set_status(hand_unit=lifeworld_hand_2)
    assert limmet_2._status == True


def test_limmet_set_status_CorrectlySetsStatus_3():
    limmet_3 = LimmetUnit(path="home,weekday,wednesday")
    lifeworld_hand_3 = HandUnit(base="home,weekday", hand="home,weekday,wednesday,noon")
    assert limmet_3._status == None
    limmet_3.set_status(hand_unit=lifeworld_hand_3)
    assert limmet_3._status == True


def test_limmet_set_status_CorrectlySetsStatus_4():
    limmet_4 = LimmetUnit(path="home,weekday,wednesday")
    lifeworld_hand_4 = HandUnit(base="home,weekday", hand="home,weekday,thursday")
    assert limmet_4._status == None
    assert limmet_4.is_in_lineage(hand=lifeworld_hand_4.hand) == False
    assert lifeworld_hand_4.open == None
    assert lifeworld_hand_4.nigh == None
    limmet_4.set_status(hand_unit=lifeworld_hand_4)
    assert limmet_4._status == False


def test_limmet_set_status_CorrectlySetsStatus_5():
    limmet_5 = LimmetUnit(path="home,weekday,wednesday,sunny")
    lifeworld_hand_5 = HandUnit(base="home,weekday", hand="home,weekday,rainy")
    assert limmet_5._status == None
    limmet_5.set_status(hand_unit=lifeworld_hand_5)
    assert limmet_5._status == False


def test_limmet_set_status_CorrectlySetsTimeRangeStatusTrue():
    limmet = LimmetUnit(path="home,timetech,24hr", open=7, nigh=7)
    lifeworld_hand = HandUnit(
        base="home,timetech,24hr", hand="home,timetech,24hr", open=0, nigh=8
    )
    assert limmet._status == None
    limmet.set_status(hand_unit=lifeworld_hand)
    assert limmet._status == True


def test_limmet_set_status_CorrectlySetsTimeRangeStatusFalse():
    limmet = LimmetUnit(path="home,timetech,24hr", open=7, nigh=7)
    lifeworld_hand = HandUnit(
        base="home,timetech,24hr", hand="home,timetech,24hr", open=8, nigh=10
    )
    assert limmet._status == None
    limmet.set_status(hand_unit=lifeworld_hand)
    assert limmet._status == False


def test_limmit_clear_works():
    limmet = LimmetUnit(path="promises,work,check email")
    limmets = {limmet.path: limmet}
    base = "promises,work"
    limmit = LimmitUnit(base=base, limmets=limmets)
    assert limmit._status == None
    limmit._status = True
    assert limmit._status == True
    limmit.clear_status()
    assert limmit._status == None


def test_limmit_set_status_CorrectlySetsStatus():
    limmet = LimmetUnit(path="home,weekday,wednesday")
    limmets = {limmet.path: limmet}
    limmit = LimmitUnit(base="home,weekday", limmets=limmets)
    x_hand = HandUnit(base="home,weekday", hand="home,weekday,wednesday,noon")
    assert limmit._status == None
    limmit.set_status(hand_unit=x_hand)
    assert limmit._status == True

    limmetW = LimmetUnit(path="home,weekday,wednesday")
    limmetR = LimmetUnit(path="home,weekday,thursday")
    limmets = {limmetW.path: limmetW, limmetR.path: limmetR}
    limmit = LimmitUnit(base="home,weekday", limmets=limmets)
    x_hand = HandUnit(base="home,weekday", hand="home,weekday,wednesday,noon")
    assert limmit._status == None
    limmit.set_status(hand_unit=x_hand)
    assert limmit._status == True

    limmetW = LimmetUnit(path="home,weekday,wednesday")
    limmetR = LimmetUnit(path="home,weekday,thursday")
    limmets = {limmetW.path: limmetW, limmetR.path: limmetR}
    limmit = LimmitUnit(base="home,weekday", limmets=limmets)
    x_hand = HandUnit(base="home,weekday", hand="home,weekday,friday")
    assert limmit._status == None
    limmit.set_status(hand_unit=x_hand)
    assert limmit._status == False


def test_yoke_root_limmits_create():
    root_x = get_yoke_with_4_levels()
    work_path = f"{root_x._desc},work"
    wednesday_path = f"{root_x._desc},weekdays,Wednesday"
    weekday_path = f"{root_x._desc},weekdays"

    wed_limmet = LimmetUnit(path=wednesday_path)
    work_wk_limmit = LimmitUnit(
        base=weekday_path, limmets={wed_limmet.path: wed_limmet}
    )
    print(f"{type(work_wk_limmit.base)=}")
    print(f"{work_wk_limmit.base=}")
    root_x.root_set_limmit_unit(path=work_path, limmit=work_wk_limmit)
    work_yoke = root_x._children["work"]
    assert work_yoke._limmits != None
    print(work_yoke._limmits)
    assert work_yoke._limmits[weekday_path] != None
    assert work_yoke._limmits[weekday_path] == work_wk_limmit


def test_yoke_root_set_limmits_status():
    root_x = get_yoke_with_4_levels()
    work_path = f"{root_x._desc},work"
    wednesday_path = f"{root_x._desc},weekdays,Wednesday"
    weekday_path = f"{root_x._desc},weekdays"

    wed_limmet = LimmetUnit(path=wednesday_path)
    work_wk_limmit = LimmitUnit(
        base=weekday_path, limmets={wed_limmet.path: wed_limmet}
    )
    print(f"{type(work_wk_limmit.base)=}")
    print(f"{work_wk_limmit.base=}")
    root_x.root_set_limmit_unit(path=work_path, limmit=work_wk_limmit)
    work_yoke = root_x._children["work"]
    assert work_yoke._limmits != None
    print(work_yoke._limmits)
    assert work_yoke._limmits[weekday_path] != None
    assert work_yoke._limmits[weekday_path] == work_wk_limmit


def test_yoke_root_hand_exists():
    root_x = get_yoke_with_4_levels()
    sunday_path = f"{root_x._desc},weekdays,Sunday"
    weekday_path = f"{root_x._desc},weekdays"
    sunday_lw_hand = HandUnit(base=weekday_path, hand=sunday_path)
    print(sunday_lw_hand)
    root_x._hands = {sunday_lw_hand.base: sunday_lw_hand}
    assert root_x._hands


def test_yoke_root_hand_create():
    root_x = get_yoke_with_4_levels()
    sunday_path = f"{root_x._desc},weekdays,Sunday"
    weekday_path = f"{root_x._desc},weekdays"
    root_x.set_hands(base=weekday_path, hand=sunday_path)
    sunday_lw_hand = HandUnit(base=weekday_path, hand=sunday_path)
    assert root_x._hands == {sunday_lw_hand.base: sunday_lw_hand}


def test_yoke_root_get_yoke_list_SetsLimmotStatusCorrectlyWhenHandSaysNo():
    root_x = get_yoke_with_4_levels_and_2limmits()
    sunday = f"{root_x._desc},weekdays,Sunday"
    weekday = f"{root_x._desc},weekdays"
    root_x.set_hands(base=weekday, hand=sunday)
    yoke_list = root_x.get_yoke_list()
    assert yoke_list
    assert len(yoke_list) == 16
    for curr_yoke in yoke_list:
        if curr_yoke._desc == "Work":
            assert curr_yoke._limmot_status == False


def test_yoke_root_get_yoke_list_SetsLimmotStatusCorrectlyWhenHandChanges():
    root_x = get_yoke_with_4_levels_and_2limmits()
    sunday = f"{root_x._desc},weekdays,Wednesday"
    weekday = f"{root_x._desc},weekdays"
    root_x.set_hands(base=weekday, hand=sunday)
    yoke_list = root_x.get_yoke_list()
    assert yoke_list
    assert len(yoke_list) == 16
    for curr_yoke in yoke_list:
        if curr_yoke._desc == "Work":
            assert curr_yoke._limmot_status == False

    states = f"{root_x._desc},nation-state"
    usa_path = f"{root_x._desc},nation-state,USA"
    root_x.set_hands(base=states, hand=usa_path)

    yoke_list = root_x.get_yoke_list()
    assert yoke_list
    assert len(yoke_list) == 16
    for curr_yoke in yoke_list:
        if curr_yoke._desc == "Work":
            assert curr_yoke._limmot_status == True

    states = f"{root_x._desc},nation-state"
    france_path = f"{root_x._desc},nation-state,France"
    root_x.set_hands(base=states, hand=france_path)

    yoke_list = root_x.get_yoke_list()
    assert yoke_list
    assert len(yoke_list) == 16
    for curr_yoke in yoke_list:
        if curr_yoke._desc == "Work":
            assert curr_yoke._limmot_status == False


def test_yoke_root_get_yoke_list_returns_correct_list():
    root_x = get_yoke_with_4_levels_and_2limmits()
    wednesday = f"{root_x._desc},weekdays,Wednesday"
    weekday = f"{root_x._desc},weekdays"
    states = f"{root_x._desc},nation-state"
    france_path = f"{root_x._desc},nation-state,France"
    root_x.set_hands(base=weekday, hand=wednesday)
    root_x.set_hands(base=states, hand=france_path)
    print(root_x._children["work"]._limmits)
    print(f"{root_x._hands=}")

    yoke_list = root_x.get_yoke_list()
    assert yoke_list
    assert len(yoke_list) == 16
    oregon_path = f"{root_x._desc},nation-state,USA,Oregon"
    usa_path = f"{root_x._desc},nation-state,USA"

    wed = LimmetUnit(path=wednesday)
    wed._status = True
    usa = LimmetUnit(path=usa_path)
    usa._status = False

    x1_limmits = {
        weekday: LimmitUnit(base=weekday, limmets={wed.path: wed}, _status=True),
        states: LimmitUnit(base=states, limmets={usa.path: usa}, _status=False),
    }

    root_x.set_hands(base=states, hand=oregon_path)

    temp_yoke = YokeChild(
        _dir=f"{root_x._desc},work",
        _children=None,
        _weight=30,
        _desc="work",
        _level=1,
        _limmits=x1_limmits,
        _limmot_status=True,
        action=True,
    )
    for curr_yoke in yoke_list:
        assert curr_yoke._limmot_status != None
        print(f"{curr_yoke._desc=}")
        print(f"{curr_yoke._limmits=}")
        for limmit in curr_yoke._limmits.values():
            assert limmit._status != None
            for limmet in limmit.limmets.values():
                assert limmet._status != None

        if curr_yoke._desc == temp_yoke._desc:
            # print(yoke)
            print(f"{curr_yoke._dir=}")
            assert curr_yoke._desc == temp_yoke._desc
            assert curr_yoke._dir == temp_yoke._dir
            print("curr_yoke._limmits")
            print(curr_yoke._limmits)
            print(curr_yoke._limmits[states])
            print(curr_yoke._limmits[states]._status)
            print("temp_yoke._limmits")
            print(temp_yoke._limmits)
            print(temp_yoke._limmits[states])
            print(temp_yoke._limmits[states]._status)
            assert len(curr_yoke._limmits) == len(temp_yoke._limmits)
            assert curr_yoke._limmits == temp_yoke._limmits


def test_yoke_root_get_yoke_list_CorrectlyCalculatesYokeAttributes():
    root_x = get_yoke_with7amCleanTableLimmit()
    yoke_list = root_x.get_yoke_list()
    for yoke in yoke_list:
        print(f"{yoke._desc=}")
        assert yoke._children_total_weight != None
        assert yoke._children_total_weight >= 0
        assert yoke._sibling_total_weight
        assert yoke._sibling_total_weight >= 1
        assert yoke._root_relative_weight > 0 and yoke._root_relative_weight <= 1
        assert yoke._ancestor_action_count != None
        if yoke._desc == "pick soap":
            assert yoke._ancestor_action_count == 2


def test_yoke_root_get_yoke_list_CorrectlyCalculatesRangeAttributes():
    root_x = get_yoke_with7amCleanTableLimmit()
    yoke_list = root_x.get_yoke_list()
    for yoke in yoke_list:
        if yoke._desc == "clean table":
            # for limmit in yoke._limmits.values():
            #     print(f"{yoke._desc=} {limmit}")
            assert yoke._limmot_status == False

    # set hands as midnight to 8am
    day24hr_base = f"{root_x._desc},timetech,24hr day"
    day24hr_hand = f"{root_x._desc},timetech,24hr day"
    day24hr_open = 0.0
    day24hr_nigh = 8.0
    root_x.set_hands(
        base=day24hr_base, hand=day24hr_hand, open=day24hr_open, nigh=day24hr_nigh
    )
    yoke_list = root_x.get_yoke_list()
    temp_yoke = None
    for yoke in yoke_list:
        # print(f"{yoke._limmot_status=} {yoke._desc=}")
        if yoke._desc == "clean table":
            temp_yoke = yoke
            # for limmit in yoke._limmits.values():
            #     print(f"{yoke._desc=} {limmit}")
    assert temp_yoke._limmot_status == True

    # set hands as 8am to 10am
    day24hr_open = 8.0
    day24hr_nigh = 10.0
    print(root_x._hands["promises,timetech,24hr day"])
    root_x.set_hands(
        base=day24hr_base, hand=day24hr_hand, open=day24hr_open, nigh=day24hr_nigh
    )
    print(root_x._hands["promises,timetech,24hr day"])
    print(root_x._children["housework"]._children["clean table"]._limmits)
    # root_x._children["housework"]._children["clean table"]._limmot_status = None
    yoke_list = root_x.get_yoke_list()
    for yoke in yoke_list:
        if yoke._desc == "clean table":
            temp_yoke = yoke
            # for limmit in yoke._limmits.values():
            #     print(f"{yoke._desc=} {limmit}")
    assert temp_yoke._limmot_status == False


def test_get_action_items():
    root_x = get_yoke_with_4_levels_and_2limmits()
    action_items = root_x.get_action_items()
    assert action_items != None
    assert len(action_items) > 0
    assert len(action_items) == 2


def test_get_agenda_returns_agenda():
    root_x = get_yoke_with_4_levels()
    agendaDocket = AgendaDocket(root_yoke=root_x)
    agenda_list = agendaDocket.get_agenda_list()
    assert agenda_list
    assert len(agenda_list) == 2
    assert agenda_list[0].description in ["work", "feed cat"]


def test_get_agenda_returns_agenda_with_only_limmit_allowed():
    root_x = get_yoke_with_4_levels_and_2limmits()
    sunday = f"{root_x._desc},weekdays,Sunday"
    weekday = f"{root_x._desc},weekdays"
    root_x.set_hands(base=weekday, hand=sunday)

    agendaDocket = AgendaDocket(root_yoke=root_x)
    agenda_list = agendaDocket.get_agenda_list()
    assert agenda_list
    assert len(agenda_list) == 1
    print(f"{agenda_list=}")
    assert agenda_list[0].description in ["feed cat"]


def test_get_agenda_returns_agenda_with_root_relative_weight():
    root_x = get_yoke_with_4_levels_and_2limmits_2hands()
    agendaDocket = AgendaDocket(root_yoke=root_x)
    agenda_list = agendaDocket.get_agenda_list()
    assert agenda_list
    assert len(agenda_list) == 2
    for agenda_item in agenda_list:
        assert agenda_item.root_relative_weight


def test_get_agenda_with_No7amItem():
    root_x = get_yoke_with7amCleanTableLimmit()
    agendaDocket = AgendaDocket(root_yoke=root_x)
    agenda_list = agendaDocket.get_agenda_list()
    assert agenda_list
    assert len(agenda_list) == 1
    clean_table = None
    for agenda_item in agenda_list:
        if agenda_item.description == "clean table":
            clean_table = agenda_item
    assert clean_table == None


def test_get_agenda_with_7amItem():
    # set hands as midnight to 8am
    root_x = get_yoke_with7amCleanTableLimmit()
    day24hr_base = f"{root_x._desc},timetech,24hr day"
    day24hr_hand = f"{root_x._desc},timetech,24hr day"
    day24hr_open = 0.0
    day24hr_nigh = 8.0
    root_x.set_hands(
        base=day24hr_base, hand=day24hr_hand, open=day24hr_open, nigh=day24hr_nigh
    )
    print(root_x._hands["promises,timetech,24hr day"])
    print(root_x._children["housework"]._children["clean table"]._limmits)
    print(root_x._children["housework"]._children["clean table"]._limmot_status)
    agendaDocket = AgendaDocket(root_yoke=root_x)
    agenda_list = agendaDocket.get_agenda_list()
    print(agenda_list)
    assert len(agenda_list) == 6
    clean_table = None
    for agenda_item in agenda_list:
        print(agenda_item.description)
        if agenda_item.description == "clean table":
            clean_table = agenda_item
    assert clean_table.description == "clean table"
