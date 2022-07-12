"""Entity Types Resource functions."""

# Copyright 2022 Google LLC
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
from typing import Dict, List

import pandas as pd
from google.cloud.dialogflowcx_v3beta1 import services
from google.cloud.dialogflowcx_v3beta1 import types
from google.protobuf import field_mask_pb2

from dfcx_scrapi.core.scrapi_base import ScrapiBase

# logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class EntityTypes(ScrapiBase):
    """Core Class for CX Entity Type Resource functions."""

    def __init__(
        self,
        creds_path: str = None,
        creds_dict: Dict = None,
        creds=None,
        scope=False,
        entity_id: str = None,
        agent_id: str = None,
    ):
        super().__init__(
            creds_path=creds_path,
            creds_dict=creds_dict,
            creds=creds,
            scope=scope,
        )

        self.entity_id = entity_id
        self.agent_id = agent_id


    @staticmethod
    def entity_type_proto_to_dataframe(
        obj: types.EntityType, mode: str = "basic"
    ):
        """Entity Types to dataframe

        Args:
          obj, EntityType protobuf object
          mode: (Optional) basic returns display_name, value of entity type and
            it's synonyms.
          advanced returns entity types and excluded phrases in a comprehensive
            format.
        """
        if mode == "basic":
            main_df = pd.DataFrame()

            entity_type_dict = {}
            entity_type_dict["display_name"] = obj.display_name
            for entity in obj.entities:
                entity_type_dict["entity_value"] = entity.value
                for synonym in entity.synonyms:
                    entity_type_dict["synonyms"] = synonym
                    main_df = pd.concat(
                        [main_df, entity_type_dict], ignore_index=True)

            return main_df

        elif mode == "advanced":

            main_df = pd.DataFrame()
            excl_phrases_df = pd.DataFrame()

            excl_phrases_dict = {
                "entity_type_id": obj.name,
                "display_name": obj.display_name,
            }
            entity_type_dict = {
                "entity_type_id": obj.name,
                "display_name": obj.display_name,
                "kind": obj.kind.name,
                "auto_expansion_mode": obj.auto_expansion_mode,
                "fuzzy_extraction": obj.enable_fuzzy_extraction,
                "redact": obj.redact,
            }
            for entity in obj.entities:
                entity_type_dict["entity_value"] = entity.value
                for synonym in entity.synonyms:
                    entity_type_dict["synonyms"] = synonym
                    main_df = pd.concat(
                        [main_df, entity_type_dict], ignore_index=True)

            for excluded_phrase in obj.excluded_phrases:
                excl_phrases_dict["excluded_phrase"] = excluded_phrase.value
                excl_phrases_df = pd.concat(
                    [excl_phrases_df, excl_phrases_dict], ignore_index=True)

            return {
                "entity_types": main_df, "excluded_phrases": excl_phrases_df
            }

        else:
            raise ValueError("Mode types: [basic, advanced]")

    def entity_types_to_df(
        self,
        agent_id: str = None,
        mode: str = "basic",
        entity_type_subset: List[str] = None) -> pd.DataFrame:
        """Extracts all Intents and Training Phrases into a Pandas DataFrame.

        Args:
          agent_id, agent to pull list of intents
          mode: (Optional) basic returns display_name, value of entity type and
            it's synonyms.
          advanced returns entity types and excluded phrases in a comprehensive
            format.
          entity_type_subset: (Optional) A list of entities to pull
            If it's None, grab all the entity_types
        """

        if not agent_id:
            agent_id = self.agent_id

        entity_types = self.list_entity_types(agent_id)
        if mode == "basic":
            main_df = pd.DataFrame()
            for obj in entity_types:
                if (entity_type_subset and
                        obj.display_name not in entity_type_subset):
                    continue

                single_entity_df = self.entity_type_proto_to_dataframe(
                    obj, mode=mode
                )
                main_df = pd.concat([main_df, single_entity_df])
            main_df = main_df.sort_values(
                ["display_name", "entity_value"])
            return main_df

        elif mode == "advanced":
            main_df = pd.DataFrame()
            excl_phrases_df = pd.DataFrame()
            for obj in entity_types:
                if (entity_type_subset and
                        obj.display_name not in entity_type_subset):
                    continue
                single_entity_dict = self.entity_type_proto_to_dataframe(
                    obj, mode=mode
                )
                main_df = pd.concat(
                    [main_df, single_entity_dict["entity_types"]])
                excl_phrases_df = pd.concat(
                    [excl_phrases_df, single_entity_dict["excluded_phrases"]])
            type_map = {
                "auto_expansion_mode": bool,
                "fuzzy_extraction": bool,
                "redact": bool
            }
            main_df = main_df.astype(type_map)

            return {
                "entity_types": main_df, "excluded_phrases": excl_phrases_df
            }

        else:
            raise ValueError("Mode types: [basic, advanced]")


    def get_entities_map(self, agent_id: str = None, reverse=False):
        """Exports Agent Entityt Names and UUIDs into a user friendly dict.

        Args:
          - agent_id, the formatted CX Agent ID to use
          - reverse, (Optional) Boolean flag to swap key:value -> value:key

        Returns:
          - intents_map, Dictionary containing Entity UUIDs as keys and
              intent.display_name as values
        """
        if not agent_id:
            agent_id = self.agent_id

        if reverse:
            entities_dict = {
                entity.display_name: entity.name
                for entity in self.list_entity_types(agent_id)
            }

        else:
            entities_dict = {
                entity.name: entity.display_name
                for entity in self.list_entity_types(agent_id)
            }

        return entities_dict

    def list_entity_types(self, agent_id: str = None):
        """Returns a list of Entity Type objects.

        Args:
          - agent_id, the formatted CX Agent ID to use

        Returns:
          - entities, List of Entity Type objects
        """
        if not agent_id:
            agent_id = self.agent_id

        request = types.entity_type.ListEntityTypesRequest()
        request.parent = agent_id

        client_options = self._set_region(agent_id)
        client = services.entity_types.EntityTypesClient(
            credentials=self.creds, client_options=client_options
        )

        response = client.list_entity_types(request)

        entities = []
        for page in response.pages:
            for entity in page.entity_types:
                entities.append(entity)

        return entities

    def get_entity_type(self, entity_id: str = None):
        """Returns a single Entity Type object.

        Args:
          - entity_id, the formatted CX Entity ID to get

        Returns:
          - response, the single Entity Type object
        """
        if not entity_id:
            entity_id = self.entity_id

        client_options = self._set_region(entity_id)
        client = services.entity_types.EntityTypesClient(
            credentials=self.creds, client_options=client_options
        )
        response = client.get_entity_type(name=entity_id)

        return response

    def create_entity_type(
        self, agent_id: str = None, obj: types.EntityType = None,
        language_code: str = None, **kwargs
    ) -> types.EntityType:
        """Creates a single Entity Type object resource.

        Args:
          - agent_id, the formatted CX Agent ID to create the object on
          - obj, The CX EntityType object in proper format.
          - language_code: Language code of the intents being uploaded. Ref:
            https://cloud.google.com/dialogflow/cx/docs/reference/language

        Returns:
          - response, copy of the Entity Type object created
        """
        if not agent_id:
            agent_id = self.agent_id

        # If entity_type_obj is given set entity_type to it
        if obj:
            entity_type = obj
            entity_type.name = ""
        else:
            entity_type = types.entity_type.EntityType()

        # set optional arguments to entity type attributes
        for key, value in kwargs.items():
            setattr(entity_type, key, value)

        client_options = self._set_region(agent_id)
        client = services.entity_types.EntityTypesClient(
            credentials=self.creds, client_options=client_options
        )

        request = types.entity_type.CreateEntityTypeRequest()

        request.parent = agent_id
        request.entity_type = entity_type

        if language_code:
            request.language_code = language_code

        response = client.create_entity_type(
            request=request
        )

        return response

    def update_entity_type(
        self,
        entity_type_id: str = None,
        obj: types.EntityType = None,
        language_code: str = None,
        **kwargs):
        """Update a single CX Entity Type object.
        Pass in a the Entity Type ID and the specified kwargs for the
        parameters in Entity Types object that you want updated. If you do not
        provide an Entity Type object, the object will be fetched based on the
        ID provided. Optionally, you can include a pre-made Entity Type object
        that will be used to replace some of the parameters in the existing
        Entity Type object as defined by the kwargs provided.

        Args:
          entity_type_id, CX Entity Type ID in proper format
          obj, (Optional) a CX Entity Type object of types.EntityType
          language_code: Language code of the intents being uploaded. Ref:
          https://cloud.google.com/dialogflow/cx/docs/reference/language

        Returns:
          response, a copy of the updated Entity Type object
        """

        if obj:
            entity_type = obj
            entity_type.name = entity_type_id
        else:
            if not entity_type_id:
                entity_type_id = self.entity_id
            entity_type = self.get_entity_type(entity_type_id)

        # set entity type attributes to args
        for key, value in kwargs.items():
            setattr(entity_type, key, value)
        paths = kwargs.keys()
        mask = field_mask_pb2.FieldMask(paths=paths)

        client_options = self._set_region(entity_type_id)
        client = services.entity_types.EntityTypesClient(
            credentials=self.creds, client_options=client_options
        )

        request = types.entity_type.UpdateEntityTypeRequest()
        request.entity_type = entity_type
        request.update_mask = mask
        if language_code:
            request.language_code = language_code

        response = client.update_entity_type(request)

        return response

    def delete_entity_type(self, entity_id: str = None, obj=None) -> None:
        """Deletes a single Entity Type resouce object.

        Args:
          entity_id, the formatted CX Entity ID to delete

        Returns:
          - None
        """
        if not entity_id:
            entity_id = self.entity_id

        if obj:
            entity_id = obj.name
        else:
            client_options = self._set_region(entity_id)
            client = services.entity_types.EntityTypesClient(
                credentials=self.creds, client_options=client_options
            )
            client.delete_entity_type(name=entity_id)
