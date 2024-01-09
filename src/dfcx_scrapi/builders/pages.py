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
from dataclasses import dataclass
from typing import List, Dict, Union, Any

import numpy as np
import pandas as pd
from google.cloud.dialogflowcx_v3beta1.types import Page
from google.cloud.dialogflowcx_v3beta1.types import Form
from google.cloud.dialogflowcx_v3beta1.types import Fulfillment
from google.cloud.dialogflowcx_v3beta1.types import TransitionRoute
from google.cloud.dialogflowcx_v3beta1.types import EventHandler

from dfcx_scrapi.builders.builders_common import BuildersCommon
from dfcx_scrapi.builders.routes import TransitionRouteBuilder
from dfcx_scrapi.builders.routes import EventHandlerBuilder
from dfcx_scrapi.builders.fulfillments import FulfillmentBuilder

# logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class PageBuilder(BuildersCommon):
    """Base Class for CX Page builder."""

    _proto_type = Page
    _proto_type_str = "Page"
    _proto_attrs = [
        "name",
        "display_name",
        "entry_fulfillment",
        "form",
        "transition_route_groups",
        "transition_routes",
        "event_handlers",
        "advanced_settings",
        "knowledge_connector_settings",
    ]


    def __str__(self) -> str:
        """String representation of the proto_obj."""
        self._check_proto_obj_attr_exist()

        return (
            f"Basic Information:\n{'='*25}\n{self._show_basic_info()}"
            f"\n\n\nParameters:\n{'='*25}\n{self._show_parameters()}"
            f"\n\n\nTransitionRoutes:\n{'='*25}"
            f"\n{self._show_transition_routes()}"
            f"\n\n\nEventHandlers:\n{'='*25}\n{self._show_event_handlers()}"
            f"\n\n\nTransitoinRouteGroups:\n{'='*25}"
            f"\n{self._show_transition_route_groups()}")

    def _show_basic_info(self) -> str:
        """String representation for the basic information of proto_obj."""
        self._check_proto_obj_attr_exist()

        entry_fulfillment_str = str(
            FulfillmentBuilder(self.proto_obj.entry_fulfillment)
        )
        return (
            f"display_name: {self.proto_obj.display_name}"
            f"\nentry_fulfillment:\n\n{entry_fulfillment_str}"
        )

    def _show_parameters(self) -> str:
        """String representation for the parameters of proto_obj."""
        self._check_proto_obj_attr_exist()

        return "\n".join([
            (
                f"display_name: {param.display_name}"
                f"\n\tentity_type: {param.entity_type}"
                f"\n\trequired: {param.required}"
                f"\n\tis_list: {param.is_list}"
                f"\n\treadct: {param.redact}"
                f"\n\tdefault_value: {param.default_value}"
            )
            for param in self.proto_obj.form.parameters
        ])

    def _show_transition_routes(self) -> str:
        """String representation for the transition routes of proto_obj."""
        self._check_proto_obj_attr_exist()

        return "\n".join([
            f"TransitionRoute {i+1}:\n{str(TransitionRouteBuilder(tr))}"
            f"\n{'*'*20}\n"
            for i, tr in enumerate(self.proto_obj.transition_routes)
        ])

    def _show_event_handlers(self) -> str:
        """String representation for the event handlers of proto_obj."""
        self._check_proto_obj_attr_exist()

        return "\n".join([
            f"EventHandler {i+1}:\n{str(EventHandlerBuilder(eh))}\n{'*'*20}\n"
            for i, eh in enumerate(self.proto_obj.event_handlers)
        ])

    def _show_transition_route_groups(self) -> str:
        """String representation for the transition route groups of proto_obj"""
        self._check_proto_obj_attr_exist()

        return "\n".join([
            f"TransitionRouteGroup {i+1}: {trg_id}"
            for i, trg_id in enumerate(self.proto_obj.transition_route_groups)
        ])

    def _create_new_proto_obj(
        self,
        display_name: str,
        entry_fulfillment: Fulfillment = None,
        overwrite: bool = False
    ) -> Page:
        """Create a new Page.

        Args:
          display_name (str):
            Required. The human-readable name of the
            page, unique within the flow.
          entry_fulfillment (Fulfillment):
            The fulfillment to call when the session is entering the page.
          overwrite (bool)
            Overwrite the new proto_obj if proto_obj already contains a Page.

        Returns:
          A Page object stored in proto_obj.
        """
        # Types error checking
        if not (display_name and isinstance(display_name, str)):
            raise ValueError("`display_name` should be a nonempty string.")
        if (entry_fulfillment and
            not isinstance(entry_fulfillment, Fulfillment)):
            raise ValueError(
                "The type of `entry_fulfillment` should be a Fulfillment."
            )
        # `overwrite` parameter error checking
        if self.proto_obj and not overwrite:
            raise UserWarning(
                "proto_obj already contains a Page."
                " If you wish to overwrite it, pass `overwrite` as True."
            )
        # Create the Page
        if overwrite or not self.proto_obj:
            if not entry_fulfillment:
                entry_fulfillment = Fulfillment()

            self.proto_obj = Page(
                display_name=display_name,
                entry_fulfillment=entry_fulfillment
            )
        self._add_proto_attrs_to_builder_obj()

        return self.proto_obj


    def show_page_info(
        self, mode: str = "whole"
    ) -> None:
        """Show the proto_obj information.

        Args:
          mode (str):
            Specifies what part of the page to show.
              Options:
              ['basic', 'whole', 'parameters',
              'routes' or 'transition routes',
              'route groups' or 'transition route groups',
              'events' or 'event handlers'
              ]
        """
        self._check_proto_obj_attr_exist()

        if mode == "basic":
            print(self._show_basic_info())
        elif mode == "parameters":
            print(self._show_parameters())
        elif mode in ["routes", "transition routes"]:
            print(self._show_transition_routes())
        elif mode in ["route groups", "transition route groups"]:
            print(self._show_transition_route_groups())
        elif mode in ["events", "event handlers"]:
            print(self._show_event_handlers())
        elif mode == "whole":
            print(self)
        else:
            raise ValueError(
                "mode should be in"
                "['basic', 'whole', 'parameters',"
                " 'routes', 'transition routes',"
                " 'route groups', 'transition route groups',"
                " 'events', 'event handlers']"
            )

    def show_stats(self) -> None:
        """Provide some stats about the Page."""
        self._check_proto_obj_attr_exist()

        stats_instance = PageStats(self.proto_obj)
        stats_instance.generate_stats()

    def create_new_page(
        self,
        display_name: str,
        entry_fulfillment: Fulfillment = None,
        overwrite: bool = False
    ) -> Page:
        """Create a new Page.

        Args:
          display_name (str):
            Required. The human-readable name of the
            page, unique within the flow.
          entry_fulfillment (Fulfillment):
            The fulfillment to call when the session is entering the page.
          overwrite (bool)
            Overwrite the new proto_obj if proto_obj already contains a Page.

        Returns:
          A Page object stored in proto_obj.
        """
        return self._create_new_proto_obj(
            display_name=display_name, entry_fulfillment=entry_fulfillment,
            overwrite=overwrite)

    def set_entry_fulfillment(
        self,
        message: Union[str, List[str], Dict[str, Any]] = None,
        response_type: str = "text",
        mode: str = None,
        webhook: str = None,
        tag: str = None,
        return_partial_responses: bool = False,
        parameter_map: Dict[str, str] = None,
    ):
        """Set the EntryFulfillment of the Page.
        This mehotd overwrites the existing Fulfillment.

        Args:
          message (str | List[str] | Dict[str, Any]):
            The output message. For each response_type
            it should be formatted like the following:
              text --> str | List[str]
                A single message as a string or
                multiple messages as a list of strings
              payload --> Dict[str, Any]
                Any dictionary which its keys are string.
                Dialogflow doesn't impose any structure on the values.
              conversation_success --> Dict[str, Any]
                Any dictionary which its keys are string.
                Dialogflow doesn't impose any structure on the values.
              output_audio_text --> str
                A text or ssml response as a string.
              live_agent_handoff --> Dict[str, Any]
                Any dictionary which its keys are string.
                Dialogflow doesn't impose any structure on the values.
              play_audio --> str
                URI of the audio clip.
                Dialogflow does not impose any validation on this value.
              telephony_transfer_call --> str
                A phone number in E.164 format as a string.
                `<https://en.wikipedia.org/wiki/E.164>`
          response_type (str):
            Type of the response message. It should be one of the following:
            'text', 'payload', 'conversation_success', 'output_audio_text',
            'live_agent_handoff', 'play_audio', 'telephony_transfer_call'
          mode (str):
            This argument is only applicable for `output_audio_text`.
            It should be one of the following: 'text', 'ssml'
          webhook (str):
            The webhook to call. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents
              /<Agent ID>/webhooks/<Webhook ID>``.
          tag (str):
            The tag is typically used by
            the webhook service to identify which fulfillment is being
            called, but it could be used for other purposes. This field
            is required if ``webhook`` is specified.
          return_partial_responses (bool):
            Whether Dialogflow should return currently
            queued fulfillment response messages in
            streaming APIs. If a webhook is specified, it
            happens before Dialogflow invokes webhook.
          parameter_map (Dict[str, str]):
            A dictionary that represents parameters as keys
            and the parameter values as it's values.
            A `None` value clears the parameter.

        Returns:
          A TransitionRoute object stored in proto_obj.
        """
        self._check_proto_obj_attr_exist()

        fb = FulfillmentBuilder()
        fb.create_new_proto_obj(
            webhook=webhook, tag=tag,
            return_partial_responses=return_partial_responses)
        fb.add_response_message(
            message=message, response_type=response_type, mode=mode)
        if not parameter_map is None:
            fb.add_parameter_presets(parameter_map)

        self.proto_obj.entry_fulfillment = fb.proto_obj

        return self.proto_obj

    def add_parameter(
        self,
        display_name: str,
        entity_type: str,
        initial_prompt_fulfillment: Fulfillment,
        required: bool = True,
        default_value: str = None,
        is_list: bool = False,
        redact: bool = False,
        reprompt_event_handlers: Union[EventHandler, List[EventHandler]] = None
    ) -> Page:
        """Add a parameter to collect from the user.

        Args:
          display_name (str):
            Required. The human-readable name of the
            parameter, unique within the form.
          entity_type (str):
            Required. The entity type of the parameter. Format:
            ``projects/-/locations/-/agents/-/
              entityTypes/<System Entity Type ID>``
            for system entity types (for example,
            ``projects/-/locations/-/agents/-/entityTypes/sys.date``),
            or
            ``projects/<Project ID>/locations/<Location ID>/
              agents/<Agent ID>/entityTypes/<Entity Type ID>``
            for developer entity types.
          initial_prompt_fulfillment (Fulfillment):
            Required. The fulfillment to provide the initial prompt that
            the agent can present to the user in order to fill the parameter.
          required (bool):
            Indicates whether the parameter is required.
            Optional parameters will not trigger prompts;
            however, they are filled if the user specifies
            them. Required parameters must be filled before
            form filling concludes.
          default_value (str):
            The default value of an optional parameter.
            If the parameter is required, the default value
            will be ignored.
          is_list (bool):
            Indicates whether the parameter represents a
            list of values.
          redact (bool):
            Indicates whether the parameter content should be redacted
            in log. If redaction is enabled, the parameter content will
            be replaced by parameter name during logging.
          reprompt_event_handlers (EventHandler | List[EventHandler]):
            The handlers for parameter-level events, used to provide reprompt
            for the parameter or transition to a different page/flow.
            The supported events are:
              - ``sys.no-match-<N>``, where N can be from 1 to 6
              - ``sys.no-match-default``
              - ``sys.no-input-<N>``, where N can be from 1 to 6
              - ``sys.no-input-default``
              - ``sys.invalid-parameter``

            ``initial_prompt_fulfillment`` provides the first prompt for
            the parameter.

            If the event handler for the corresponding event can't be found on
            the parameter, ``initial_prompt_fulfillment`` will be re-prompted.

        Returns:
          A Page object stored in proto_obj.
        """
        self._check_proto_obj_attr_exist()

        # Types error checking
        if not (display_name and isinstance(display_name, str)):
            raise ValueError("`display_name` should be a nonempty string.")
        if not (entity_type and isinstance(entity_type, str)):
            raise ValueError("`entity_type` should be a valid entity type id.")
        if not (initial_prompt_fulfillment and
            isinstance(initial_prompt_fulfillment, Fulfillment)):
            raise ValueError(
                "`initial_prompt_fulfillment` should be a Fulfillment."
            )
        if not(
            isinstance(required, bool) and
            isinstance(is_list, bool) and
            isinstance(redact, bool)
        ):
            raise ValueError(
                "`is_list`, `required`, and `redact` should be bool."
            )
        if reprompt_event_handlers:
            self._is_type_or_list_of_types(
                reprompt_event_handlers, EventHandler, "reprompt_event_handlers"
            )
            if not isinstance(reprompt_event_handlers, list):
                reprompt_event_handlers = [reprompt_event_handlers]

        if required:
            the_param = Form.Parameter(
                display_name=display_name,
                required=required,
                entity_type=entity_type,
                is_list=is_list,
                redact=redact
            )
        else:
            if not isinstance(default_value, str):
                raise ValueError("`default_value` should be a string.")
            the_param = Form.Parameter(
                display_name=display_name,
                required=required,
                entity_type=entity_type,
                is_list=is_list,
                redact=redact,
                default_value=default_value
            )

        the_param.fill_behavior = Form.Parameter.FillBehavior(
            initial_prompt_fulfillment=initial_prompt_fulfillment,
            reprompt_event_handlers=reprompt_event_handlers
        )
        self.proto_obj.form.parameters.append(the_param)

        return self.proto_obj

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
    ) -> Page:
        """Add single or multiple TransitionRoutes to the Page.
        You can either pass TransitionRoute objects or create a TransitionRoute
        on the fly by passing other parameters. Note that `transition_routes`
        takes priority over other parameters.

        Args:
          transition_routes (TransitionRoute | List[TransitionRoute]):
            A single or list of TransitionRoutes to add
            to the Page existed in proto_obj.
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
          A Page object stored in proto_obj.
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

    def add_event_handler(
        self,
        event_handlers: Union[EventHandler, List[EventHandler]] = None,
        event: str = None,
        target_page: str = None,
        target_flow: str = None,
        trigger_fulfillment: Fulfillment = None,
        agent_response: Union[str, List[str]] = None,
        parameter_map: Dict[str, str] = None,
    ) -> Page:
        """Add single or multiple EventHandlers to the Page.
        You can either pass EventHandler objects or create a EventHandler
        on the fly by passing other parameters. Note that `event_handlers`
        takes priority over other parameters.

        Args:
          event_handlers (EventHandler | List[EventHandler]):
            A single or list of EventHandler to add
            to the Page existing in proto_obj.
          event (str):
            The name of the event to handle.
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
          A Page object stored in proto_obj.
        """
        self._check_proto_obj_attr_exist()

        if not event_handlers is None:
            self._is_type_or_list_of_types(
                event_handlers, EventHandler, "event_handlers")

            if not isinstance(event_handlers, list):
                event_handlers = [event_handlers]
        else:
            ehb = EventHandlerBuilder()
            ehb.create_new_proto_obj(
                event, trigger_fulfillment, target_page, target_flow)
            if trigger_fulfillment is None:
                ehb.set_fulfillment(
                    message=agent_response, parameter_map=parameter_map)
            event_handlers = [ehb.proto_obj]

        self.proto_obj.event_handlers.extend(event_handlers)
        return self.proto_obj

    def add_transition_route_group(
        self,
        transition_route_groups: Union[str, List[str]]
    ) -> Page:
        """Add single or multiple TransitionRouteGroups to the Page.

        Args:
          transition_route_groups (str | List[str]):
            A single or list of TransitionRouteGroup's id to add
            to the Page existing in proto_obj. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/
              flows/<Flow ID>/transitionRouteGroups/<TransitionRouteGroup ID>``.

        Returns:
          A Page object stored in proto_obj.
        """
        self._check_proto_obj_attr_exist()

        # Type/Error checking
        self._is_type_or_list_of_types(
            transition_route_groups, str, "transition_route_groups"
        )

        if not isinstance(transition_route_groups, list):
            transition_route_groups = [transition_route_groups]
        self.proto_obj.transition_route_groups.extend(transition_route_groups)

        return self.proto_obj

    def remove_parameter(
        self,
        display_name: Union[str, List[str]]
    ) -> Page:
        """Remove single or multiple parameters from the Page.

        Args:
          display_name (str | List[str]):
            A string or a list of strings corresponding to
            the name of the parameter(s).

        Returns:
          A Page object stored in proto_obj.
        """
        self._check_proto_obj_attr_exist()

        # Types error checking
        if not display_name:
            raise ValueError("`display_name` should not be empty.")
        self._is_type_or_list_of_types(display_name, str, "display_name")

        if not isinstance(display_name, list):
            display_name = [display_name]

        new_params = [
            param
            for param in self.proto_obj.form.parameters
            if param.display_name not in display_name
        ]
        self.proto_obj.form.parameters = new_params

        return self.proto_obj

    def remove_transition_route(
        self,
        transition_route: TransitionRoute = None,
        intent: str = None,
        condition: str = None
    ) -> Page:
        """Remove a transition route from the Page.

        At least one of the `transition_route`, `intent`, or `condition` should
        be specfied.

        Args:
            transition_route (TransitionRoute):
              The TransitionRoute to remove from the Page.
            intent (str):
              TransitionRoute's intent that should be removed from the Page.
            condition (str):
              TransitionRoute's condition that should be removed from the Page.

        Returns:
          A Page object stored in proto_obj.
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

    def remove_event_handler(
        self,
        event_handlers: Union[EventHandler, List[EventHandler]] = None,
        event_names: Union[str, List[str]] = None
    ) -> Page:
        """Remove single or multiple EventHandlers from the Page.

        Args:
          event_handlers (EventHandler | List[EventHandler]):
            A single or list of EventHandler to remove
              from the Page existing in proto_obj.
            Only one of the `event_handlers` and
              `event_names` should be specified.
          event_names (str | List[str]):
            A single or list of EventHandler's event names corresponding to the
              EventHandler to remove from the Page existing in proto_obj.
            Only one of the `event_handlers` and
              `event_names` should be specified.

        Returns:
          A Page object stored in proto_obj.
        """
        self._check_proto_obj_attr_exist()

        if event_handlers and event_names:
            raise UserWarning(
                "Only one of the `event_handlers` and "
                "`event_names` should be specified."
            )
        if event_handlers:
            new_ehs = self._find_unmatched_event_handlers(event_handlers)
        elif event_names:
            new_ehs = self._find_unmatched_event_handlers_by_name(event_names)
        else:
            raise UserWarning(
                "At least one of the `event_handlers` and "
                "`event_names` should be specified."
            )

        self.proto_obj.event_handlers = new_ehs

        return self.proto_obj

    def remove_transition_route_group(
        self,
        transition_route_groups: Union[str, List[str]]
    ) -> Page:
        """Remove single or multiple TransitionRouteGroups from the Page.

        Args:
          transition_route_groups (str | List[str]):
            A single or list of TransitionRouteGroup's id to remove
            from the Page existing in proto_obj. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/
              flows/<Flow ID>/transitionRouteGroups/<TransitionRouteGroup ID>``.

        Returns:
          A Page object stored in proto_obj.
        """
        self._check_proto_obj_attr_exist()

        # Type error checking
        self._is_type_or_list_of_types(
            transition_route_groups, str, "transition_route_groups"
        )

        if not isinstance(transition_route_groups, list):
            transition_route_groups = [transition_route_groups]

        new_trgs = [
            trg
            for trg in self.proto_obj.transition_route_groups
            if trg not in transition_route_groups
        ]
        self.proto_obj.transition_route_groups = new_trgs

        return self.proto_obj


    class _Dataframe(BuildersCommon._DataframeCommon): # pylint: disable=W0212
        """An internal class to store DataFrame related methods."""

        def _create_form_params_df(
            self,
            form_parameter_list: List[Form.Parameter],
            mode: str = "basic"
        ) -> pd.DataFrame:
            """Create a DataFrame from the form parameters of a page.

            Args:
              params (List[Form.Parameter]):
                A list of page's form parameters.
              mode (str):
                Whether to return 'basic' DataFrame or 'advanced' one.

            Returns:
                A pandas DataFrame
            """
            cols_map = {
                "basic": [
                    "parameter_display_name", "parameter_entity_type",
                    "has_fulfillment", "has_fulfillment_webhook",
                ],
                "advanced": [
                    "parameter_display_name", "parameter_entity_type",
                    "parameter_is_required", "parameter_is_list",
                    "parameter_is_redact", "parameter_default_value",
                    "messages", "preset_parameters", "conditional_cases",
                    "webhook", "webhook_tag", "return_partial_responses",
                ]
            }
            cols = cols_map[mode]
            if not form_parameter_list:
                return pd.DataFrame(columns=cols)

            out_df = pd.DataFrame(columns=cols)
            for param in form_parameter_list:

                if mode == "basic":
                    param_df = pd.DataFrame({
                        "parameter_display_name": [str(param.display_name)],
                        "parameter_entity_type": [str(param.entity_type)],
                    })
                elif mode == "advanced":
                    required = bool(param.required)
                    tmp_val = str(param.default_value)
                    default_val = np.nan if required else tmp_val
                    param_df = pd.DataFrame({
                        "parameter_display_name": [str(param.display_name)],
                        "parameter_entity_type": [str(param.entity_type)],
                        "parameter_is_required": [required],
                        "parameter_is_list": [bool(param.is_list)],
                        "parameter_is_redact": [bool(param.redact)],
                        "parameter_default_value": [default_val],
                    })

                # Initial Prompt Fulfillment
                prompt_ff = param.fill_behavior.initial_prompt_fulfillment
                prompt_ff_builder = FulfillmentBuilder(prompt_ff)
                prompt_ff_df = prompt_ff_builder.to_dataframe(mode)
                tmp_df = pd.concat([param_df, prompt_ff_df], axis=1)

                out_df = pd.concat([out_df, tmp_df], ignore_index=True)

                # Reprompt Event Handlers
                ehs_df = pd.DataFrame()
                for eh in param.fill_behavior.reprompt_event_handlers:
                    ehb = EventHandlerBuilder(eh)
                    ehb_df = ehb.to_dataframe(mode)
                    ehs_df = pd.concat([ehs_df, ehb_df], ignore_index=True)

                if ehs_df.empty:
                    return out_df

                tmp_param_df = pd.concat(
                    [param_df] * len(ehs_df), ignore_index=True)
                param_eh_df = pd.concat([tmp_param_df, ehs_df], axis=1)
                out_df = pd.concat([out_df, param_eh_df], ignore_index=True)

            return out_df


        def proto_to_dataframe(
            self, obj: Page, mode: str = "basic"
        ) -> pd.DataFrame:
            """Converts a Page protobuf object to pandas Dataframe.

            Args:
              obj (Page):
                Page protobuf object
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

            ehs_df = pd.DataFrame(
                columns=self._dataframes_map["EventHandler"][mode]
            )
            for eh in obj.event_handlers:
                ehb = EventHandlerBuilder(eh)
                ehb_df = ehb.to_dataframe(mode)
                ehs_df = pd.concat([ehs_df, ehb_df], ignore_index=True)

            trgs_df = pd.DataFrame({
                "route_groups": list(obj.transition_route_groups)
            })

            entry_fb = FulfillmentBuilder(obj.entry_fulfillment)
            entry_fb_df = entry_fb.to_dataframe(mode)
            parameters_df = self._create_form_params_df(
                form_parameter_list=obj.form.parameters, mode=mode
            )

            # Concatenate `routes_df` and `ehs_df` and add the rest of the info
            page_df = pd.concat(
                [entry_fb_df, parameters_df, routes_df, ehs_df, trgs_df],
                axis=0, ignore_index=True
            )
            page_df["name"] = str(obj.name)
            page_df["display_name"] = str(obj.display_name)
            page_df["flow"] = str(obj.name).split("/pages", maxsplit=1)[0]

            return page_df[self._dataframes_map["Page"][mode]]


@dataclass
class PageStats():
    """A class for tracking the stats of CX Page object."""
    page_proto_obj: Page

    # Entry Fulfillment
    has_entry_fulfill: bool = False

    # Parameters
    parameters_count: int = 0
    parameters_with_event_handler_count: int = 0
    parameters_with_webhook_fulfill_count: int = 0
    parameters_ratio: int = 0

    # Transition Routes
    transition_routes_count: int = 0
    routes_with_fulfill_count: int = 0
    routes_with_webhook_fulfill_count: int = 0
    intent_routes_count: int = 0
    cond_routes_count: int = 0
    intent_and_cond_routes_count: int = 0

    # Event Handlers
    event_handlers_count: int = 0
    events_with_fulfill_count: int = 0
    events_with_webhook_fulfill_count: int = 0

    # Transition Route Groups
    transition_route_groups_count: int = 0


    def calc_transition_route_stats(self):
        """Calculating TransitionRoute related stats."""
        self.transition_routes_count = len(
            self.page_proto_obj.transition_routes
        )
        for tr in self.page_proto_obj.transition_routes:
            if tr.trigger_fulfillment:
                self.routes_with_fulfill_count += 1
                fb = FulfillmentBuilder(tr.trigger_fulfillment)
                if fb.has_webhook():
                    self.routes_with_webhook_fulfill_count += 1
            if tr.intent and tr.condition:
                self.intent_and_cond_routes_count += 1
            elif tr.intent and not tr.condition:
                self.intent_routes_count += 1
            elif not tr.intent and tr.condition:
                self.cond_routes_count += 1

    def create_transition_route_str(self) -> str:
        """String representation of TransitionRoutes stats."""
        transition_routes_str = (
            f"# of Transition Routes: {self.transition_routes_count}"
        )
        routes_with_fulfill_str = (
            f"# of routes with fulfillment: {self.routes_with_fulfill_count}"
        )
        routes_with_webhook_fulfill_str = (
            "# of routes uses webhook for fulfillment:"
            f" {self.routes_with_webhook_fulfill_count}"
        )
        intent_routes_str = f"# of intent routes: {self.intent_routes_count}"
        cond_routes_str = f"# of condition routes: {self.cond_routes_count}"
        intent_and_cond_routes_str = (
            "# of intent and condition routes:"
            f" {self.intent_and_cond_routes_count}"
        )

        return (
            f"{transition_routes_str}\n\t{intent_routes_str}"
            f"\n\t{cond_routes_str}\n\t{intent_and_cond_routes_str}"
            f"\n\t{routes_with_fulfill_str}"
            f"\n\t{routes_with_webhook_fulfill_str}"
        )


    def calc_event_handler_stats(self):
        """Calculating EventHandler related stats."""
        self.event_handlers_count = len(self.page_proto_obj.event_handlers)
        for eh in self.page_proto_obj.event_handlers:
            fb = FulfillmentBuilder(eh.trigger_fulfillment)
            if fb.has_webhook():
                self.events_with_webhook_fulfill_count += 1
            if eh.trigger_fulfillment:
                self.events_with_fulfill_count += 1

    def create_event_handler_str(self) -> str:
        """String representation of EventHandlers stats."""
        event_handlers_str = f"# of Event Handlers: {self.event_handlers_count}"
        events_with_fulfill_str = (
            "# of Event Handlers with fulfillment:"
            f" {self.events_with_fulfill_count}"
        )
        events_with_webhook_fulfill_str = (
            "# of Event Handlers uses webhook for fulfillment:"
            f" {self.events_with_webhook_fulfill_count}"
        )

        return (
            f"{event_handlers_str}\n\t{events_with_fulfill_str}"
            f"\n\t{events_with_webhook_fulfill_str}"
        )


    def calc_parameter_stats(self):
        """Calculating Parameter related stats."""
        self.parameters_count = len(self.page_proto_obj.form.parameters)
        for param in self.page_proto_obj.form.parameters:
            fb = FulfillmentBuilder(
                param.fill_behavior.initial_prompt_fulfillment
            )
            if fb.has_webhook():
                self.parameters_with_webhook_fulfill_count += 1
            if param.fill_behavior.reprompt_event_handlers:
                self.parameters_with_event_handler_count += 1

        if self.parameters_count != 0:
            self.parameters_ratio = (
                self.parameters_with_event_handler_count/self.parameters_count
            )

    def create_parameter_str(self) -> str:
        """String representation of Page's parameters stats."""
        parameters_str = f"# of Parameters: {self.parameters_count}"
        parameters_with_event_handler_str = (
            "# of Parameters with Event Handlers:"
            f" {self.parameters_with_event_handler_count}"
            f" (Ratio: {self.parameters_ratio})"
        )
        parameters_with_webhook_fulfill_str = (
            "# of Parameters uses webhook for fulfillment:"
            f" {self.parameters_with_webhook_fulfill_count}"
        )

        return (
            f"{parameters_str}\n\t{parameters_with_event_handler_str}"
            f"\n\t{parameters_with_webhook_fulfill_str}"
        )


    def create_entry_fulfillment_str(self) -> str:
        """String representation for Page's Entry Fulfillment."""
        self.has_entry_fulfill = bool(self.page_proto_obj.entry_fulfillment)
        return f"Has entry fulfillment: {self.has_entry_fulfill}"


    def create_transition_route_group_str(self) -> str:
        """String representation of TransitionRouteGroup stats."""
        self.transition_route_groups_count = len(
            self.page_proto_obj.transition_route_groups
        )
        return (
            "# of Transition Route Groups:"
            f" {self.transition_route_groups_count}"
        )


    def generate_stats(self):
        """Generate stats for the Page."""
        self.calc_parameter_stats()
        self.calc_transition_route_stats()
        self.calc_event_handler_stats()

        has_entry_fulfill_str = self.create_entry_fulfillment_str()
        params_stats_str = self.create_parameter_str()
        routes_stats_str = self.create_transition_route_str()
        events_stats_str = self.create_event_handler_str()
        route_groups_stats_str = self.create_transition_route_group_str()

        out = (
            f"{has_entry_fulfill_str}\n{params_stats_str}\n{routes_stats_str}"
            f"\n{events_stats_str}\n{route_groups_stats_str}"
        )
        print(out)
