"""A set of builder methods to create CX proto resource objects"""

# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from typing import List, Dict, Union

import pandas as pd
from google.cloud.dialogflowcx_v3beta1.types import Fulfillment
from google.cloud.dialogflowcx_v3beta1.types import TransitionRoute
from google.cloud.dialogflowcx_v3beta1.types import TransitionRouteGroup

from dfcx_scrapi.builders.builders_common import BuildersCommon
from dfcx_scrapi.builders.routes import TransitionRouteBuilder

# logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class TransitionRouteGroupBuilder(BuildersCommon):
    """Base Class for CX TransitionRouteGroup builder."""

    _proto_type = TransitionRouteGroup
    _proto_type_str = "TransitionRouteGroup"
    _proto_attrs = [
        "name",
        "display_name",
        "transition_routes",
    ]


    def __str__(self) -> str:
        """String representation of the proto_obj."""
        self._check_proto_obj_attr_exist()

        transition_routes_str = "\n".join([
            f"\n\n - Transition Route{i+1}:\n{str(TransitionRouteBuilder(tr))}"
            for i, tr in enumerate(self.proto_obj.transition_routes)
        ])

        return (
            f"display_name: {self.proto_obj.display_name}"
            f"\nTransitionRoutes:\n{'-'*20}\n{transition_routes_str}"
        )

    def _create_new_proto_obj(
        self,
        display_name: str,
        transition_routes: Union[TransitionRoute, List[TransitionRoute]] = None,
        overwrite: bool = False
    ) -> TransitionRouteGroup:
        """Create a new TransitionRouteGroup.

        Args:
          display_name (str):
            Required. The human-readable name of the
            transition route group, unique within the flow.
            The display name can be no longer than 30 characters.
          transition_routes (TransitionRoute | List[TransitionRoute]):
            Transition routes associated with this TransitionRouteGroup.
            Refer to `builders.routes.TransitionRouteBuilder` to build one.
          overwrite (bool)
            Overwrite the new proto_obj if proto_obj already
            contains a TransitionRouteGroup.

        Returns:
          A TransitionRouteGroup object stored in proto_obj.
        """
        # Types error checking
        if not (display_name and isinstance(display_name, str)):
            raise ValueError("display_name should be a nonempty string.")
        if transition_routes and not (
            isinstance(transition_routes, TransitionRoute) or
            (isinstance(transition_routes, list) and all(
                isinstance(tr, TransitionRoute) for tr in transition_routes))
        ):
            raise ValueError(
                "transition_routes should be either a TransitionRoute or"
                " a list of TransitionRoutes."
            )
        # `overwrite` parameter error checking
        if self.proto_obj and not overwrite:
            raise UserWarning(
                "proto_obj already contains a TransitionRouteGroup."
                " If you wish to overwrite it, pass overwrite as True."
            )
        # Create the TransitionRouteGroup
        if overwrite or not self.proto_obj:
            if not transition_routes:
                transition_routes = []
            if not isinstance(transition_routes, list):
                transition_routes = [transition_routes]
            self.proto_obj = TransitionRouteGroup(
                display_name=display_name,
                transition_routes=transition_routes
            )
        self._add_proto_attrs_to_builder_obj()

        return self.proto_obj


    def show_transition_route_group(self):
        """Show the proto_obj information."""
        self._check_proto_obj_attr_exist()

        print(self)

    def create_new_transition_route_group(
        self,
        display_name: str,
        transition_routes: Union[TransitionRoute, List[TransitionRoute]] = None,
        overwrite: bool = False
    ) -> TransitionRouteGroup:
        """Create a new TransitionRouteGroup.

        Args:
          display_name (str):
            Required. The human-readable name of the
            transition route group, unique within the flow.
            The display name can be no longer than 30 characters.
          transition_routes (TransitionRoute | List[TransitionRoute]):
            Transition routes associated with this TransitionRouteGroup.
            Refer to `builders.routes.TransitionRouteBuilder` to build one.
          overwrite (bool)
            Overwrite the new proto_obj if proto_obj already
            contains a TransitionRouteGroup.

        Returns:
          A TransitionRouteGroup object stored in proto_obj.
        """
        return self._create_new_proto_obj(
            display_name=display_name, transition_routes=transition_routes,
            overwrite=overwrite)

    def add_transition_route(
        self,
        transition_routes: Union[TransitionRoute, List[TransitionRoute]] = None,
        intent: str = None,
        condition: str = None,
        target_page: str = None,
        target_flow: str = None,
        trigger_fulfillment: Fulfillment = None,
        agent_response: Union[str, List[str]] = None,
        parameter_map: Dict[str, str] = None,
    ) -> TransitionRouteGroup:
        """Add single or multiple TransitionRoutes to the TransitionRouteGroup.
        You can either pass TransitionRoute objects or create a TransitionRoute
        on the fly by passing other parameters. Note that `transition_routes`
        takes priority over other parameters.

        Args:
          transition_routes (TransitionRoute | List[TransitionRoute]):
            A single or list of TransitionRoutes to add
            to the TransitionRouteGroup existed in proto_obj.
          intent (str):
            Indicates that the transition can only happen when the given
            intent is matched.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/
              agents/<Agent ID>/intents/<Intent ID>``.
            At least one of ``intent`` or ``condition`` must be specified.
            When both ``intent`` and ``condition`` are specified,
            the transition can only happen when both are fulfilled.
          condition (str):
            The condition to evaluate.
            See the conditions reference:
            https://cloud.google.com/dialogflow/cx/docs/reference/condition
            At least one of ``intent`` or ``condition`` must be specified.
            When both ``intent`` and ``condition`` are specified,
            the transition can only happen when both are fulfilled.
          target_page (str):
            The target page to transition to. Format:
            ``projects/<Project ID>/locations/<Location ID>/
              agents/<Agent ID>/flows/<Flow ID>/pages/<Page ID>``.
            At most one of ``target_page`` and ``target_flow``
            can be specified at the same time.
          target_flow (str):
            The target flow to transition to. Format:
            ``projects/<Project ID>/locations/<Location ID>/
              agents/<Agent ID>/flows/<Flow ID>``.
            At most one of ``target_page`` and ``target_flow``
            can be specified at the same time.
          trigger_fulfillment (Fulfillment):
            The fulfillment to call when the condition is satisfied.
            When ``trigger_fulfillment`` and ``target`` are defined,
            ``trigger_fulfillment`` is executed first.
          agent_response (str | List[str]):
            Agent's response message (Fulfillment). A single message as
            a string or multiple messages as a list of strings.
          parameter_map (Dict[str, str]):
            A dictionary that represents parameters as keys
            and the parameter values as it's values.
            A `None` value clears the parameter.

        Returns:
          A TransitionRouteGroup object stored in proto_obj.
        """
        self._check_proto_obj_attr_exist()

        if not transition_routes is None:
            self._is_type_or_list_of_types(
                transition_routes, TransitionRoute, "transition_routes")

            if not isinstance(transition_routes, list):
                transition_routes = [transition_routes]
        else:
            trb = TransitionRouteBuilder()
            trb.create_new_proto_obj(
                intent, condition, trigger_fulfillment,
                target_page, target_flow)
            if trigger_fulfillment is None:
                trb.set_fulfillment(
                    message=agent_response, parameter_map=parameter_map)
            transition_routes = [trb.proto_obj]

        self.proto_obj.transition_routes.extend(transition_routes)
        return self.proto_obj

    def remove_transition_route(
        self,
        transition_route: TransitionRoute = None,
        intent: str = None,
        condition: str = None
    ) -> TransitionRouteGroup:
        """Remove a transition route from the TransitionRouteGroup.

        At least one of the `transition_route`, `intent`, or `condition` should
        be specfied.

        Args:
            transition_route (TransitionRoute):
              The TransitionRoute to remove from the TransitionRouteGroup.
            intent (str):
              TransitionRoute's intent that should be removed from
              the TransitionRouteGroup.
            condition (str):
              TransitionRoute's condition that should be removed from
              the TransitionRouteGroup.

        Returns:
          A TransitionRouteGroup object stored in proto_obj.
        """
        self._check_proto_obj_attr_exist()

        new_routes = []
        for tr in self.proto_obj.transition_routes:
            if self._match_transition_route(
                transition_route=tr, target_route=transition_route,
                intent=intent, condition=condition
            ):
                continue
            new_routes.append(tr)
        self.proto_obj.transition_routes = new_routes

        return self.proto_obj


    class _Dataframe(BuildersCommon._DataframeCommon): # pylint: disable=W0212
        """An internal class to store DataFrame related methods."""

        def proto_to_dataframe(
            self, obj: TransitionRouteGroup, mode: str = "basic"
        ) -> pd.DataFrame:
            """Converts a TransitionRouteGroup protobuf object
            to pandas Dataframe.

            Args:
              obj (TransitionRouteGroup):
                TransitionRouteGroup protobuf object
              mode (str):
                Whether to return 'basic' DataFrame or 'advanced' one.
                Refer to `data.dataframe_schemas.json` for schemas.

            Returns:
              A pandas Dataframe
            """
            if mode not in ["basic", "advanced"]:
                raise ValueError("Mode types: ['basic', 'advanced'].")

            routes_df = pd.DataFrame(
                columns=self._dataframes_map["TransitionRoute"][mode]
            )
            for route in obj.transition_routes:
                trb = TransitionRouteBuilder(route)
                trb_df = trb.to_dataframe(mode)
                routes_df = pd.concat([routes_df, trb_df], ignore_index=True)

            flow_id = str(obj.name).split(
                "/transitionRouteGroups", maxsplit=1
            )[0]
            routes_df["name"] = str(obj.name)
            routes_df["display_name"] = str(obj.display_name)
            routes_df["flow"] = flow_id

            return routes_df[self._dataframes_map["TransitionRouteGroup"][mode]]
