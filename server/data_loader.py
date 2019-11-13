# -*- coding: utf-8 -*-

from uuid import UUID
from typing import Union, List, MutableMapping, Tuple

from promise import Promise
from promise.dataloader import DataLoader

TAG_ARGS_SEPARATOR = "::"
PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG = "0"


def make_personal_info_from_resume_id_loader_hash(
    resume_id: Union[UUID, str]
) -> str:  # noqa
    resume_id = str(resume_id)
    return (
        f"{PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG}{TAG_ARGS_SEPARATOR}{resume_id}" # noqa
    )  # noqa


def personal_info_from_resume_id_loader(index_id_list: List[Tuple[int, str]]) -> None: # noqa
    pass


class AppDataLoader(DataLoader):
    def batch_load_fn(self, keys: List[str]) -> None:
        tags_index_args_map: MutableMapping[str, List[Tuple[int, str]]] = {}

        for index, key in enumerate(keys):
            tag, args = key.split(TAG_ARGS_SEPARATOR, 2)
            index_args_list = tags_index_args_map.get(tag, [])
            index_args_list.append((index, args,))
            tags_index_args_map[tag] = index_args_list

        for tag in tags_index_args_map:
            index_args_list = tags_index_args_map[tag]

        return Promise.resolve([key for key in keys])
