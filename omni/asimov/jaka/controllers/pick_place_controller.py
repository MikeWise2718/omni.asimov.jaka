# Copyright (c) 2021-2023, NVIDIA CORPORATION. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto. Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
from typing import List, Optional

import omni.asimov.manipulators.controllers as manipulators_controllers
from omni.isaac.core.articulations import Articulation
# from omni.isaac.franka.controllers.rmpflow_controller import RMPFlowController
from .rmpflow_controller import RMPFlowController
from omni.asimov.manipulators.grippers.parallel_gripper import ParallelGripper


class PickPlaceController(manipulators_controllers.PickPlaceController):
    """[summary]

    Args:
        name (str): [description]
        gripper (ParallelGripper): [description]
        robot_articulation (Articulation): [description]
        end_effector_initial_height (Optional[float], optional): [description]. Defaults to None.
        events_dt (Optional[List[float]], optional): [description]. Defaults to None.
    """

    def __init__(
        self,
        name: str,
        gripper: ParallelGripper,
        robot_articulation: Articulation,
        end_effector_initial_height: Optional[float] = None,
        events_dt: Optional[List[float]] = None,
        rmpconfig: dict = None,
    ) -> None:
        self._eventnames = ["0:goto target", "1:go down", "2:settle", "3:close grip", "4:go up", "5:goto goal", "6:go down", "7:open grip", "8:go up", "9:goto begin","10:stop"]
        if events_dt is None:
            # events_dt = [0.008, 0.005, 1, 0.1, 0.05, 0.05, 0.0025, 1, 0.008, 0.08]
            events_dt = [0.008, 0.005, 0.1,  0.1, 0.005, 0.005, 0.005, 0.1, 0.008, 0.08]
            # steps        125    200    10    10   200    200    200   10   125    12.5
            # phase         0      1    2    3      4     5       6     7    8      9
       # if self._events_dt is None:
       #     self._events_dt = [0.008, 0.005, 0.1, 0.1, 0.0025, 0.001, 0.0025, 0.1, 0.008, 0.08]
            #                    125    200    10    10   400    1000    400   10   125     12.5
            #                      0      1     2     3     4       5      6   7     8        9

        manipulators_controllers.PickPlaceController.__init__(
            self,
            name=name,
            cspace_controller=RMPFlowController(
                rmpconfig=rmpconfig,
                name=name + "_cspace_controller", robot_articulation=robot_articulation
            ),
            gripper=gripper,
            end_effector_initial_height=end_effector_initial_height,
            events_dt=events_dt,
        )
        return
