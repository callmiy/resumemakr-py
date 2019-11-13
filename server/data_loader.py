# -*- coding: utf-8 -*-

from uuid import UUID
from typing import Union, List, MutableMapping, Tuple, Any

from promise import Promise
from promise.dataloader import DataLoader

from server.apps.resumes.commons import PersonalInfoLike
from server.apps.resumes.logic import ResumeLogic

TAG_ARGS_SEPARATOR = "::"
PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG = "0"


def make_personal_info_from_resume_id_loader_hash(
    resume_id: Union[UUID, str]
) -> str:  # noqa
    resume_id = str(resume_id)
    return (
        f"{PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG}{TAG_ARGS_SEPARATOR}{resume_id}" # noqa
    )  # noqa


def personal_info_from_resume_id_loader(index_resume_id_list: List[Tuple[int, str]]) -> List[Tuple[int, PersonalInfoLike]]: # noqa
    ids_list: List[str] = []
    resume_id_index_map: MutableMapping[str, int] = {}

    for (index, resume_id,) in index_resume_id_list:
        ids_list.append(resume_id)
        resume_id_index_map[resume_id] = index

    resume_id_personal_info_map = {
            p.resume_id: for p in ResumeLogic.get_personal_infos(ids_list)
    }

    index_personal_info_list: List[Tuple[index, PersonalInfoLike]] = []

    for resume_id in ids_list:
        index = resume_id_index_map[resume_id]
        personal_info = resume_id_personal_info_map.get(resume_id)
        index_personal_info_list.append((index, personal_info))

    return index_personal_info_list

class AppDataLoader(DataLoader):
    def batch_load_fn(self, keys: List[str]) -> None:
        tags_index_args_map: MutableMapping[str, List[Tuple[int, str]]] = {}

        for index, key in enumerate(keys):
            tag, args = key.split(TAG_ARGS_SEPARATOR, 2)
            index_args_list = tags_index_args_map.get(tag, [])
            index_args_list.append((index, args,))
            tags_index_args_map[tag] = index_args_list

        index_resource_list: List[Tuple[int, Any]] = []

        for tag in tags_index_args_map:
            index_args_list = tags_index_args_map[tag]

            if tag = PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG:
                index_resource_list.append(personal_info_from_resume_id_loader(index_args_list))

        return Promise.resolve([
            resource[1] for resource in sorted(index_resource_list, key=lambda (index, _): index)
        ])
