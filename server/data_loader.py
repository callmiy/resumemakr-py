# -*- coding: utf-8 -*-

from typing import Any, List, MutableMapping, Optional, Tuple, Union, TypeVar, Callable # noqa E501
from uuid import UUID

from promise import Promise
from promise.dataloader import DataLoader

from server.apps.resumes.logic import ResumesLogic
from server.apps.resumes.resumes_commons import PersonalInfoLike, EducationLike # noqa E501

T = TypeVar('T')
IndexIdListType = List[Tuple[int, str]]
FromIdLoaderType = List[Tuple[int, Optional[T]]]

TAG_ARGS_SEPARATOR = "::"
PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG = "0"
EDUCATION_FROM_RESUME_ID_LOADER_TAG = '1'
EXPERIENCE_FROM_RESUME_ID_LOADER_TAG = '1'
HOBBY_FROM_RESUME_ID_LOADER_TAG = '1'
SKILL_FROM_RESUME_ID_LOADER_TAG = '1'
SPOKEN_LANGUAGE_FROM_RESUME_ID_LOADER_TAG = '1'
SUPPLEMENTARY_SKILL_FROM_RESUME_ID_LOADER_TAG = '1'


def make_personal_info_from_resume_id_loader_hash(
    resume_id: Union[UUID, str]
) -> str:  # noqa
    resume_id = str(resume_id)
    return (
        f"{PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG}{TAG_ARGS_SEPARATOR}{resume_id}" # noqa
    )  # noqa


def make_education_from_resume_id_loader_hash(
    resume_id: Union[UUID, str]
) -> str:  # noqa
    resume_id = str(resume_id)
    return (
        f"{EDUCATION_FROM_RESUME_ID_LOADER_TAG}{TAG_ARGS_SEPARATOR}{resume_id}" # noqa 501
    )  # noqa 501


def make_experience_from_resume_id_loader_hash(
    resume_id: Union[UUID, str]
) -> str:  # noqa
    resume_id = str(resume_id)
    return (
        f"{EDUCATION_FROM_RESUME_ID_LOADER_TAG}{TAG_ARGS_SEPARATOR}{resume_id}" # noqa 501
    )  # noqa 501


def make_skill_from_resume_id_loader_hash(
    resume_id: Union[UUID, str]
) -> str:  # noqa
    resume_id = str(resume_id)
    return (
        f"{SKILL_FROM_RESUME_ID_LOADER_TAG}{TAG_ARGS_SEPARATOR}{resume_id}" # noqa 501
    )  # noqa 501

def personal_info_from_resume_id_loader(index_resume_id_list: IndexIdListType) -> FromIdLoaderType[PersonalInfoLike]: # noqa E501
    return from_resume_id_loader(index_resume_id_list, ResumesLogic.get_personal_infos) # noqa E501


def education_from_resume_id_loader(index_resume_id_list: IndexIdListType) -> FromIdLoaderType[EducationLike]: # noqa E501
    return from_resume_id_loader(index_resume_id_list, ResumesLogic.get_educations) # noqa E501

def from_resume_id_loader(index_resume_id_list: IndexIdListType, resource_getter_fn: Callable[[List[str]], List[T]]) -> FromIdLoaderType[T]: # noqa 501
    resume_ids_list: List[str] = []
    resume_id_index_map: MutableMapping[str, int] = {}

    for (index, resume_id,) in index_resume_id_list:
        resume_ids_list.append(resume_id)
        resume_id_index_map[resume_id] = index

    resume_id_personal_info_map = {str(p.resume_id): p for p in resource_getter_fn(resume_ids_list)} # noqa 501

    index_resource_list: List[Tuple[int, Optional[T]]] = []

    for resume_id in resume_ids_list:
        index = resume_id_index_map[resume_id]
        personal_info = resume_id_personal_info_map.get(resume_id)
        index_resource_list.append((index, personal_info))

    return index_resource_list


class AppDataLoader(DataLoader):
    def batch_load_fn(self, keys: List[str]) -> None:
        tags_index_args_map: MutableMapping[str, List[Tuple[int, str]]] = {}

        for index, key in enumerate(keys):
            tag, args = key.split(TAG_ARGS_SEPARATOR, 2)
            index_args_list = tags_index_args_map.get(tag, [])
            index_args_list.append((index, args,))
            tags_index_args_map[tag] = index_args_list

        index_resource_list: List[Tuple[int, Any]] = [] # type: ignore[disallow_any_explicit] # noqa

        for tag in tags_index_args_map:
            index_args_list = tags_index_args_map[tag]

            if tag == PERSONAL_INFO_FROM_RESUME_ID_LOADER_TAG:
                index_resource_list.extend(personal_info_from_resume_id_loader(index_args_list)) # noqa

        return Promise.resolve([
            resource[1] for resource in sorted(index_resource_list, key=lambda member: member[0]) # noqa
        ])
